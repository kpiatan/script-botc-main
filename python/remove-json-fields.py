import json
import os

def filter_json(file_path):
    """
    Mantém apenas os campos "name", "ability" e "id" no JSON, e remove "_br" do campo "id".
    :param file_path: Caminho do arquivo JSON.
    :return: O JSON filtrado como string.
    """
    # Lê o JSON do arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        input_json = json.load(f)

    # Filtra os campos "name", "ability" e "id"
    filtered_json = []
    for item in input_json:
        filtered_item = {
            "name": item.get("name"),
            "ability": item.get("ability"),
            "id": item.get("id", "").replace("_br", "")  # Remove "_br" do campo "id"
        }
        filtered_json.append(filtered_item)

    return json.dumps(filtered_json, indent=4, ensure_ascii=False)

# Exemplo de uso
if __name__ == "__main__":
    # Caminho para o arquivo JSON
    file_path = os.path.join("data", "all.json")

    # Aplica o filtro
    result = filter_json(file_path)

    # Exibe o resultado
    print("JSON filtrado:\n", result)

    # Opcional: Salvar o resultado em um novo arquivo
    output_path = os.path.join("data", "filtered_all.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"JSON filtrado salvo em: {output_path}")
