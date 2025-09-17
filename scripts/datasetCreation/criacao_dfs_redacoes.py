import os
import pandas as pd
import json
from funcs import qtd_frases, qtd_palavras

# Definindo o diretório raiz onde a estrutura de pastas das modificações começa
root_directory = os.getcwd()

dirlist = os.listdir(root_directory)
dirlist.pop(dirlist.index("Scripts"))

for year in dirlist:
    data = []

    jsonfile = ""
    for file in os.listdir(os.path.join(root_directory, year)):
        jsonfile = os.path.join(root_directory, year, file) if file.endswith(".json") else jsonfile

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
    df.to_csv(os.path.join(root_directory, year, "DatasetCandidatos.csv"))