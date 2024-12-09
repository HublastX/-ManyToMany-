import json

try:
    with open("data/config.json", "r", encoding="UTF-8") as file:
        config: dict = json.load(file)
except Exception as e:
    raise Exception(f"ERROR ao carregar config.json: {e}")


def extrair_dados_config(config: dict = config):
    try:
    
        regras_gerais = "\n".join([f"- {rule}" for rule in config["rules"]["general"]])
        interacao_regras = "\n".join(
            [f"- {rule}" for rule in config["rules"]["interaction_guidelines"]]
        )
        formato_resposta = "\n".join(
            [f"- {rule}" for rule in config["rules"]["response_format"]]
        )
        regras = f"Regras Gerais:\n{regras_gerais}\n\nDiretrizes de Interação:\n{interacao_regras}\n\nFormato de Resposta:\n{formato_resposta}"

        # Estrutura do Prompt
        prompt_context = config["prompt_structure"]["context"]
        response_structure = config["prompt_structure"]["response_structure"]
        examples = config["prompt_structure"]["examples"]

       
        for example in examples:
            for key in [
                "greeting",
                "response_body",
                "additional_information",
                "closure",
            ]:
                if key in example["response"]:
                    example["response"][key] = (
                        example["response"][key].replace("(", "").replace(")", "")
                    )

       
        name = config["name"]
        description = config["description"]

      
        return name, description, regras, prompt_context, response_structure, examples

    except KeyError as e:
        print(f"Erro ao acessar a chave: {e}")
        return None, None, None, None, None, None
