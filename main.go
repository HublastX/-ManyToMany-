package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"sync"

	"github.com/gin-gonic/gin"
)

type WebhookData struct {
	Entry []struct {
		Changes []struct {
			Field string       `json:"field"`
			Value WebhookValue `json:"value"`
		} `json:"changes"`
	} `json:"entry"`
	Object string `json:"object"`
}

type WebhookValue struct {
	MessagingProduct string `json:"messaging_product"`
	Metadata         struct {
		DisplayPhoneNumber string `json:"display_phone_number"`
		PhoneNumberID      string `json:"phone_number_id"`
	} `json:"metadata"`
	Contacts []struct {
		Profile struct {
			Name string `json:"name"`
		} `json:"profile"`
		WaID string `json:"wa_id"`
	} `json:"contacts"`
	Messages []struct {
		From      string `json:"from"`
		ID        string `json:"id"`
		Timestamp string `json:"timestamp"`
		Type      string `json:"type"`
		Text      struct {
			Body string `json:"body"`
		} `json:"text"`
	} `json:"messages"`
	Statuses []struct {
		ID          string `json:"id"`
		RecipientID string `json:"recipient_id"`
		Status      string `json:"status"`
		Timestamp   string `json:"timestamp"`
	} `json:"statuses"`
}

var tokenSend = "EAAM8AX6oBoIBO7skGgJfeTknyNrbtnrMEoogB8w4npuyLEC1ivSNWZAH6MZBaAKKE1cr4RGx0J84jSH2uyqSRi3IANyI2kpPhEv5JjkHBd5zsBfhqxSd86NXoFhTtg34TQFHVykAQWN5lCBJf2mlpEcpg3ZCLYUFaXy2QCS3ITThNcqAoyHEBEhvi6h5TTJ6q2ICIV52Lm88IHIgtYZAtanxDvclqtPixtQ4MOgt"
var idNumberSend = "523859527469741"

// Função para processar a mensagem recebida
func receiveMessage(c *gin.Context) {
	var data WebhookData

	// Ler o corpo do request
	if err := c.ShouldBindJSON(&data); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "No data received"})
		return
	}

	log.Printf("Dados recebidos do webhook: %+v\n", data)

	var wg sync.WaitGroup

	for _, entry := range data.Entry {
		for _, change := range entry.Changes {
			if change.Field == "messages" {
				wg.Add(1)

				// Usar o tipo explicitamente nomeado
				value := change.Value

				// Processa as mensagens em paralelo
				go func(value WebhookValue) {
					defer wg.Done()

					for _, message := range value.Messages {
						sender := message.From
						text := message.Text.Body

						// Adiciona o número 9 no número do telefone
						newSender := sender[:1+strings.Index(sender[1:], "9")+1] + "9" + sender[1+strings.Index(sender[1:], "9")+1:]

						// Exemplo de log ou resposta imediata (para debugging)
						log.Printf("Mensagem de %s: %s", newSender, text)

						// Chama a função sendMessage para enviar uma resposta
						go sendMessage(newSender, "heelo")
					}
				}(value) // Passando a estrutura `value` com o tipo correto
			}

			// Processa os status
			if len(change.Value.Statuses) > 0 {
				wg.Add(1)

				// Processa os status em paralelo
				go func(statuses []struct {
					ID          string `json:"id"`
					RecipientID string `json:"recipient_id"`
					Status      string `json:"status"`
					Timestamp   string `json:"timestamp"`
				}) {
					defer wg.Done()

					for _, status := range statuses {
						log.Printf("Processed status: %s", status.Status)
					}
				}(change.Value.Statuses)
			}
		}
	}

	wg.Wait()
}

// Função que envia a mensagem para o usuário
func sendMessage(number string, text string) {
	url := fmt.Sprintf("https://graph.facebook.com/v21.0/%s/messages", idNumberSend)
	headers := map[string]string{
		"Authorization": fmt.Sprintf("Bearer %s", tokenSend),
		"Content-Type":  "application/json",
	}

	// Dados para enviar a mensagem
	data := map[string]interface{}{
		"messaging_product": "whatsapp",
		"to":                number,
		"type":              "text",
		"text": map[string]interface{}{
			"body": text,
		},
	}

	// Marshal para JSON
	body, err := json.Marshal(data)
	if err != nil {
		log.Printf("Erro ao criar JSON: %s", err)
		return
	}

	// Criar requisição HTTP
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(body))
	if err != nil {
		log.Printf("Erro ao criar requisição: %s", err)
		return
	}

	// Adicionar headers à requisição
	for key, value := range headers {
		req.Header.Add(key, value)
	}

	// Enviar a requisição
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Erro ao enviar requisição: %s", err)
		return
	}
	defer resp.Body.Close()

	// Verificar o status da resposta
	if resp.StatusCode == http.StatusOK {
		log.Println("Mensagem enviada com sucesso!")
	} else {
		log.Printf("Erro ao enviar mensagem: %d %s", resp.StatusCode, resp.Status)
	}
}

func main() {
	r := gin.Default()

	// Endpoint para receber mensagens e status
	r.POST("/webhook", receiveMessage)

	r.Run(":5000")
}
