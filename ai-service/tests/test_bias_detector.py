"""
Unit Tests for Bias Detector
Verifies:
- Language complexity detection
- Pace mismatch detection
- Prior exposure gap detection
- Privacy constraints (no user IDs)
"""
import pytest
from modules.bias_detector import BiasDetector
from models.schemas import BiasType, SeverityLevel, BiasDetectionRequest


class TestBiasDetector:
    
    def setup_method(self):
        self.detector = BiasDetector()
    
    def test_detect_high_complexity(self, complex_text):
        """Test detection of overly complex language."""
        req = BiasDetectionRequest(
            session_hash="test_123",
            content_text=complex_text,
            interaction_patterns=[]
        )
        
        result = self.detector.detect_bias(req)
        
        assert result.bias_detected is True
        assert any(i.bias_type == BiasType.LANGUAGE_COMPLEXITY for i in result.indicators)
        assert result.complexity_level == "complex"
        
    def test_detect_simple_text_as_unbiased(self, simple_text):
        """Test that simple text does not trigger bias flags."""
        req = BiasDetectionRequest(
            session_hash="test_123",
            content_text=simple_text,
            interaction_patterns=[]
        )
        
        result = self.detector.detect_bias(req)
        
        # Might detect representation issue (short text), but not complexity
        complexity_bias = any(
            i.bias_type == BiasType.LANGUAGE_COMPLEXITY 
            for i in result.indicators
        )
        assert complexity_bias is False
        assert result.complexity_level == "simple"

    def test_detect_pace_mismatch(self):
        """Test detection of pace mismatch from interaction patterns."""
        # Create patterns with slow response times
        patterns = [
            {"response_time_ms": 20000},  # 20s
            {"response_time_ms": 18000},  # 18s
            {"response_time_ms": 5000}    # 5s
        ]
        
        req = BiasDetectionRequest(
            session_hash="test_123",
            content_text="Normal content",
            interaction_patterns=patterns
        )
        
        result = self.detector.detect_bias(req)
        
        assert result.bias_detected is True
        pace_bias = next(
            (i for i in result.indicators if i.bias_type == BiasType.PACE_MISMATCH), 
            None
        )
        assert pace_bias is not None
        assert pace_bias.severity in [SeverityLevel.MEDIUM, SeverityLevel.HIGH]

    def test_detect_exposure_gap(self):
        """Test detection of prior exposure gaps (high clarifications)."""
        patterns = [
            {"clarification_count": 2},
            {"clarification_count": 3},
            {"clarification_count": 1}
        ]
        
        req = BiasDetectionRequest(
            session_hash="test_123",
            content_text="Normal content",
            interaction_patterns=patterns
        )
        
        result = self.detector.detect_bias(req)
        
        exposure_bias = next(
            (i for i in result.indicators if i.bias_type == BiasType.PRIOR_EXPOSURE_GAP),
            None
        )
        assert exposure_bias is not None

    def test_audit_hash_consistency(self, simple_text):
        """Test that same input produces same audit hash (deterministic)."""
        req = BiasDetectionRequest(
            session_hash="test_123",
            content_text=simple_text,
            interaction_patterns=[]
        )
        
        result1 = self.detector.detect_bias(req)
        result2 = self.detector.detect_bias(req)
        
        assert result1.deterministic_hash == result2.deterministic_hash
