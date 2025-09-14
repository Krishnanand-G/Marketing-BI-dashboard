# AI-Powered Marketing Intelligence Dashboard

A comprehensive BI dashboard that combines traditional analytics with Google Gemini AI to provide intelligent insights, automated recommendations, and interactive chat capabilities for marketing performance analysis.

## 🚀 Features

### 📊 Core Analytics
- **Interactive Filters**: Date range, platform, and state selection
- **Performance Trends**: Revenue vs marketing spend correlation
- **Platform Analysis**: ROAS, CTR, CPC comparison across Facebook, Google, TikTok
- **Tactic Performance**: Campaign effectiveness analysis
- **Weekly Patterns**: Day-of-week performance insights

### 🤖 AI-Powered Features
- **AI Performance Summary**: Automated analysis with strategic recommendations
- **Intelligent Trend Analysis**: Pattern recognition and forecasting
- **Smart Platform Recommendations**: Budget optimization with specific percentages
- **Interactive AI Chat**: Natural language queries about your data
- **Automated Insights**: Real-time AI-generated recommendations

## 🎯 Key Metrics

- **Total Revenue**: $26.8M over 120 days
- **Marketing Spend**: $9.5M with 2.81x overall ROAS
- **Platform Performance**: TikTok (2.71x), Google (2.66x), Facebook (2.60x)
- **Campaign Types**: 6 different tactics across 3 platforms
- **Geographic Coverage**: CA and NY markets

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Gemini API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Process data**:
   ```bash
   python data_processor.py
   ```

3. **Configure Gemini API**:
   - Edit `gemini_config.py` and replace `"your_gemini_api_key_here"` with your API key
   - Or set environment variable: `export GEMINI_API_KEY="your_key"`

4. **Run dashboard**:
   ```bash
   streamlit run marketing_dashboard.py
   ```

5. **Access**: Open http://localhost:8501

## 📁 Project Structure

```
BI Dashboard/
├── Data/                          # Raw data files
│   ├── Facebook.csv              # Facebook campaign data
│   ├── Google.csv                # Google campaign data
│   ├── TikTok.csv                # TikTok campaign data
│   └── business.csv              # Daily business metrics
├── data_processor.py             # Data cleaning and processing
├── marketing_dashboard.py        # Main AI-enhanced dashboard
├── ai_insights.py               # AI insights generation
├── gemini_config.py             # Gemini API configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🤖 AI Features Usage

### AI Chat Assistant
Ask questions in the sidebar chat:
- "Which platform should I invest more in?"
- "What's the best day of the week for campaigns?"
- "How can I improve my ROAS?"
- "Which tactic is most effective?"

### AI Analysis Tabs
1. **Performance Summary**: Click "🔄 Generate AI Summary"
2. **Trend Analysis**: Click "📈 Analyze Trends"
3. **Platform Recommendations**: Click "🎯 Get Recommendations"

### Example AI Insights
```
"Based on your Q2 performance, you achieved a strong 2.81x ROAS with $26.8M revenue. 
I recommend increasing TikTok budget by 15% due to its superior 2.71x ROAS performance. 
Focus on retargeting campaigns as they show the highest conversion rates."
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Upload files to GitHub repository
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Set `GEMINI_API_KEY` environment variable
4. Deploy with `marketing_dashboard.py` as main file

### Other Platforms
- **Heroku**: Add `Procfile` and set environment variables
- **Railway/Render**: Direct GitHub integration with environment variables

## 🔧 Configuration

### Gemini API Setup
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Configure in `gemini_config.py` or set environment variable
3. Dashboard works without AI (fallback mode) if API unavailable

### Data Processing
The `data_processor.py` script:
- Loads and cleans all CSV files
- Combines marketing data from all platforms
- Calculates derived metrics (ROAS, CTR, CPC, etc.)
- Joins marketing and business data
- Generates processed datasets for dashboard

## 📈 Business Value

### For Marketing Teams
- **Automated Analysis**: 10x faster insights than manual analysis
- **Strategic Recommendations**: AI-driven budget optimization
- **Performance Benchmarking**: Compare against industry standards
- **Risk Assessment**: Identify potential issues before they impact ROI

### For Executives
- **Executive Summaries**: High-level AI-generated reports
- **Strategic Planning**: Data-driven recommendations for growth
- **ROI Optimization**: Maximize marketing efficiency
- **Competitive Intelligence**: AI analysis of market positioning

## 🎨 Dashboard Sections

1. **Executive Summary**: High-level KPI cards with real-time updates
2. **AI-Powered Insights**: Three tabs with AI analysis and recommendations
3. **Performance Trends**: Time-series analysis with correlation insights
4. **Platform Performance**: Channel comparison with interactive charts
5. **Tactic Analysis**: Campaign effectiveness by platform and tactic
6. **Weekly Patterns**: Temporal insights and optimal timing
7. **Key Insights**: Automated recommendations and findings

## 🔍 Data Sources

- **Marketing Data**: 3,600 records (1,200 per platform)
- **Business Data**: 120 daily records
- **Time Period**: 120 days (May 16 - September 12, 2025)
- **Geographic Coverage**: CA, NY states
- **Campaign Types**: ASC, Prospecting, Non-Branded Search, Display, Retargeting, Spark Ads

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **AI**: Google Gemini API
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud, Heroku, Railway, Render

## 🚨 Troubleshooting

### AI Not Available
- Check API key configuration
- Verify internet connection
- Ensure Gemini API quota not exceeded
- Dashboard works without AI (fallback mode)

### Data Issues
- Ensure CSV files are in `Data/` folder
- Run `python data_processor.py` first
- Check for missing or corrupted data

### Deployment Issues
- Verify all dependencies in `requirements.txt`
- Check environment variables are set
- Ensure all files are in repository root

## 🎉 Success Metrics

The AI-enhanced dashboard delivers:
- **🚀 Unique Value**: First-of-its-kind AI-powered marketing BI dashboard
- **⚡ Speed**: 10x faster insights than manual analysis
- **🎯 Accuracy**: AI-driven recommendations based on data patterns
- **💬 Interactivity**: Natural language data exploration
- **📈 Scalability**: Handles growing datasets with AI processing
- **🔧 Usability**: Intuitive interface with powerful AI backend

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Verify API key and dependencies
3. Test locally before deployment
4. Check console logs for error messages

---

**Built with ❤️ using Streamlit, Plotly & Google Gemini AI**

*Transform your marketing data into actionable insights with the power of AI!* 🤖✨