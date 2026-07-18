import pandas as pd
import requests
import os
import json
from sqlalchemy import create_engine
from dotenv import load_dotenv

#Load environmet from .env
load_dotenv()

#Mysql config
db_config = {
    'host' : os.getenv('host'),
    'user' : os.getenv('user'),
    'password' : os.getenv('password'),
    'database' : os.getenv('database')
}

def get_data():
    url_api = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-7.8014&longitude=110.3647&hourly=temperature_2m,rain,weather_code,precipitation_probability&timezone=Asia%2FBangkok&forecast_days=1")
    data_json = url_api.json()
    return data_json

def main_data(file):
    df = pd.DataFrame(file['hourly'])
    df['city'] = "Jakarta"
    df.rename = df(columns={'temperature_2m' : 'temperature'})
    df_filtered = df[['time', 'city', 'temperature', 'rain', 'weather_code', 'precipitation_probability']]
    return df_filtered

def connect_db(file):
    engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    file.to_sql(name='weather_report', con=engine, if_exists='append', index=False)
    engine.dispose()
    return file