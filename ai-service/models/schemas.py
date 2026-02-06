"""
ANANYA-AI Pydantic Schemas
Request/Response models for API endpoints

PRIVACY NOTICE:
- No user identifiers (userId, email, name) are accepted
- Only anonymized session data is processed
- All requests are stateless
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# ============== Enums ==============

class BiasType(str, Enum):
    """Types of bias detected in academic content/interactions."""
    LANGUAGE_COMPLEXITY = "language_complexity"
    PACE_MISMATCH = "pace_mismatch"
    PRIOR_EXPOSURE_GAP = "prior_exposure_gap"
    REPRESENTATION_ISSUE = "representation_issue"


class SeverityLevel(str, Enum):
    """Severity levels for detected bias."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AdaptationType(str, Enum):
    """Types of content adaptation."""
    SIMPLIFY_LANGUAGE = "simplify_language"
    ADD_EXAMPLES = "add_examples"
    CHANGE_REPRESENTATION = "change_representation"
    ADJUST_PACE = "adjust_pace"


# ============== Interaction Analysis ==============

class InteractionData(BaseModel):
    """
    Anonymized interaction data from a learning session.
    NO user identifiers allowed.
    """
    session_hash: str = Field(..., description="Anonymized session identifier")
    content_id: str = Field(..., description="Content/topic identifier")
    
    # Interaction metrics (no PII)
    response_time_ms: int = Field(..., ge=0, description="Time to respond in milliseconds")
    action_type: str = Field(..., description="Type of action: read, question, clarification")
    content_text: Optional[str] = Field(None, description="The content being interacted with")
    
    # Pattern indicators
    is_repeated_error: bool = Field(False, description="Whether this is a repeated error")
    clarification_count: int = Field(0, ge=0, description="Number of clarifications requested")
    time_on_content_seconds: int = Field(0, ge=0, description="Time spent on content")


class InteractionAnalysisResult(BaseModel):
    """Result of analyzing interaction patterns."""
    session_hash: str
    
    # Pattern analysis
    response_pattern: str = Field(..., description="Detected response pattern")
    engagement_level: str = Field(..., description="low, medium, high")
    comprehension_indicators: Dict[str, Any] = Field(default_factory=dict)
    
    # Flags for potential issues (no labeling)
    requires_adaptation: bool = Field(False)
    suggested_adaptations: List[AdaptationType] = Field(default_factory=list)


# ============== Bias Detection ==============

class BiasDetectionRequest(BaseModel):
    """
    Request for bias detection in content or interactions.
    Operates on patterns only, no demographic inference.
    """
    session_hash: str = Field(..., description="Anonymized session identifier")
    content_text: str = Field(..., description="Content to analyze for bias")
    
    # Interaction context (anonymized)
    interaction_patterns: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of anonymized interaction patterns"
    )
    
    # Optional: Previous adaptations applied
    previous_adaptations: List[str] = Field(default_factory=list)


class BiasIndicator(BaseModel):
    """A single bias indicator detected."""
    bias_type: BiasType
    severity: SeverityLevel
    confidence: float = Field(..., ge=0.0, le=1.0)
    description: str
    affected_content_segment: Optional[str] = None


class BiasDetectionResult(BaseModel):
    """Result of bias detection analysis."""
    session_hash: str
    
    # Bias indicators found
    bias_detected: bool = Field(False)
    indicators: List[BiasIndicator] = Field(default_factory=list)
    
    # Content metrics
    readability_score: float = Field(..., description="Flesch-Kincaid grade level")
    complexity_level: str = Field(..., description="simple, moderate, complex")
    
    # Recommendations (not labels)
    recommended_actions: List[AdaptationType] = Field(default_factory=list)
    
    # Audit fields
    analysis_timestamp: str
    deterministic_hash: str = Field(..., description="Hash for audit trail")


# ============== Adaptive Explanations ==============

class AdaptationRequest(BaseModel):
    """
    Request to generate adapted content.
    No user profiling - based on interaction signals only.
    """
    session_hash: str = Field(..., description="Anonymized session identifier")
    original_content: str = Field(..., description="Original content to adapt")
    
    # What adaptations to apply
    requested_adaptations: List[AdaptationType] = Field(
        ..., min_length=1, description="Types of adaptation to apply"
    )
    
    # Current context (no demographics)
    current_complexity_level: Optional[str] = Field(None)
    interaction_signals: Dict[str, Any] = Field(
        default_factory=dict,
        description="Signals from interactions (time, errors, etc.)"
    )


class AdaptedContent(BaseModel):
    """A single adapted version of content."""
    adaptation_type: AdaptationType
    content: str
    complexity_level: str  # simple, moderate, original
    changes_made: List[str]


class AdaptationResult(BaseModel):
    """Result of content adaptation."""
    session_hash: str
    original_content: str
    
    # Adapted versions
    adaptations: List[AdaptedContent] = Field(default_factory=list)
    
    # Metadata
    primary_recommendation: Optional[AdaptedContent] = None
    adaptation_reasoning: str
    
    # Audit
    deterministic_hash: str
