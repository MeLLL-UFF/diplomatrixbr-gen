from openai import OpenAI
import os

client = OpenAI(
    api_key="YOUR API KEY HERE"
)

temps = [0.3, 0.5, 0.7]

srcpath = "ProvasDiplomatas"

dirlist = os.listdir(srcpath)
dirlist.pop(dirlist.index("2022"))
dirlist.pop(dirlist.index("2023"))

for dir in dirlist:
    with open(os.path.join(srcpath, dir, "prompt.txt"), 'r', encoding='utf8') as p:
        prompt = p.read()

    # Caminho para armazenar as redações geradas
    path = os.path.join(srcpath, dir, "RedacoesModelos\\CHATGPT 4o")

    for temp in temps:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        f = open(f"{path}\\gpt4o_temp0{temp*10:.0f}.txt", "w")
        f.write(completion.choices[0].message.content)
        f.close()

        print(f"{temp} - {dir}")