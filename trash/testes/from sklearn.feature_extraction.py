import matplotlib.pyplot as plt
import numpy as np
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
    "Quais médicos estão disponíveis?",
    "Preciso de ajuda para me cadastrar",
    "Como posso me inscrever?",
    "Registrar novo paciente",
    "Gostaria de agendar uma consulta",
    "Como posso marcar uma consulta?",
    "Desmarcar minha consulta",
    "Quero cancelar minha consulta",
    "Ver horários de consultas",
    "Quais são os horários de atendimento?",
    "Datas disponíveis para consulta",
    "Ver especialidades médicas",
    "Quais especialidades estão disponíveis?",
    "Médicos disponíveis para consulta",
    "Como posso criar uma conta?",
    "Quero fazer um agendamento",
    "Cancelar meu agendamento",
    "Mostrar horários de consultas",
    "Quais são as especialidades que vocês têm?",
    "Quero saber os médicos disponíveis"
]

intencoes = ["cadastrar_usuario", "cadastrar_usuario", "cadastrar_usuario", 
             "agendar_consulta", "agendar_consulta", "cancelar_consulta", 
             "ver_calendario", "ver_calendario", "ver_calendario",
             "ver_especialidades", "ver_especialidades", "ver_especialidades",
             "cadastrar_usuario", "cadastrar_usuario", "cadastrar_usuario",
             "agendar_consulta", "agendar_consulta", "cancelar_consulta",
             "cancelar_consulta", "ver_calendario", "ver_calendario",
             "ver_calendario", "ver_especialidades", "ver_especialidades",
             "ver_especialidades", "cadastrar_usuario", "agendar_consulta",
             "cancelar_consulta", "ver_calendario", "ver_especialidades",
             "ver_especialidades"]

# Vetorização das frases
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(frases)

# Treinar modelo de classificação
model = LogisticRegression()
model.fit(X, intencoes)

# Frases de teste
frases_teste = [
    "Como posso criar uma conta no sistema?",
    "Preciso agendar uma consulta médica",
    "Gostaria de cancelar meu agendamento",
    "Registrar um novo paciente no sistema",
    "Mostrar os horários disponíveis para consultas",
    "Quais especialidades médicas vocês oferecem?",
    "Como faço para me cadastrar?",
    "Quero marcar uma consulta com o médico",
    "Cancelar minha consulta agendada",
    "Quero ver os horários de atendimento",
    "Quais são as especialidades disponíveis?",
    "Quais médicos estão disponíveis para consulta?"
]

intencoes_esperadas = ["cadastrar_usuario", "agendar_consulta", "cancelar_consulta", "cadastrar_usuario", 
                       "ver_calendario", "ver_especialidades", "cadastrar_usuario", "agendar_consulta", 
                       "cancelar_consulta", "ver_calendario", "ver_especialidades", "ver_especialidades"]

# Vetorização das frases de teste
X_teste = vectorizer.transform(frases_teste)

# Fazer previsões
predicoes = model.predict(X_teste)

# 1. Confusion Matrix
conf_matrix = confusion_matrix(intencoes_esperadas, predicoes)

# Visualizar a Confusion Matrix com Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.matshow(conf_matrix, cmap='Blues')
fig.colorbar(cax)


# Adicionar rótulos de texto
for (i, j), val in np.ndenumerate(conf_matrix):
    ax.text(j, i, val, ha='center', va='center')

plt.title("Confusion Matrix")
plt.xlabel("Previsões")
plt.ylabel("Valores Reais")
plt.savefig('confusion_matrix.png')  # Salvar o gráfico em um arquivo
plt.close()  # Fechar a figura

# 2. Relatório de Métricas
print("Relatório de Classificação:")
print(classification_report(intencoes_esperadas, predicoes))

# 3. Acurácia Geral
acuracia = accuracy_score(intencoes_esperadas, predicoes)
print(f"Acurácia: {acuracia:.2f}")
print(predicoes)

nova_frase = ["Como faço pra me cadastra no sistema", "quero ver a minha agenda ", "quero cancelar a minha consulta", "quero ver os horários disponíveis", "quais são as especialidades disponíveis", "quais médicos estão disponíveis", 
"como posso cria uma conta", "quero fazer um agendamento", "cancelar meu agendamento", "mostrar horários de consultas", "quais são as especialidades que vocês têm", "quero saber os médicos disponíveis"]

for i in nova_frase:
    X_nova = vectorizer.transform([i])
    predicao_nova = model.predict(X_nova)
    print(f"{i}: {predicao_nova[0]}")