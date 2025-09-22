import os
import nltk
nltk.download('stopwords')
import pandas as pd
import json
from evaluate import load
from ctc_score import DialogScorer, FactualConsistencyScorer
import torch

bleu, bertScore, rouge = load("bleu"), load("bertscore"), load("rouge")

factualScorer = FactualConsistencyScorer(align='E-bert', device='cuda' if torch.cuda.is_available() else 'cpu')
dialogScorer = DialogScorer(align='E-bert', device='cuda' if torch.cuda.is_available() else 'cpu')

rootPath = os.path.join(os.getcwd(), "results", "metrics")

yearList = os.listdir(rootPath)

for year in yearList:
    jsonFile = os.path.join(os.getcwd(), "base_essays", f"{year}.json")

    dfCandidates = pd.read_csv(os.path.join(rootPath, year, "DatasetCandidatos.csv"))

    with open(jsonFile, 'r', encoding='utf8') as j:
        jsonCandidates = json.load(j)

    referenceColumn = 'redacao'
    statement = jsonCandidates['Pergunta']
    predictionColumn = 'texto_prompt'

    dfModels = pd.read_csv(os.path.join(rootPath, year, "DatasetModels.csv"))

    metricsResults = []

    for indexCandidate, rowsCandidate in dfCandidates.iterrows():
        referenceText = rowsCandidate[referenceColumn]

        for indexEssay, rowsEssay in dfModels.iterrows():
            predictionText = rowsEssay[predictionColumn]
            
            # Calculando ROUGE
            rougeResults = rouge.compute(predictions=[predictionText], references=[referenceText])

            # Calculando BERTscore
            bertScoreResults = bertScore.compute(predictions=[predictionText], references=[referenceText], model_type='bert-base-multilingual-cased')

            # Calculando BLEU
            bleuResults = bleu.compute(predictions=[predictionText], references=[referenceText])

            # Calculando CTC
            groundness = dialogScorer.score(fact=statement, dialog_history=[], hypo=predictionText, aspect='groundedness')
            groundnessReference = dialogScorer.score(fact=referenceText, dialog_history=[], hypo=predictionText, aspect='groundedness')
            factual = factualScorer.score(grounding=statement, hypo=predictionText)
            factualReference = factualScorer.score(grounding=referenceText, hypo=predictionText)
            ctcResults = {'groundness': groundness, 'groundnessRef': groundnessReference, 'factual': factual, 'factualRef': factualReference}

            metricsResults.append({
                'id': f"{indexCandidate}_{rowsCandidate['candidato']}",
                'generatorModel': rowsEssay['modelo'],
                'bleuScore': bleuResults['bleu'],
                'bertScorePrecision': bertScoreResults['precision'][0],
                'bertScoreRecall': bertScoreResults['recall'][0],
                'bertScoreF1': bertScoreResults['f1'][0],
                'rouge1': rougeResults['rouge1'],
                'rouge2': rougeResults['rouge2'],
                'rougeL': rougeResults['rougeL'],
                'rougeLsum': rougeResults['rougeLsum'],
                'ctcGroundness': ctcResults['groundness'],
                'ctcGroundnessRef': ctcResults['groundnessRef'],
                'ctcFactual': ctcResults['factual'],
                'ctcFactualRef': ctcResults['factualRef']
            })

        metricsDf = pd.DataFrame(metricsResults)

    os.makedirs(os.path.join(os.getcwd(), "results", "metrics", year), exist_ok=True)

    metricsDf.to_csv(os.path.join(os.getcwd(), "results", "metrics", year, "MetricasRedacoesDiplomatas.csv"), index=False, sep=';', decimal=',')