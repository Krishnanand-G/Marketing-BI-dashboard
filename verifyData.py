import pandas as pd 

def verify_data_files() :
    files = ['Data/business.csv', 'Data/Facebook.csv', 'Data/Google.csv', 'Data/TikTok.csv']

    for file in files: 
        try:
            df = pd.read_csv(file)
            print(f"\n{file}:")
            print(f"    Shape: {df.shape}")
            print(f"    Columns: {list(df.columns)}")
            print(f"    Date range: {df['date'].min()} to {df['date'].max()}")

            if 'tactic' in df.columns:
                print(f"    Tactics: {df['tactic'].unique()}")
            
            if 'state' in df.columns:
                print(f"    States: {df['state'].unique()}")
            
        except Exception as e:
                print(f"Error reading {file}: {e}")

if __name__ == "__main__" : 
     verify_data_files()
            