# 📊 Customer Sentiment Alert Agent

An AI-powered hackathon project that monitors customer feedback in real-time, detects negative sentiment, flags urgent cases, and sends alerts via Slack. Built with Python, Streamlit, and HuggingFace Transformers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)

## 🎯 Project Overview

This project demonstrates how AI can help businesses stay on top of customer sentiment by:
- **Real-time Monitoring**: Simulates live customer feedback streaming
- **AI Sentiment Analysis**: Uses pre-trained HuggingFace models to detect positive/negative sentiment
- **Smart Urgency Detection**: Automatically flags urgent issues based on keywords
- **Instant Alerts**: Sends notifications to Slack for urgent customer issues
- **Visual Dashboard**: Beautiful Streamlit interface with color-coded feedback

Perfect for hackathons, demos, and as a foundation for production customer service tools!

## 🏗️ Project Structure

```
customer-sentiment-alert/
│
├── data/
│   └── sample_feedback.csv          # Sample customer feedback data
│
├── src/
│   ├── sentiment_analyzer.py        # AI sentiment analysis module
│   ├── alert_system.py              # Slack/Email alert handlers
│   └── utils.py                     # Data loading and streaming utilities
│
├── app.py                           # Streamlit dashboard application
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## ✨ Features

### 1. **AI-Powered Sentiment Analysis**
- Uses HuggingFace's `distilbert-base-uncased-finetuned-sst-2-english` model
- Detects POSITIVE/NEGATIVE sentiment with confidence scores
- Processes feedback in real-time

### 2. **Smart Urgency Detection**
Automatically flags HIGH urgency when negative feedback contains:
- "scam"
- "refund"
- "angry"
- "worst"
- "crash"

### 3. **Multi-Channel Alert System**
- **Slack Integration**: Sends formatted alerts via webhook
- **Visual Alerts**: Color-coded dashboard (red for urgent, green for positive)
- **Email Support**: Placeholder for future email notifications

### 4. **Interactive Dashboard**
- Real-time feedback streaming simulation
- Live statistics tracking
- Feedback history
- Configurable stream delay
- Easy Slack webhook integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) Slack workspace with webhook access

### Installation

1. **Clone or navigate to the project directory:**
   ```powershell
   cd "g:\AI hack\customer-sentiment-alert"
   ```

2. **Create a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Streamlit dashboard:**
   ```powershell
   streamlit run app.py
   ```

2. **The dashboard will open in your browser** (usually at `http://localhost:8501`)

3. **Configure Slack (Optional):**
   - Get a Slack webhook URL from your Slack workspace
   - Enter it in the sidebar
   - Enable "Slack Alerts" checkbox

4. **Start Monitoring:**
   - Click the "▶️ Start Monitoring" button
   - Watch as feedback is processed in real-time
   - Urgent alerts will be highlighted in red and sent to Slack

## 📊 Demo Flow

1. **Initial State**: Dashboard shows metrics at zero
2. **Click "Start Monitoring"**: AI model loads (first run takes ~10 seconds)
3. **Live Stream**: Feedback appears one by one with configurable delays
4. **Sentiment Analysis**: Each item is analyzed and color-coded
5. **Urgent Alerts**: High-urgency items trigger Slack notifications
6. **Statistics Update**: Real-time metrics show positive/negative/urgent counts
7. **History View**: Review all processed feedback in the history section

## 📁 Using Your Own Data

### ✅ The system now supports ANY CSV file format!

The application automatically detects and adapts to your CSV structure:

1. **Drop your CSV file** into the `data/` folder
2. Update the path in the code or name it `sample_feedback.csv`
3. The system will:
   - ✅ Auto-detect text columns (looks for review/feedback/comment/text columns)
   - ✅ Create IDs if they don't exist
   - ✅ Use existing date columns or generate timestamps
   - ✅ Handle any source/category column
   - ✅ Work with large datasets (configure max items in sidebar)

### 📋 CSV Requirements

**Minimum requirement:** Your CSV must have at least ONE column with text data (reviews, comments, feedback, etc.)

**Supported formats:**
- ✅ Standard format: `id, text, source, timestamp`
- ✅ Reviews: `review_text, rating, date, product_name`
- ✅ Social media: `tweet, user, created_at`
- ✅ Support tickets: `description, category, submitted_date`
- ✅ Any CSV with text content!

### 🎛️ Configuration Options

Adjust these in the sidebar:
- **Stream Delay**: 0.5 - 5 seconds (how fast feedback appears)
- **Max Items**: 5 - 1000 (limit items for large datasets)
- **Slack Webhook**: Optional alert integration

## 🎨 Dashboard Features

### Metrics Display
- **Total Feedback**: Running count of processed items
- **Positive**: Count of positive sentiment feedback
- **Negative**: Count of negative sentiment feedback
- **🚨 Urgent**: Count of high-urgency alerts

### Feedback Cards
- **Green Cards**: Positive or low-urgency feedback
- **Red Cards**: High-urgency negative feedback requiring immediate attention
- Each card shows: ID, source, timestamp, full text, sentiment score, and urgency level

### Configuration Sidebar
- Slack webhook URL input
- Alert toggle
- Stream delay adjustment (1-5 seconds)
- About section

## 🔧 Customization

### Adding More Sample Data
Edit `data/sample_feedback.csv`:
```csv
id,text,source,timestamp
6,"Your custom feedback here",Twitter,2025-10-01 17:00:00
```

### Changing Urgency Keywords
Edit `src/sentiment_analyzer.py`:
```python
self.urgency_keywords = ["scam", "refund", "angry", "worst", "crash", "your_keyword"]
```

### Using Different AI Models
Edit `src/sentiment_analyzer.py`:
```python
self.sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="your-preferred-model"
)
```

### Integrating Real APIs
Replace `simulate_stream()` in `app.py` with real API calls to:
- Twitter API
- Reddit API
- App Store/Play Store reviews
- Customer support tickets

## 🧪 Testing Individual Modules

Each module can be tested independently:

```powershell
# Test sentiment analyzer
python src/sentiment_analyzer.py

# Test alert system
python src/alert_system.py

# Test utilities
python src/utils.py
```

## 📦 No-Code Prototype Phase

Before building this full application, you can prototype the workflow using:

### Option 1: Google Sheets + Zapier
1. Create a Google Sheet with feedback entries
2. Use Zapier to:
   - Monitor new rows
   - Send to sentiment analysis API
   - Post alerts to Slack based on results

### Option 2: Google Sheets + Make (Integromat)
1. Set up Google Sheet as data source
2. Create Make scenario:
   - Trigger: New row in sheet
   - Action: Analyze sentiment
   - Condition: If negative + urgent keywords
   - Action: Send Slack message

This no-code approach is perfect for:
- Quick concept validation
- Non-technical stakeholder demos
- Rapid iteration before coding

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **Dashboard** | Streamlit | Interactive web interface |
| **AI/NLP** | HuggingFace Transformers | Sentiment analysis |
| **Data Processing** | Pandas | Data manipulation |
| **Alerts** | Slack Webhooks | Real-time notifications |
| **Data Storage** | CSV | Sample data (easily replaceable) |

## 🎯 Future Enhancements

- [ ] Integrate real-time Twitter/Reddit APIs
- [ ] Add email notification support
- [ ] Implement database for persistent storage
- [ ] Add sentiment trend graphs and analytics
- [ ] Multi-language support
- [ ] Custom AI model fine-tuning
- [ ] Team collaboration features
- [ ] Response templates for common issues
- [ ] Priority queue for customer service reps

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project for hackathons, learning, or commercial applications.

## 🙋 Support

For questions or issues:
- Check the code comments (each function is well-documented)
- Review the console output for debugging information
- Test individual modules independently

## 🏆 Hackathon Tips

1. **Demo Preparation**: Load the app before your presentation to cache the AI model
2. **Visual Impact**: Use the red urgent alerts to show the system's value
3. **Story**: Walk through a scenario where urgent feedback triggers immediate action
4. **Extensions**: Mention how easily this can integrate with real APIs
5. **Business Value**: Emphasize cost savings from catching issues early

## 📸 Screenshots

*(In a real hackathon, add screenshots here showing:)*
- Dashboard with live monitoring
- Urgent alert example
- Slack notification
- Metrics display

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [Slack Webhooks Guide](https://api.slack.com/messaging/webhooks)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Built with ❤️ for hackathons and rapid prototyping**

*Remember: This is a foundation. The real power comes from connecting it to real data sources and customizing it for your specific use case!*
