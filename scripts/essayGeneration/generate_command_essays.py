import cohere
from funcs import getYearsList
import os
import json

co = cohere.Client(api_key="YOUR API KEY HERE")

temps = [0.3, 0.5, 0.7]

#Always remember to check if os.getcwd == "diplomatrixbr-gen"
yearlist = getYearsList()

for year in yearlist:
    with open(os.path.join(os.getcwd(), f"base_essays\{year}.json"), 'r', encoding='utf8') as p:
        yearJson = json.dump(p)
        prompt = yearJson["Pergunta"]

    # Path to store generated essays
    path = os.path.join(os.getcwd(), f"results\\gen_essays\\{year}\\COMMAND-R+")

    os.makedirs(path, exist_ok=True)

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