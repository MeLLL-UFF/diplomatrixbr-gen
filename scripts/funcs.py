import os

def getYearsList():
    path = os.path.join(os.getcwd(), "base_essays")
    return list(map(lambda s: s.split(".")[0], os.listdir(path)))

def qtd_frases(s:str):
    s = s.replace("...", "@@@")
    s = s.replace("!", "@@@")
    s = s.replace("?", "@@@")
    s = s.replace(".", "@@@")
    
    frases = s.split("@@@")
    return len(frases[0:-1]) if len(frases[-1]) < 5 else len(frases)

def qtd_palavras(s:str):
    return len(s.split(' '))

#The function "namingConsistency" is used to make sure the filenames have a consistency and are standarized,
#this ensures that errors are avoided in future csv. manipulation
#
#NOTE: Feel free to name the models anyway wanted, this is just the way things were made in this project

def namingConsistency(name:str):
    dic = {
        "command-r-plus-08-2024-temp03": "command_r_plus_08_2024_temp03",
        "command-r-plus-08-2024-temp05": "command_r_plus_08_2024_temp05",
        "command-r-plus-08-2024-temp07": "command_r_plus_08_2024_temp07",
        "gemma-2-9b-it-temp03": "gemma_2_9b_it_temp03",
        "gemma-2-9b-it-temp05": "gemma_2_9b_it_temp05",
        "gemma-2-9b-it-temp07": "gemma_2_9b_it_temp07",
        "Llama-3.1-8B-Instruct-temp03": "llama_3.1_8b_instruct_temp03",
        "Llama-3.1-8B-Instruct-temp05": "llama_3.1_8b_instruct_temp05",
        "Llama-3.1-8B-Instruct-temp07": "llama_3.1_8b_instruct_temp07",
        "Mistral-7B-Instruct-v0.3-temp03": "mistral_7b_instruct_v0.3_temp03",
        "Mistral-7B-Instruct-v0.3-temp05": "mistral_7b_instruct_v0.3_temp05",
        "Mistral-7B-Instruct-v0.3-temp07": "mistral_7b_instruct_v0.3_temp07",
        "Phi-3-small-8k-instruct-temp03": "phi_3_small_8k_instruct_temp03",
        "Phi-3-small-8k-instruct-temp05": "phi_3_small_8k_instruct_temp05",
        "Phi-3-small-8k-instruct-temp07": "phi_3_small_8k_instruct_temp07",
        "Qwen2.5-7B-Instruct-temp03": "qwen2.5_7b_instruct_temp03",
        "Qwen2.5-7B-Instruct-temp05": "qwen2.5_7b_instruct_temp05",
        "Qwen2.5-7B-Instruct-temp07": "qwen2.5_7b_instruct_temp07"
    }

    return dic.get(name)

#NOTE: Make sure the keys in this dictionary are the same as the values no the previous function
#This function is only used to shorten the models names so it shouldn't be a huge problem

def namesToCode(name:str):
    dic = {
        "gpt4o_temp03": "gpt4o_03",
        "gpt4o_temp05": "gpt4o_05",
        "gpt4o_temp07": "gpt4o_07",
        "command_r_plus_08_2024_temp03": "command_r_plus_03",
        "command_r_plus_08_2024_temp03": "command_r_plus_03",
        "command_r_plus_08_2024_temp05": "command_r_plus_05",
        "gemma_27b_temp03": "gemma27b_03",
        "gemma_27b_temp05": "gemma27b_05",
        "gemma_27b_temp07": "gemma27b_07",
        "gemma_2_9b_it_temp03": "gemma9b_03",
        "gemma_2_9b_it_temp05": "gemma9b_05",
        "gemma_2_9b_it_temp07": "gemma9b_07",
        "llama_405b_temp03": "llama405b_03",
        "llama_405b_temp05": "llama405b_05",
        "llama_405b_temp07": "llama405b_07",
        "llama_3.1_8b_instruct_temp03": "llama8b_03",
        "llama_3.1_8b_instruct_temp05": "llama8b_05",
        "llama_3.1_8b_instruct_temp07": "llama8b_07",
        "mixtral_22b_temp03": "mixtral22b_03",
        "mixtral_22b_temp05": "mixtral22b_05",
        "mixtral_22b_temp07": "mixtral22b_07",
        "mistral_7b_instruct_v0.3_temp03": "mixtral7b_03",
        "mistral_7b_instruct_v0.3_temp05": "mixtral7b_05",
        "mistral_7b_instruct_v0.3_temp07": "mixtral7b_07",
        "phi_3_small_8k_instruct_temp03": "phi3_03",
        "phi_3_small_8k_instruct_temp05": "phi3_05",
        "phi_3_small_8k_instruct_temp07": "phi3_07",
        "phi_4_temp03": "phi4_03",
        "phi_4_temp05": "phi4_05",
        "phi_4_temp07": "phi4_07",
        "qwen_72b_temp03": "qwen72b_03",
        "qwen_72b_temp05": "qwen72b_05",
        "qwen_72b_temp07": "qwen72b_07",
        "qwen2.5_7b_instruct_temp03": "qwen7b_03",
        "qwen2.5_7b_instruct_temp05": "qwen7b_05",
        "qwen2.5_7b_instruct_temp07": "qwen7b_07",
        "sabia3_temp03": "sabia_03",
        "sabia3_temp05": "sabia_05",
        "sabia3_temp07": "sabia_07"
    }

    return dic.get(name)