import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)

# Frases de treinamento
frases = [
    "Quero me cadastrar como paciente",
    "Como faço para me registrar?",
    "Cadastrar usuário",
    "Quero marcar uma consulta",
    "Como agendar uma consulta médica?",
    "Cancelar minha consulta",
    "Quero ver o calendário de consultas",
    "Quais são os horários disponíveis?",
    "Quais datas disponiveis para consulta?",
    "Quero ver as especialidades disponíveis",
    "Quais são as especialidades médicas?",
    "Quais médicos estão disponíveis?"
]
intencoes = ["cadastrar_usuario", "cadastrar_usuario", "cadastrar_usuario", 
             "agendar_consulta", "agendar_consulta", "cancelar_consulta", 
             "ver_calendario", "ver_calendario", "ver_calendario",
             "ver_especialidades", "ver_especialidades", "ver_especialidades"]

# Vetorização das frases
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(frases)

# Treinar modelo de classificação
model = LogisticRegression()
model.fit(X, intencoes)

# Frases de teste
frases_teste = [
    "Quero cadastrar meu nome",
    "Preciso agendar uma consulta",
    "Gostaria de cancelar minha consulta",
    "Registrar usuário no sistema",
    "Quero ver o calendário de consultas",
    "Quais são as especialidades médicas?"

]
intencoes_esperadas = ["cadastrar_usuario", "agendar_consulta", "cancelar_consulta", "cadastrar_usuario"
                       "ver_calendario", "ver_especialidades"]

# Vetorização das frases de teste
X_teste = vectorizer.transform(frases_teste)

# Fazer previsões
predicoes = model.predict(X_teste)

# 1. Confusion Matrix
conf_matrix = confusion_matrix(intencoes_esperadas, predicoes)

# Visualizar a Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=model.classes_, yticklabels=model.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Previsões")
plt.ylabel("Valores Reais")
plt.show()

# 2. Relatório de Métricas
print("Relatório de Classificação:")
print(classification_report(intencoes_esperadas, predicoes))

# 3. Acurácia Geral
acuracia = accuracy_score(intencoes_esperadas, predicoes )
print(f"Acurácia: {acuracia:.2f}")
print(predicoes)