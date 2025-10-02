"""
Alert System Module
Handles sending alerts to external services like Slack.
"""

import requests
from typing import Optional


def send_slack_alert(message: str, webhook_url: str) -> bool:
    """
    Send an alert message to Slack via webhook.
    
    Args:
        message (str): The alert message to send
        webhook_url (str): The Slack webhook URL to post to
        
    Returns:
        bool: True if alert was sent successfully, False otherwise
    """
    try:
        # Prepare the payload for Slack
        payload = {
            "text": message,
            "username": "Sentiment Alert Bot",
            "icon_emoji": ":warning:"
        }
        
        # Send POST request to Slack webhook
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        # Check if request was successful
        if response.status_code == 200:
            print(f"✅ Slack alert sent successfully!")
            return True
        else:
            print(f"❌ Failed to send Slack alert. Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending Slack alert: {e}")
        return False


def format_alert_message(feedback_id: int, text: str, sentiment: str, 
                        score: float, urgency: str, source: str, 
                        timestamp: str) -> str:
    """
    Format a structured alert message for urgent feedback.
    
    Args:
        feedback_id (int): ID of the feedback
        text (str): The feedback text
        sentiment (str): Detected sentiment
        score (float): Confidence score
        urgency (str): Urgency level
        source (str): Source of feedback (Twitter, App Review, etc.)
        timestamp (str): When the feedback was received
        
    Returns:
        str: Formatted alert message
    """
    alert = f"""
🚨 *URGENT CUSTOMER FEEDBACK ALERT* 🚨

*Feedback ID:* {feedback_id}
*Source:* {source}
*Timestamp:* {timestamp}

*Sentiment:* {sentiment} (Confidence: {score})
*Urgency Level:* {urgency}

*Feedback Text:*
"{text}"

⚠️ *Action Required:* Please review and respond to this customer immediately.
    """
    return alert.strip()


def send_email_alert(message: str, recipient: str, 
                     smtp_config: Optional[dict] = None) -> bool:
    """
    Placeholder for email alert functionality.
    Can be implemented with smtplib for production use.
    
    Args:
        message (str): The alert message
        recipient (str): Email address to send to
        smtp_config (dict, optional): SMTP server configuration
        
    Returns:
        bool: Success status
    """
    # TODO: Implement email sending with smtplib
    print(f"📧 Email alert would be sent to: {recipient}")
    print(f"Message: {message[:100]}...")
    return True


# Example usage for testing
if __name__ == "__main__":
    # Test message formatting
    test_message = format_alert_message(
        feedback_id=123,
        text="This is a scam! I want my refund now!",
        sentiment="NEGATIVE",
        score=0.998,
        urgency="HIGH",
        source="Twitter",
        timestamp="2025-10-01 14:30:00"
    )
    
    print("Formatted Alert Message:")
    print(test_message)
    print("\n" + "="*50 + "\n")
    
    # Note: Replace with actual webhook URL to test
    # Example: send_slack_alert(test_message, "https://hooks.slack.com/services/YOUR/WEBHOOK/URL")
    print("To test Slack alerts, add your webhook URL and uncomment the line above.")
