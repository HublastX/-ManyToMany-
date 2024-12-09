package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"

	"github.com/gin-gonic/gin"
)

var secretKeyWebhook = "my_verify_token"

func verifyWebhook(c *gin.Context) {
	mode := c.Query("hub.mode")
	token := c.Query("hub.verify_token")
	challenge := c.Query("hub.challenge")

	if mode == "subscribe" && token == secretKeyWebhook {
		c.Data(http.StatusOK, "text/plain", []byte(challenge))
		return
	}

	c.String(http.StatusForbidden, "Forbidden")
}

func processMessage(message map[string]interface{}) (map[string]string, error) {
	sender, ok := message["from"].(string)
	if !ok {
		return nil, fmt.Errorf("missing sender information")
	}

	text, _ := message["text"].(map[string]interface{})["body"].(string)

	idx := strings.Index(sender[1:], "9") + 1
	newSender := sender[:1+idx] + "9" + sender[1+idx:]

	return map[string]string{"new_sender": newSender, "user_text": text}, nil
}

func receiveMessage(c *gin.Context) {
	var data map[string]interface{}
	if err := c.ShouldBindJSON(&data); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "No data received"})
		return
	}

	log.Printf("Received data: %s", prettyJSON(data))

	entries, ok := data["entry"].([]interface{})
	if !ok || len(entries) == 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid data"})
		return
	}

	var wg sync.WaitGroup
	ch := make(chan gin.H, len(entries)) // Canal para os resultados

	for _, e := range entries {
		entry, ok := e.(map[string]interface{})
		if !ok {
			ch <- gin.H{"error": "Invalid entry format"}
			continue
		}

		changes, ok := entry["changes"].([]interface{})
		if !ok || len(changes) == 0 {
			ch <- gin.H{"error": "No changes found"}
			continue
		}

		for _, chg := range changes {
			wg.Add(1)
			go func(chg interface{}) {
				defer wg.Done()

				change, ok := chg.(map[string]interface{})
				if !ok {
					ch <- gin.H{"error": "Invalid change format"}
					return
				}

				value, ok := change["value"].(map[string]interface{})
				if !ok {
					ch <- gin.H{"error": "Invalid value format"}
					return
				}

				field, ok := change["field"].(string)
				if !ok {
					ch <- gin.H{"error": "Invalid field format"}
					return
				}

				if field == "messages" {
					messages, _ := value["messages"].([]interface{})
					if len(messages) == 0 {
						ch <- gin.H{"error": "No messages found"}
						return
					}

					for _, msg := range messages {
						message, ok := msg.(map[string]interface{})
						if !ok {
							ch <- gin.H{"error": "Invalid message format"}
							return
						}

						result, err := processMessage(message)
						if err != nil {
							ch <- gin.H{"error": err.Error()}
							return
						}

						ch <- gin.H{"new_sender": result["new_sender"], "user_text": result["user_text"]}
						return
					}
				}

				if statuses, ok := value["statuses"].([]interface{}); ok && len(statuses) > 0 {
					for _, s := range statuses {
						status, ok := s.(map[string]interface{})
						if !ok {
							ch <- gin.H{"error": "Invalid status format"}
							return
						}

						statusType, ok := status["status"].(string)
						if !ok {
							ch <- gin.H{"error": "Missing status information"}
							return
						}

						log.Printf("Processed status: %s", statusType)
						ch <- gin.H{"status": statusType}
						return
					}
				}

				ch <- gin.H{"error": "Invalid change data"}
			}(chg)
		}
	}

	wg.Wait()
	close(ch)

	results := []gin.H{}
	for res := range ch {
		results = append(results, res)
	}

	c.JSON(http.StatusOK, results)
}

func prettyJSON(data interface{}) string {
	bytes, _ := json.MarshalIndent(data, "", "  ")
	return string(bytes)
}

func main() {
	r := gin.Default()

	r.GET("/webhook", verifyWebhook)
	r.POST("/webhook", receiveMessage)

	port := os.Getenv("PORT")
	if port == "" {
		port = "5000"
	}

	if err := r.Run(":" + port); err != nil {
		log.Fatalf("Failed to run server: %v", err)
	}
}
