import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Definir as opções
opcoes = [
    "Usuário quer se cadastrar como novo paciente",
    "Usuário quer marcar horário",
    "Usuário quer ver horários disponíveis",
    "Usuário quer mostrar horários disponíveis"
]


vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)

opcoes_vec = vectorizer.fit_transform(opcoes)

def generate_improved_prompt(user_input):
    
    user_vec = vectorizer.transform([user_input])
    
    
    similaridades = cosine_similarity(user_vec, opcoes_vec)
    
    
    indice_max = np.argmax(similaridades)
    maior_similaridade = similaridades[0, indice_max]
    
    
    limiar = 0.5
    
    if maior_similaridade >= limiar:
        return f"Sim, {indice_max + 1}"  
    else:
        return "Não"


user_input = "quer horário disponíveis"

print(generate_improved_prompt(user_input))
