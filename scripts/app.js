document.addEventListener('DOMContentLoaded', function () {
  let characters = []; // Variável global para armazenar personagens carregados
  let jinxes = [];

  // Carrega os jinxes
  fetch('data/jinxes.json')
    .then(response => response.json())
    .then(data => jinxes = data)
    .catch(error => console.error('Erro ao carregar jinxes:', error));

  // Carrega os personagens do JSON local
  fetch('data/characters.json')
    .then(response => response.json())
    .then(data => {
      characters = data; // Armazena os personagens carregados
      renderCharacterList(characters);
    })
    .catch(error => {
      console.error('Erro ao carregar os personagens:', error);
    });

  // Defina a ordem desejada dos tipos
  const order = ['townsfolk', 'outsider', 'minion', 'demon'];

  // Função para mapear os tipos para os nomes em português
  function getTypeInPortuguese(type) {
    const typeMap = {
      'townsfolk': 'Aldeões',
      'outsider': 'Forasteiros',
      'minion': 'Lacaios',
      'demon': 'Demônios',
      'travellers': 'Viajantes',
      'fabled': 'Lendas',
      // Adicione mais tipos conforme necessário
    };

    return typeMap[type.toLowerCase()] || type; // Retorna o tipo original se não houver tradução
  }

  // Renderiza a lista de personagens
  function renderCharacterList(characters) {
    const characterList = document.getElementById('character-list');

    if (!characterList) {
      console.error("Elemento #character-list não encontrado.");
      return;
    }

    // Ordena os personagens por 'order' antes de agrupá-los por tipo
    characters.sort((a, b) => a.order - b.order); 

    // Agrupa os personagens por tipo
    const types = {};
    characters.forEach(character => {
      if (!types[character.type]) {
        types[character.type] = [];
      }
      types[character.type].push(character);
    });

    // Renderiza os personagens agrupados por tipo
    Object.keys(types).forEach(type => {
      const typeSection = document.createElement('div');
      typeSection.classList.add('type-section');

      const toggleButton = document.createElement('button');
      toggleButton.textContent = getTypeInPortuguese(type); // Exibe o nome em português
      toggleButton.classList.add('toggle-button');
      toggleButton.addEventListener('click', () => {
        const list = typeSection.querySelector('ul');
        list.style.display = list.style.display === 'none' ? 'block' : 'none';
      });

      typeSection.appendChild(toggleButton);

      const ul = document.createElement('ul');
      ul.style.display = 'block';

      types[type].forEach(character => {
        const li = document.createElement('li');
        li.textContent = character.name;

        const img = document.createElement('img');
        img.src = `images/Icon_${character.id}.png`;
        img.alt = character.name;
        img.style.width = '40px';
        img.style.marginRight = '10px';

        li.prepend(img);

        // Evento de seleção
        li.addEventListener('click', function () {
          li.classList.toggle('selected');
          updateSelectedCharacters();
        });

        ul.appendChild(li);
      });

      typeSection.appendChild(ul);
      characterList.appendChild(typeSection);
    });
  }

// Define as cores específicas para os tipos
const typeColors = {
  'townsfolk': '#008bc1', // Azul para Cidadãos
  'outsider': '#808080',  // Cinza para Forasteiros
  'minion': '#7f0c10',     // Vermelho para Lacaios
};

let colorIndex = 0;

// Atualiza os personagens selecionados na folha A4
function updateSelectedCharacters() {
  const selectedCharacters = document.querySelectorAll('#character-list li.selected');
  const selectedContainer = document.getElementById('selected-characters');
  const selectedIdsInput = document.getElementById('selected-ids'); // Novo elemento

  if (!selectedContainer) {
    console.error("Elemento #selected-characters não encontrado.");
    return;
  }

  selectedContainer.innerHTML = ''; // Limpa o conteúdo anterior

  // Cria os dois contêineres
  const typeListContainer = document.createElement('div'); // Tipos na esquerda
  typeListContainer.classList.add('type-list-container');
  const characterGridContainer = document.createElement('div'); // Personagens na direita
  characterGridContainer.classList.add('character-grid-container');

  // Agrupa personagens por tipo
  const groupedByType = {};
  selectedCharacters.forEach(character => {
    const characterName = character.textContent.trim();
    const characterImg = character.querySelector('img').src;

    const match = characterImg.match(/Icon_([\w-]+)\.png/);
    if (!match || !match[1]) return;

    const characterId = match[1];
    const characterData = characters.find(c => c.id === characterId);
    const characterType = characterData?.type || 'Desconhecido';

    if (!groupedByType[characterType]) {
      groupedByType[characterType] = [];
    }
    groupedByType[characterType].push({ name: characterName, img: characterImg, ability: characterData?.ability });
  });

  // Atualiza o campo de IDs com os IDs dos personagens selecionados
  
// Atualiza o campo de IDs com os IDs dos personagens selecionados (MANTENHA ESSA PARTE)
const formattedIds = Array.from(selectedCharacters) // ✅ Renomeado para "formattedIds"
  .map(character => character.textContent.trim())
  .map(characterName => {
    const characterData = characters.find(c => c.name === characterName);
    return characterData?.id;
  })
  .filter(id => id)
  .map(id => `"${id}"`)
  .join(', ');

selectedIdsInput.value = `[${formattedIds}]`; // ✅ Usando o novo nome

// FUNÇÃO SEPARADA PARA ATUALIZAR JINX (ADICIONE ISSO)
function updateJinxDisplay() {
  const selectedIds = Array.from(document.querySelectorAll('#character-list li.selected')).map(li => {
    const imgSrc = li.querySelector('img').src;
    const match = imgSrc.match(/Icon_([\w-]+)\.png/);
    return match ? match[1] : null;
  }).filter(Boolean);

  const hasJinx = jinxes.some(jinx => 
    selectedIds.includes(jinx.character1) && 
    selectedIds.includes(jinx.character2)
  );

  const showJinx = document.getElementById('show-jinx').checked;
  const jinxElement = document.getElementById('a4-jinx');
  
  if (jinxElement) {
    jinxElement.style.display = (hasJinx && showJinx) ? 'flex' : 'none';
    jinxElement.classList.toggle('has-jinx', hasJinx && showJinx);
  }
}

// NO EVENT LISTENER DO CHECKBOX (MODIFIQUE PARA)
document.getElementById('show-jinx').addEventListener('change', updateJinxDisplay);
  // Ordena as chaves dos tipos com base na ordem definida
  order.forEach(type => {
    if (groupedByType[type]) {
      // Contêiner do grupo
      const typeContainer = document.createElement('div');
      typeContainer.classList.add('type-container');

      // Cabeçalho do tipo
      const typeHeader = document.createElement('div');
      typeHeader.textContent = getTypeInPortuguese(type); // Tradução
      typeHeader.classList.add('type-header');
    
      // Adiciona uma classe específica com base no tipo
      if (type === 'townsfolk' || type === 'outsider') {
        typeHeader.classList.add('townsfolk');
      } else if (type === 'demon' || type === 'minion') {
        typeHeader.classList.add('demon');
      }
    
      // Contêiner dos personagens
      const typeCharacters = document.createElement('div');
      typeCharacters.classList.add('type-characters');
    
      groupedByType[type].forEach(character => {
        const characterDiv = document.createElement('div');
        characterDiv.classList.add('selected-character');
    
        const img = document.createElement('img');
        img.src = character.img;
    
        const infoDiv = document.createElement('div');
        infoDiv.classList.add('info');
    
        const name = document.createElement('p');
        name.classList.add('name');
        name.textContent = character.name;
    
        const ability = document.createElement('p');
        ability.classList.add('ability');
        ability.textContent = character.ability || 'Habilidade não encontrada';
    
        infoDiv.appendChild(name);
        infoDiv.appendChild(ability);
        characterDiv.appendChild(img);
        characterDiv.appendChild(infoDiv);
    
        typeCharacters.appendChild(characterDiv);
      });
    
      // Monta o contêiner do grupo
      typeContainer.appendChild(typeHeader);
      typeContainer.appendChild(typeCharacters);
      typeListContainer.appendChild(typeContainer);

      // Adiciona a linha horizontal
      if (type === 'demon') {
        // Não adiciona linha após "Demônios"
        return;
      }

      const hr = document.createElement('hr');
      hr.classList.add('horizontal-line');

      // Define a cor da linha baseada no tipo
      if (type === 'townsfolk') {
        hr.style.borderTopColor = typeColors['townsfolk']; // Azul para Cidadãos
      } else if (type === 'outsider') {
        hr.style.borderTopColor = typeColors['outsider']; // Cinza para Forasteiros
      } else if (type === 'minion') {
        hr.style.borderTopColor = typeColors['minion']; // Vermelho para Lacaios
      }

      // Adiciona a linha ao final do tipo
      typeListContainer.appendChild(hr);
    }
  });

  // Adiciona os contêineres principais à folha
  selectedContainer.appendChild(typeListContainer);
  selectedContainer.appendChild(characterGridContainer);
  updateJinxDisplay();
}

// Substitua a função applyIdsFromTextarea por esta versão
function applyIdsFromTextarea() {
  const input = document.getElementById('selected-ids').value;
  
  // Extrai todos os IDs usando uma expressão regular flexível
  const rawIds = input.toLowerCase()
    .replace(/[^a-z0-9\s,"'\[\]]/g, ' ') // Remove caracteres especiais
    .match(/([a-z0-9]+)/g) || []; // Captura sequências alfanuméricas

  // Limpa seleções atuais
  document.querySelectorAll('#character-list li.selected').forEach(li => {
    li.classList.remove('selected');
  });

  // Mapeia para IDs válidos existentes
  const validIds = rawIds
    .map(id => id.trim())
    .filter(id => characters.some(c => c.id === id));

  // Seleciona os novos personagens
  validIds.forEach(id => {
    const character = characters.find(c => c.id === id);
    if (character) {
      const li = Array.from(document.querySelectorAll('#character-list li')).find(item => {
        return item.textContent.trim() === character.name;
      });
      if (li) li.classList.add('selected');
    }
  });

  updateSelectedCharacters();
}

// Substitua o evento do botão por um observer no textarea
const idsTextarea = document.getElementById('selected-ids');

// Função para detectar colagem/digitação
function handleTextareaInput() {
  if (idsTextarea.value.trim().length > 0) {
    applyIdsFromTextarea();
  }
}

// Adicione os listeners
idsTextarea.addEventListener('input', handleTextareaInput);
idsTextarea.addEventListener('paste', handleTextareaInput);

// Remova a parte do código que referencia o botão (se houver)

// Opcional: Atualizar automaticamente ao digitar (remova se preferir só o botão)
document.getElementById('selected-ids').addEventListener('input', () => {
  if (document.getElementById('selected-ids').value.trim().startsWith('[')) {
    applyIdsFromTextarea();
  }
});

});

// Identifique o elemento de texto editável
const topTextElement = document.getElementById('a4-header');

// Função para atualizar o título da página
function updatePageTitle() {
  const textContent = topTextElement.textContent.trim(); // Obtem o texto
  document.title = `${textContent}-PT`; // Atualiza o título com "-PT"
}

// Adicione o evento de entrada (input) para atualizar em tempo real
topTextElement.addEventListener('input', updatePageTitle);

// Atualiza o título inicial
updatePageTitle();

// Adicione este código após os listeners do textarea
document.getElementById('show-jinx').addEventListener('change', () => {
  updateSelectedCharacters();
});
