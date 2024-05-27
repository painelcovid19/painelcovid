import pandas as pd
from elasticsearch import Elasticsearch, client
from elasticsearch_dsl import Search
from tqdm import tqdm
from dotenv import load_dotenv, find_dotenv
from libs.painel_covid_libs import save_data
import os

load_dotenv(find_dotenv())

data_source = os.environ.get("DATA_SOURCE")

locations = {
    "Redenção": ["REDENCAO", "CE"],
    "Acarape": ["ACARAPE", "CE"],
    "SFC": ["SAO FRANCISCO DO CONDE", "BA"],
}

client = Elasticsearch(
    "https://imunizacao-es.saude.gov.br/",
    headers={
        "Authorization": "Basic aW11bml6YWNhb19wdWJsaWM6cWx0bzV0JjdyX0ArI1Rsc3RpZ2k=",
        "Content-Type": "application/json",
        "Cookie": "ELASTIC-PROD=1618079452.839.9136.791476",
    },
    request_timeout=30,
)

for key in locations.keys():
    city, state = locations[key]

    print(f"Starting to retrieve vaccination data for {city} ({state})...")

    s = (
        Search(using=client)
        .query("match_phrase", paciente_endereco_nmMunicipio=city)
        .query("match_phrase", paciente_endereco_uf=state)
    )

    print("Query = ", s.to_dict())

    total_hits = s.count()
    print("Total hits = ", total_hits)

    scan = s.scan()

    data = []
    for hit in tqdm(s.scan(), total=total_hits):
        data.append(
            {
                "vacina_dataAplicacao": hit.vacina_dataAplicacao,
                "vacina_descricao_dose": hit.vacina_descricao_dose,
                # "vacina_fabricante_nome": hit.vacina_fabricante_nome,
                # "vacina_nome": hit.vacina_nome,
                "paciente_idade": hit.paciente_idade,
                "paciente_enumSexoBiologico": hit.paciente_enumSexoBiologico,
                # "paciente_dataNascimento": hit.paciente_dataNascimento,
            }
        )

    df = pd.DataFrame(data)
    df["vacina_dataAplicacao"] = pd.to_datetime(
        df["vacina_dataAplicacao"], infer_datetime_format=True
    )

    df["vacina_dataAplicacao"] = df["vacina_dataAplicacao"].dt.date

    df.set_index("vacina_dataAplicacao", drop=True, inplace=True)
    df.sort_index(inplace=True)

    print("Saving CSV...")
    file_name = f"vaccines-{city}-{state}.csv".lower().replace(" ", "-")
    save_data(df, file_name, data_source)
