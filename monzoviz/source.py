from datetime import datetime
import pandas as pd

def _load_data(csv_path):
        
        return_cols = ['category', 'entity', 'date', 'amount', 'balance']
    
        df = pd.read_csv(csv_path)
        df['entity'] = df['Name'].str.upper()
        df['date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
        df['amount'] = df['Money In'].fillna(0) + df['Money Out'].fillna(0)
        df['category'] = df['Category']

        df['balance'] = df['amount'].cumsum()

        return df[return_cols]

class MonzoData:
    
    def __init__(self, csv_path):
        
        self.df = _load_data(csv_path)
        
    def get_outgoings(self):
        
        return self.df[self.df['amount'] < 0]

    def get_categories(self):
        
        return list(self.df['category'].unique())
    