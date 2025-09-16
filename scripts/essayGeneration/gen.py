from huggingface_hub import login
import argparse
import transformers
import torch
import gc
import os

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

    instruct = '''###Contexto
    Você é um candidato que deverá elaborar uma redação para concorrer ao cargo de diplomata brasileiro. Sua redação será avaliada de acordo com os seguintes Critérios e Instrução.

    ###Critérios
    Apresentação/impressão geral do texto, coerência, legibilidade e estilo;
    Capacidade de argumentação (objetividade, sistematização, conteúdo e pertinência das informações);
    Capacidade de análise e reflexão;
    A redação deve ter entre 65 e 70 linhas;

    ###Instrução
    Com base na leitura dos excertos de troca de cartas entre Albert Einstein e Sigmund Freud no ano de 1932, discorra acerca do papel da diplomacia, fazendo referência a uma ou mais ideias mencionadas nos textos apresentados e a momentos históricos.

    Albert Einstein: “Existe alguma forma de livrar a humanidade da ameaça de guerra? É possível controlar a evolução da mente do homem, de modo a torná-lo à prova das psicoses do ódio e da destrutividade?” Sigmund Freud: “O senhor começa com a relação entre direito e poder. Posso substituir a palavra ‘poder’ por violência? Conflitos de interesse entre os homens se resolvem mediante o emprego da violência. Esse é o estado original, o domínio do poder maior, da violência crua ou apoiada na inteligência. Sabemos que houve um caminho da violência para o direito. A humanidade trocou numerosas, mesmo intermináveis pequenas guerras por raras, mas tanto mais devastadoras grandes guerras. Quando os homens são incitados à guerra, neles há toda uma série de motivos a responder afirmativamente, nobres e baixos. Não se trata de eliminar completamente as tendências agressivas humanas; pode-se tentar desviá-las a ponto de não terem que se manifestar na guerra. Se a disposição para a guerra é uma decorrência do instinto de destruição, então será natural recorrer, contra ela, ao antagonista desse instinto. Tudo o que produz laços emocionais entre as pessoas tem efeito contrário à guerra. Essas ligações podem ser de dois tipos. Primeiro, relações como as que se tem com um objeto amoroso. O outro tipo de ligação emocional é o que se dá pela identificação. Em sua forma atual, a guerra já não oferece oportunidade de satisfazer o antigo ideal heroico, e no futuro, graças ao aperfeiçoamento dos meios de destruição, uma guerra significaria a eliminação de um ou até mesmo de ambos os adversários. Não se podem condenar igualmente todas as espécies de guerras; enquanto houver nações e reinos que estejam dispostos à destruição implacável de outros, esses outros têm que se armar para a guerra. Mas pode não ser uma esperança utópica que a influência desses dois fatores, da atitude cultural e do justificado medo das consequências de uma guerra futura, venha a terminar com as guerras. Tudo o que promove a evolução cultural também trabalha contra a guerra.'''

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
        
        os.makedirs(output_path, exist_ok=True)
        
        file_name = model_id
        if '/' in file_name:
            file_name = file_name.split('/')[-1]

        with open(os.path.join(output_path, f"{file_name}-temp0{temp*10:.0f}.txt"), "w", encoding="utf-8") as f:
            f.write(generated_texts)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run text generation with Hugging Face pipeline.")
    parser.add_argument('--model_id', type=str, required=True, help="Hugging Face Model ID.")
    parser.add_argument('--hf_token', type=str, required=True, help="Hugging Face API token.")
    parser.add_argument('--temps', type=float, nargs='+', required=True, help="List of temperatures to use for generation.")
    parser.add_argument('--output_path', type=str, required=True, help="Path to save the generated outputs.")

    args = parser.parse_args()


    main(args.model_id, args.hf_token, args.temps, args.output_path)