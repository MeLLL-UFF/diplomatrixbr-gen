from openai import OpenAI
from ..funcs import getYearsList
import os
import json

client = OpenAI(
    api_key="YOU-API-KEY-HERE"
)

temps = [0.3, 0.5, 0.7]

#Always remember to check if os.getcwd == "diplomatrixbr-gen"
yearlist = getYearsList()

for year in yearlist:
    with open(os.path.join(os.getcwd(), "base_essays", f"{year}.json"), 'r', encoding='utf8') as p:
        yearJson = json.load(p)
        prompt = yearJson["Pergunta"]

    # Path to store generated essays
    path = os.path.join(os.getcwd(), "results", "gen_essays", year, "CHATGPT-4o")

    os.makedirs(path, exist_ok=True)

    for temp in temps:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        with open(os.path.join(path, f"gpt4o_temp0{temp*10:.0f}.txt"), "w", encoding='utf8') as f:
            f.write(completion.choices[0].message.content)