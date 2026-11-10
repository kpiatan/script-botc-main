
import re
import json
from collections import Counter
from pathlib import Path

# ==================================================
# CONFIGURAÇÕES
# ==================================================

# Pasta onde está este script
pasta_script = Path(__file__).resolve().parent

# Arquivos
arquivo_scripts = pasta_script.parent / "data" / "scripts.txt"
arquivo_roles = pasta_script.parent / "data" / "roles.json"

# Marcador de atualização
marcador = "===== CONTAGEM ATUALIZADA ATÉ: "

# Campos que não são personagens
ignorar = {
    "_meta",
    "name",
    "author",
    "isOfficial",
    "undefined"
}

# Categorias e seus nomes para exibição
categorias = {
    "townsfolk": "ALDEÕES (TOWNSFOLK)",
    "outsider": "FORASTEIROS (OUTSIDERS)",
    "minion": "LACAIOS (MINIONS)",
    "demon": "DEMÔNIOS (DEMONS)",
    "traveller": "VIAJANTES (TRAVELLERS)",
    "fabled": "FABLED",
    "loric": "LORIC"
}


# ==================================================
# CARREGAR BASE DE PERSONAGENS
# ==================================================

print("\nCarregando base de personagens...")

with open(arquivo_roles, "r", encoding="utf-8") as f:
    roles = json.load(f)

# Cria dicionário ID -> categoria
tipos = {
    role["id"]: role["team"]
    for role in roles
    if isinstance(role, dict)
    and "id" in role
    and "team" in role
}

print(f"Personagens carregados: {len(tipos)}")


# ==================================================
# LER ARQUIVO DE SCRIPTS
# ==================================================

with open(arquivo_scripts, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Remove marcador antigo, se existir
conteudo = re.sub(
    r"===== CONTAGEM ATUALIZADA ATÉ:.*?=====",
    "",
    conteudo
)


# ==================================================
# EXTRAIR PERSONAGENS
# ==================================================

# Formato 1: {"id": "washerwoman"}
com_id = re.findall(
    r'"id"\s*:\s*"([^"]+)"',
    conteudo
)

# Formato 2: "washerwoman"
# Remove previamente os campos id para não duplicar
conteudo_sem_id = re.sub(
    r'"id"\s*:\s*"[^"]+"',
    '',
    conteudo
)

sem_id = re.findall(
    r'"([a-zA-Z][a-zA-Z0-9_]*)"',
    conteudo_sem_id
)

# Junta os dois formatos
todos = com_id + sem_id

# Remove metadados
todos = [
    personagem
    for personagem in todos
    if personagem not in ignorar
]


# ==================================================
# CONTABILIZAR PERSONAGENS
# ==================================================

contagem = Counter(todos)

# Cria um contador separado para cada categoria
contagem_por_tipo = {
    categoria: Counter()
    for categoria in categorias
}

# Personagens não identificados
nao_identificados = Counter()

for personagem, quantidade in contagem.items():

    tipo = tipos.get(personagem)

    if tipo in contagem_por_tipo:
        contagem_por_tipo[tipo][personagem] = quantidade
    else:
        nao_identificados[personagem] = quantidade


# ==================================================
# EXIBIR RESULTADOS
# ==================================================

print("\n" + "=" * 55)
print("       ESTATÍSTICAS DOS SCRIPTS DE BOTC")
print("=" * 55)

for categoria, nome in categorias.items():

    personagens = contagem_por_tipo[categoria]

    if not personagens:
        continue

    print(f"\n{'=' * 55}")
    print(f" {nome}")
    print("=" * 55)

    for personagem, quantidade in personagens.most_common():
        print(f"{personagem:25} {quantidade:>5}")

    print("-" * 35)
    print(f"{'Total da categoria:':25} {sum(personagens.values()):>5}")
    total_disponiveis = sum(
        1 for role in roles
        if role.get("team") == categoria
    )

    print(
        f"{'Personagens diferentes:':25} "
        f"{len(personagens)}/{total_disponiveis}"
    )


# ==================================================
# PERSONAGENS NÃO IDENTIFICADOS
# ==================================================

if nao_identificados:

    print("\n" + "=" * 55)
    print(" PERSONAGENS NÃO IDENTIFICADOS")
    print("=" * 55)

    for personagem, quantidade in nao_identificados.most_common():
        print(f"{personagem:25} {quantidade:>5}")


# ==================================================
# RESUMO GERAL
# ==================================================

print("\n" + "=" * 55)
print(" RESUMO GERAL")
print("=" * 55)

print(f"{'Total de aparições:':30} {sum(contagem.values()):>5}")
print(f"{'Personagens diferentes:':30} {len(contagem):>5}")
print(f"{'Personagens na base oficial:':30} {len(contagem) - len(nao_identificados):>5}")
print(f"{'Personagens não identificados:':30} {len(nao_identificados):>5}")

print("=" * 55)


# ==================================================
# ATUALIZAR MARCADOR NO ARQUIVO
# ==================================================

nome_script = input(
    "\nAté qual script esta contagem foi atualizada? "
)

if nome_script.strip():

    conteudo_original = arquivo_scripts.read_text(
        encoding="utf-8"
    )

    # Remove marcador anterior
    conteudo_original = re.sub(
        r"\n?===== CONTAGEM ATUALIZADA ATÉ:.*?=====\s*",
        "\n",
        conteudo_original
    )

    # Adiciona novo marcador
    novo_marcador = (
        f"\n{marcador}{nome_script.strip()} =====\n"
    )

    arquivo_scripts.write_text(
        conteudo_original.rstrip() + novo_marcador,
        encoding="utf-8"
    )

    print(f"\nMarcador atualizado: {nome_script}")

print("\nContagem finalizada!")
