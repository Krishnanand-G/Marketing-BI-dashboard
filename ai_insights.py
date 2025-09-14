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
            Analyze this marketing data and provide concise insights:

            METRICS ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):
            Revenue: ${total_revenue:,.0f} | Spend: ${total_spend:,.0f} | ROAS: {roas:.2f}x | Orders: {total_orders:,} | AOV: ${aov:.0f}

            PLATFORMS:
            {platform_performance.to_string()}

            Provide:
            1. Executive summary (1-2 sentences)
            2. Top 3 recommendations
            3. Key risks/opportunities
            4. Budget allocation

            Keep response under 200 words. Be direct and actionable.
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
            
            weekly_data = filtered_data.groupby('day_of_week').agg({
                'total_revenue': 'mean',
                'total_roas': 'mean'
            }).round(2)
            
            best_day = weekly_data['total_revenue'].idxmax()
            worst_day = weekly_data['total_revenue'].idxmin()
            
            prompt = f"""
            Analyze trends and provide concise insights:

            TRENDS ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):
            Revenue: {revenue_trend:.1f}% daily | Spend: {spend_trend:.1f}% daily | ROAS: {roas_trend:.1f}% daily
            Best day: {best_day} | Worst day: {worst_day}

            WEEKLY DATA:
            {weekly_data.to_string()}

            Provide:
            1. Trend summary (1-2 sentences)
            2. Timing recommendations
            3. Budget optimization
            4. Specific actions

            Keep response under 150 words. Be direct.
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
            
            platform_analysis = filtered_data.groupby('platform').agg({
                'spend': 'sum',
                'attributed_revenue': 'sum',
                'roas': 'mean',
                'ctr': 'mean',
                'cpc': 'mean',
                'impression': 'sum'
            }).round(2)
            
            tactic_analysis = filtered_data.groupby(['platform', 'tactic']).agg({
                'roas': 'mean',
                'spend': 'sum'
            }).round(2)
            
            prompt = f"""
            Analyze platform performance and provide concise recommendations:

            PLATFORMS:
            {platform_analysis.to_string()}

            TACTICS:
            {tactic_analysis.to_string()}

            Provide:
            1. Platform ranking (top 3)
            2. Budget reallocation (%)
            3. Tactic optimizations
            4. Scaling opportunities
            5. Risk mitigation

            Keep response under 200 words. Be specific with numbers.
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
            Answer this marketing question concisely:

            QUESTION: {user_question}

            DATA ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}):
            Revenue: ${total_revenue:,.0f} | Spend: ${total_spend:,.0f} | ROAS: {roas:.2f}x
            Platforms: {list(filtered_marketing['platform'].unique())}
            States: {list(filtered_marketing['state'].unique())}
            Tactics: {list(filtered_marketing['tactic'].unique())}

            Provide a direct, data-driven answer. Keep it under 100 words.
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
        
        **Metrics:** Revenue: ${total_revenue:,.0f} | Spend: ${total_spend:,.0f} | ROAS: {roas:.2f}x
        
        **Efficiency:** {'Strong' if roas > 2.5 else 'Moderate' if roas > 2.0 else 'Needs improvement'} (${total_revenue/total_spend:.2f} per $1 spent)
        
        *Configure API key for advanced analytics*
        """
