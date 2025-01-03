import json
import os

# Caminhos dos arquivos
characters_file = os.path.join('data', 'order.json')
filtered_all_file = os.path.join('data', 'filtered_all.json')
output_file = 'updated_characters.json'

# Carregar os arquivos JSON
with open(characters_file, 'r', encoding='utf-8') as f:
    characters = json.load(f)

with open(filtered_all_file, 'r', encoding='utf-8') as f:
    filtered_all = json.load(f)

# Criar um dicionário para acessar os dados rapidamente pelo id
filtered_all_dict = {item['id']: item for item in filtered_all}

# Atualizar os dados no arquivo characters.json
for character in characters:
    character_id = character.get('id')
    if character_id and character_id in filtered_all_dict:
        filtered_data = filtered_all_dict[character_id]
        # Atualizar os campos "name" e "ability"
        character['name'] = filtered_data.get('name', character.get('name'))
        character['ability'] = filtered_data.get('ability', character.get('ability'))

# Salvar o arquivo atualizado
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(characters, f, ensure_ascii=False, indent=4)

print(f'Arquivo atualizado salvo como {output_file}')
