from collections import defaultdict
import os

class ClassificarPalavrasSintatico:
    def __init__(self):
        self.regras = defaultdict(set)
        self.carregar_regras()

    def carregar_regras(self, ):
        with open('Regras/mapeamento_regras.txt', 'r', encoding='utf-8') as file:
            mapeamento = {}
            for linha in file:
                if '=' in linha:
                    chave, valor = linha.strip().split('=')
                    mapeamento[chave] = valor
                
            for tipos, arquivo in mapeamento.items():
                caminho = os.path.join('Regras', 'tipos', arquivo)
                try:
                    with open(caminho, 'r', encoding='utf-8') as regras_file:
                        for regra in regras_file:
                            self.regras[tipos].add(regra.strip().lower())
                except FileNotFoundError:
                    print(f"Arquivo {caminho} nao encontrado.")
            
    def classificar_palavra(self, palavra):
        palavra = palavra.lower()
        for tipo, regras in self.regras.items():
            if palavra in regras:
                return tipo
        return "desconhecido"
    
    def classificar_frase(self, frase):
        palavras = frase
        classificacoes = []
        for palavra in palavras:
            classificacao = self.classificar_palavra(palavra)
            classificacoes.append((palavra, classificacao))
        return classificacoes