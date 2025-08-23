import pandas as pd 

# carregar dados da planilha
caminho = 'C:/Users/sabado/Desktop/PYTHON AD WILLIAM MARQUES/01_base_vendas.xlsx'

df1 = pd.read_excel(caminho,sheet_name='Relatório de Vendas')
df2 = pd.read_excel(caminho,sheet_name='Relatório de Vendas1')

#exibir as primeiras linhas das tabelas

print('------ Primeiro Relatório ------')
print(df1.head())

print('------ Segundo Relatório ------')
print(df2.head())

#verificar se ha duplicatas
print('Duplicatas no Relatório 01')
print(df1.duplicated().sum())

print('Duplicatas no Relatório 02')
print(df2.duplicated().sum())

#Vamos consolidar as duas tabelas

print('Dados Consolidados!')
dfconsolidada = pd.concat([df1,df2],ignore_index=True)
print(dfconsolidada.head())

# exibir o numero de clientes por cidade
clientesPorCidade = dfconsolidada.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False)
print('Clientes por Cidade')
print(clientesPorCidade)

# Numero de vendas por plano!

vendasPorPlano = dfconsolidada['Plano Vendido'].value_counts()
print('Numero de vendas por Plano')
print(vendasPorPlano)

#exibir as 3 cidades com mais clientes:
top3Cidades = clientesPorCidade.head(3)
print('Top 3 Cidades')
print(top3Cidades)

# adicionar uma nova coluna de status (exemplo ficticio de analise)
# vamos classificar os planos como premiun se for entreprise, os demais serão 'padrão'

dfconsolidada['Status'] = dfconsolidada['Plano Vendido'].apply(lambda x: 'Premiun' if x == 'Enterprise' else 'Padrão')

#exibir a distribuição dos status
statusDist = dfconsolidada['Status'].value_counts()

print('Distribuição dos status')
print(statusDist)

#Salvar a tabela em um arquivo novo
#Primeiro em Excel
dfconsolidada.to_excel('dados_consolidados.xlsx',index=False)
print('Dados salvos na planilha do Excel')
#Depois em CSV
dfconsolidada.to_csv('dados_consolidados.csv',index=False)
print('Dados salvos em CSV')

#Mensagem final
print('----Programa finalizado!----')
