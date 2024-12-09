from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# --- Atendimento Bancário ---
frases_bancarias = [
    "Quero abrir uma conta corrente",
    "Como faço para criar uma conta poupança?",
    "Abrir uma conta empresarial",
    "Qual o saldo da minha conta?",
    "Como consultar meu extrato bancário?",
    "Quero bloquear meu cartão",
    "Meu cartão foi roubado, preciso de ajuda",
    "Quero alterar a senha do meu cartão",
    "Como faço para mudar a senha do aplicativo?",
    "Preciso de um empréstimo"
]

intencoes_bancarias = [
    "abrir_conta", "abrir_conta", "abrir_conta",
    "consultar_saldo", "consultar_extrato",
    "bloquear_cartao", "bloquear_cartao",
    "alterar_senha", "alterar_senha",
    "pedir_emprestimo"
]

# --- Suporte Técnico de Dispositivos ---
frases_suporte = [
    "Meu computador não liga",
    "Como faço para atualizar o sistema operacional?",
    "O som do meu notebook não funciona",
    "Preciso configurar minha impressora",
    "Minha internet está muito lenta",
    "Quero saber como conectar meu celular ao Wi-Fi",
    "A tela do meu celular quebrou, o que fazer?",
    "Preciso de ajuda para reinstalar o Windows",
    "Meu celular está travando muito",
    "Quero trocar a senha do meu roteador"
]

intencoes_suporte = [
    "problema_hardware", "atualizar_sistema", "problema_audio",
    "configurar_impressora", "problema_internet", "conectar_wifi",
    "problema_tela", "reinstalar_sistema", "problema_desempenho",
    "alterar_senha"
]


frases_ecommerce = [
    "Quero saber o status do meu pedido",
    "Como rastrear minha encomenda?",
    "Quero cancelar uma compra",
    "Preciso trocar um produto",
    "Meu produto chegou com defeito",
    "Como faço para devolver um item?",
    "Quero saber mais sobre formas de pagamento",
    "O boleto não foi gerado, o que fazer?",
    "Quero alterar o endereço de entrega",
    "Meu pedido está atrasado"
]

intencoes_ecommerce = [
    "consultar_pedido", "consultar_pedido", "cancelar_pedido",
    "trocar_produto", "problema_produto", "devolver_produto",
    "formas_pagamento", "problema_pagamento",
    "alterar_endereco", "problema_entrega"
]


frases = frases_bancarias + frases_suporte + frases_ecommerce
intencoes = intencoes_bancarias + intencoes_suporte + intencoes_ecommerce


X_train, X_test, y_train, y_test = train_test_split(frases, intencoes, test_size=0.3, random_state=42)


vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


model = LogisticRegression(max_iter=200)
model.fit(X_train_vec, y_train)

# Avaliação
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Teste com nova frase
nova_frase = ["Quero compra algo"]
X_novo = vectorizer.transform(nova_frase)
predicao = model.predict(X_novo)

print(f"Intenção detectada: {predicao[0]}")