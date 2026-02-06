"""
Unit Tests for Interaction Analyzer
Verifies:
- Pattern extraction from metrics
- Adaptation flags
- Engagement assessment
"""
import pytest
from modules.interaction_analyzer import InteractionAnalyzer
from models.schemas import InteractionData


class TestInteractionAnalyzer:
    
    def setup_method(self):
        self.analyzer = InteractionAnalyzer()
    
    def test_analyze_slow_response(self, slow_interaction):
        """Test analysis of struggle patterns (slow response)."""
        result = self.analyzer.analyze_single_interaction(slow_interaction)
        
        assert result.response_pattern == "deliberate"
        assert result.requires_adaptation is True
        assert result.comprehension_indicators["response_speed"] == "taking_time"
        
    def test_analyze_quick_response(self):
        """Test analysis of comfortable patterns (quick response)."""
        interaction = InteractionData(
            session_hash="test_123",
            content_id="abc",
            response_time_ms=500,  # Quick
            action_type="read",
            content_text="Simple",
            is_repeated_error=False,
            clarification_count=0,
            time_on_content_seconds=5
        )
        
        result = self.analyzer.analyze_single_interaction(interaction)
        
        assert result.response_pattern == "quick"
        assert result.requires_adaptation is False
        
    def test_analyze_help_seeking(self):
        """Test analysis of help-seeking behavior."""
        interaction = InteractionData(
            session_hash="test_123",
            content_id="abc",
            response_time_ms=5000,
            action_type="clarification",
            content_text="Confusing",
            is_repeated_error=False,
            clarification_count=1,
            time_on_content_seconds=20
        )
        
        result = self.analyzer.analyze_single_interaction(interaction)
        
        assert result.response_pattern == "seeking_help"
        assert result.engagement_level == "high"  # Help seeking = engagement
        assert result.comprehension_indicators["help_seeking"] is True
