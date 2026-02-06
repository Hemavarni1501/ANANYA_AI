"""
Unit Tests for Adaptive Engine
Verifies:
- Content adaptation generation
- Simplification logic
- Pacing adjustments
"""
import pytest
from modules.adaptive_engine import AdaptiveEngine
from models.schemas import AdaptationRequest, AdaptationType


class TestAdaptiveEngine:
    
    def setup_method(self):
        self.engine = AdaptiveEngine()
    
    def test_simplify_language(self, complex_text):
        """Test language simplification."""
        req = AdaptationRequest(
            session_hash="test_123",
            original_content=complex_text,
            requested_adaptations=[AdaptationType.SIMPLIFY_LANGUAGE],
            interaction_signals={"clarification_count": 5}
        )
        
        result = self.engine.generate_adaptation(req)
        
        assert len(result.adaptations) > 0
        adaptation = result.adaptations[0]
        assert adaptation.adaptation_type == AdaptationType.SIMPLIFY_LANGUAGE
        assert adaptation.complexity_level == "simple"
        assert len(adaptation.content) < len(complex_text)  # Should be shorter/simpler

    def test_add_examples(self):
        """Test example generation."""
        content = "Neural networks are function approximators."
        req = AdaptationRequest(
            session_hash="test_123",
            original_content=content,
            requested_adaptations=[AdaptationType.ADD_EXAMPLES],
            interaction_signals={"is_repeated_error": True}
        )
        
        result = self.engine.generate_adaptation(req)
        
        adaptation = result.adaptations[0]
        assert adaptation.adaptation_type == AdaptationType.ADD_EXAMPLES
        assert "example" in adaptation.content.lower() or "instance" in adaptation.content.lower()

    def test_adjust_pace(self):
        """Test pacing adjustment (chunking)."""
        # Create long content
        long_content = "Sentence 1. " * 20
        
        req = AdaptationRequest(
            session_hash="test_123",
            original_content=long_content,
            requested_adaptations=[AdaptationType.ADJUST_PACE],
            interaction_signals={"response_time_ms": 20000}
        )
        
        result = self.engine.generate_adaptation(req)
        
        adaptation = result.adaptations[0]
        assert adaptation.adaptation_type == AdaptationType.ADJUST_PACE
        # Check for chunk separators
        assert "\n\n---\n\n" in adaptation.content or len(adaptation.changes_made) > 0

    def test_multiple_adaptations(self, complex_text):
        """Test requesting multiple adaptations at once."""
        req = AdaptationRequest(
            session_hash="test_123",
            original_content=complex_text,
            requested_adaptations=[
                AdaptationType.SIMPLIFY_LANGUAGE, 
                AdaptationType.CHANGE_REPRESENTATION
            ],
            interaction_signals={}
        )
        
        result = self.engine.generate_adaptation(req)
        
        assert len(result.adaptations) == 2
        assert result.primary_recommendation is not None
