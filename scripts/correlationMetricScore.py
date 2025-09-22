import pandas as pd
import os
from funcs import getYearsList, modelDictionary
import sys

allYears = getYearsList()

rootPath = os.getcwd()

df = []
other = []
for year in allYears:
    datasetPath = os.path.join(rootPath, "results", "metrics", year)
    
    try:
        temp = pd.read_csv(os.path.join(datasetPath, "DatasetCandidatos.csv"), sep=",", decimal=".")
    except FileNotFoundError:
        problemPath = os.path.join(datasetPath, "DatasetCandidatos.csv")
        sys.exit(f"{problemPath} not found. Make sure you pass the correct filepath.")
    
    temp = temp.loc[:, "candidato":"nota"]

    candidatos = temp["candidato"].to_list()
    lista = list(year + "_" + c for c in candidatos)
    
    temp["candidato"] = pd.Series(lista)

    df.append(temp)

    try:
        temp = pd.read_csv(os.path.join(datasetPath, "MetricasRedacoesDiplomatas.csv"), sep=";", decimal=",")
    except FileNotFoundError:
        problemPath = os.path.join(datasetPath, "MetricasRedacoesDiplomatas.csv")
        sys.exit(f"{problemPath} not found. Make sure you pass the correct filepath.")

    candidatos = (temp["id"].str.split("_", n=1).str[-1]).to_list()
    lista = list(year + "_" + c for c in candidatos)

    temp["id"] = pd.Series(lista)

    other.append(temp)

df = pd.concat(df)
other = pd.concat(other)

modelComparison = other.rename(columns={"id": "candidato"})

modelComparison = (modelComparison.set_index("candidato")).join(df.set_index('candidato'))

modelComparison = modelComparison.reindex(columns=["generatorModel","nota","BLEU_score","BERTScore_Precision","BERTScore_Recall","BERTScore_F1","rouge1","rouge2","rougeL","rougeLsum","CTC_groundness","CTC_groundness_ref","CTC_factual","CTC_factual_ref"])

modelComparison = modelComparison.sort_values(by=["generatorModel", "nota"], ascending=[True, False])

modelComparison.index = modelComparison["generatorModel"]

modelComparison = modelComparison.loc[:, "nota":]

modelComparison = modelComparison.rename(columns={"nota": "Correlation"})

modelComparison = modelComparison.rename(index=modelDictionary)

modelList = modelComparison.index.unique().to_list()
modelList.sort()

os.makedirs(os.path.join(rootPath, "results", "correlations"), exist_ok=True)

series = [pd.DataFrame(modelComparison.loc[m].corr('pearson').loc["Correlation"].loc["BLEU_score":]) for m in modelList]
(pd.concat(series, keys=modelList, names=["Modelos", "Metricas"]).sort_values(by=["Metricas", "Correlation"], ascending=[True, False])).to_csv(os.path.join(rootPath, "results", "correlations", "PearsonCorrelation.csv"))

series = [pd.DataFrame(modelComparison.loc[m].corr('spearman').loc["Correlation"].loc["BLEU_score":]) for m in modelList]
(pd.concat(series, keys=modelList, names=["Modelos", "Metricas"]).sort_values(by=["Metricas", "Correlation"], ascending=[True, False])).to_csv(os.path.join(rootPath, "results", "correlations", "SpearmanCorrelation.csv"))

series = [pd.DataFrame(modelComparison.loc[m].corr('kendall').loc["Correlation"].loc["BLEU_score":]) for m in modelList]
(pd.concat(series, keys=modelList, names=["Modelos", "Metricas"]).sort_values(by=["Metricas", "Correlation"], ascending=[True, False])).to_csv(os.path.join(rootPath, "results", "correlations", "KendallCorrelation.csv"))