import pandas as pd
import os
from packages.utils import get_datas, rename_city, columns, new_columns
from packages.ibge_codes import codigosIBGE_CE, codigosIBGE_BA
from libs.painel_covid_libs import save_data
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

data_source = os.environ.get("DATA_SOURCE")

df_cases = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv")

all_codes = codigosIBGE_CE + codigosIBGE_BA
datas = get_datas(all_codes, df_cases)

macrorregions_data = pd.concat(datas)

macrorregions_data = macrorregions_data[columns]

macrorregions_data.columns = new_columns

macrorregions_data["city"] = macrorregions_data["city"].apply(rename_city)

macrorregion_CE = macrorregions_data[macrorregions_data["state"] == "CE"]
macrorregion_BA = macrorregions_data[macrorregions_data["state"] == "BA"]

macrorregion_CE.reset_index(drop=True, inplace=True)
macrorregion_BA.reset_index(drop=True, inplace=True)


macrorregion_CE = macrorregion_CE.sort_values(by="city", ignore_index=True)
macrorregion_BA = macrorregion_BA.sort_values(by="city", ignore_index=True)

save_data(macrorregion_BA, "df_dados_macro_regioes_bahia.csv", data_source)
save_data(macrorregion_CE, "df_dados_macro_regioes_ceara.csv", data_source)

