import pandas as pd
import requests
import os
import json
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

#Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#Load environmet from .env
load_dotenv()

#Mysql config
db_config = {
    'host' : os.getenv('DB_HOST'),
    'user' : os.getenv('DB_USER'),
    'password' : os.getenv('DB_PASSWORD'),
    'database' : os.getenv('DB_DATABASE')
}

#Main URL
url = "https://api.open-meteo.com/v1/forecast?latitude=-7.8014&longitude=110.3647&hourly=temperature_2m,rain,weather_code,precipitation_probability&timezone=Asia%2FBangkok&forecast_days=1"

logging.info("Script Started")

# def url_response(url):
#     try:
#         get_url_response = requests.get(url)
#         if get_url_response.status_code == 200:
#             logging.info(f"Response Success : {get_url_response.status_code}")
#         else:
#             logging.info(f"Response Failed : {get_url_response.status_code}")
#             return None
#     except Exception as e:
#         logging.error(f"An Error Occured : {e}")

def get_data(url):
    try:
        get_url = requests.get(url)
        if get_url.status_code == 200:
            logging.info(f"Response Success : {get_url.status_code}")
            data_json = get_url.json()
            return data_json
        else:
            logging.warning(f"Response Failed : {get_url.status_code}")
            return None
    except Exception as e:
        logging.error(f"An Error Occured : {e}")
        return None
    
def main_data(file):
    df = pd.DataFrame(file['hourly'])
    df['time'] = pd.to_datetime(df['time'])
    df['city'] = "Yogyakarta"
    df = df.rename(columns={'temperature_2m' : 'temperature'})
    df_filtered = df[['time', 'city', 'temperature', 'rain', 'weather_code', 'precipitation_probability']]
    return df_filtered

def connect_db(file):
    engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    file.to_sql(name='weather_report', con=engine, if_exists='append', index=False)
    engine.dispose()
    return file

try:
#    check_response = url_response(url)
    main_file = get_data(url)
    cleaned_file = main_data(main_file)
    connect_db(cleaned_file)
    logging.info(f"Import Success!. {len(cleaned_file)} Row Inserted. Check MySQL for Validation.")
except Exception as e:
    logging.error(f"Something Went Wrong : {e}")
