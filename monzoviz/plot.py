import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def group_date(df):
    return_df = df.copy()
    return_df.index = return_df['date'] 
    return_df = return_df.groupby(pd.Grouper(freq="M"))
    return_df = return_df.sum().reset_index()
    return return_df

def get_date_range(year_start, year_end):
    
    date_range = pd.DataFrame(columns=['date'])

    for year in range(year_start, year_end + 1):
        for month in range(1, 12 + 1):
            date_range = date_range.append({
                'date': pd.datetime(year, month, 1)
            }, ignore_index = True)
            
    date_range.index = date_range['date']
    date_range = date_range.groupby(pd.Grouper(freq='M')).count().rename(columns={'date': 'count'}).reset_index()
        
    return date_range

def plotly_stacked_bar(df, att_groups, year_start=2017, year_end=2020):
    
    data = []
    date_range = get_date_range(year_start, year_end)

    for entity in df[att_groups].unique():
        right = df[df[att_groups] == entity]
        right = group_date(right)
        joined = pd.merge(date_range, right, on='date', how='left')
        joined['amount'].fillna(0, inplace=True)
        values = joined['amount']
        values = [-x for x in values]
        data.append(go.Bar(name=entity, x=date_range['date'].to_list(), y=values))
        
    fig = go.Figure(data=data)

    # Change the bar mode
    fig.update_layout(barmode='stack')
    
    return fig

def plotly_ongoing_balance(df):

    df_grouped_day = df[["date", "balance"]].groupby(by=["date"]).max().reset_index()
    fig = px.line(df_grouped_day, x="date", y="balance")
    return fig