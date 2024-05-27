#!/bin/bash

echo "===================PAINEL_COVID ETL PROCESS==================="

echo "----------starting loading accumuated data-------------"
python scripts/covid_br/get_accumulated_data.py && python scripts/covid_br/get_df_cases.py /
python scripts/covid_br/get_macroregion_data.py && python scripts/get_vaccination_data.py

echo "----------finished loading accumuated data-------------"
