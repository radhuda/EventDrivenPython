import json
from dataDownload import transform
import boto3
import psycopg2
from sqlalchemy import create_engine


# Links to our daily csv files
nytimes_link = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
john_hopkins_link = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv?opt_id=oeu1597324410905r0.13823075358019055'


# DB params are stored in a hidden file called dbparams.json
with open("dbparams.json","r") as f:
    db_param = json.load(f)


# Engine is created with the help of sqlalchemy and psycopg2_binary
engine = create_engine(F"postgresql://{db_param['user']}:{db_param['password']}@{db_param['hostname']}:{db_param['port']}/{db_param['dbname']}")


def lambda_handler(event, context):
    # This will try transform the csv files links. If unsuccessful it will return status code 301
    ##This refers to dataDownload.py file. Transform is the custom function that returns our dataframe
    error, df = transform(nytimes_link, john_hopkins_link)
    if error != None:
        return {
        "statusCode": 301,
        "body": json.dumps({
            "message": error,
        }),
    }

    # This will try to load the dataframe into our database. If it fails it will return status code 303 else 200
    try:
        df.to_sql('covidData', engine, if_exists='append')
            
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": 'success',
            }),
        }
    except:
        return {
            "statusCode": 303,
            "body": json.dumps({
                "message": 'error while trying to load into database',
            }),
        }


