import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MarketingDataProcessor:
    def __init__(self):
        self.fb_data = None
        self.google_data = None
        self.tiktok_data = None
        self.business_data = None
        self.combined_marketing = None
        self.final_data = None
        
    def load_data(self):
        """Load all CSV files"""
        print("Loading data...")
        self.fb_data = pd.read_csv('Data/Facebook.csv')
        self.google_data = pd.read_csv('Data/Google.csv')
        self.tiktok_data = pd.read_csv('Data/TikTok.csv')
        self.business_data = pd.read_csv('Data/business.csv')
        print("Data loaded successfully!")
        
    def clean_data(self):
        """Clean and standardize data"""
        print("Cleaning data...")
        
        marketing_dfs = [self.fb_data, self.google_data, self.tiktok_data]
        platform_names = ['Facebook', 'Google', 'TikTok']
        
        for i, df in enumerate(marketing_dfs):
            df['date'] = pd.to_datetime(df['date'])
            
            df['platform'] = platform_names[i]
            
            df.columns = df.columns.str.replace(' ', '_')
            
            numeric_cols = ['impression', 'clicks', 'spend', 'attributed_revenue']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        
        self.business_data['date'] = pd.to_datetime(self.business_data['date'])
        
        self.business_data.columns = self.business_data.columns.str.replace('# of orders', 'num_of_orders')
        self.business_data.columns = self.business_data.columns.str.replace('# of new orders', 'num_of_new_orders')
        self.business_data.columns = self.business_data.columns.str.replace(' ', '_')
        
        numeric_cols = ['num_of_orders', 'num_of_new_orders', 'new_customers', 'total_revenue', 'gross_profit', 'COGS']
        for col in numeric_cols:
            if col in self.business_data.columns:
                self.business_data[col] = pd.to_numeric(self.business_data[col], errors='coerce')
        
        print("Data cleaning completed!")
        
    def combine_marketing_data(self):
        print("Combining marketing data...")
        
        self.combined_marketing = pd.concat([
            self.fb_data,
            self.google_data, 
            self.tiktok_data
        ], ignore_index=True)
        
        self.combined_marketing = self.combined_marketing.groupby([
            'date', 'platform', 'state', 'tactic'
        ]).agg({
            'impression': 'sum',
            'clicks': 'sum', 
            'spend': 'sum',
            'attributed_revenue': 'sum'
        }).reset_index()
        
        print("Marketing data combined successfully!")
        
    def create_metrics(self):
        print("Creating metrics and KPIs...")
        
        self.combined_marketing['ctr'] = (self.combined_marketing['clicks'] / self.combined_marketing['impression'] * 100).round(2)
        self.combined_marketing['cpc'] = (self.combined_marketing['spend'] / self.combined_marketing['clicks']).round(2)
        self.combined_marketing['roas'] = (self.combined_marketing['attributed_revenue'] / self.combined_marketing['spend']).round(2)
        self.combined_marketing['cpm'] = (self.combined_marketing['spend'] / self.combined_marketing['impression'] * 1000).round(2)
        
        self.business_data['avg_order_value'] = (self.business_data['total_revenue'] / self.business_data['num_of_orders']).round(2)
        self.business_data['customer_acquisition_cost'] = 0  # Will be calculated after joining
        self.business_data['gross_margin'] = ((self.business_data['gross_profit'] / self.business_data['total_revenue']) * 100).round(2)
        self.business_data['new_customer_rate'] = ((self.business_data['new_customers'] / self.business_data['num_of_orders']) * 100).round(2)
        
        print("Metrics created successfully!")
        
    def join_data(self):
        print("Joining marketing and business data...")
        
        daily_marketing = self.combined_marketing.groupby('date').agg({
            'impression': 'sum',
            'clicks': 'sum',
            'spend': 'sum', 
            'attributed_revenue': 'sum'
        }).reset_index()
        
        self.final_data = pd.merge(
            self.business_data, 
            daily_marketing, 
            on='date', 
            how='left'
        )
        
        marketing_cols = ['impression', 'clicks', 'spend', 'attributed_revenue']
        for col in marketing_cols:
            self.final_data[col] = self.final_data[col].fillna(0)
        
        self.final_data['total_roas'] = np.where(
            self.final_data['spend'] > 0,
            self.final_data['attributed_revenue'] / self.final_data['spend'],
            0
        ).round(2)
        
        self.final_data['marketing_contribution'] = (
            self.final_data['attributed_revenue'] / self.final_data['total_revenue'] * 100
        ).round(2)
        
        self.final_data['total_ctr'] = np.where(
            self.final_data['impression'] > 0,
            self.final_data['clicks'] / self.final_data['impression'] * 100,
            0
        ).round(2)
        
        self.final_data['day_of_week'] = self.final_data['date'].dt.day_name()
        self.final_data['week'] = self.final_data['date'].dt.isocalendar().week
        self.final_data['month'] = self.final_data['date'].dt.month
        
        print("Data joining completed!")
        
    def process_all(self):
        self.load_data()
        self.clean_data()
        self.combine_marketing_data()
        self.create_metrics()
        self.join_data()
        
        print("Data processing completed successfully!")
        print(f"Final dataset shape: {self.final_data.shape}")
        print(f"Combined marketing data shape: {self.combined_marketing.shape}")
        
        return self.final_data, self.combined_marketing

if __name__ == "__main__":
    processor = MarketingDataProcessor()
    final_data, marketing_data = processor.process_all()
    
    # Save processed data
    final_data.to_csv('processed_business_data.csv', index=False)
    marketing_data.to_csv('processed_marketing_data.csv', index=False)
    
    print("Processed data saved to CSV files!")
