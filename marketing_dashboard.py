import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import AI insights
from ai_insights import AIInsightsGenerator

# Page configuration
st.set_page_config(
    page_title="AI-Powered Marketing Intelligence Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .ai-section {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
    .ai-insight-box {
        background-color: #f8f9ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the processed data"""
    try:
        business_data = pd.read_csv('processed_business_data.csv')
        marketing_data = pd.read_csv('processed_marketing_data.csv')
        
        # Convert date columns
        business_data['date'] = pd.to_datetime(business_data['date'])
        marketing_data['date'] = pd.to_datetime(marketing_data['date'])
        
        return business_data, marketing_data
    except FileNotFoundError:
        st.error("Processed data files not found. Please run data_processor.py first.")
        return None, None

def create_kpi_cards(data, selected_date_range):
    """Create KPI cards for the selected period"""
    # Convert date range to datetime
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    filtered_data = data[
        (data['date'] >= start_date) & 
        (data['date'] <= end_date)
    ]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_revenue = filtered_data['total_revenue'].sum()
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"{filtered_data['total_revenue'].mean():.0f}/day"
        )
    
    with col2:
        total_orders = filtered_data['num_of_orders'].sum()
        st.metric(
            label="📦 Total Orders",
            value=f"{total_orders:,}",
            delta=f"{filtered_data['num_of_orders'].mean():.0f}/day"
        )
    
    with col3:
        total_spend = filtered_data['spend'].sum()
        roas = filtered_data['attributed_revenue'].sum() / total_spend if total_spend > 0 else 0
        st.metric(
            label="🎯 ROAS",
            value=f"{roas:.2f}x",
            delta=f"${total_spend:,.0f} spend"
        )
    
    with col4:
        new_customers = filtered_data['new_customers'].sum()
        st.metric(
            label="👥 New Customers",
            value=f"{new_customers:,}",
            delta=f"{filtered_data['new_customers'].mean():.0f}/day"
        )
    
    with col5:
        avg_order_value = filtered_data['total_revenue'].sum() / total_orders if total_orders > 0 else 0
        st.metric(
            label="💵 AOV",
            value=f"${avg_order_value:.0f}",
            delta=f"{(filtered_data['gross_margin'].mean()):.1f}% margin"
        )

def create_revenue_trends_chart(data, selected_date_range):
    """Create revenue and marketing trends chart"""
    # Convert date range to datetime
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    filtered_data = data[
        (data['date'] >= start_date) & 
        (data['date'] <= end_date)
    ].sort_values('date')
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue Trends', 'Marketing Spend vs Revenue', 'Order Volume', 'ROAS Performance'),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Revenue trends
    fig.add_trace(
        go.Scatter(x=filtered_data['date'], y=filtered_data['total_revenue'], 
                  name='Total Revenue', line=dict(color='#1f77b4', width=3)),
        row=1, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=filtered_data['date'], y=filtered_data['attributed_revenue'], 
                  name='Attributed Revenue', line=dict(color='#ff7f0e', width=2)),
        row=1, col=1, secondary_y=True
    )
    
    # Marketing spend vs revenue
    fig.add_trace(
        go.Scatter(x=filtered_data['spend'], y=filtered_data['total_revenue'],
                  mode='markers', name='Spend vs Revenue', marker=dict(color='#2ca02c', size=8)),
        row=1, col=2, secondary_y=False
    )
    
    # Order volume
    fig.add_trace(
        go.Bar(x=filtered_data['date'], y=filtered_data['num_of_orders'],
               name='Orders', marker_color='#d62728'),
        row=2, col=1, secondary_y=False
    )
    
    # ROAS performance
    fig.add_trace(
        go.Scatter(x=filtered_data['date'], y=filtered_data['total_roas'],
                  name='ROAS', line=dict(color='#9467bd', width=3)),
        row=2, col=2, secondary_y=False
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    fig.update_yaxes(title_text="Attributed Revenue ($)", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
    fig.update_yaxes(title_text="Orders", row=2, col=1)
    fig.update_yaxes(title_text="ROAS", row=2, col=2)
    
    return fig

def create_platform_analysis(marketing_data, selected_date_range, selected_platforms, selected_states):
    """Create platform performance analysis"""
    # Convert date range to datetime
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    filtered_data = marketing_data[
        (marketing_data['date'] >= start_date) & 
        (marketing_data['date'] <= end_date) &
        (marketing_data['platform'].isin(selected_platforms)) &
        (marketing_data['state'].isin(selected_states))
    ]
    
    # Platform performance summary
    platform_summary = filtered_data.groupby('platform').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'clicks': 'sum',
        'impression': 'sum',
        'roas': 'mean',
        'ctr': 'mean',
        'cpc': 'mean'
    }).reset_index()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Platform Spend Distribution', 'ROAS by Platform', 
                       'Click-Through Rate by Platform', 'Cost Per Click by Platform'),
        specs=[[{"type": "pie"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Spend distribution pie chart
    fig.add_trace(
        go.Pie(labels=platform_summary['platform'], values=platform_summary['spend'],
               name="Spend Distribution", hole=0.3),
        row=1, col=1
    )
    
    # ROAS by platform
    fig.add_trace(
        go.Bar(x=platform_summary['platform'], y=platform_summary['roas'],
               name='ROAS', marker_color='#1f77b4'),
        row=1, col=2
    )
    
    # CTR by platform
    fig.add_trace(
        go.Bar(x=platform_summary['platform'], y=platform_summary['ctr'],
               name='CTR', marker_color='#ff7f0e'),
        row=2, col=1
    )
    
    # CPC by platform
    fig.add_trace(
        go.Bar(x=platform_summary['platform'], y=platform_summary['cpc'],
               name='CPC', marker_color='#2ca02c'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    fig.update_yaxes(title_text="ROAS", row=1, col=2)
    fig.update_yaxes(title_text="CTR (%)", row=2, col=1)
    fig.update_yaxes(title_text="CPC ($)", row=2, col=2)
    
    return fig, platform_summary

def create_tactic_analysis(marketing_data, selected_date_range, selected_platforms, selected_states):
    """Create tactic performance analysis"""
    # Convert date range to datetime
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    filtered_data = marketing_data[
        (marketing_data['date'] >= start_date) & 
        (marketing_data['date'] <= end_date) &
        (marketing_data['platform'].isin(selected_platforms)) &
        (marketing_data['state'].isin(selected_states))
    ]
    
    tactic_summary = filtered_data.groupby(['platform', 'tactic']).agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean',
        'cpc': 'mean'
    }).reset_index()
    
    fig = px.bar(
        tactic_summary, 
        x='platform', 
        y='roas', 
        color='tactic',
        title='ROAS by Platform and Tactic',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(height=400)
    
    return fig, tactic_summary

def create_weekly_analysis(data, selected_date_range):
    """Create weekly performance analysis"""
    # Convert date range to datetime
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    filtered_data = data[
        (data['date'] >= start_date) & 
        (data['date'] <= end_date)
    ].copy()
    
    # Group by day of week
    weekly_data = filtered_data.groupby('day_of_week').agg({
        'total_revenue': 'mean',
        'num_of_orders': 'mean',
        'spend': 'mean',
        'attributed_revenue': 'mean',
        'total_roas': 'mean'
    }).reset_index()
    
    # Order days properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_data['day_of_week'] = pd.Categorical(weekly_data['day_of_week'], categories=day_order, ordered=True)
    weekly_data = weekly_data.sort_values('day_of_week')
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Average Revenue by Day of Week', 'Average ROAS by Day of Week')
    )
    
    fig.add_trace(
        go.Bar(x=weekly_data['day_of_week'], y=weekly_data['total_revenue'],
               name='Revenue', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=weekly_data['day_of_week'], y=weekly_data['total_roas'],
               name='ROAS', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(title_text="Day of Week")
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    fig.update_yaxes(title_text="ROAS", row=1, col=2)
    
    return fig, weekly_data

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI-Powered Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Initialize AI insights
    ai_generator = AIInsightsGenerator()
    ai_available = ai_generator.initialize()
    
    if ai_available:
        st.success("🤖 AI Insights Available - Powered by Google Gemini")
    else:
        st.warning("⚠️ AI Insights Not Available - Configure Gemini API key for enhanced analysis")
    
    # Load data
    business_data, marketing_data = load_data()
    
    if business_data is None or marketing_data is None:
        st.stop()
    
    # Sidebar filters
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Date range selector
    min_date = business_data['date'].min().date()
    max_date = business_data['date'].max().date()
    
    selected_date_range = st.sidebar.date_input(
        "📅 Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(selected_date_range) != 2:
        selected_date_range = (min_date, max_date)
    
    # Platform selector
    available_platforms = marketing_data['platform'].unique().tolist()
    selected_platforms = st.sidebar.multiselect(
        "🌐 Select Platforms",
        options=available_platforms,
        default=available_platforms
    )
    
    # State selector
    available_states = marketing_data['state'].unique().tolist()
    selected_states = st.sidebar.multiselect(
        "🗺️ Select States",
        options=available_states,
        default=available_states
    )
    
    # Metric selector
    st.sidebar.header("📈 Key Metrics")
    
    # Calculate summary metrics for the selected period
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    filtered_business = business_data[
        (business_data['date'] >= start_date) & 
        (business_data['date'] <= end_date)
    ]
    
    total_revenue = filtered_business['total_revenue'].sum()
    total_spend = filtered_business['spend'].sum()
    total_roas = filtered_business['attributed_revenue'].sum() / total_spend if total_spend > 0 else 0
    
    st.sidebar.metric("Total Revenue", f"${total_revenue:,.0f}")
    st.sidebar.metric("Total Marketing Spend", f"${total_spend:,.0f}")
    st.sidebar.metric("Overall ROAS", f"{total_roas:.2f}x")
    
    # AI Chat Section
    st.sidebar.header("💬 AI Chat Assistant")
    user_question = st.sidebar.text_area(
        "Ask AI about your data:",
        placeholder="e.g., Which platform should I invest more in?",
        height=100
    )
    
    if st.sidebar.button("🤖 Ask AI") and user_question:
        with st.sidebar:
            with st.spinner("AI is analyzing..."):
                ai_response = ai_generator.chat_with_data(
                    user_question, business_data, marketing_data, selected_date_range
                )
                st.success("AI Response:")
                st.write(ai_response)
    
    # Main dashboard content
    st.header("🎯 Executive Summary")
    create_kpi_cards(business_data, selected_date_range)
    
    # AI-Powered Insights Section
    st.header("🤖 AI-Powered Insights")
    
    tab1, tab2, tab3 = st.tabs(["📊 Performance Summary", "📈 Trend Analysis", "🎯 Platform Recommendations"])
    
    with tab1:
        st.subheader("AI Performance Analysis")
        if st.button("🔄 Generate AI Summary"):
            with st.spinner("AI is analyzing your performance..."):
                ai_summary = ai_generator.generate_performance_summary(
                    business_data, marketing_data, selected_date_range
                )
                st.markdown(f'<div class="ai-insight-box">{ai_summary}</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("AI Trend Analysis")
        if st.button("📈 Analyze Trends"):
            with st.spinner("AI is analyzing trends..."):
                trend_analysis = ai_generator.generate_trend_analysis(
                    business_data, selected_date_range
                )
                st.markdown(f'<div class="ai-insight-box">{trend_analysis}</div>', unsafe_allow_html=True)
    
    with tab3:
        st.subheader("AI Platform Recommendations")
        if st.button("🎯 Get Recommendations"):
            with st.spinner("AI is generating recommendations..."):
                recommendations = ai_generator.generate_platform_recommendations(
                    marketing_data, selected_date_range, selected_platforms
                )
                st.markdown(f'<div class="ai-insight-box">{recommendations}</div>', unsafe_allow_html=True)
    
    st.header("📈 Performance Trends")
    trends_chart = create_revenue_trends_chart(business_data, selected_date_range)
    st.plotly_chart(trends_chart, use_container_width=True)
    
    # Platform analysis
    st.header("🌐 Platform Performance")
    platform_chart, platform_summary = create_platform_analysis(
        marketing_data, selected_date_range, selected_platforms, selected_states
    )
    st.plotly_chart(platform_chart, use_container_width=True)
    
    # Display platform summary table
    st.subheader("📊 Platform Summary Table")
    platform_summary_display = platform_summary.round(2)
    st.dataframe(platform_summary_display, use_container_width=True)
    
    # Tactic analysis
    st.header("🎯 Tactic Performance")
    tactic_chart, tactic_summary = create_tactic_analysis(
        marketing_data, selected_date_range, selected_platforms, selected_states
    )
    st.plotly_chart(tactic_chart, use_container_width=True)
    
    # Weekly analysis
    st.header("📅 Weekly Performance Patterns")
    weekly_chart, weekly_data = create_weekly_analysis(business_data, selected_date_range)
    st.plotly_chart(weekly_chart, use_container_width=True)
    
    # Insights section
    st.header("💡 Key Insights")
    
    # Calculate insights
    filtered_marketing = marketing_data[
        (marketing_data['date'] >= start_date) & 
        (marketing_data['date'] <= end_date) &
        (marketing_data['platform'].isin(selected_platforms)) &
        (marketing_data['state'].isin(selected_states))
    ]
    
    best_platform = filtered_marketing.groupby('platform')['roas'].mean().idxmax()
    best_tactic = filtered_marketing.groupby('tactic')['roas'].mean().idxmax()
    best_day = weekly_data.loc[weekly_data['total_revenue'].idxmax(), 'day_of_week']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"🏆 **Best Performing Platform:** {best_platform}")
    
    with col2:
        st.info(f"🎯 **Best Performing Tactic:** {best_tactic}")
    
    with col3:
        st.info(f"📅 **Best Day of Week:** {best_day}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            🤖 AI-Powered Marketing Intelligence Dashboard | Built with Streamlit, Plotly & Google Gemini
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
