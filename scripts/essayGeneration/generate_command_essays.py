import cohere
import os

co = cohere.Client(api_key="YOUR API KEY HERE")

temps = [0.3, 0.5, 0.7]

srcpath = "ProvasDiplomatas"

dirlist = os.listdir(srcpath)
dirlist.pop(dirlist.index("2022"))
dirlist.pop(dirlist.index("2023"))

for dir in dirlist:
    with open(os.path.join(srcpath, dir, "prompt.txt"), 'r', encoding='utf8') as p:
        prompt = p.read()

    # Caminho para armazenar as redações geradas
    path = os.path.join(srcpath, dir, "RedacoesModelos\\COMMAND R")

    for temp in temps:
        response = co.chat(
            message=prompt,
            temperature=temp,
            p=0.4,
            max_tokens=1024
        )

        f = open(f"{path}\\command_r_plus_08_2024_temp0{temp*10:.0f}.txt", "w")
        f.write(response.text)
        f.close()