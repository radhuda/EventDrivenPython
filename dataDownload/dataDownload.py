import pandas as pd

# import requests
def transform(nytimes_link, john_hopkins_link):
    error = None
    df = None
    
    try:
        nytimes_df = pd.read_csv(nytimes_link)
        john_hopkins_df = pd.read_csv(john_hopkins_link)
    except: 
        error = "problem reading in csv links"
        return error, df
    try:
        # Filtering for US only from John Hopkins data
        john_hopkins_df = john_hopkins_df[john_hopkins_df["Country/Region"]=='US']
        john_hopkins_df.columns = [x.lower() for x in john_hopkins_df.columns]
        #Converting to datetime object
        nytimes_df['date'] = pd.to_datetime(nytimes_df['date'], infer_datetime_format=True)
        john_hopkins_df['date'] = pd.to_datetime(john_hopkins_df['date'], infer_datetime_format=True)
        #changing index to date
        nytimes_df = nytimes_df.set_index(['date'])
        john_hopkins_df = john_hopkins_df.set_index(['date'])
        #dropping all columns on john hopkins except recovered 
        john_hopkins_df = john_hopkins_df[['recovered']]
        #Joining dataframes
        df = nytimes_df.join(john_hopkins_df)
    except:
        error = "problem in transformation"
        return error, df
        

    return error, df