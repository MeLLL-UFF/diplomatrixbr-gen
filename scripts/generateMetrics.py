import os
import nltk
nltk.download('stopwords')
import pandas as pd
import json
from evaluate import load
from ctc_score import DialogScorer, FactualConsistencyScorer
import torch

bleu, bert_score, rouge = load("bleu"), load("bertscore"), load("rouge")

factual_scorer = FactualConsistencyScorer(align='E-bert', device='cuda' if torch.cuda.is_available() else 'cpu')
dial_scorer = DialogScorer(align='E-bert', device='cuda' if torch.cuda.is_available() else 'cpu')


root_path = os.getcwd()

dirlist = os.listdir(root_path)

#dirlist.pop(dirlist.index("Scripts"))
dirlist = [dirlist.pop(dirlist.index("2022"))]

for year in dirlist:
    #Procura JSON dentro de cada diretório
    jsonfile = os.path.join(root_path, year)
    for file in os.listdir(os.path.join(root_path, year)):
        jsonfile = os.path.join(jsonfile, file) if file.endswith(".json") else jsonfile

    #df_candidates = pd.read_csv(os.path.join(root_path, year, "DatasetCandidatos.csv"))
    df_candidates = pd.read_csv(os.path.join(root_path, "2022\Dataset\dataset_redacoes_candidatos.csv"))

    with open(jsonfile, 'r', encoding='utf8') as j:
        json_candidates = json.load(j)

    reference_column = 'redacao'
    statement = json_candidates['Pergunta']
    prediction_column = 'texto_prompt_0'

    #df_models = pd.read_csv(os.path.join(root_path, year, "Dataset.csv"))
    df_models = pd.read_csv(os.path.join(root_path, "2022\Dataset\dataset_redacoes_prompt0.csv"))

    metrics_results = []

    for index_candidate, rows_candidate in df_candidates.iterrows():
        reference_text = rows_candidate[reference_column]

        for index_essay, rows_essay in df_models.iterrows():
            prediction_text = rows_essay[prediction_column]
            
            # Calculando ROUGE
            rouge_results = rouge.compute(predictions=[prediction_text], references=[reference_text])

            # Calculando BERTscore
            bertscore_results = bert_score.compute(predictions=[prediction_text], references=[reference_text], model_type='bert-base-multilingual-cased')

            # Calculando BLEU
            bleu_results = bleu.compute(predictions=[prediction_text], references=[reference_text])

            # Calculando CTC
            groundness = dial_scorer.score(fact=statement, dialog_history=[], hypo=prediction_text, aspect='groundedness')
            groundness_reference = dial_scorer.score(fact=reference_text, dialog_history=[], hypo=prediction_text, aspect='groundedness')
            factual = factual_scorer.score(grounding=statement, hypo=prediction_text)
            factual_reference = factual_scorer.score(grounding=reference_text, hypo=prediction_text)
            CTC_results = {'groundness': groundness, 'groundness_ref': groundness_reference, 'factual': factual, 'factual_ref': factual_reference}

            metrics_results.append({
                'id': f"{index_candidate}_{rows_candidate['candidato']}",
                'modification_type': prediction_column,
                'generator_model': rows_essay['modelo'],
                'BLEU_score': bleu_results['bleu'],
                'BERTScore_Precision': bertscore_results['precision'][0],
                'BERTScore_Recall': bertscore_results['recall'][0],
                'BERTScore_F1': bertscore_results['f1'][0],
                'rouge1': rouge_results['rouge1'],
                'rouge2': rouge_results['rouge2'],
                'rougeL': rouge_results['rougeL'],
                'rougeLsum': rouge_results['rougeLsum'],
                'CTC_groundness': CTC_results['groundness'],
                'CTC_groundness_ref': CTC_results['groundness_ref'],
                'CTC_factual': CTC_results['factual'],
                'CTC_factual_ref': CTC_results['factual_ref']
            })

        metrics_df = pd.DataFrame(metrics_results)

    metrics_df.to_csv(f"{root_path}/{year}/MetricasRedacoesDiplomatas.csv", index=False, sep=';', decimal=',')