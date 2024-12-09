from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Frases de treinamento
frases = [
    "Quero me cadastrar como paciente",
    "Como faço para me registrar?",
    "Cadastrar usuário",
    "Quero marcar uma consulta",
    "Como agendar uma consulta médica?",
    "Cancelar minha consulta"
]
intencoes = ["cadastrar_usuario", "cadastrar_usuario", "cadastrar_usuario", 
             "agendar_consulta", "agendar_consulta", "cancelar_consulta"]


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(frases)


model = LogisticRegression()
model.fit(X, intencoes)


nova_frase = ["Olá, quero me cadastrar como paciente"]
X_novo = vectorizer.transform(nova_frase)
predicao = model.predict(X_novo)
print(predicao)

print(f"Intenção detectada: {predicao[0]}")
