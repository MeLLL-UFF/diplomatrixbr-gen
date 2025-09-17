from huggingface_hub import login
import argparse
import transformers
import torch
import gc
import os
import json

def getYearsList():
    path = os.path.join(os.getcwd(), "base_essays")
    return list(map(lambda s: s.split(".")[0], os.listdir(path)))


def main(model_id, hf_token, temps, output_path):
    login(token=hf_token)

    device = f'cuda' if torch.cuda.is_available() else 'cpu'
    
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

    pipeline = transformers.pipeline(
        task="text-generation",
        trust_remote_code=True,
        model=model_id,
        tokenizer=tokenizer,
        # The quantization line
        model_kwargs={"torch_dtype": torch.bfloat16},
        device=device,
    )

    yearList = getYearsList()

    baseEssaysPath = "base_essays"

    for year in yearList:
        with open(os.path.join(baseEssaysPath, f"{year}.json"), "r", encoding="utf-8") as j:
            yearJson = json.load(j)
            prompt = yearJson["Pergunta"]

        instruct = f'''###Contexto
        Você é um candidato que deverá elaborar uma redação para concorrer ao cargo de diplomata brasileiro. Sua redação será avaliada de acordo com os seguintes Critérios e Instrução.

        ###Critérios
        Apresentação/impressão geral do texto, coerência, legibilidade e estilo;
        Capacidade de argumentação (objetividade, sistematização, conteúdo e pertinência das informações);
        Capacidade de análise e reflexão;
        A redação deve ter entre 65 e 70 linhas;

        ###Instrução
        {prompt}'''

        torch.cuda.empty_cache()
        torch.cuda.synchronize()

        for temp in temps:
            messages = [
                {"role": "user", "content": instruct}
            ]
            
            outputs = pipeline(
                messages,
                max_new_tokens=1024,
                do_sample=True,
                temperature=temp,
                top_p=0.4,
            )

            generated_texts = outputs[0]["generated_text"][1]['content']#[len(instruct):]
            #print(generated_texts)
            del outputs
            del messages
            torch.cuda.empty_cache()
            gc.collect()
            
            resultEssaysPath = "results/teste"

            os.makedirs(os.path.join(resultEssaysPath, output_path), exist_ok=True)
            
            file_name = model_id
            if '/' in file_name:
                file_name = file_name.split('/')[-1]

            with open(os.path.join(resultEssaysPath, output_path, f"{file_name}-temp0{temp*10:.0f}.txt"), "w", encoding="utf-8") as f:
                f.write(generated_texts)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run text generation with Hugging Face pipeline.")
    parser.add_argument('--model_id', type=str, required=True, help="Hugging Face Model ID.")
    parser.add_argument('--hf_token', type=str, required=True, help="Hugging Face API token.")
    parser.add_argument('--temps', type=float, nargs='+', required=True, help="List of temperatures to use for generation.")
    parser.add_argument('--output_path', type=str, required=True, help="Path to save the generated outputs.")

    args = parser.parse_args()


    main(args.model_id, args.hf_token, args.temps, args.output_path)