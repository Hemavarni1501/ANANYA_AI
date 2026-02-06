"""
ANANYA-AI Text Analysis Utilities
Readability, complexity, and linguistic analysis tools

Uses textstat for readability metrics - no external API calls needed.
"""
import textstat
import re
from typing import Dict, Any, List, Tuple


class TextAnalyzer:
    """
    Analyzes text for readability, complexity, and linguistic features.
    Used by bias detection to identify language complexity issues.
    """
    
    @staticmethod
    def get_readability_metrics(text: str) -> Dict[str, float]:
        """
        Calculate comprehensive readability metrics.
        
        Returns:
            Dict with multiple readability scores
        """
        if not text or len(text.strip()) < 10:
            return {
                "flesch_kincaid_grade": 0.0,
                "flesch_reading_ease": 100.0,
                "gunning_fog": 0.0,
                "smog_index": 0.0,
                "automated_readability_index": 0.0,
                "coleman_liau_index": 0.0,
                "dale_chall_readability": 0.0,
            }
        
        return {
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
            "flesch_reading_ease": textstat.flesch_reading_ease(text),
            "gunning_fog": textstat.gunning_fog(text),
            "smog_index": textstat.smog_index(text),
            "automated_readability_index": textstat.automated_readability_index(text),
            "coleman_liau_index": textstat.coleman_liau_index(text),
            "dale_chall_readability": textstat.dale_chall_readability_score(text),
        }
    
    @staticmethod
    def get_complexity_level(flesch_kincaid_grade: float) -> str:
        """
        Convert Flesch-Kincaid grade to complexity level.
        
        Args:
            flesch_kincaid_grade: Grade level score
            
        Returns:
            'simple', 'moderate', or 'complex'
        """
        if flesch_kincaid_grade <= 6:
            return "simple"
        elif flesch_kincaid_grade <= 10:
            return "moderate"
        else:
            return "complex"
    
    @staticmethod
    def get_text_statistics(text: str) -> Dict[str, int]:
        """
        Get basic text statistics.
        
        Returns:
            Dict with word count, sentence count, etc.
        """
        return {
            "word_count": textstat.lexicon_count(text, removepunct=True),
            "sentence_count": textstat.sentence_count(text),
            "syllable_count": textstat.syllable_count(text),
            "char_count": len(text),
            "avg_words_per_sentence": round(
                textstat.lexicon_count(text, removepunct=True) / 
                max(textstat.sentence_count(text), 1), 2
            ),
        }
    
    @staticmethod
    def identify_complex_words(text: str, syllable_threshold: int = 3) -> List[str]:
        """
        Identify words that may be difficult to understand.
        
        Args:
            text: Text to analyze
            syllable_threshold: Minimum syllables to consider complex
            
        Returns:
            List of complex words found
        """
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        complex_words = []
        
        for word in set(words):  # Unique words only
            if textstat.syllable_count(word) >= syllable_threshold:
                complex_words.append(word)
        
        return sorted(complex_words)
    
    @staticmethod
    def identify_jargon_patterns(text: str) -> List[Dict[str, Any]]:
        """
        Identify potential jargon or technical language patterns.
        Uses heuristics - not demographic assumptions.
        
        Returns:
            List of potential jargon indicators
        """
        patterns = []
        
        # Academic/technical patterns
        academic_markers = [
            r'\b(therefore|hence|thus|wherein|whereby|herein)\b',
            r'\b(aforementioned|notwithstanding|pursuant)\b',
            r'\b(paradigm|methodology|framework|implementation)\b',
            r'\b(utilizing|commenced|terminated|facilitated)\b',
        ]
        
        for pattern in academic_markers:
            matches = re.findall(pattern, text.lower())
            if matches:
                patterns.append({
                    "type": "academic_language",
                    "matches": list(set(matches)),
                    "suggestion": "Consider simpler alternatives"
                })
        
        # Long sentence detection
        sentences = re.split(r'[.!?]+', text)
        long_sentences = [s.strip() for s in sentences if len(s.split()) > 30]
        if long_sentences:
            patterns.append({
                "type": "long_sentences",
                "count": len(long_sentences),
                "suggestion": "Break into shorter sentences"
            })
        
        return patterns
    
    @staticmethod
    def simplify_text(text: str, level: str = "moderate") -> str:
        """
        Apply basic text simplification.
        
        Args:
            text: Original text
            level: 'simple' or 'moderate'
            
        Returns:
            Simplified text
        """
        simplified = text
        
        # Common academic → simple word replacements
        replacements = {
            "utilize": "use",
            "implement": "do",
            "facilitate": "help",
            "commence": "start",
            "terminate": "end",
            "prior to": "before",
            "subsequent to": "after",
            "in order to": "to",
            "due to the fact that": "because",
            "at this point in time": "now",
            "in the event that": "if",
            "for the purpose of": "to",
            "in addition to": "also",
            "with regard to": "about",
            "in accordance with": "following",
            "nevertheless": "but",
            "furthermore": "also",
            "consequently": "so",
            "approximately": "about",
            "sufficient": "enough",
            "demonstrate": "show",
            "indicate": "show",
            "obtain": "get",
            "require": "need",
            "assist": "help",
            "attempt": "try",
            "determine": "find out",
            "establish": "set up",
            "evaluate": "check",
            "identify": "find",
            "maintain": "keep",
            "modify": "change",
            "perform": "do",
            "provide": "give",
            "regarding": "about",
            "remain": "stay",
            "request": "ask for",
            "select": "choose",
            "therefore": "so",
            "currently": "now",
            "additional": "more",
            "component": "part",
            "methodology": "method",
            "functionality": "feature",
        }
        
        for complex_word, simple_word in replacements.items():
            # Case-insensitive replacement preserving first letter case
            pattern = re.compile(re.escape(complex_word), re.IGNORECASE)
            simplified = pattern.sub(simple_word, simplified)
        
        if level == "simple":
            # Additional simplification: break long sentences
            sentences = re.split(r'([.!?]+)', simplified)
            new_sentences = []
            
            for i, sentence in enumerate(sentences):
                if i % 2 == 0:  # Actual sentences (not punctuation)
                    words = sentence.split()
                    if len(words) > 20:
                        # Try to split at conjunctions
                        midpoint = len(words) // 2
                        new_sentences.append(' '.join(words[:midpoint]) + '.')
                        new_sentences.append(' '.join(words[midpoint:]))
                    else:
                        new_sentences.append(sentence)
                else:
                    if new_sentences:
                        new_sentences[-1] += sentence
            
            simplified = ' '.join(new_sentences)
        
        return simplified.strip()
    
    @staticmethod
    def generate_reading_time_estimate(text: str, wpm: int = 200) -> Dict[str, Any]:
        """
        Estimate reading time for content.
        
        Args:
            text: Content text
            wpm: Words per minute (default 200 for average reader)
            
        Returns:
            Dict with reading time estimates
        """
        word_count = textstat.lexicon_count(text, removepunct=True)
        minutes = word_count / wpm
        
        return {
            "word_count": word_count,
            "estimated_minutes": round(minutes, 1),
            "estimated_seconds": round(minutes * 60),
            "complexity_adjusted_minutes": round(
                minutes * (1 + (textstat.flesch_kincaid_grade(text) / 20)), 1
            )
        }
