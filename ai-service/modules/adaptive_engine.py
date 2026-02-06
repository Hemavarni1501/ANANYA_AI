"""
ANANYA-AI Adaptive Explanation Engine
Generates adapted content based on detected bias signals.

Capabilities:
- Multiple difficulty variants per concept
- Language simplification
- Alternative representation formats
- Contextual example generation

PRIVACY CONSTRAINTS:
- No user profiling used
- Adaptations based on interaction signals only
- No persistent learner state
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import re

from models.schemas import (
    AdaptationRequest,
    AdaptationResult,
    AdaptedContent,
    AdaptationType,
)
from utils.text_analysis import TextAnalyzer
from config import settings


class AdaptiveEngine:
    """
    Generates adapted explanations based on interaction signals.
    
    This engine creates multiple versions of content optimized
    for different comprehension needs - WITHOUT profiling learners.
    """
    
    def __init__(self):
        """Initialize the adaptive engine."""
        self.text_analyzer = TextAnalyzer()
        self.simplification_levels = settings.SIMPLIFICATION_LEVELS
    
    def generate_adaptation(
        self, 
        request: AdaptationRequest
    ) -> AdaptationResult:
        """
        Generate adapted versions of content.
        
        Args:
            request: AdaptationRequest with original content and signals
            
        Returns:
            AdaptationResult with adapted versions
        """
        adaptations: List[AdaptedContent] = []
        
        # Process each requested adaptation type
        for adaptation_type in request.requested_adaptations:
            adapted = self._apply_adaptation(
                request.original_content,
                adaptation_type,
                request.interaction_signals
            )
            if adapted:
                adaptations.append(adapted)
        
        # Determine primary recommendation
        primary = self._select_primary_adaptation(
            adaptations, 
            request.interaction_signals
        )
        
        # Build reasoning
        reasoning = self._build_adaptation_reasoning(
            request.requested_adaptations,
            request.interaction_signals
        )
        
        # Generate deterministic hash
        audit_hash = self._generate_audit_hash(
            request.session_hash,
            request.original_content,
            adaptations
        )
        
        return AdaptationResult(
            session_hash=request.session_hash,
            original_content=request.original_content,
            adaptations=adaptations,
            primary_recommendation=primary,
            adaptation_reasoning=reasoning,
            deterministic_hash=audit_hash,
        )
    
    def _apply_adaptation(
        self,
        content: str,
        adaptation_type: AdaptationType,
        signals: Dict[str, Any]
    ) -> Optional[AdaptedContent]:
        """Apply a specific adaptation type to content."""
        
        if adaptation_type == AdaptationType.SIMPLIFY_LANGUAGE:
            return self._simplify_language(content, signals)
        elif adaptation_type == AdaptationType.ADD_EXAMPLES:
            return self._add_examples(content, signals)
        elif adaptation_type == AdaptationType.CHANGE_REPRESENTATION:
            return self._change_representation(content, signals)
        elif adaptation_type == AdaptationType.ADJUST_PACE:
            return self._adjust_pace(content, signals)
        
        return None
    
    def _simplify_language(
        self, 
        content: str, 
        signals: Dict[str, Any]
    ) -> AdaptedContent:
        """
        Simplify the language in content.
        Creates a more accessible version.
        """
        # Determine simplification level based on signals
        clarification_count = signals.get("clarification_count", 0)
        
        if clarification_count > 3:
            level = "simple"
        else:
            level = "moderate"
        
        # Apply text simplification
        simplified = self.text_analyzer.simplify_text(content, level)
        
        # Track changes made
        changes = []
        
        # Get original and new metrics
        orig_metrics = self.text_analyzer.get_readability_metrics(content)
        new_metrics = self.text_analyzer.get_readability_metrics(simplified)
        
        orig_grade = orig_metrics.get("flesch_kincaid_grade", 0)
        new_grade = new_metrics.get("flesch_kincaid_grade", 0)
        
        if new_grade < orig_grade:
            changes.append(
                f"Reduced reading level from grade {orig_grade:.1f} to {new_grade:.1f}"
            )
        
        # Count word replacements
        orig_words = set(content.lower().split())
        new_words = set(simplified.lower().split())
        replaced_count = len(orig_words - new_words)
        if replaced_count > 0:
            changes.append(f"Simplified {replaced_count} complex terms")
        
        # Check sentence structure changes
        orig_sentences = content.count('.') + content.count('!') + content.count('?')
        new_sentences = simplified.count('.') + simplified.count('!') + simplified.count('?')
        if new_sentences > orig_sentences:
            changes.append("Broke long sentences into shorter ones")
        
        if not changes:
            changes.append("Applied vocabulary simplification")
        
        return AdaptedContent(
            adaptation_type=AdaptationType.SIMPLIFY_LANGUAGE,
            content=simplified,
            complexity_level=level,
            changes_made=changes,
        )
    
    def _add_examples(
        self, 
        content: str, 
        signals: Dict[str, Any]
    ) -> AdaptedContent:
        """
        Add examples to content.
        Generates contextual examples to aid understanding.
        """
        changes = []
        
        # Check if examples already exist
        example_markers = ["for example", "e.g.", "for instance", "such as"]
        has_examples = any(marker in content.lower() for marker in example_markers)
        
        # Extract key concepts from content
        key_concepts = self._extract_key_concepts(content)
        
        # Generate example additions
        enhanced_content = content
        
        if not has_examples and key_concepts:
            # Add a general example section
            example_section = self._generate_example_section(key_concepts)
            enhanced_content = content + "\n\n" + example_section
            changes.append(f"Added example section for {len(key_concepts)} key concepts")
        
        # Add inline examples for complex terms
        inline_examples = self._add_inline_examples(enhanced_content)
        if inline_examples != enhanced_content:
            enhanced_content = inline_examples
            changes.append("Added inline examples for complex terms")
        
        if not changes:
            changes.append("Content already contains sufficient examples")
        
        return AdaptedContent(
            adaptation_type=AdaptationType.ADD_EXAMPLES,
            content=enhanced_content,
            complexity_level="moderate",
            changes_made=changes,
        )
    
    def _change_representation(
        self, 
        content: str, 
        signals: Dict[str, Any]
    ) -> AdaptedContent:
        """
        Change the representation format of content.
        Converts between formats (text → bullets, abstract → concrete).
        """
        changes = []
        modified = content
        
        # Convert dense paragraphs to bullet points
        if len(content) > 200 and content.count('\n') < 3:
            bulleted = self._convert_to_bullets(content)
            if bulleted != content:
                modified = bulleted
                changes.append("Converted dense text to bullet points")
        
        # Add structural markers
        if not any(marker in content for marker in ['•', '-', '*', '1.', '2.']):
            structured = self._add_structure(modified)
            if structured != modified:
                modified = structured
                changes.append("Added structural organization")
        
        # Add summary at the beginning if content is long
        if len(content) > 500:
            with_summary = self._add_summary(modified)
            if with_summary != modified:
                modified = with_summary
                changes.append("Added summary introduction")
        
        if not changes:
            changes.append("Reorganized content structure")
        
        return AdaptedContent(
            adaptation_type=AdaptationType.CHANGE_REPRESENTATION,
            content=modified,
            complexity_level="moderate",
            changes_made=changes,
        )
    
    def _adjust_pace(
        self, 
        content: str, 
        signals: Dict[str, Any]
    ) -> AdaptedContent:
        """
        Adjust content for different pacing.
        Breaks content into smaller, digestible chunks.
        """
        changes = []
        
        # Split into logical chunks
        chunks = self._split_into_chunks(content)
        
        if len(chunks) > 1:
            # Add transition markers
            paced_content = self._add_pace_markers(chunks)
            changes.append(f"Divided content into {len(chunks)} digestible sections")
        else:
            paced_content = content
            changes.append("Content is already appropriately paced")
        
        # Add "pause and reflect" prompts for long content
        if len(content) > 800:
            with_pauses = self._add_reflection_prompts(paced_content)
            if with_pauses != paced_content:
                paced_content = with_pauses
                changes.append("Added reflection checkpoints")
        
        return AdaptedContent(
            adaptation_type=AdaptationType.ADJUST_PACE,
            content=paced_content,
            complexity_level="simple",
            changes_made=changes,
        )
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content for example generation."""
        # Simple extraction: look for capitalized terms, technical words
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        
        # Also look for terms in quotes or emphasis
        quoted = re.findall(r'"([^"]+)"', content)
        
        # Filter to unique concepts
        concepts = list(set(words + quoted))[:5]  # Limit to 5
        
        return concepts
    
    def _generate_example_section(self, concepts: List[str]) -> str:
        """Generate an example section for concepts."""
        if not concepts:
            return ""
        
        lines = ["**Examples to help understand:**", ""]
        for concept in concepts[:3]:  # Limit examples
            lines.append(f"• **{concept}**: [This concept can be understood as...]")
        
        return "\n".join(lines)
    
    def _add_inline_examples(self, content: str) -> str:
        """Add inline examples after complex terms."""
        # This is a simplified implementation
        # In production, this would use NLP to identify terms needing examples
        complex_words = self.text_analyzer.identify_complex_words(content)
        
        if not complex_words:
            return content
        
        # Add simple clarification for first few complex words found
        modified = content
        for word in complex_words[:2]:  # Limit to avoid over-modification
            # Find word in content and add parenthetical
            pattern = rf'\b({re.escape(word)})\b'
            if word not in ["example", "understanding"]:  # Avoid meta-words
                # Only add if not already have parenthetical after
                if f"{word} (" not in modified.lower():
                    modified = re.sub(
                        pattern,
                        r'\1 (in simpler terms)',
                        modified,
                        count=1,
                        flags=re.IGNORECASE
                    )
        
        return modified
    
    def _convert_to_bullets(self, content: str) -> str:
        """Convert paragraph text to bullet points."""
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        if len(sentences) < 3:
            return content
        
        bullets = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                bullets.append(f"• {sentence}")
        
        return "\n".join(bullets)
    
    def _add_structure(self, content: str) -> str:
        """Add structural organization to content."""
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        
        if len(paragraphs) < 2:
            # Try to split a long paragraph
            sentences = re.split(r'(?<=[.!?])\s+', content)
            if len(sentences) >= 4:
                mid = len(sentences) // 2
                return '\n\n'.join([
                    ' '.join(sentences[:mid]),
                    ' '.join(sentences[mid:])
                ])
            return content
        
        # Add numbers/headers to paragraphs
        structured = []
        for i, para in enumerate(paragraphs, 1):
            if para.strip():
                structured.append(f"**Part {i}:**\n{para}")
        
        return '\n\n'.join(structured)
    
    def _add_summary(self, content: str) -> str:
        """Add a brief summary at the beginning."""
        # Extract first sentence as basis for summary
        first_sentence = re.split(r'(?<=[.!?])\s+', content)[0]
        
        if len(first_sentence) > 100:
            first_sentence = first_sentence[:100] + "..."
        
        summary = f"**Quick Overview:** {first_sentence}\n\n---\n\n"
        return summary + content
    
    def _split_into_chunks(self, content: str) -> List[str]:
        """Split content into logical chunks for pacing."""
        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        
        if len(paragraphs) >= 3:
            return paragraphs
        
        # If single paragraph, split by sentences into groups
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        if len(sentences) < 4:
            return [content]
        
        # Group sentences into chunks of 2-3
        chunks = []
        chunk_size = 3
        for i in range(0, len(sentences), chunk_size):
            chunk = ' '.join(sentences[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def _add_pace_markers(self, chunks: List[str]) -> str:
        """Add markers between chunks for pacing."""
        if len(chunks) <= 1:
            return chunks[0] if chunks else ""
        
        marked_chunks = []
        for i, chunk in enumerate(chunks):
            marked_chunks.append(chunk)
            if i < len(chunks) - 1:
                marked_chunks.append("\n\n---\n\n")
        
        return ''.join(marked_chunks)
    
    def _add_reflection_prompts(self, content: str) -> str:
        """Add reflection prompts for longer content."""
        # Find midpoint
        midpoint = len(content) // 2
        
        # Find a sentence break near midpoint
        search_start = max(0, midpoint - 50)
        search_end = min(len(content), midpoint + 50)
        
        for i in range(midpoint, search_end):
            if content[i] in '.!?' and i + 1 < len(content):
                insert_point = i + 1
                reflection = "\n\n💡 **Pause and reflect:** What's the main point so far?\n\n"
                return content[:insert_point] + reflection + content[insert_point:]
        
        return content
    
    def _select_primary_adaptation(
        self, 
        adaptations: List[AdaptedContent],
        signals: Dict[str, Any]
    ) -> Optional[AdaptedContent]:
        """Select the primary recommended adaptation."""
        if not adaptations:
            return None
        
        # Priority based on signals
        signal_priority = {}
        
        if signals.get("clarification_count", 0) > 2:
            signal_priority[AdaptationType.SIMPLIFY_LANGUAGE] = 1
        if signals.get("is_repeated_error"):
            signal_priority[AdaptationType.ADD_EXAMPLES] = 1
        if signals.get("response_time_ms", 0) > 15000:
            signal_priority[AdaptationType.ADJUST_PACE] = 1
        
        # Find highest priority adaptation
        for adaptation in adaptations:
            if adaptation.adaptation_type in signal_priority:
                return adaptation
        
        # Default to first adaptation
        return adaptations[0]
    
    def _build_adaptation_reasoning(
        self,
        requested_types: List[AdaptationType],
        signals: Dict[str, Any]
    ) -> str:
        """Build reasoning explanation for adaptations."""
        reasons = []
        
        for adapt_type in requested_types:
            if adapt_type == AdaptationType.SIMPLIFY_LANGUAGE:
                reasons.append(
                    "Language simplified based on interaction patterns indicating "
                    "comprehension barriers"
                )
            elif adapt_type == AdaptationType.ADD_EXAMPLES:
                reasons.append(
                    "Examples added to provide concrete understanding of abstract concepts"
                )
            elif adapt_type == AdaptationType.CHANGE_REPRESENTATION:
                reasons.append(
                    "Content restructured to offer alternative learning pathway"
                )
            elif adapt_type == AdaptationType.ADJUST_PACE:
                reasons.append(
                    "Content chunked to allow for gradual comprehension"
                )
        
        return " | ".join(reasons) if reasons else "Standard adaptation applied"
    
    def _generate_audit_hash(
        self,
        session_hash: str,
        original: str,
        adaptations: List[AdaptedContent]
    ) -> str:
        """Generate deterministic hash for audit trail."""
        data = {
            "session": session_hash,
            "original_hash": hashlib.sha256(original.encode()).hexdigest()[:16],
            "adaptation_types": sorted([a.adaptation_type.value for a in adaptations])
        }
        data_str = str(sorted(data.items()))
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def generate_multiple_variants(
        self,
        content: str,
        num_variants: int = 3
    ) -> List[AdaptedContent]:
        """
        Generate multiple difficulty variants of content.
        
        Args:
            content: Original content
            num_variants: Number of variants to generate (default 3)
            
        Returns:
            List of adapted content at different complexity levels
        """
        variants = []
        
        # Original complexity
        variants.append(AdaptedContent(
            adaptation_type=AdaptationType.SIMPLIFY_LANGUAGE,
            content=content,
            complexity_level="original",
            changes_made=["Original content preserved"]
        ))
        
        # Moderate simplification
        moderate = self.text_analyzer.simplify_text(content, "moderate")
        variants.append(AdaptedContent(
            adaptation_type=AdaptationType.SIMPLIFY_LANGUAGE,
            content=moderate,
            complexity_level="moderate",
            changes_made=["Vocabulary simplified", "Technical terms clarified"]
        ))
        
        # Maximum simplification
        simple = self.text_analyzer.simplify_text(content, "simple")
        variants.append(AdaptedContent(
            adaptation_type=AdaptationType.SIMPLIFY_LANGUAGE,
            content=simple,
            complexity_level="simple",
            changes_made=[
                "Maximum vocabulary simplification",
                "Sentences shortened",
                "Complex structures removed"
            ]
        ))
        
        return variants[:num_variants]
