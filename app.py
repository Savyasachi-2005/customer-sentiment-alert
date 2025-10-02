"""
Customer Sentiment Alert Dashboard
Real-time monitoring dashboard for customer feedback sentiment analysis.
"""

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.sentiment_analyzer import SentimentAnalyzer
from src.alert_system import send_slack_alert, format_alert_message
from src.utils import load_data, simulate_stream


# Page configuration
st.set_page_config(
    page_title="Customer Sentiment Alert Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .urgent-alert {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000;
    }
    .urgent-alert h3 {
        color: #c62828;
        margin-top: 0;
    }
    .urgent-alert strong {
        color: #000000;
    }
    .normal-feedback {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000;
    }
    .normal-feedback h3 {
        color: #2e7d32;
        margin-top: 0;
    }
    .normal-feedback strong {
        color: #000000;
    }
    .negative-feedback {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000;
    }
    .negative-feedback h3 {
        color: #e65100;
        margin-top: 0;
    }
    .negative-feedback strong {
        color: #000000;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = None
    if 'monitoring' not in st.session_state:
        st.session_state.monitoring = False
    if 'feedback_history' not in st.session_state:
        st.session_state.feedback_history = []
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            'total': 0,
            'positive': 0,
            'negative': 0,
            'urgent': 0
        }


def load_analyzer():
    """Load the sentiment analyzer (cached in session state)."""
    if st.session_state.analyzer is None:
        with st.spinner("Loading AI model... This may take a moment on first run."):
            st.session_state.analyzer = SentimentAnalyzer()
    return st.session_state.analyzer


def display_feedback(feedback: dict, analysis: dict):
    """
    Display a single feedback item with appropriate styling.
    
    Args:
        feedback (dict): Raw feedback data
        analysis (dict): Sentiment analysis results
    """
    is_urgent = analysis['urgency'] == 'HIGH'
    is_positive = analysis['sentiment'] == 'POSITIVE'
    
    # Truncate text if too long (for display purposes)
    text_display = feedback['text']
    if len(text_display) > 300:
        text_display = text_display[:300] + "..."
    
    # Truncate source name if too long
    source_display = str(feedback['source'])
    if len(source_display) > 50:
        source_display = source_display[:50] + "..."
    
    # Choose styling based on urgency and sentiment
    if is_urgent:
        st.markdown(f"""
            <div class="urgent-alert">
                <h3>🚨 URGENT: {source_display}</h3>
                <p><strong>ID:</strong> {feedback['id']} | <strong>Time:</strong> {feedback['timestamp']}</p>
                <p><strong>Feedback:</strong> {text_display}</p>
                <p><strong>Sentiment:</strong> {analysis['sentiment']} 
                   (Confidence: {analysis['score']}) | 
                   <strong>Urgency:</strong> <span style="color: #c62828; font-weight: bold;">{analysis['urgency']}</span></p>
            </div>
        """, unsafe_allow_html=True)
    elif is_positive:
        st.markdown(f"""
            <div class="normal-feedback">
                <h3>✅ {source_display}</h3>
                <p><strong>ID:</strong> {feedback['id']} | <strong>Time:</strong> {feedback['timestamp']}</p>
                <p><strong>Feedback:</strong> {text_display}</p>
                <p><strong>Sentiment:</strong> <span style="color: #2e7d32; font-weight: bold;">{analysis['sentiment']}</span> 
                   (Confidence: {analysis['score']}) | 
                   <strong>Urgency:</strong> {analysis['urgency']}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Negative but not urgent
        st.markdown(f"""
            <div class="negative-feedback">
                <h3>⚠️ {source_display}</h3>
                <p><strong>ID:</strong> {feedback['id']} | <strong>Time:</strong> {feedback['timestamp']}</p>
                <p><strong>Feedback:</strong> {text_display}</p>
                <p><strong>Sentiment:</strong> <span style="color: #e65100; font-weight: bold;">{analysis['sentiment']}</span> 
                   (Confidence: {analysis['score']}) | 
                   <strong>Urgency:</strong> {analysis['urgency']}</p>
            </div>
        """, unsafe_allow_html=True)


def update_stats(analysis: dict):
    """Update statistics based on new analysis."""
    st.session_state.stats['total'] += 1
    if analysis['sentiment'] == 'POSITIVE':
        st.session_state.stats['positive'] += 1
    else:
        st.session_state.stats['negative'] += 1
    if analysis['urgency'] == 'HIGH':
        st.session_state.stats['urgent'] += 1


def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.title("📊 Customer Sentiment Alert Dashboard")
    st.markdown("Real-time monitoring of customer feedback with AI-powered sentiment analysis")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # CSV file selection
    import os
    csv_files = [f for f in os.listdir('data') if f.endswith('.csv')]
    selected_csv = st.sidebar.selectbox(
        "Select CSV File",
        csv_files,
        index=csv_files.index('sample_feedback_clean.csv') if 'sample_feedback_clean.csv' in csv_files else 0,
        help="Choose which CSV file to load"
    )
    
    # Slack webhook configuration
    slack_webhook = st.sidebar.text_input(
        "Slack Webhook URL (optional)",
        type="password",
        help="Enter your Slack webhook URL to receive alerts"
    )
    slack_enabled = st.sidebar.checkbox(
        "Enable Slack Alerts",
        value=False,
        disabled=not slack_webhook
    )
    
    # Stream delay configuration
    stream_delay = st.sidebar.slider(
        "Stream Delay (seconds)",
        min_value=0.5,
        max_value=5.0,
        value=1.0,
        step=0.5,
        help="Delay between processing each feedback item"
    )
    
    # Max items to process
    max_items = st.sidebar.number_input(
        "Max Items to Process",
        min_value=5,
        max_value=1000,
        value=50,
        step=5,
        help="Limit the number of feedback items to process (useful for large datasets)"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 About")
    st.sidebar.info(
        "This dashboard monitors customer feedback in real-time, "
        "analyzes sentiment using AI, and alerts your team about urgent issues. "
        "Supports any CSV format!"
    )
    
    # Main content area - Create metric placeholders
    col1, col2, col3, col4 = st.columns(4)
    
    metric_total = col1.empty()
    metric_positive = col2.empty()
    metric_negative = col3.empty()
    metric_urgent = col4.empty()
    
    # Initial metric display
    metric_total.metric("Total Feedback", st.session_state.stats['total'])
    metric_positive.metric("Positive", st.session_state.stats['positive'], 
                          delta_color="normal")
    metric_negative.metric("Negative", st.session_state.stats['negative'],
                          delta_color="inverse")
    metric_urgent.metric("🚨 Urgent", st.session_state.stats['urgent'],
                        delta_color="inverse")
    
    st.markdown("---")
    
    # Control buttons
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        start_button = st.button("▶️ Start Monitoring", type="primary", 
                                 disabled=st.session_state.monitoring)
    
    with col_btn2:
        stop_button = st.button("⏹️ Stop Monitoring", 
                               disabled=not st.session_state.monitoring)
    
    if stop_button:
        st.session_state.monitoring = False
        st.rerun()
    
    # Feedback display area
    feedback_container = st.container()
    
    if start_button:
        st.session_state.monitoring = True
        st.session_state.feedback_history = []  # Clear previous history
        st.session_state.stats = {'total': 0, 'positive': 0, 'negative': 0, 'urgent': 0}  # Reset stats
        
        # Load data and analyzer
        try:
            df = load_data(f"data/{selected_csv}")
            
            # Limit the number of rows to process
            total_available = len(df)
            if total_available > max_items:
                df = df.head(max_items)
                st.info(f"📊 Processing {max_items} out of {total_available} available feedback items. Adjust 'Max Items to Process' in sidebar to change.")
            else:
                st.info(f"📊 Processing all {total_available} feedback items from the dataset.")
            
            analyzer = load_analyzer()
            
            with feedback_container:
                st.subheader("📱 Live Feedback Stream")
                
                # Create a placeholder for progress
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                # Container for all feedback items
                feedback_display = st.container()
                
                total_items = len(df)
                
                # Process feedback stream
                for idx, feedback in enumerate(simulate_stream(df, delay=stream_delay)):
                    if not st.session_state.monitoring:
                        break
                    
                    # Update progress
                    progress_text.text(f"Processing feedback {idx + 1} of {total_items}...")
                    progress_bar.progress((idx + 1) / total_items)
                    
                    # Analyze sentiment
                    analysis = analyzer.analyze(feedback['text'])
                    
                    # Update statistics
                    update_stats(analysis)
                    
                    # Update metrics in real-time
                    metric_total.metric("Total Feedback", st.session_state.stats['total'])
                    metric_positive.metric("Positive", st.session_state.stats['positive'], 
                                          delta_color="normal")
                    metric_negative.metric("Negative", st.session_state.stats['negative'],
                                          delta_color="inverse")
                    metric_urgent.metric("🚨 Urgent", st.session_state.stats['urgent'],
                                        delta_color="inverse")
                    
                    # Display feedback in the container (each one stays visible)
                    with feedback_display:
                        display_feedback(feedback, analysis)
                    
                    # Send Slack alert if urgent and enabled
                    if analysis['urgency'] == 'HIGH' and slack_enabled and slack_webhook:
                        alert_message = format_alert_message(
                            feedback_id=feedback['id'],
                            text=feedback['text'],
                            sentiment=analysis['sentiment'],
                            score=analysis['score'],
                            urgency=analysis['urgency'],
                            source=feedback['source'],
                            timestamp=feedback['timestamp']
                        )
                        success = send_slack_alert(alert_message, slack_webhook)
                        if success:
                            st.success(f"✅ Slack alert sent for feedback #{feedback['id']}")
                    
                    # Add to history
                    st.session_state.feedback_history.append({
                        'feedback': feedback,
                        'analysis': analysis
                    })
                
                # Clear progress indicators
                progress_text.empty()
                progress_bar.empty()
                
                st.session_state.monitoring = False
                st.success("✅ Monitoring completed! All feedback processed.")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.monitoring = False
    
    # Display feedback history
    if st.session_state.feedback_history:
        st.markdown("---")
        st.subheader("📜 Feedback History")
        
        with st.expander("View All Previous Feedback", expanded=False):
            for item in reversed(st.session_state.feedback_history):
                display_feedback(item['feedback'], item['analysis'])


if __name__ == "__main__":
    main()
