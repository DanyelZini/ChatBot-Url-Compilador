from ClassificarPalavrasSintatico import ClassificarPalavrasSintatico
from AnalisadorLexico import AnalisadorLexico
from urllib.parse import quote

class AnalisadorSintatico:
    def __init__(self):
        self.lexico = AnalisadorLexico()
        self.classificador = ClassificarPalavrasSintatico()
        self.base_url = "https://catalogobiblioteca.ufmg.br/pesquisa_avancada?"
        self.tabela_regras_definidas = []


        self.titulo = []
        self.autor = []
        self.assunto = []
        self.parte_url = []

    def atualizar_regras(self):
        atualizada = self.classificador.classificar_frase(self.lexico.tabela_atual)
        for palavra, tipo in atualizada:
            self.tabela_regras_definidas.append((palavra, tipo))

    def inserir_tabelas_regras(self):
        self.atualizar_regras()
        print(self.tabela_regras_definidas)
        i = 0
        while i < len(self.tabela_regras_definidas):
            palavra, tipo = self.tabela_regras_definidas[i]
            
            if tipo == "autor":
                nome, contagem = self.proxima_palavra(i, ["desconhecido", "nomes"], tipo)
                if nome:
                    self.autor.append(nome)
                    i += contagem + 1
                else:
                    i += 1
            elif tipo == "titulo":
                titulo, contagem = self.proxima_palavra(i, ["desconhecido", "nomes"], tipo)
                if titulo:
                    self.titulo.append(titulo)
                    i += contagem + 1
                else:
                    i += 1 
            elif tipo == "assunto":
                assunto, contagem = self.proxima_palavra(i, ["desconhecido", "nomes"], tipo)
                if assunto:
                    self.assunto.append(assunto)
                    i += contagem + 1
                else:
                    i += 1
            elif tipo == "nomes":
                nome, contagem = self.proxima_palavra(i, ["desconhecido", "nomes"], tipo)
                if nome:
                    self.autor.append(" ".join([palavra, nome]))
                    self.titulo.append(" ".join([palavra, nome]))
                    i += contagem + 1
            elif tipo == "desconhecido":
                desconhecido, contagem = self.proxima_palavra(i, ["desconhecido"], tipo)
                if desconhecido:
                    desconhecido = " ".join([palavra, desconhecido])
                    tipo = input("Tipo de palavra desconhecida, defina -> (autor/titulo/assunto): \n>").strip().lower()
                if tipo == "autor":
                    self.autor.append(desconhecido)
                    i += contagem + 1
                    print(i)
                    if self.tabela_regras_definidas[i][0] == "autor":
                        desconhecido, contagem = self.proxima_palavra(i, ["desconhecido"], tipo)
                        print(f"Desconhecido: {desconhecido}, Contagem: {contagem}")
                        if desconhecido:
                            self.titulo.append(desconhecido)
                        i += contagem + 1

                elif tipo == "titulo":
                    self.titulo.append(desconhecido)
                    i += contagem + 1
                elif tipo == "assunto":
                    self.assunto.append(desconhecido)
                    i += contagem + 1
                else:
                    i += 1
            else:
                i += 1 
            print(f"Autor: {self.autor}, Titulo: {self.titulo}, Assunto: {self.assunto}")

        self.juntar_palavras()
        print(f"juntando: {self.parte_url}")
        print(f"URL formatada: {self.formatar_url()}")
        self.tabela_regras_definidas.clear()

    def proxima_palavra(self, numero, tipo_proximo, tipo_atual):
        frase = ""
        palavras_lidas = 0

        if (numero + 1 < len(self.tabela_regras_definidas) and 
            self.tabela_regras_definidas[numero+1][1] in tipo_proximo):
            
            palavra_atual = self.tabela_regras_definidas[numero+1][0]
            proxima_part, contagem = self.proxima_palavra(numero+1, tipo_proximo, tipo_atual)

            frase = f"{palavra_atual} {proxima_part}".strip()
            palavras_lidas = contagem + 1

        return frase, palavras_lidas
    
    def juntar_palavras(self):
        if not hasattr(self, 'parte_url'):
            self.parte_url = []
        
        self.parte_url.clear()
        
        for autor in getattr(self, 'autor', []):
            self.parte_url.append(("AUTOR", quote(autor)))
        
        for titulo in getattr(self, 'titulo', []):
            self.parte_url.append(("TITULO", quote(titulo)))
        
        for assunto in getattr(self, 'assunto', []):
            self.parte_url.append(("ASSUNTO", quote(assunto)))
    
    def formatar_url(self):
        if not hasattr(self, 'base_url'):
            self.base_url = ""
        
        url = self.base_url
        params = []
        
        for i, (tipo, valor) in enumerate(self.parte_url, 1):
            prefix = "" if i == 1 else str(i)
            
            if i > 1:
                condition = "OR" if tipo == self.parte_url[i-2][0] or valor == self.parte_url[i-2][1] else "AND"
                params.append(f"condition{i-1 if i != 2 else ''}={condition}")

            params.extend([
                f"for{prefix}={tipo}",
                f"q{prefix}={valor}"
            ])
            
            
            print(f"Adicionando: {tipo}={valor} na URL")
        
        url += "&".join(params) + "&keyword_type=P"
        
        self.assunto.clear()
        self.titulo.clear()
        self.autor.clear()
        self.parte_url.clear()
        
        return url