import json
import os

def salvar_evolucao(hist):

    os.makedirs("logs", exist_ok=True)

    with open("logs/evolucao.json","w") as f:

        json.dump(hist,f,indent=4)