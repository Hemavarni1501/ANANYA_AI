"""
ANANYA-AI Interaction Analyzer Module
Analyzes learning interaction patterns WITHOUT user profiling.

This module extracts patterns from:
- Response latency
- Repeated errors
- Clarification frequency
- Engagement signals

PRIVACY GUARANTEE:
- No demographic inference
- No student labeling
- Pattern analysis only
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import statistics

from models.schemas import (
    InteractionData,
    InteractionAnalysisResult,
    AdaptationType,
)


class InteractionAnalyzer:
    """
    Analyzes interaction patterns to detect potential learning barriers.
    Does NOT profile or label students.
    """
    
    # Thresholds (configurable, not based on demographics)
    DEFAULT_SLOW_RESPONSE_MS = 10000  # 10 seconds
    DEFAULT_FAST_RESPONSE_MS = 1000   # 1 second
    DEFAULT_HIGH_CLARIFICATION_COUNT = 3
    
    def __init__(self):
        """Initialize the interaction analyzer."""
        self.slow_response_threshold = self.DEFAULT_SLOW_RESPONSE_MS
        self.fast_response_threshold = self.DEFAULT_FAST_RESPONSE_MS
        self.high_clarification_threshold = self.DEFAULT_HIGH_CLARIFICATION_COUNT
    
    def analyze_single_interaction(
        self, 
        interaction: InteractionData
    ) -> InteractionAnalysisResult:
        """
        Analyze a single interaction and return patterns.
        
        Args:
            interaction: Anonymized interaction data
            
        Returns:
            Analysis result with pattern indicators
        """
        # Determine response pattern
        response_pattern = self._classify_response_pattern(
            interaction.response_time_ms,
            interaction.action_type
        )
        
        # Determine engagement level
        engagement_level = self._assess_engagement(
            interaction.time_on_content_seconds,
            interaction.action_type,
            interaction.clarification_count
        )
        
        # Build comprehension indicators
        comprehension_indicators = self._build_comprehension_indicators(interaction)
        
        # Determine if adaptation is needed
        requires_adaptation, suggested_adaptations = self._determine_adaptations(
            interaction, comprehension_indicators
        )
        
        return InteractionAnalysisResult(
            session_hash=interaction.session_hash,
            response_pattern=response_pattern,
            engagement_level=engagement_level,
            comprehension_indicators=comprehension_indicators,
            requires_adaptation=requires_adaptation,
            suggested_adaptations=suggested_adaptations,
        )
    
    def analyze_interaction_sequence(
        self,
        interactions: List[InteractionData]
    ) -> Dict[str, Any]:
        """
        Analyze a sequence of interactions for patterns.
        
        Args:
            interactions: List of anonymized interactions
            
        Returns:
            Aggregated pattern analysis
        """
        if not interactions:
            return {
                "pattern_summary": "insufficient_data",
                "trend": "neutral",
                "adaptation_urgency": "low"
            }
        
        # Calculate response time statistics
        response_times = [i.response_time_ms for i in interactions]
        avg_response = statistics.mean(response_times)
        response_trend = self._calculate_trend(response_times)
        
        # Count clarifications
        total_clarifications = sum(i.clarification_count for i in interactions)
        repeated_errors = sum(1 for i in interactions if i.is_repeated_error)
        
        # Determine overall pattern
        if avg_response > self.slow_response_threshold:
            pattern_summary = "struggling"
            adaptation_urgency = "high"
        elif repeated_errors > len(interactions) * 0.3:
            pattern_summary = "persistent_difficulty"
            adaptation_urgency = "high"
        elif total_clarifications > len(interactions) * 2:
            pattern_summary = "needs_clarification"
            adaptation_urgency = "medium"
        elif response_trend == "improving":
            pattern_summary = "progressing"
            adaptation_urgency = "low"
        else:
            pattern_summary = "stable"
            adaptation_urgency = "low"
        
        return {
            "pattern_summary": pattern_summary,
            "trend": response_trend,
            "adaptation_urgency": adaptation_urgency,
            "metrics": {
                "avg_response_time_ms": round(avg_response),
                "total_clarifications": total_clarifications,
                "repeated_error_rate": round(repeated_errors / len(interactions), 2),
                "interaction_count": len(interactions)
            }
        }
    
    def _classify_response_pattern(
        self, 
        response_time_ms: int, 
        action_type: str
    ) -> str:
        """Classify the response pattern based on timing and action."""
        if action_type == "clarification":
            return "seeking_help"
        elif response_time_ms > self.slow_response_threshold:
            return "deliberate"
        elif response_time_ms < self.fast_response_threshold:
            return "quick"
        else:
            return "normal"
    
    def _assess_engagement(
        self, 
        time_on_content: int, 
        action_type: str,
        clarification_count: int
    ) -> str:
        """Assess engagement level - not performance or ability."""
        # High engagement indicators
        if action_type == "question" or clarification_count > 0:
            return "high"  # Asking questions = engaged
        elif time_on_content > 60:  # More than 1 minute
            return "high"
        elif time_on_content < 5:  # Less than 5 seconds
            return "low"
        else:
            return "medium"
    
    def _build_comprehension_indicators(
        self, 
        interaction: InteractionData
    ) -> Dict[str, Any]:
        """Build comprehension indicators without labeling ability."""
        indicators = {
            "response_speed": "normal",
            "help_seeking": False,
            "persistence": True,
            "content_engagement": "present"
        }
        
        # Response speed indicator
        if interaction.response_time_ms > self.slow_response_threshold:
            indicators["response_speed"] = "taking_time"
        elif interaction.response_time_ms < self.fast_response_threshold:
            indicators["response_speed"] = "quick"
        
        # Help-seeking behavior (positive indicator, not weakness)
        if interaction.clarification_count > 0 or interaction.action_type == "clarification":
            indicators["help_seeking"] = True
        
        # Persistence despite errors (positive indicator)
        if interaction.is_repeated_error:
            indicators["persistence"] = True
            indicators["may_benefit_from"] = "alternative_explanation"
        
        return indicators
    
    def _determine_adaptations(
        self, 
        interaction: InteractionData,
        indicators: Dict[str, Any]
    ) -> tuple[bool, List[AdaptationType]]:
        """Determine if and what adaptations might help."""
        adaptations = []
        
        # Slow response might benefit from simpler language
        if indicators.get("response_speed") == "taking_time":
            adaptations.append(AdaptationType.SIMPLIFY_LANGUAGE)
        
        # Repeated errors might benefit from different examples
        if interaction.is_repeated_error:
            adaptations.append(AdaptationType.ADD_EXAMPLES)
            adaptations.append(AdaptationType.CHANGE_REPRESENTATION)
        
        # High clarification count suggests need for simpler explanation
        if interaction.clarification_count >= self.high_clarification_threshold:
            adaptations.append(AdaptationType.SIMPLIFY_LANGUAGE)
        
        requires_adaptation = len(adaptations) > 0
        
        return requires_adaptation, adaptations
    
    def _calculate_trend(self, values: List[int]) -> str:
        """Calculate trend in a series of values."""
        if len(values) < 3:
            return "insufficient_data"
        
        # Simple trend: compare first half to second half
        midpoint = len(values) // 2
        first_half_avg = statistics.mean(values[:midpoint])
        second_half_avg = statistics.mean(values[midpoint:])
        
        threshold = 0.1  # 10% change threshold
        
        if second_half_avg < first_half_avg * (1 - threshold):
            return "improving"  # Response times decreasing = improving
        elif second_half_avg > first_half_avg * (1 + threshold):
            return "struggling"
        else:
            return "stable"
    
    @staticmethod
    def generate_deterministic_hash(data: Dict[str, Any]) -> str:
        """Generate deterministic hash for audit trail."""
        # Sort keys for deterministic ordering
        sorted_str = str(sorted(data.items()))
        return hashlib.sha256(sorted_str.encode()).hexdigest()[:16]
