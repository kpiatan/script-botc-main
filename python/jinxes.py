import json
import os

# Caminhos dos arquivos
djinn_file = os.path.join('data', 'djinn.txt')              # Arquivo de entrada (texto bruto)
jinxes_new_file = os.path.join('data', 'jinxes_new.json')   # Arquivo de saída (JSON)

# Carregar conteúdo de texto do arquivo djinn.txt
with open(djinn_file, 'r', encoding='utf-8') as f:
    texto = f.read()

# Função para transformar o texto no formato desejado
def transformar_texto(texto):
    linhas = texto.strip().split('\n')
    resultado = []

    for linha in linhas:
        if ':' in linha:
            cabecalho, descricao = linha.split(':', 1)
            partes = [p.strip().lower() for p in cabecalho.split(' / ')]
            if len(partes) == 2:
                personagem1, personagem2 = partes
                resultado.append({
                    "character1": personagem1,
                    "character2": personagem2,
                    "description": descricao.strip()
                })

    return resultado

# Aplicar a transformação
jinxes_data = transformar_texto(texto)

# Salvar o resultado no novo arquivo JSON
with open(jinxes_new_file, 'w', encoding='utf-8') as f:
    json.dump(jinxes_data, f, indent=4, ensure_ascii=False)

print(f"Arquivo salvo em: {jinxes_new_file}")
