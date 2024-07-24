import pandas as pd
import os
import csv
from packages.utils import get_last_update_date, rename_city
from libs.painel_covid_libs import save_data, read_data
import s3fs
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

data_source = os.environ.get("DATA_SOURCE")

columns = [
    "city",
     "ibgeID", 
     "date",
     "state", 
     "totalCases",
      "totalCases_per_100k_inhabitants", 
      "deaths", 
      "newCases", 
      "newDeaths"
      ]

campis_url = "https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time_changesOnly.csv.gz?raw=true"
rt_url = "https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time.csv.gz?raw=true"

def get_dataset(url):

    df_cases = pd.read_csv(url, compression='gzip')

    df_filter = (df_cases["city"] == "Acarape/CE") | (df_cases["city"] == "Redenção/CE") | (df_cases["city"] == "São Francisco do Conde/BA") \
    | (df_cases["city"] == "Fortaleza/CE") | (df_cases["city"] == "Salvador/BA") 

    df_cities = df_cases[df_filter][columns]

    df_cities.columns = ["city", "city_ibge_code", "date", "state", "last_available_confirmed", "last_available_confirmed_per_100k_inhabitants", "last_available_deaths", "new_confirmed", "new_deaths"]

    df_cities = df_cities.sort_values(by="city")
    df_cities["city"] = df_cities["city"].apply(rename_city)

    df_Acarape =df_cities[df_cities["city"] == "Acarape"].sort_values(by="date", ascending=False)
    df_Redencao = df_cities[df_cities["city"] == "Redenção"].sort_values(by="date", ascending=False)
    df_SFC = df_cities[df_cities["city"] == "São Francisco do Conde"].sort_values(by="date", ascending=False)
    df_Fortaleza = df_cities[df_cities["city"] == "Fortaleza"].sort_values(by="date", ascending=False)
    df_Salvador = df_cities[df_cities["city"] == "Salvador"].sort_values(by="date", ascending=False)

    df_cities = pd.concat([df_Acarape, df_Redencao, df_SFC, df_Fortaleza, df_Salvador])
    df_cities.reset_index(inplace=True)
    df_cities.drop("index", axis=1, inplace=True)

    return df_cities

directory = "painelcovid/data"
if not os.path.exists(directory):
    os.makedirs(directory)

df_campis = get_dataset(url=campis_url)
save_data(df_campis,"df_cidades_campi.csv", data_source)


last_updated_date = []
last_updated_date.append(get_last_update_date(df_campis[df_campis["city"] == "Acarape"]))
last_updated_date.append(get_last_update_date(df_campis[df_campis["city"] == "Redenção"]))
last_updated_date.append(get_last_update_date(df_campis[df_campis["city"] == "São Francisco do Conde"]))

last_updated_df = pd.DataFrame(last_updated_date)
    
save_data(last_updated_df, "last_update_dates.csv", data_source)

df_rt = get_dataset(url=rt_url)
save_data(df_rt, "df_cidades_rt.csv", data_source)