# 📚 Chatbot para Linguagem lógica de Destino

Este projeto é um **chatbot** desenvolvido em Python que interpreta comandos de uma **frase** e os converte em uma **URL de busca** para o site da biblioteca da UFMG que pertence ao Pergamum:  
[https://catalogobiblioteca.ufmg.br/pesquisa_avancada](https://catalogobiblioteca.ufmg.br/pesquisa_avancada)

O objetivo do sistema é facilitar o processo de busca por livros, autores ou assuntos, permitindo que o usuário escreva frases como, por exemplo:

> Livros de Machado de Assis sobre romance

O chatbot interpreta essa frase e gera a URL correspondente para busca no site da biblioteca:

> https://catalogobiblioteca.ufmg.br/pesquisa_avancada?for=AUTOR&q=Machado%20Assis&condition=AND&for2=ASSUNTO&q2=romance&keyword_type=P

## 🔎 Analisador Léxico

O Analisador Léxico é o primeiro componente do chatbot.  
Ele é responsável por **ler a frase do usuário e transformá-la em tokens**, que são as palavras ou símbolos relevantes para a construção da URL.  

### Etapas do Analisador Léxico:
1. 📜 **Tokenização**  
   - Percorre a frase caractere por caractere, agrupando letras em palavras.
   - Reconhece espaços, pontuação e caracteres especiais para separar as palavras.

2. 🚫 **Remoção de Stopwords**  
   - Palavras irrelevantes para a busca (como *de*, *em*, *por*, *o*, *a*, etc.) são descartadas.
   - As stopwords são lidas de um arquivo `stopwords.txt` presente no pasta `Arquivos`.

3. 🆗 **Validação de caracteres**
   - Verifica se cada caractere pertence ao alfabeto permitido (letras, números e símbolos aceitos).
   - Se encontrar algum caractere inválido, levanta um erro e interrompe o programa.

4. 🔄 **Normalização e similaridade**
   - Caso encontre uma palavra parecida com outra já existente na tabela de símbolos (com alta similaridade), ela é substituída para evitar duplicidade.

### Resultado:
Após essa análise, o Analisador Léxico gera:
- Uma fila com os **tokens válidos da frase**.
- Uma tabela de simbolos prontos para serem processados pelo Analisador Sintático, sem stopwords.
- Uma tabela de símbolos atualizada com as palavras inseridas no ultimo momento.

Esse processo garante que apenas as palavras relevantes para a pesquisa sejam passadas para as próximas etapas, facilitando a classificação e a construção da URL.

## 🧩 Analisador Sintático

O Analisador Sintático é o sistema que recebe a tabela de simbolos pelo Analisador Léxico e os organiza conforme as regras para montar os parâmetros da URL.

Ele é responsável por:
- Identificar se cada palavra corresponde a um **autor**, **título**, **assunto** ou é desconhecida.
- Agrupar as palavras relacionadas no lugar correto.
- Montar a URL com os parâmetros corretos para a busca.

### Etapas do Analisador Sintático:
1. 🔗 **Classificação dos tokens**
   - Usa o `ClassificarPalavrasSintatico` para associar cada palavra a um tipo: `autor`, `titulo`, `assunto`, `nomes` ou `desconhecido`.
   - Essa classificação é baseada nas regras e listas contidas nos arquivos em `Regras/`.

2. 🗃️ **Construção das listas**
   - As palavras são agrupadas em três listas principais:
     - `autor`: nomes dos autores.
     - `titulo`: palavras que representam o título.
     - `assunto`: termos que indicam a área ou tema.

3. 🔄 **Tratamento de palavras desconhecidas**
   - Caso encontre uma palavra que não está nas regras, pergunta ao usuário a que categoria ela pertence (`autor`, `titulo` ou `assunto`) para que seja incluída corretamente.

4. 🔗 **Juntar as palavras para montar os parâmetros**
   - Junta as palavras de cada categoria em strings completas (ex.: "Machado de Assis" ou "romance brasileiro") e aplica o encoding para URL.

5. 🌐 **Geração da URL final**
   - Usa as listas para montar a URL no formato aceito pelo site da biblioteca, com os parâmetros adequados e as condições (`AND`, `OR`) quando necessário.
   - Exemplo de entrada:

   > Obras de romance escrito por Machado de Assis

   - Saida esperada:
    
    > https://catalogobiblioteca.ufmg.br/pesquisa_avancada?for=AUTOR&q=Machado%20Assis&condition=AND&for2=TITULO&q2=romance&keyword_type=P
    

### Resultado:
O Analisador Sintático transforma os dados da tabela em uma URL completa e válida, pronta para ser usada no site da biblioteca.

### 🔍 Classificador de Palavras Sintático

O **Classificador de Palavras Sintático** é um componente interno utilizado pelo Analisador Sintático para identificar a função de cada palavra na frase do usuário.

Ele lê previamente um conjunto de **regras** definidas em arquivos na pasta `Regras/` e usa essas regras para classificar os tokens como `autor`, `titulo`, `assunto`, `nomes` ou `desconhecido`.

#### Como funciona:
1. 📂 **Carregamento das regras**
   - No início da execução, ele lê o arquivo `Regras/mapeamento_regras.txt`, que mapeia os tipos (`autor`, `titulo`, etc.) para os respectivos arquivos contendo as palavras de cada categoria.

2. 🔗 **Classificação**
   - Para cada palavra recebida, o classificador verifica se ela está em alguma das listas carregadas.
   - Se encontrar, retorna o tipo correspondente (`autor`, `titulo`, `assunto`, etc.).
   - Se não encontrar, classifica como `desconhecido`.

3. 📝 **Classificação de frases**
   - Além de palavras individuais, ele pode processar uma lista e devolver uma lista com as palavras acompanhadas de suas classificações.

#### Resultado:
O Classificador fornece ao Analisador Sintático as informações necessárias para montar as listas corretas de `autor`, `titulo` e `assunto`.

Essa separação permite que as regras possam ser facilmente editadas nos arquivos sem precisar alterar o código-fonte.

## 🚀 Instalação e Execução

Foi utilizado no projeto o **Python 3.12.3**, para evitar possiveis erros utilize-o.

### 📥 Requisitos
- Python **3.12.3** (ou compatível)

### 📂 Clonar o repositório
Primeiro, clone este repositório:
```bash
git clone <https://github.com/DanyelZini/ChatBot-Url-Compilador.git>
cd ChatBot-Url-Compilador/
```

E execute o arquivo:
>Main.py



