from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Frases de treinamento
frases = [
    "Meu Wi-Fi não está funcionando",
    "Como faço para reiniciar o roteador?",
    "Preciso de ajuda com a internet",
    "Minha tela está travada",
    "O celular não responde aos toques",
    "Quero trocar a senha do meu e-mail",
    "Como alterar minha senha de acesso?"
]

# Intenções correspondentes
intencoes = ["problema_internet", "problema_internet", "problema_internet",
             "problema_tela", "problema_tela", "alterar_senha", "alterar_senha"]

# Transformação do texto para TF-IDF
vectorizer = TfidfVectorizer()
print(vectorizer)
X = vectorizer.fit_transform(frases)
print(X)
# Treinamento do modelo
model = LogisticRegression()
model.fit(X, intencoes)
print(model)

# Testando com uma nova frase
nova_frase = ["Minha internet não funciona corretamente"]
X_novo = vectorizer.transform(nova_frase)
print(X_novo)
predicao = model.predict(X_novo)

print(f"Intenção detectada: {predicao[0]}")
