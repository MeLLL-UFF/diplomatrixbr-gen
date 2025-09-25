import cohere
from ..funcs import getYearsList
import os
import json

co = cohere.Client(api_key="YOU-API-KEY-HERE")

temps = [0.3, 0.5, 0.7]

#Always remember to check if os.getcwd == "diplomatrixbr-gen"
yearlist = getYearsList()

for year in yearlist:
    with open(os.path.join(os.getcwd(), "base_essays", f"{year}.json"), 'r', encoding='utf8') as p:
        yearJson = json.load(p)
        prompt = yearJson["Pergunta"]

    # Path to store generated essays
    path = os.path.join(os.getcwd(), "results", "gen_essays", year, "COMMAND-R+")

    os.makedirs(path, exist_ok=True)

    for temp in temps:
        response = co.chat(
            message=prompt,
            temperature=temp,
            p=0.4,
            max_tokens=1024
        )

        with open(os.path.join(path, f"command_r_plus_08_2024_temp0{temp*10:.0f}.txt"), "w", encoding='utf8') as f:
            f.write(response.text)