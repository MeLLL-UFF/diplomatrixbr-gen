import os
import pandas as pd
from funcs import qtd_frases, qtd_palavras, namingConsistency

def read_file_content(file_path):
    """ Lê o conteúdo de um arquivo de texto e retorna como uma string. """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ANSI') as file:
            return file.read()

# Definindo o diretório raiz onde a estrutura de pastas das modificações começa
essayPath = os.path.join(os.getcwd(), "results\gen_essays")

yearList = os.listdir(essayPath)

for year in yearList:
    data = []
    
    # Pastas com os textos de referência
    for model in os.listdir(os.path.join(essayPath, year)):

        modelDir = os.path.join(essayPath, year, model)
        for text in os.listdir(modelDir):
            if(text.endswith('.txt')):
                filename = text.split("\\")[-1]
                filename = os.path.splitext(filename)[0]
                text_content = read_file_content(os.path.join(modelDir, text))
                data.append({
                    #MODEL NAMING CONSISTENCY!!!
                    'modelo': namingConsistency(filename),

                    'Quantidade de Palavras': qtd_palavras(text_content),
                    'Quantidade de Frases': qtd_frases(text_content),
                    'texto_prompt': text_content
                    })

    df = pd.DataFrame(data)

    df.to_csv(f"results\metrics\{year}\DatasetModels.csv")