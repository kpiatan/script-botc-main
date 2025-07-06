import json

# Script para processar o arquivo roles.json e gerar order.json
# Este programa lê um arquivo JSON contendo uma lista de papéis do jogo na ordem que são mostrados nos scripts,
# extrai o id, tipo (roleType) e atribui uma ordem sequencial a cada papel.
# O resultado é salvo em um novo arquivo JSON (order.json) com os campos: id, type e order.
def process_roles_file(input_file, output_file):
    try:
        # Ler o arquivo roles.json
        with open(input_file, 'r', encoding='utf-8') as file:
            roles = json.load(file)

        # Processar os dados
        processed_roles = []
        for index, role in enumerate(roles, start=1):
            processed_roles.append({
                "id": role["id"],
                "type": role["roleType"],
                "order": index
            })

        # Salvar no arquivo order.json
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(processed_roles, file, indent=4, ensure_ascii=False)

        print(f"Arquivo '{output_file}' salvo com sucesso!")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_file}' não foi encontrado.")
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{input_file}' não está no formato JSON válido.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Nome dos arquivos
input_file = "./data/roles.json"
output_file = "./data/order.json"

# Executar o processamento
process_roles_file(input_file, output_file)
