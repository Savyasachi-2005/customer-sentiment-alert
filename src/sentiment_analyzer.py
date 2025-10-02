"""
Sentiment Analyzer Module
Uses HuggingFace Transformers for sentiment analysis and applies urgency rules.
"""

from transformers import pipeline
from typing import Dict


class SentimentAnalyzer:
    """
    Analyzes customer feedback sentiment and determines urgency level.
    Uses a pre-trained HuggingFace model for sentiment classification.
    """
    
    def __init__(self):
        """
        Initialize the sentiment analysis pipeline.
        Uses distilbert-base-uncased-finetuned-sst-2-english model by default.
        """
        print("Loading sentiment analysis model...")
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        print("Model loaded successfully!")
        
        # Keywords that indicate high urgency when combined with negative sentiment
        self.urgency_keywords = [
            "scam", "refund", "angry", "worst", "crash", 
            "terrible", "horrible", "awful", "disaster", "garbage",
            "poor experience", "poor service", "poor cleanliness",
            "defective", "broken", "never again", "waste of money"
        ]
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze the sentiment of a given text and determine urgency level.
        
        Args:
            text (str): The customer feedback text to analyze
            
        Returns:
            dict: Dictionary containing:
                - sentiment (str): "POSITIVE" or "NEGATIVE"
                - score (float): Confidence score rounded to 3 decimals
                - urgency (str): "HIGH" or "LOW"
        """
        # Get sentiment from HuggingFace model
        result = self.sentiment_pipeline(text)[0]
        
        sentiment = result['label']
        score = round(result['score'], 3)
        
        # Determine urgency based on sentiment and keywords
        urgency = self._determine_urgency(text, sentiment)
        
        return {
            "sentiment": sentiment,
            "score": score,
            "urgency": urgency
        }
    
    def _determine_urgency(self, text: str, sentiment: str) -> str:
        """
        Determine if the feedback is urgent based on sentiment and keywords.
        
        Args:
            text (str): The feedback text
            sentiment (str): The detected sentiment (POSITIVE/NEGATIVE)
            
        Returns:
            str: "HIGH" if urgent, "LOW" otherwise
        """
        # Only negative feedback can be urgent
        if sentiment == "NEGATIVE":
            text_lower = text.lower()
            
            # Check if any urgency keyword is present
            for keyword in self.urgency_keywords:
                if keyword in text_lower:
                    return "HIGH"
            
            # Additional check: count number of "poor" mentions (indicates severe issues)
            poor_count = text_lower.count("poor")
            if poor_count >= 2:  # Multiple poor ratings = urgent
                return "HIGH"
        
        return "LOW"
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze multiple texts at once.
        
        Args:
            texts (list): List of feedback texts
            
        Returns:
            list: List of analysis results
        """
        return [self.analyze(text) for text in texts]


# Example usage for testing
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # Test samples
    test_texts = [
        "This product is amazing! Best purchase ever.",
        "Worst experience! This is a scam and I want a refund!",
        "Pretty good overall, minor issues but okay."
    ]
    
    for text in test_texts:
        result = analyzer.analyze(text)
        print(f"\nText: {text}")
        print(f"Result: {result}")
