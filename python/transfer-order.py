import json
import os

# Script para atualizar o arquivo characters.json com dados filtrados de order.json
# Este script lê os arquivos updated_characters.json e characters.json,
# combina os dados mantendo apenas os campos id, type, order, name do updated e ability do characters,
# e salva o resultado em um novo arquivo new.json.

# Definir os caminhos relativos
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
updated_characters_path = os.path.join(base_dir, 'updated_characters.json')
original_characters_path = os.path.join(base_dir, 'characters.json')
output_path = os.path.join(base_dir, 'new.json')

# Carregar os dois arquivos
with open(updated_characters_path, 'r', encoding='utf-8') as f:
    updated_characters = json.load(f)

with open(original_characters_path, 'r', encoding='utf-8') as f:
    original_characters = json.load(f)

# Criar um dicionário de lookup por id
original_lookup = {char['id']: char for char in original_characters}

# Construir o novo array
new_characters = []

for char in updated_characters:
    char_id = char['id']
    new_char = {
        'id': char_id,
        'type': char['type'],
        'order': char['order'],
        'name': original_lookup.get(char_id, {}).get('name', ''),
        'ability': original_lookup.get(char_id, {}).get('ability', '')
    }
    new_characters.append(new_char)

# Salvar no new.json dentro de data
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(new_characters, f, ensure_ascii=False, indent=4)

print(f'Arquivo new.json criado com sucesso em: {output_path}')
