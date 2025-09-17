from openai import OpenAI
from funcs import getYearsList
import os
import json

client = OpenAI(
    api_key="YOUR API KEY HERE"
)

temps = [0.3, 0.5, 0.7]

#Always remember to check if os.getcwd == "diplomatrixbr-gen"
yearlist = getYearsList()

for year in yearlist:
    with open(os.path.join(os.getcwd(), f"base_essays\{year}.json"), 'r', encoding='utf8') as p:
        yearJson = json.dump(p)
        prompt = yearJson["Pergunta"]

    # Path to store generated essays
    path = os.path.join(os.getcwd(), f"results\\gen_essays\\{year}\\CHATPGT-4o")

    os.makedirs(path, exist_ok=True)

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