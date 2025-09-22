import maritalk
from funcs import getYearsList
import os
import json

sabia3 = maritalk.MariTalk(
        key= "YOUR API KEY HERE",
        model="sabia-3"
)

temps = [0.3, 0.5, 0.7]

#Always remember to check if os.getcwd == "diplomatrixbr-gen"
yearlist = getYearsList()

for year in yearlist:
    with open(os.path.join(os.getcwd(), f"base_essays\{year}.json"), 'r', encoding='utf8') as p:
        yearJson = json.dump(p)
        prompt = yearJson["Pergunta"]

    # Path to store generated essays
    path = os.path.join(os.getcwd(), f"results\\gen_essays\\{year}\\SABIA")

    os.makedirs(path, exist_ok=True)

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