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