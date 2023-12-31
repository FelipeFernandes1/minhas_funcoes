# -*- coding: utf-8 -*-
"""Pacote_AED.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YtJz7xYpyzoQX56XTHtetbhwqnGnIYI-
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np
import statsmodels.api as sm

#Função para analisar variáveis qualitativas
def qualitativa(coluna):
  #temas
  minha_paleta = ['royalblue','skyblue','lightsteelblue', 'cornflowerblue']
  sns.set_palette(minha_paleta)

  #Tabela de frequencia
  tabela = coluna.value_counts().reset_index()
  nome_coluna = tabela.columns[1]
  tabela = tabela.rename(columns={nome_coluna: 'frequencia_absoluta'})
  tabela = tabela.rename(columns={'index': nome_coluna})
  tabela['frequencia_relativa'] = tabela['frequencia_absoluta']/tabela['frequencia_absoluta'].sum()
  tabela['frequencia_acumulada'] = tabela['frequencia_relativa'].cumsum()
  variavel = tabela.columns[0]
  print('TABELA DE FREQUÊNCIA')
  print(' ')
  print(tabela.to_string(index=False))
  print(' ')

  #verificando valores nulos/ausentes
  print(f'''CONTAGEM DE VALORES NULOS/AUSENTES
{len(coluna)-coluna.count()}''')
  print(' ')

  if len(coluna.value_counts()) > 3:
    print('GRÁFICO DE BARRAS')
    #Plotando gráficos de barra
    plt.figure(figsize=(5, 3))
    sns.barplot(x=tabela[variavel], y=tabela['frequencia_relativa'], palette=minha_paleta , edgecolor='black')
    plt.xlabel(variavel)
    plt.ylabel('frequencia_relativa')
    plt.tight_layout()
    plt.show()
  else:
    print('GRÁFICO DE PIZZA')
    plt.figure(figsize=(3, 3))
    plt.pie(tabela['frequencia_relativa'], labels=tabela[variavel], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.show()

#Função para analisar variáveis quantitativas
def quantitativa(coluna):
  #temas
  minha_paleta = ['royalblue','skyblue','lightsteelblue', 'cornflowerblue']
  sns.set_palette(minha_paleta)

  #Analisando as medidas estatísticas
  print(f'''MEDIDAS ESTATÍSTICAS

  {coluna.describe()}

CONTAGEM DE VALORES NULOS/AUSENTES
  {len(coluna)-coluna.count()}''')
  print('')

  print('HISTOGRAMA E BOXPLOT')
  # Plotando histograma e boxplot
  num_bins = 1 + int(math.log2(len(coluna))) # Calculando o número de bins usando a regra de Sturges
  fig, axes = plt.subplots(1, 2, figsize=(6, 3))
  sns.histplot(x=coluna, bins=num_bins, kde=False, ax=axes[0])
  axes[0].set_ylabel('Frequência absoluta')
  axes[0].set_xlabel(coluna.name)
  sns.boxplot(y=coluna, ax=axes[1])
  axes[1].set_xlabel(coluna.name)
  axes[1].set_ylabel('')
  plt.tight_layout()
  plt.show()

#Criando a função para calcular o Information Value
def tabela_iv(explicativa, resposta, faixas=0):
    
  #Criando as listas para formar um ranking das variáveis
  global variavel, valor, coeficiente, resultado
  if 'variavel' not in locals() and 'variavel' not in globals():
    variavel = []
  if 'valor' not in locals() and 'valor' not in globals():
    valor = []
  if 'coeficiente' not in locals() and 'coeficiente' not in globals():
    coeficiente = []
  if 'resultado' not in locals() and 'resultado' not in globals():
    resultado = []
    
    #temas
  minha_paleta = ['royalblue','skyblue','lightsteelblue', 'cornflowerblue']
  sns.set_palette(minha_paleta)

  numerica = ''
  if type(explicativa) != str and explicativa.nunique() > 15:
    numerica = 'Sim'
    plt.figure(figsize=(4, 3))
    sns.boxplot(x=resposta, y=explicativa)
    plt.xlabel(resposta.name)
    plt.ylabel(explicativa.name)
    plt.tight_layout()
    plt.show()
    if faixas != 0:
      explicativa = pd.cut(explicativa, bins=faixas)
      explicativa = explicativa.astype(str)
    else:
      faixas = 1 + int(math.log2(len(explicativa)))
      explicativa = pd.cut(explicativa, bins=faixas)
      explicativa = explicativa.astype(str)

  df_iv = pd.crosstab(explicativa, resposta)
  variavel_resposta = resposta.name
  df_iv['Freq_absoluta'] = df_iv[1] + df_iv[0]
  df_iv['Freq_relativa'] = df_iv['Freq_absoluta']/df_iv['Freq_absoluta'].sum()
  df_iv['Valor_Um_relativo'] = (df_iv[1]/df_iv[1].sum())
  df_iv['Valor_Zero_relativo'] = (df_iv[0]/df_iv[0].sum())
  df_iv['Taxa_Valor_Um'] = (df_iv[1]/df_iv['Freq_absoluta'])
  df_iv['Odds'] = df_iv['Valor_Um_relativo']/df_iv['Valor_Zero_relativo']
  df_iv['IV'] = (df_iv['Valor_Um_relativo']-df_iv['Valor_Zero_relativo'])* np.log(df_iv['Odds'])
  df_iv['IV'].replace(np.inf, 0, inplace=True)
  df_iv = df_iv.sort_values(by='Taxa_Valor_Um')
  df_iv = df_iv.drop(columns=['Freq_absoluta','Freq_relativa','Valor_Um_relativo','Valor_Zero_relativo'])
  soma_iv = round(df_iv['IV'].sum(), 2)

  benchmark = ''
  if soma_iv <= 0.02:
     benchmark = 'MUITO FRACO'
  elif soma_iv < 0.1:
    benchmark = 'FRACO'
  elif soma_iv < 0.3:
    benchmark = 'MÉDIO'
  elif soma_iv < 0.5:
    benchmark = 'FORTE'
  else:
    benchmark = 'MUITO FORTE'

  variavel.append(explicativa.name)
  valor.append(benchmark)
  coeficiente.append('IV')
  resultado.append(soma_iv)

  df_iv2 = df_iv.reset_index()

  print(df_iv),print(f'''
O INFORMATION VALUE TOTAL É: {soma_iv}
CLASSIFICADO COMO: {benchmark}''')
  if numerica != 'Sim': 
    #Plotando gráficos de barra
    plt.figure(figsize=(5, 3))
    sns.barplot(x=df_iv2.iloc[:,0].astype(str), y=df_iv2.iloc[:,3], palette=minha_paleta, edgecolor='black')
    plt.xlabel(df_iv2.iloc[:,0].name)
    plt.ylabel('Taxa(valor 1)')
    plt.tight_layout()
    plt.show()
  return df_iv2

#Criando função para calcular o coeficiente de determinação
def r_quadrado(qualitativa, quantitativa):
    
  #Criando as listas para formar um ranking das variáveis
  global variavel, valor, coeficiente, resultado
  if 'variavel' not in locals() and 'variavel' not in globals():
    variavel = []
  if 'valor' not in locals() and 'valor' not in globals():
    valor = []
  if 'coeficiente' not in locals() and 'coeficiente' not in globals():
    coeficiente = []
  if 'resultado' not in locals() and 'resultado' not in globals():
    resultado = []

  #temas
  minha_paleta = ['royalblue','skyblue','lightsteelblue', 'cornflowerblue']
  sns.set_palette(minha_paleta)

  df = pd.get_dummies(qualitativa, drop_first=True)
  variavel_dummie = sm.add_constant(df)
  modelo = sm.OLS(quantitativa, variavel_dummie).fit() #Cria um modelo de regressão linear simples
  r_squared = round(modelo.rsquared, 2) #Extrai o R²

  benchmark = ''
  if r_squared <= 0.25:
     benchmark = 'FRACO'
  elif r_squared < 0.5:
    benchmark = 'MÉDIO'
  elif r_squared < 0.75:
    benchmark = 'FORTE'
  else:
    benchmark = 'MUITO FORTE'

  variavel.append(qualitativa.name)
  valor.append(benchmark)
  coeficiente.append('R²')
  resultado.append(r_squared)

  print(f'''O COEFICIENTE DE DETERMINAÇÃO(R²) É: {r_squared}
CLASSIFICADO COMO: {benchmark}''')
  plt.figure(figsize=(4, 3))
  sns.boxplot(x=qualitativa, y=quantitativa)
  plt.xlabel(qualitativa.name)
  plt.ylabel(quantitativa.name)
  plt.tight_layout()
  plt.show()

#Função para calcular a correlação de Person
def person(explicativa, resposta):

  #Criando as listas para formar um ranking das variáveis
  global variavel, valor, coeficiente, resultado
  if 'variavel' not in locals() and 'variavel' not in globals():
    variavel = []
  if 'valor' not in locals() and 'valor' not in globals():
    valor = []
  if 'coeficiente' not in locals() and 'coeficiente' not in globals():
    coeficiente = []
  if 'resultado' not in locals() and 'resultado' not in globals():
    resultado = []
      
  correlacao = round(explicativa.corr(resposta), 2)

  benchmark = ''
  if correlacao <= -0.7:
     benchmark = 'FORTEMENTE NEGATIVA'
  elif correlacao <= 0.6:
    benchmark = 'FRACA'
  else:
    benchmark = 'FORTEMENTE POSITIVA'

  variavel.append(explicativa.name)
  valor.append(benchmark)
  coeficiente.append('Person')
  resultado.append(correlacao)

  print(f"A CORRELAÇÃO DE PERSON ENTRE {explicativa.name.upper()} E {resposta.name.upper()} É: {correlacao}")
  print(f'CLASSIFICAÇÃO: {benchmark}')
  print('')

  #Plotando o gráfico de dispersão
  plt.figure(figsize=(4, 3))
  sns.scatterplot(x=explicativa, y=resposta)
  plt.xlabel(explicativa.name)
  plt.ylabel(resposta.name)
  plt.show()

#Função para excluir os outliers de uam variável explicativa em realação a uma variável resposta binária
def outliers(explicativa, resposta, dataframe):
  for classe in range(0, 2):
    explicativa_classe = explicativa[resposta == classe]
    Q1 = np.percentile(explicativa_classe, 25)
    Q3 = np.percentile(explicativa_classe, 75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    outliers_indices = np.where((resposta == classe) & ((explicativa < limite_inferior) | (explicativa > limite_superior)))
    dataframe = dataframe.drop(outliers_indices[0])

  dataframe.reset_index(drop=True, inplace=True)
  return dataframe

#Criando o ranking
def ranking():
  global variavel, valor, coeficiente, resultado
  df_ranking = pd.DataFrame({'Variável': variavel,
                             'Valor': valor,
                             'Resultado': resultado,
                             'Coeficiente': coeficiente})
  
  df_ranking = df_ranking.sort_values(by='Resultado', ascending=False)
  return df_ranking
