"""
ANANYA-AI Bias Detection Module
Core innovation: Detect academic bias WITHOUT demographic profiling.

Detects:
- Language complexity mismatch
- Pace mismatch
- Prior exposure gaps
- Representation issues

CRITICAL CONSTRAINTS (from PRD.md):
❌ No demographic inference
❌ No student labeling
❌ No intelligence prediction
❌ No identity storage

All detection is based on INTERACTION PATTERNS only.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib

from models.schemas import (
    BiasDetectionRequest,
    BiasDetectionResult,
    BiasIndicator,
    BiasType,
    SeverityLevel,
    AdaptationType,
)
from utils.text_analysis import TextAnalyzer
from config import settings


class BiasDetector:
    """
    Detects bias in academic content and learning interactions.
    
    This module identifies potential barriers in content that may
    disadvantage learners - WITHOUT profiling individual students.
    """
    
    def __init__(self):
        """Initialize the bias detector with configured thresholds."""
        self.complexity_threshold_high = settings.COMPLEXITY_THRESHOLD_HIGH
        self.complexity_threshold_medium = settings.COMPLEXITY_THRESHOLD_MEDIUM
        self.text_analyzer = TextAnalyzer()
    
    def detect_bias(self, request: BiasDetectionRequest) -> BiasDetectionResult:
        """
        Analyze content and interaction patterns for potential bias.
        
        Args:
            request: BiasDetectionRequest with content and interaction data
            
        Returns:
            BiasDetectionResult with detected indicators
        """
        indicators: List[BiasIndicator] = []
        recommended_actions: List[AdaptationType] = []
        
        # 1. Analyze content complexity
        readability_metrics = self.text_analyzer.get_readability_metrics(
            request.content_text
        )
        complexity_indicators = self._detect_language_complexity_bias(
            request.content_text, readability_metrics
        )
        indicators.extend(complexity_indicators)
        
        # 2. Analyze interaction patterns for pace mismatch
        if request.interaction_patterns:
            pace_indicators = self._detect_pace_mismatch(
                request.interaction_patterns
            )
            indicators.extend(pace_indicators)
        
        # 3. Detect prior exposure gaps (based on interaction patterns)
        if request.interaction_patterns:
            exposure_indicators = self._detect_prior_exposure_gaps(
                request.interaction_patterns
            )
            indicators.extend(exposure_indicators)
        
        # 4. Check for representation issues in content
        representation_indicators = self._detect_representation_issues(
            request.content_text
        )
        indicators.extend(representation_indicators)
        
        # Build recommendations based on detected bias
        recommended_actions = self._build_recommendations(indicators)
        
        # Determine overall complexity level
        fk_grade = readability_metrics.get("flesch_kincaid_grade", 0)
        complexity_level = self.text_analyzer.get_complexity_level(fk_grade)
        
        # Generate deterministic hash for audit
        audit_hash = self._generate_audit_hash(
            request.session_hash,
            request.content_text,
            indicators
        )
        
        return BiasDetectionResult(
            session_hash=request.session_hash,
            bias_detected=len(indicators) > 0,
            indicators=indicators,
            readability_score=fk_grade,
            complexity_level=complexity_level,
            recommended_actions=recommended_actions,
            analysis_timestamp=datetime.utcnow().isoformat(),
            deterministic_hash=audit_hash,
        )
    
    def _detect_language_complexity_bias(
        self, 
        content: str, 
        metrics: Dict[str, float]
    ) -> List[BiasIndicator]:
        """
        Detect if content language is unnecessarily complex.
        
        High complexity that could be simplified = potential bias
        against learners without advanced vocabulary.
        """
        indicators = []
        fk_grade = metrics.get("flesch_kincaid_grade", 0)
        
        # High complexity detection
        if fk_grade >= self.complexity_threshold_high:
            indicators.append(BiasIndicator(
                bias_type=BiasType.LANGUAGE_COMPLEXITY,
                severity=SeverityLevel.HIGH,
                confidence=0.85,
                description=(
                    f"Content readability at grade level {fk_grade:.1f} "
                    f"may exclude learners without advanced vocabulary"
                ),
                affected_content_segment=content[:200] if len(content) > 200 else content
            ))
        elif fk_grade >= self.complexity_threshold_medium:
            indicators.append(BiasIndicator(
                bias_type=BiasType.LANGUAGE_COMPLEXITY,
                severity=SeverityLevel.MEDIUM,
                confidence=0.70,
                description=(
                    f"Content at grade level {fk_grade:.1f} - "
                    f"consider providing simpler alternatives"
                ),
                affected_content_segment=None
            ))
        
        # Detect jargon patterns
        jargon_patterns = self.text_analyzer.identify_jargon_patterns(content)
        if jargon_patterns:
            for pattern in jargon_patterns:
                if pattern["type"] == "academic_language":
                    indicators.append(BiasIndicator(
                        bias_type=BiasType.LANGUAGE_COMPLEXITY,
                        severity=SeverityLevel.LOW,
                        confidence=0.60,
                        description=(
                            f"Academic jargon detected: {', '.join(pattern['matches'][:5])}"
                        ),
                        affected_content_segment=None
                    ))
        
        # Detect complex words
        complex_words = self.text_analyzer.identify_complex_words(content)
        if len(complex_words) > 10:
            indicators.append(BiasIndicator(
                bias_type=BiasType.LANGUAGE_COMPLEXITY,
                severity=SeverityLevel.MEDIUM,
                confidence=0.65,
                description=(
                    f"High density of complex words ({len(complex_words)} found)"
                ),
                affected_content_segment=None
            ))
        
        return indicators
    
    def _detect_pace_mismatch(
        self, 
        interaction_patterns: List[Dict[str, Any]]
    ) -> List[BiasIndicator]:
        """
        Detect pace mismatch from interaction patterns.
        
        Pace mismatch = content delivery speed doesn't match
        learner's processing speed (based on patterns, not profiling).
        """
        indicators = []
        
        if not interaction_patterns:
            return indicators
        
        # Analyze response times
        response_times = [
            p.get("response_time_ms", 0) 
            for p in interaction_patterns 
            if "response_time_ms" in p
        ]
        
        if not response_times:
            return indicators
        
        avg_response = sum(response_times) / len(response_times)
        
        # Count slow responses (taking more than threshold)
        slow_threshold_ms = 15000  # 15 seconds
        slow_responses = sum(1 for t in response_times if t > slow_threshold_ms)
        slow_ratio = slow_responses / len(response_times)
        
        if slow_ratio > 0.5:  # More than half responses are slow
            indicators.append(BiasIndicator(
                bias_type=BiasType.PACE_MISMATCH,
                severity=SeverityLevel.HIGH,
                confidence=0.75,
                description=(
                    "Interaction patterns suggest content pace may be too fast. "
                    f"{slow_ratio:.0%} of responses exceeded expected time."
                ),
                affected_content_segment=None
            ))
        elif slow_ratio > 0.3:
            indicators.append(BiasIndicator(
                bias_type=BiasType.PACE_MISMATCH,
                severity=SeverityLevel.MEDIUM,
                confidence=0.60,
                description=(
                    "Some pace mismatch detected. Consider offering "
                    "pace adjustment options."
                ),
                affected_content_segment=None
            ))
        
        return indicators
    
    def _detect_prior_exposure_gaps(
        self, 
        interaction_patterns: List[Dict[str, Any]]
    ) -> List[BiasIndicator]:
        """
        Detect patterns suggesting prior exposure gaps.
        
        This detects when content assumes prior knowledge that
        may not be universal - WITHOUT assuming demographics.
        """
        indicators = []
        
        # Count clarification requests
        clarification_count = sum(
            p.get("clarification_count", 0) 
            for p in interaction_patterns
        )
        
        # Count repeated errors (same concept multiple times)
        repeated_errors = sum(
            1 for p in interaction_patterns if p.get("is_repeated_error", False)
        )
        
        total_interactions = len(interaction_patterns)
        if total_interactions == 0:
            return indicators
        
        clarification_ratio = clarification_count / total_interactions
        error_ratio = repeated_errors / total_interactions
        
        # High clarification rate suggests assumed prior knowledge
        if clarification_ratio > 1.5:  # More than 1.5 clarifications per interaction
            indicators.append(BiasIndicator(
                bias_type=BiasType.PRIOR_EXPOSURE_GAP,
                severity=SeverityLevel.HIGH,
                confidence=0.70,
                description=(
                    "High clarification rate suggests content may assume "
                    "prior knowledge that isn't universal"
                ),
                affected_content_segment=None
            ))
        
        # Repeated errors on same concepts
        if error_ratio > 0.4:
            indicators.append(BiasIndicator(
                bias_type=BiasType.PRIOR_EXPOSURE_GAP,
                severity=SeverityLevel.MEDIUM,
                confidence=0.65,
                description=(
                    "Repeated errors suggest foundational concepts "
                    "may need additional scaffolding"
                ),
                affected_content_segment=None
            ))
        
        return indicators
    
    def _detect_representation_issues(
        self, 
        content: str
    ) -> List[BiasIndicator]:
        """
        Detect potential representation issues in content.
        
        Checks for:
        - Single format only (no alternatives)
        - Lack of examples
        - Abstract without concrete
        """
        indicators = []
        
        # Check for lack of examples
        example_markers = ["for example", "e.g.", "for instance", "such as", "example:"]
        has_examples = any(marker in content.lower() for marker in example_markers)
        
        if len(content) > 500 and not has_examples:
            indicators.append(BiasIndicator(
                bias_type=BiasType.REPRESENTATION_ISSUE,
                severity=SeverityLevel.LOW,
                confidence=0.55,
                description=(
                    "Content lacks concrete examples which may "
                    "disadvantage learners who benefit from examples"
                ),
                affected_content_segment=None
            ))
        
        # Check for purely abstract content (no numbers, no concrete terms)
        import re
        has_numbers = bool(re.search(r'\d+', content))
        has_lists = bool(re.search(r'^\s*[-•*]\s+', content, re.MULTILINE))
        
        if len(content) > 300 and not has_numbers and not has_lists:
            indicators.append(BiasIndicator(
                bias_type=BiasType.REPRESENTATION_ISSUE,
                severity=SeverityLevel.LOW,
                confidence=0.50,
                description=(
                    "Content is highly abstract. Consider adding "
                    "concrete representations or structured lists."
                ),
                affected_content_segment=None
            ))
        
        return indicators
    
    def _build_recommendations(
        self, 
        indicators: List[BiasIndicator]
    ) -> List[AdaptationType]:
        """Build recommended actions based on detected bias."""
        recommendations = set()
        
        for indicator in indicators:
            if indicator.bias_type == BiasType.LANGUAGE_COMPLEXITY:
                recommendations.add(AdaptationType.SIMPLIFY_LANGUAGE)
            elif indicator.bias_type == BiasType.PACE_MISMATCH:
                recommendations.add(AdaptationType.ADJUST_PACE)
            elif indicator.bias_type == BiasType.PRIOR_EXPOSURE_GAP:
                recommendations.add(AdaptationType.ADD_EXAMPLES)
                recommendations.add(AdaptationType.SIMPLIFY_LANGUAGE)
            elif indicator.bias_type == BiasType.REPRESENTATION_ISSUE:
                recommendations.add(AdaptationType.ADD_EXAMPLES)
                recommendations.add(AdaptationType.CHANGE_REPRESENTATION)
        
        return list(recommendations)
    
    def _generate_audit_hash(
        self, 
        session_hash: str, 
        content: str, 
        indicators: List[BiasIndicator]
    ) -> str:
        """Generate deterministic hash for audit trail."""
        data = {
            "session": session_hash,
            "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16],
            "indicator_count": len(indicators),
            "indicator_types": sorted([i.bias_type.value for i in indicators])
        }
        data_str = str(sorted(data.items()))
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def get_bias_summary(
        self, 
        indicators: List[BiasIndicator]
    ) -> Dict[str, Any]:
        """Generate a summary of detected bias for reporting."""
        if not indicators:
            return {
                "bias_detected": False,
                "summary": "No significant bias indicators detected",
                "severity_distribution": {}
            }
        
        severity_counts = {}
        type_counts = {}
        
        for indicator in indicators:
            # Count by severity
            sev = indicator.severity.value
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            
            # Count by type
            bt = indicator.bias_type.value
            type_counts[bt] = type_counts.get(bt, 0) + 1
        
        return {
            "bias_detected": True,
            "total_indicators": len(indicators),
            "severity_distribution": severity_counts,
            "type_distribution": type_counts,
            "highest_severity": max(
                [i.severity for i in indicators], 
                key=lambda s: ["low", "medium", "high"].index(s.value)
            ).value
        }
