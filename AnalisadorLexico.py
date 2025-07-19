from collections import deque
from difflib import SequenceMatcher

class AnalisadorLexico:
    def __init__(self):
        # Alfabeto
        self.alfabeto = set(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ'
            '!@#$%¨&*()_+-=[]{};:",./<>?\\| \t\n'
        )
        
        # Caracteres especiais
        self.caracteres_especiais = set(".,;:?!\"'()[]{}-_+=*/\\@#$%&|<>^~´`“”")
        
        # Estruturas de dados
        self.stopwords = set()
        self.tabela_simbolos = []
        self.tabela_atual = []
        self.fila_tokens = deque()

        self.carregar_stopwords("./Arquivos/stopwords.txt")

    def carregar_stopwords(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as file:
                self.stopwords = {line.strip() for line in file if line.strip()}
        except FileNotFoundError:
            print(f"Erro: Arquivo de stopwords nao encontrado em {caminho}")

    def caractere_valido(self, char):
        return char in self.alfabeto

    def tokenizar(self, texto):
        self.tabela_atual.clear()
        buffer = []
        for char in texto:
            if not self.caractere_valido(char):
                raise ValueError(f"Caractere invalido: {repr(char)}")
            
            if char in self.caracteres_especiais or char.isspace():
                if buffer:
                    self.processar_palavra(''.join(buffer))
                    buffer = []
                if not char.isspace():
                    self.fila_tokens.append(char) 
            else:
                buffer.append(char)
        
        if buffer: 
            self.processar_palavra(''.join(buffer))

    def processar_palavra(self, palavra):
        if palavra.lower() not in self.stopwords:
            similar = self.similaridade(palavra)
            token = similar if similar else palavra
            if token not in self.tabela_simbolos:
                self.tabela_simbolos.append(token)
            self.fila_tokens.append(token)    
            self.tabela_atual.append(token)  

    def similaridade(self, palavra, limiar=0.7):
        for simbolo in self.tabela_simbolos:
            if SequenceMatcher(None, palavra.lower(), simbolo.lower()).ratio() >= limiar:
                return simbolo
        return ""