import json
import tkinter as tk
from tkinter import filedialog

# Esse script simplifica um arquivo JSON, mantendo apenas os campos id, type (troca para team), name e ability.
# Ele usa uma interface gráfica para selecionar o arquivo de entrada e o local de saída.

def simplificar_json():
    root = tk.Tk()
    root.withdraw()  # esconde a janela principal

    # selecionar arquivo de entrada
    entrada = filedialog.askopenfilename(
        title="Selecione o arquivo JSON de entrada",
        filetypes=[("Arquivos JSON", "*.json")]
    )
    if not entrada:
        print("Nenhum arquivo selecionado.")
        return

    # selecionar arquivo de saída
    saida = filedialog.asksaveasfilename(
        title="Salvar arquivo simplificado como...",
        defaultextension=".json",
        filetypes=[("Arquivos JSON", "*.json")]
    )
    if not saida:
        print("Nenhum arquivo de saída escolhido.")
        return

    # processar
    with open(entrada, "r", encoding="utf-8") as f:
        dados = json.load(f)

    resultado = []
    for item in dados:
        if "name" in item and "ability" in item:
            novo_item = {
                "id": item.get("id"),
                "type": item.get("team"),
                "name": item.get("name"),
                "ability": item.get("ability")
            }
            resultado.append(novo_item)

    with open(saida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"Arquivo salvo em: {saida}")

if __name__ == "__main__":
    simplificar_json()
