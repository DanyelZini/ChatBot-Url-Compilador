# from AnalisadorLexico import Analis
from AnalisadorSintatico import AnalisadorSintatico
import os

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    analisador = AnalisadorSintatico()
    print("--------------------------- Search Engine ---------------------------")
    while(True):
        if(analisador.lexico.tabela_simbolos.__len__() != 0):
            print(analisador.lexico.tabela_simbolos)
        if(analisador.lexico.fila_tokens.__len__() != 0):
            print(analisador.lexico.fila_tokens)            
        

        entrada = input("> ").strip()
        if(entrada == "sair" or entrada == "0"):
            break
        analisador.lexico.tokenizar(entrada if entrada else " ")
        analisador.inserir_tabelas_regras()
        print("\n")

print("--------------------------- Close Search ---------------------------")
