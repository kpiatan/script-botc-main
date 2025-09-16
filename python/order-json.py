#!/usr/bin/env python3
# renumber_orders.py
"""
Leia um JSON, renumera o campo "order" conforme a posição do objeto na lista,
e garante que a chave "order" fique imediatamente após "type" (ou no fim se não houver "type").
Abre diálogos para escolher arquivo de entrada e saída.
"""

import json
import tkinter as tk
from tkinter import filedialog
from collections import OrderedDict
from typing import Any

def process_list(lst: list) -> list:
    """Processa uma lista de objetos (dicionários), renumerando 'order' por posição."""
    new_list = []
    for idx, item in enumerate(lst, start=1):
        # Se não for um dict, processa recursivamente (caso haja listas internas)
        if not isinstance(item, dict):
            if isinstance(item, list):
                new_list.append(process_list(item))
            else:
                new_list.append(item)
            continue

        # item é um dict/OrderedDict: copiamos as chaves, pulamos 'order' original
        novo = OrderedDict()
        type_seen = False
        for k, v in item.items():
            if k == "order":
                # pule o 'order' original — vamos inserir um novo na posição desejada
                continue
            # copia a chave como estava
            novo[k] = v
            # logo após copiar 'type', insere o 'order' com o índice atual
            if k == "type":
                novo["order"] = idx
                type_seen = True

        # se não teve 'type', coloca 'order' no fim
        if not type_seen:
            novo["order"] = idx

        new_list.append(novo)
    return new_list

def process_data(data: Any) -> Any:
    """
    Se data for uma lista de objetos, processa-a.
    Se for um dict, percorre chaves e processa listas de objetos encontradas.
    Mantém outras estruturas intactas.
    """
    if isinstance(data, list):
        # se a lista contém dicionários, renumera essa lista
        if any(isinstance(x, dict) for x in data):
            return process_list(data)
        # caso contrário, processa recursivamente elementos (listas/dicts)
        return [process_data(x) if isinstance(x, (list, dict)) else x for x in data]

    if isinstance(data, dict):
        novo = OrderedDict()
        for k, v in data.items():
            if isinstance(v, list) and any(isinstance(x, dict) for x in v):
                # lista que contém objetos -> renumera essa lista
                novo[k] = process_list(v)
            elif isinstance(v, (list, dict)):
                # estrutura aninhada -> processa recursivamente
                novo[k] = process_data(v)
            else:
                novo[k] = v
        return novo

    # tipos escalares
    return data

def escolher_arquivos_e_processar():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    entrada = filedialog.askopenfilename(
        title="Selecione o arquivo JSON de entrada",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if not entrada:
        print("Nenhum arquivo de entrada selecionado. Saindo.")
        return

    saida = filedialog.asksaveasfilename(
        title="Selecione onde salvar o JSON de saída",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if not saida:
        print("Nenhum arquivo de saída selecionado. Saindo.")
        return

    # Ler mantendo a ordem das chaves de cada objeto
    with open(entrada, "r", encoding="utf-8") as f:
        dados = json.load(f, object_pairs_hook=OrderedDict)

    # Processar (renumerar)
    novos = process_data(dados)

    # Salvar
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(novos, f, ensure_ascii=False, indent=4)

    print(f"Arquivo salvo em: {saida}")

if __name__ == "__main__":
    escolher_arquivos_e_processar()
