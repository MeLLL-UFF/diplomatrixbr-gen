import os
import maritalk

sabia3 = maritalk.MariTalk(
        key= "YOUR API KEY HERE",
        model="sabia-3"
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
    path = os.path.join(srcpath, dir, "RedacoesModelos\\SABIA")
    print(path)

    for temp in temps:
        answer = sabia3.generate(
                prompt,
                do_sample=True,
                max_tokens=2048,
                temperature=temp,
                top_p=0.4
            )["answer"]
        
        with open(f"{path}\\sabia3_temp0{temp*10:.0f}.txt", "w") as f:
            f.write(answer)