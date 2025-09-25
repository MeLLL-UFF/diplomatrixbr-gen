import os
import pandas as pd
import json
from ..funcs import qtd_frases, qtd_palavras, getYearsList

# Definindo o diretório raiz onde a estrutura de pastas das modificações começa
root_directory = os.getcwd()

essayPath = os.path.join(os.getcwd(), "base_essays")
resultsPath = os.path.join(os.getcwd(), "results", "metrics")

yearList = os.listdir(essayPath)

for year in yearList:
    data = []

    jsonfile = os.path.join(essayPath, year)

    # Lendo o JSON para um arquivo
    with open(jsonfile, 'r', encoding='utf8') as j:
        essay_data = json.load(j)

    name = 'Nome'
    score = 'Nota'
    essay = 'Redação'

    # Adicionando os dados ao DataFrame
    for i in essay_data['Candidatos']:
        data.append({
            'candidato': i[name],
            'nota': i[score],
            'quantidade de palavras': qtd_palavras(i[essay]),
            'quantidade de frases': qtd_frases(i[essay]),
            'redacao': i[essay]
        })

    df = pd.DataFrame(data)
    df.to_csv(os.path.join(resultsPath, year.split(".")[0], "DatasetCandidatos.csv"))