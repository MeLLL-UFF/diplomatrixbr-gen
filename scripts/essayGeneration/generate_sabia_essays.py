import maritalk
from ..funcs import getYearsList
import os
import json

sabia3 = maritalk.MariTalk(
        key= "YOUR-API-KEY-HERE",
        model="sabia-3"
)

temps = [0.3, 0.5, 0.7]

#Always remember to check if os.getcwd == "diplomatrixbr-gen"
yearlist = getYearsList()

for year in yearlist:
    with open(os.path.join(os.getcwd(), "base_essays", f"{year}.json"), 'r', encoding='utf8') as p:
        yearJson = json.load(p)
        prompt = yearJson["Pergunta"]

    # Path to store generated essays
    path = os.path.join(os.getcwd(), "results", "gen_essays", year, "SABIA")

    os.makedirs(path, exist_ok=True)

    for temp in temps:
        answer = sabia3.generate(
                prompt,
                do_sample=True,
                max_tokens=2048,
                temperature=temp,
                top_p=0.4
            )["answer"]
        
        with open(os.path.join(path, f"sabia3_temp0{temp*10:.0f}.txt"), "w", encoding="utf-8") as f:
            f.write(answer)