"""
ANANYA-AI FastAPI Application
Bias-Aware Academic Support AI Services

Port: 8002 (as per TECH_STACK.md)

Endpoints:
- POST /analyze-interaction - Extract response patterns
- POST /detect-bias - Identify unfair complexity  
- POST /generate-adaptation - Adjust explanations

PRIVACY ENFORCEMENT:
- No user identifiers accepted in any endpoint
- All processing is stateless
- Deterministic output for auditability
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ananya-ai")

# Import configuration
from config import settings

# Import models
from models.schemas import (
    InteractionData,
    InteractionAnalysisResult,
    BiasDetectionRequest,
    BiasDetectionResult,
    AdaptationRequest,
    AdaptationResult,
)

# Import core modules
from modules.bias_detector import BiasDetector
from modules.adaptive_engine import AdaptiveEngine
from modules.interaction_analyzer import InteractionAnalyzer


# Initialize AI modules
bias_detector = BiasDetector()
adaptive_engine = AdaptiveEngine()
interaction_analyzer = InteractionAnalyzer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("🚀 ANANYA-AI Service starting...")
    logger.info(f"📍 Running on port {settings.API_PORT}")
    logger.info("✅ Bias Detector initialized")
    logger.info("✅ Adaptive Engine initialized")
    logger.info("✅ Interaction Analyzer initialized")
    logger.info("🔒 Privacy mode: ENABLED (no user identifiers accepted)")
    yield
    logger.info("👋 ANANYA-AI Service shutting down...")


# Create FastAPI application
app = FastAPI(
    title="ANANYA-AI Service",
    description=(
        "Bias-Aware Academic Support AI - Detects and mitigates academic bias "
        "through ethical, privacy-preserving AI. No user profiling or demographic inference."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return {
        "service": "ANANYA-AI",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "privacy_mode": "enabled"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check for monitoring."""
    return {
        "status": "healthy",
        "services": {
            "bias_detector": "operational",
            "adaptive_engine": "operational",
            "interaction_analyzer": "operational"
        },
        "configuration": {
            "complexity_threshold_high": settings.COMPLEXITY_THRESHOLD_HIGH,
            "complexity_threshold_medium": settings.COMPLEXITY_THRESHOLD_MEDIUM,
            "log_user_identifiers": settings.LOG_USER_IDENTIFIERS  # Should be False
        }
    }


# ============== Core AI Endpoints ==============

@app.post(
    "/analyze-interaction",
    response_model=InteractionAnalysisResult,
    tags=["AI Core"],
    summary="Analyze interaction patterns",
    description="Extract response patterns from anonymized interaction data. No user profiling."
)
async def analyze_interaction(interaction: InteractionData):
    """
    Analyze a single learning interaction.
    
    This endpoint processes anonymized interaction data to detect:
    - Response patterns (quick, normal, deliberate)
    - Engagement levels (based on behavior, not demographics)
    - Comprehension indicators (from interaction signals)
    - Suggested adaptations (if needed)
    
    **Privacy Guarantee**: No user identifiers processed or stored.
    """
    try:
        logger.info(f"Analyzing interaction for session: {interaction.session_hash[:8]}...")
        
        result = interaction_analyzer.analyze_single_interaction(interaction)
        
        logger.info(
            f"Analysis complete. Pattern: {result.response_pattern}, "
            f"Requires adaptation: {result.requires_adaptation}"
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing interaction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze interaction. Please try again."
        )


@app.post(
    "/detect-bias",
    response_model=BiasDetectionResult,
    tags=["AI Core"],
    summary="Detect bias in content/interactions",
    description="Identify language complexity, pace mismatch, and exposure gaps without demographic inference."
)
async def detect_bias(request: BiasDetectionRequest):
    """
    Detect potential bias in academic content and interactions.
    
    This endpoint analyzes:
    - **Language Complexity**: Is content unnecessarily complex?
    - **Pace Mismatch**: Does delivery speed match comprehension patterns?
    - **Prior Exposure Gaps**: Does content assume non-universal prior knowledge?
    - **Representation Issues**: Are alternative formats needed?
    
    **Privacy Guarantee**: 
    - Works on interaction patterns only
    - No demographic inference
    - No student labeling or profiling
    """
    try:
        logger.info(f"Detecting bias for session: {request.session_hash[:8]}...")
        
        result = bias_detector.detect_bias(request)
        
        if result.bias_detected:
            logger.info(
                f"Bias detected: {len(result.indicators)} indicator(s). "
                f"Complexity level: {result.complexity_level}"
            )
        else:
            logger.info("No significant bias detected.")
        
        return result
        
    except Exception as e:
        logger.error(f"Error detecting bias: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to detect bias. Please try again."
        )


@app.post(
    "/generate-adaptation",
    response_model=AdaptationResult,
    tags=["AI Core"],
    summary="Generate adapted explanations",
    description="Create simplified or alternative content representations based on interaction signals."
)
async def generate_adaptation(request: AdaptationRequest):
    """
    Generate adapted versions of academic content.
    
    Available adaptation types:
    - **SIMPLIFY_LANGUAGE**: Reduce complexity, simplify vocabulary
    - **ADD_EXAMPLES**: Add concrete examples and illustrations
    - **CHANGE_REPRESENTATION**: Convert format (paragraph → bullets, etc.)
    - **ADJUST_PACE**: Break into smaller, digestible chunks
    
    **Privacy Guarantee**:
    - Based on interaction signals, not user profiles
    - No persistent learner state
    - Deterministic output for auditability
    """
    try:
        logger.info(
            f"Generating adaptation for session: {request.session_hash[:8]}... "
            f"Types: {[a.value for a in request.requested_adaptations]}"
        )
        
        result = adaptive_engine.generate_adaptation(request)
        
        logger.info(
            f"Generated {len(result.adaptations)} adaptation(s). "
            f"Primary: {result.primary_recommendation.adaptation_type.value if result.primary_recommendation else 'None'}"
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating adaptation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate adaptation. Please try again."
        )


# ============== Utility Endpoints ==============

@app.post(
    "/analyze-content",
    tags=["Utilities"],
    summary="Analyze content readability",
    description="Get readability metrics for academic content."
)
async def analyze_content(content: dict):
    """
    Analyze content for readability metrics.
    
    Returns Flesch-Kincaid grade level, reading ease, and other metrics.
    """
    from utils.text_analysis import TextAnalyzer
    
    text = content.get("text", "")
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text content is required"
        )
    
    analyzer = TextAnalyzer()
    
    return {
        "readability": analyzer.get_readability_metrics(text),
        "statistics": analyzer.get_text_statistics(text),
        "complexity_level": analyzer.get_complexity_level(
            analyzer.get_readability_metrics(text).get("flesch_kincaid_grade", 0)
        ),
        "complex_words": analyzer.identify_complex_words(text)[:10],
        "reading_time": analyzer.generate_reading_time_estimate(text)
    }


@app.post(
    "/simplify-text",
    tags=["Utilities"],
    summary="Simplify text content",
    description="Apply text simplification without full adaptation flow."
)
async def simplify_text(request: dict):
    """
    Quick text simplification utility.
    
    Args:
        text: The text to simplify
        level: 'simple' or 'moderate' (default: moderate)
    """
    from utils.text_analysis import TextAnalyzer
    
    text = request.get("text", "")
    level = request.get("level", "moderate")
    
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text content is required"
        )
    
    if level not in ["simple", "moderate"]:
        level = "moderate"
    
    analyzer = TextAnalyzer()
    simplified = analyzer.simplify_text(text, level)
    
    return {
        "original": text,
        "simplified": simplified,
        "level": level,
        "original_grade": analyzer.get_readability_metrics(text).get("flesch_kincaid_grade", 0),
        "simplified_grade": analyzer.get_readability_metrics(simplified).get("flesch_kincaid_grade", 0)
    }


# ============== Entry Point ==============

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
