package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
)

type Message struct {
	Number string `json:"number"`
	Text   string `json:"text"`
}

type Response struct {
	Status int    `json:"status"`
	Body   string `json:"body"`
}

var (
	tokenSend    = "EAAM8AX6oBoIBO7skGgJfeTknyNrbtnrMEoogB8w4npuyLEC1ivSNWZAH6MZBaAKKE1cr4RGx0J84jSH2uyqSRi3IANyI2kpPhEv5JjkHBd5zsBfhqxSd86NXoFhTtg34TQFHVykAQWN5lCBJf2mlpEcpg3ZCLYUFaXy2QCS3ITThNcqAoyHEBEhvi6h5TTJ6q2ICIV52Lm88IHIgtYZAtanxDvclqtPixtQ4MOgt"
	idNumberSend = "523859527469741"
)

func sendMessage(msg Message, wg *sync.WaitGroup, ch chan Response) {
	defer wg.Done()

	url := fmt.Sprintf("https://graph.facebook.com/v21.0/%s/messages", idNumberSend)
	headers := map[string]string{
		"Authorization": fmt.Sprintf("Bearer %s", tokenSend),
		"Content-Type":  "application/json",
	}

	data := map[string]interface{}{
		"messaging_product": "whatsapp",
		"to":                msg.Number,
		"type":              "text",
		"text": map[string]interface{}{
			"preview_url": true,
			"body":        msg.Text,
		},
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		ch <- Response{Status: http.StatusInternalServerError, Body: fmt.Sprintf("JSON error: %v", err)}
		return
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		ch <- Response{Status: http.StatusInternalServerError, Body: fmt.Sprintf("Request error: %v", err)}
		return
	}

	for key, value := range headers {
		req.Header.Set(key, value)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		ch <- Response{Status: http.StatusInternalServerError, Body: fmt.Sprintf("Request failed: %v", err)}
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		ch <- Response{Status: resp.StatusCode, Body: "Mensagem enviada com sucesso!"}
	} else {
		ch <- Response{Status: resp.StatusCode, Body: fmt.Sprintf("Erro: %s", resp.Status)}
	}
}

func sendMessages(messages []Message) {
	var wg sync.WaitGroup
	ch := make(chan Response, len(messages))

	for _, msg := range messages {
		wg.Add(1)
		go sendMessage(msg, &wg, ch)
	}

	wg.Wait()
	close(ch)

	for resp := range ch {
		log.Printf("Status: %d, Response: %s", resp.Status, resp.Body)
	}
}

func main() {
	if tokenSend == "" || idNumberSend == "" {
		log.Fatal("Ambiente não configurado corretamente. Verifique TOKEN_SEND e ID_NUMBER_SEND.")
	}

	messages := []Message{
		{Number: "+5571999889073", Text: "è hora de trabalhar"},
	}

	sendMessages(messages)
}
