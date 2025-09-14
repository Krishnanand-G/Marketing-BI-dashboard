# Marketing Dashboard

A dashboard that displays marketing data with AI-powered insights.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Process data:
   ```bash
   python data_processor.py
   ```

3. Get Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. Add API key to `.streamlit/secrets.toml`

5. Run dashboard:
   ```bash
   streamlit run marketing_dashboard.py
   ```

## Features

- Interactive charts and metrics
- AI analysis and recommendations
- Platform comparison (Facebook, Google, TikTok)
- Campaign performance tracking
- Date range filtering

## Data Requirements

Place CSV files in `Data/` folder:
- `Facebook.csv`
- `Google.csv` 
- `TikTok.csv`
- `business.csv`

## Deployment

**Streamlit Cloud:**
1. Upload to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Add API key in secrets
4. Deploy

## Troubleshooting

- AI not working: Check API key
- No data: Run `data_processor.py` first
- Won't start: Check dependencies

Built with Streamlit, Plotly, and Google Gemini.