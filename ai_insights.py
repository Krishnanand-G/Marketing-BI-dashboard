import pandas as pd
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from gemini_config import configure_gemini, get_gemini_model

class AIInsightsGenerator:
    def __init__(self):
        self.model = None
        self.is_configured = False
        
    def initialize(self):
        if configure_gemini():
            self.model = get_gemini_model()
            self.is_configured = True
            return True
        return False
    
    def generate_performance_summary(self, business_data, marketing_data, selected_date_range):
        if not self.is_configured:
            return self._get_fallback_summary(business_data, marketing_data, selected_date_range)
        
        try:
            start_date = pd.to_datetime(selected_date_range[0])
            end_date = pd.to_datetime(selected_date_range[1])
            
            filtered_business = business_data[
                (business_data['date'] >= start_date) & 
                (business_data['date'] <= end_date)
            ]
            
            filtered_marketing = marketing_data[
                (marketing_data['date'] >= start_date) & 
                (marketing_data['date'] <= end_date)
            ]
            
            total_revenue = filtered_business['total_revenue'].sum()
            total_spend = filtered_business['spend'].sum()
            roas = filtered_business['attributed_revenue'].sum() / total_spend if total_spend > 0 else 0
            total_orders = filtered_business['num_of_orders'].sum()
            new_customers = filtered_business['new_customers'].sum()
            aov = total_revenue / total_orders if total_orders > 0 else 0
            
            platform_performance = filtered_marketing.groupby('platform').agg({
                'spend': 'sum',
                'attributed_revenue': 'sum',
                'roas': 'mean'
            }).round(2)
            
            prompt = f"""
            As a marketing intelligence expert, analyze this e-commerce performance data and provide actionable insights:

            PERFORMANCE METRICS ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):
            - Total Revenue: ${total_revenue:,.0f}
            - Marketing Spend: ${total_spend:,.0f}
            - Overall ROAS: {roas:.2f}x
            - Total Orders: {total_orders:,}
            - New Customers: {new_customers:,}
            - Average Order Value: ${aov:.0f}

            PLATFORM PERFORMANCE:
            {platform_performance.to_string()}

            Please provide:
            1. A concise executive summary (2-3 sentences)
            2. Top 3 actionable recommendations
            3. Key risks or opportunities to watch
            4. Specific budget allocation suggestions

            Focus on practical, data-driven insights that a marketing manager can implement immediately.
            """
            
            response = self.model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                return response.text
            else:
                return "AI response format error. Please try again."
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg:
                return f"AI model not available. Error: {error_msg}. Please check your API key and model access."
            else:
                return f"AI analysis failed: {error_msg}. Using fallback analysis."
    
    def generate_trend_analysis(self, business_data, selected_date_range):
        if not self.is_configured:
            return "AI analysis not available. Please configure Gemini API key."
        
        try:
            start_date = pd.to_datetime(selected_date_range[0])
            end_date = pd.to_datetime(selected_date_range[1])
            
            filtered_data = business_data[
                (business_data['date'] >= start_date) & 
                (business_data['date'] <= end_date)
            ].sort_values('date')
            
            revenue_trend = filtered_data['total_revenue'].pct_change().mean() * 100
            spend_trend = filtered_data['spend'].pct_change().mean() * 100
            roas_trend = filtered_data['total_roas'].pct_change().mean() * 100
            
            # Weekly performance
            weekly_data = filtered_data.groupby('day_of_week').agg({
                'total_revenue': 'mean',
                'total_roas': 'mean'
            }).round(2)
            
            best_day = weekly_data['total_revenue'].idxmax()
            worst_day = weekly_data['total_revenue'].idxmin()
            
            prompt = f"""
            Analyze these marketing performance trends and provide strategic insights:

            TREND ANALYSIS ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):
            - Revenue Growth Trend: {revenue_trend:.1f}% daily average
            - Marketing Spend Trend: {spend_trend:.1f}% daily average  
            - ROAS Trend: {roas_trend:.1f}% daily average

            WEEKLY PERFORMANCE:
            {weekly_data.to_string()}
            Best performing day: {best_day}
            Worst performing day: {worst_day}

            Please provide:
            1. Trend interpretation and implications
            2. Seasonal patterns and timing recommendations
            3. Budget optimization suggestions based on trends
            4. Specific actions to improve performance

            Be specific and actionable in your recommendations.
            """
            
            response = self.model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                return response.text
            else:
                return "AI response format error. Please try again."
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg:
                return f"AI model not available. Error: {error_msg}. Please check your API key and model access."
            else:
                return f"Trend analysis failed: {error_msg}"
    
    def generate_platform_recommendations(self, marketing_data, selected_date_range, selected_platforms):
        """Generate AI-powered platform recommendations"""
        if not self.is_configured:
            return "AI analysis not available. Please configure Gemini API key."
        
        try:
            start_date = pd.to_datetime(selected_date_range[0])
            end_date = pd.to_datetime(selected_date_range[1])
            
            filtered_data = marketing_data[
                (marketing_data['date'] >= start_date) & 
                (marketing_data['date'] <= end_date) &
                (marketing_data['platform'].isin(selected_platforms))
            ]
            
            # Platform analysis
            platform_analysis = filtered_data.groupby('platform').agg({
                'spend': 'sum',
                'attributed_revenue': 'sum',
                'roas': 'mean',
                'ctr': 'mean',
                'cpc': 'mean',
                'impression': 'sum'
            }).round(2)
            
            # Tactic analysis
            tactic_analysis = filtered_data.groupby(['platform', 'tactic']).agg({
                'roas': 'mean',
                'spend': 'sum'
            }).round(2)
            
            prompt = f"""
            As a digital marketing strategist, analyze this platform performance data and provide optimization recommendations:

            PLATFORM PERFORMANCE:
            {platform_analysis.to_string()}

            TACTIC PERFORMANCE:
            {tactic_analysis.to_string()}

            Please provide:
            1. Platform ranking and performance assessment
            2. Budget reallocation recommendations with specific percentages
            3. Tactic optimization suggestions for each platform
            4. Scaling opportunities and growth strategies
            5. Risk mitigation for underperforming areas

            Focus on maximizing ROI and providing specific, measurable recommendations.
            """
            
            response = self.model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                return response.text
            else:
                return "AI response format error. Please try again."
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg:
                return f"AI model not available. Error: {error_msg}. Please check your API key and model access."
            else:
                return f"Platform analysis failed: {error_msg}"
    
    def chat_with_data(self, user_question, business_data, marketing_data, selected_date_range):
        """Interactive chat with the data using AI"""
        if not self.is_configured:
            return "AI chat not available. Please configure Gemini API key."
        
        try:
            start_date = pd.to_datetime(selected_date_range[0])
            end_date = pd.to_datetime(selected_date_range[1])
            
            filtered_business = business_data[
                (business_data['date'] >= start_date) & 
                (business_data['date'] <= end_date)
            ]
            
            filtered_marketing = marketing_data[
                (marketing_data['date'] >= start_date) & 
                (marketing_data['date'] <= end_date)
            ]
            
            total_revenue = filtered_business['total_revenue'].sum()
            total_spend = filtered_business['spend'].sum()
            roas = filtered_business['attributed_revenue'].sum() / total_spend if total_spend > 0 else 0
            
            prompt = f"""
            You are a marketing intelligence AI assistant. Answer this question about the marketing data:

            QUESTION: {user_question}

            CONTEXT DATA ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):
            - Total Revenue: ${total_revenue:,.0f}
            - Marketing Spend: ${total_spend:,.0f}
            - ROAS: {roas:.2f}x
            - Platforms: {list(filtered_marketing['platform'].unique())}
            - States: {list(filtered_marketing['state'].unique())}
            - Tactics: {list(filtered_marketing['tactic'].unique())}

            Provide a helpful, data-driven answer based on the available information. If the question requires data not available in the context, explain what additional data would be needed.
            """
            
            response = self.model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                return response.text
            else:
                return "AI response format error. Please try again."
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg:
                return f"AI model not available. Error: {error_msg}. Please check your API key and model access."
            else:
                return f"Chat analysis failed: {error_msg}"
    
    def _get_fallback_summary(self, business_data, marketing_data, selected_date_range):
        """Fallback summary when AI is not available"""
        start_date = pd.to_datetime(selected_date_range[0])
        end_date = pd.to_datetime(selected_date_range[1])
        
        filtered_business = business_data[
            (business_data['date'] >= start_date) & 
            (business_data['date'] <= end_date)
        ]
        
        total_revenue = filtered_business['total_revenue'].sum()
        total_spend = filtered_business['spend'].sum()
        roas = filtered_business['attributed_revenue'].sum() / total_spend if total_spend > 0 else 0
        
        return f"""
        **Performance Summary** ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})
        
        **Key Metrics:**
        - Total Revenue: ${total_revenue:,.0f}
        - Marketing Spend: ${total_spend:,.0f}
        - Overall ROAS: {roas:.2f}x
        
        **Quick Insights:**
        - Marketing efficiency is {'strong' if roas > 2.5 else 'moderate' if roas > 2.0 else 'needs improvement'}
        - Revenue per dollar spent: ${total_revenue/total_spend:.2f}
        """
