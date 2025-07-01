import pandas as pd
import numpy as np
import random
import datetime

class GeradorDados:

    def __init__(self, quantidade):
        self.quantidade = quantidade

    def gerar_dados_a(self):

        def gerar_data():
            """
            Gerardpr de datas aleatórias considerando meses bissexto e 
            demais dias"""

            ano = random.randint(2020, datetime.date.today().year-1)
            mes = random.randint(1,12)

            #fevereiro

            if mes == 2:

                #ano bissexto
                if(ano % 4 == 0 and ano % 100!=0) or ano % 400 == 0:
                    dia = random.randint(1,29)
                else:
                    dia = random.randint(1,28)
            
            #meses com 30 dias
            elif mes in [4,6,9,11]:
                dia = random.randint(1,30)

            #mes com 31 dias
            else:
                dia = random.randint(1,31)

            return datetime.date(ano, mes, dia)
        
        dicionario = {
            #'Id_Venda' : [ loop for loop in range(self.quantidade)],
            'Id_Venda' : random.sample(range(0,(self.quantidade*2)),self.quantidade),
            'Valor_Imovel' : [random.randint(150000, 350000) for loop in range(self.quantidade)],

            'Comissao_Venda' : [random.randint(1, 6) /100 for loop in range(self.quantidade)],
            'Data_Venda' : [np.random.choice(['Casa Residencial', 'Apartamento'], p =[0.25, 0.75]
            ) for loop in range(self.quantidade)],
        }

        Base = pd.DataFrame(dicionario)
        return Base
    
    def gerar_dados_b(self):

        dicionario = {
            'Id_Venda' : random.sample(range(0,(self.quantidade*2)), self.quantidade),
            'Vendedor' : [np.random.choice(['Gabriel Sousa', 'Nicole Gomes']) for loop in range(self.quantidade)]
        }

        Base = pd.DataFrame(dicionario)
        return Base
    
Base_A = GeradorDados(500).gerar_dados_a()
Base_B = GeradorDados(500).gerar_dados_b()
Base_Dados = pd.merge(Base_A, Base_B, how='inner', on='Id_Venda')
"""print(Base_Dados.shape)
print(Base_Dados.head())"""

#Vamos incluir 2 registros nulos na base de dados
Base_Dados.iloc[0:2,1] = np.nan

#Analisando
"""print(Base_Dados.head())"""

#Classe para calcular a média de uma coluna e comparar com ela mesma

class Calculo:

    #Metodo construtor
    def __init__(self, df, nome_coluna):
        self.df = df
        self.nome_coluna = str(nome_coluna)
        self.df[self.nome_coluna] = self.preencher_nulos_com_media()
        self.media = self.calculo_media()

    #Função para calcular a média da coluna
    def calculo_media(self):
        return self.df[self.nome_coluna].mean()
    
    #Preencher com a média
    def preencher_nulos_com_media(self):
        media = self.df[self.nome_coluna].mean()
        return self.df[self.nome_coluna].fillna(media)
    
    #Funçção para comparar a média com os registros
    def comparar_media(self, valor):
        if valor > self.media:
            return "acima da média"
        elif valor < self.media:
            return "abaixo da média"
        else:
            return "igual à média"
        
    #Função para retornar o df
    def resultado(self):
        return self.df[self.nome_coluna].apply(self.comparar_media)
    
Base_Dados['Classe'] = Calculo(Base_Dados, 'Valor_Imovel').resultado()

print(Base_Dados.head())