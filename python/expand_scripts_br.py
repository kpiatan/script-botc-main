import json
import re
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO DOS CAMINHOS
# ============================================================

# Estrutura:
#
# script-botc-main/
# ├── data/
# │   └── all.json
# ├── json/
# │   ├── arquivo1.json
# │   └── arquivo2.json
# └── python/
#     └── expand_scripts_br.py
#

BASE_DIR = Path(__file__).resolve().parent.parent

ALL_JSON = BASE_DIR / "data" / "all.json"
JSON_DIR = BASE_DIR / "json"


# ============================================================
# CARREGAR ALL.JSON
# ============================================================

def carregar_all_json():
    """Carrega o all.json e cria um índice por ID."""

    with open(ALL_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    personagens = {}

    for personagem in data:

        personagem_id = personagem.get("id")

        if not personagem_id:
            continue

        # ID original
        personagens[personagem_id] = personagem

        # Também permite procurar sem o "_br"
        #
        # Exemplo:
        # washerwoman_br
        #
        # também será encontrado como:
        # washerwoman

        if personagem_id.endswith("_br"):
            id_sem_br = personagem_id[:-3]
            personagens[id_sem_br] = personagem

    return personagens


# ============================================================
# CARREGAR UM ARQUIVO DE SCRIPT
# ============================================================

def carregar_script(arquivo):
    """
    Carrega um arquivo de script.

    Aceita JSON normal e também o formato antigo:

        [*chef*, *librarian*, *empath*]

    convertendo automaticamente para:

        ["chef", "librarian", "empath"]
    """

    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # Primeiro tenta JSON normal
    try:
        return json.loads(conteudo)

    except json.JSONDecodeError:

        # ----------------------------------------------------
        # Tenta corrigir o formato:
        #
        # [*chef*, *librarian*, *empath*]
        #
        # para:
        #
        # ["chef", "librarian", "empath"]
        # ----------------------------------------------------

        conteudo_corrigido = re.sub(
            r"\*([A-Za-z0-9_]+)\*",
            r'"\1"',
            conteudo
        )

        try:
            return json.loads(conteudo_corrigido)

        except json.JSONDecodeError as e:

            print("  ERRO: JSON inválido")
            print(f"  Linha: {e.lineno}")
            print(f"  Coluna: {e.colno}")
            print(f"  Mensagem: {e.msg}")

            return None


# ============================================================
# PROCESSAR UM ARQUIVO
# ============================================================

def processar_arquivo(arquivo, personagens, ids_nao_encontrados):

    print(f"Processando: {arquivo.name}")

    data = carregar_script(arquivo)

    # Não conseguiu carregar
    if data is None:
        return False, 0

    resultado = []

    encontrados_neste_arquivo = 0

    # ========================================================
    # O script normalmente é uma lista
    # ========================================================

    if isinstance(data, list):

        for item in data:

            # ------------------------------------------------
            # Objeto/dicionário
            #
            # Exemplo:
            # {"id": "_meta", ...}
            # ------------------------------------------------

            if isinstance(item, dict):

                personagem_id = item.get("id")

                # _meta não é personagem
                if personagem_id == "_meta":
                    resultado.append(item)
                    continue

                # Objeto sem ID
                if not personagem_id:
                    resultado.append(item)
                    continue

                personagem = personagens.get(personagem_id)

                if personagem:

                    resultado.append(personagem)
                    encontrados_neste_arquivo += 1

                else:

                    print(
                        f"  Aviso: ID não encontrado: "
                        f"{personagem_id}"
                    )

                    resultado.append(item)

                    ids_nao_encontrados.add(personagem_id)

            # ------------------------------------------------
            # String
            #
            # Exemplo:
            # "chef"
            # ------------------------------------------------

            elif isinstance(item, str):

                personagem_id = item

                personagem = personagens.get(personagem_id)

                if personagem:

                    resultado.append(personagem)
                    encontrados_neste_arquivo += 1

                else:

                    print(
                        f"  Aviso: ID não encontrado: "
                        f"{personagem_id}"
                    )

                    # Mantém o ID original
                    resultado.append(item)

                    ids_nao_encontrados.add(personagem_id)

            # ------------------------------------------------
            # Outro tipo
            # ------------------------------------------------

            else:

                print(
                    f"  Aviso: item inesperado: {item}"
                )

                resultado.append(item)

    # ========================================================
    # Caso o JSON seja um objeto em vez de uma lista
    # ========================================================

    elif isinstance(data, dict):

        print("  Aviso: arquivo possui objeto JSON em vez de lista.")

        resultado = data

    # ========================================================
    # Formato inesperado
    # ========================================================

    else:

        print(
            f"  ERRO: formato JSON inesperado."
        )

        return False, 0

    # ========================================================
    # SALVAR
    # ========================================================

    arquivo_saida = arquivo.parent / f"TEMP_{arquivo.name}"

    with open(arquivo_saida, "w", encoding="utf-8") as f:

        json.dump(
            resultado,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"  Criado: {arquivo_saida.name} "
        f"({encontrados_neste_arquivo} personagens expandidos)"
    )

    return True, encontrados_neste_arquivo


# ============================================================
# MAIN
# ============================================================

def main():

    print("Carregando all.json...")

    try:

        personagens = carregar_all_json()

    except Exception as e:

        print(f"Erro ao carregar all.json: {e}")
        return

    print(
        f"Encontrados {len(personagens)} IDs."
    )

    print()

    # ========================================================
    # ENCONTRAR OS ARQUIVOS
    # ========================================================

    arquivos = [
        arquivo
        for arquivo in JSON_DIR.glob("*.json")
        if not arquivo.name.startswith("TEMP_")
    ]

    if not arquivos:

        print("Nenhum arquivo JSON encontrado.")
        return

    print(
        f"Encontrados {len(arquivos)} arquivos para processar."
    )

    print()

    # ========================================================
    # CONTADORES
    # ========================================================

    processados = 0
    erros = 0
    total_personagens = 0

    ids_nao_encontrados = set()

    # ========================================================
    # PROCESSAR
    # ========================================================

    for arquivo in arquivos:

        sucesso, quantidade = processar_arquivo(
            arquivo,
            personagens,
            ids_nao_encontrados
        )

        if sucesso:

            processados += 1
            total_personagens += quantidade

        else:

            erros += 1

        print()

    # ========================================================
    # RESUMO
    # ========================================================

    print()
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)

    print(
        f"Arquivos encontrados:        {len(arquivos)}"
    )

    print(
        f"Arquivos processados:        {processados}"
    )

    print(
        f"Arquivos com erro:           {erros}"
    )

    print(
        f"Personagens expandidos:      {total_personagens}"
    )

    print(
        f"IDs não encontrados:          "
        f"{len(ids_nao_encontrados)}"
    )

    # ========================================================
    # IDs NÃO ENCONTRADOS
    # ========================================================

    if ids_nao_encontrados:

        print()
        print("IDs não encontrados:")
        print("-" * 40)

        for personagem_id in sorted(ids_nao_encontrados):

            print(f"  - {personagem_id}")

    # ========================================================
    # FINAL
    # ========================================================

    print()
    print("=" * 60)

    if erros == 0:

        print(
            "Todos os arquivos foram processados!"
        )

    else:

        print(
            "Processamento concluído, mas alguns "
            "arquivos apresentaram erros."
        )

    print("=" * 60)


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    main()