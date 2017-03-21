#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Implementação do algoritmo
#de Naïve Bayes
#
#bayes.py
#como usar: >>python3.2 <programa>.py <arquivo>
#
# Arquivos necessários: conectores.txt, separadores.txt, index.txt
#
####################################

#### procedimentos ####
#le arquivo completo
def read_arq(arquivo,ext):
	conteudo =""
	lista= []
	arq = open('./'+arquivo+ext , 'rt',encoding='utf-8')
	conteudo = arq.readline()
	while conteudo != '':
		if(conteudo[-1] =='\n'):
			conteudo = conteudo[:-1] 
		lista.append(conteudo)
		conteudo = arq.readline()
	arq.close()
	return lista

def write_arq(arquivo,string):
	arq = open("./"+arquivo,'a+')
	print("Escrevendo arquivo.")
	arq.write(string+"\n")
	arq.close()
	print("salvo com sucesso")

#separa o texto em palavras
def separaPalavras(p_frase):
	#--strings
	texto = p_frase

	#--contadores
	i = 0
	j = 0

	#--estruturais
	palavras  = [""]

	#--constantes
	separadores= read_arq("separadores",".txt")
	conectores = read_arq("conectores",".txt")
	maiusculo = ["A","B","C","D","E","F","G","H","I","J","L","M","N","O","P","Q","R","S","T","U","V","X","Y","Z"]

	#separa o texto em palavras
	while i < len(texto):
		if (not (texto[i] in separadores)):
			palavras[j] = palavras[j]+ texto[i]
		else:
			#se for separador, verifico o anterior
			if ( not (texto[i-1] in separadores)):
				#se o ant nao for separador verifico se é conector
				if((texto[i-1] in maiusculo) and (texto[i] in conectores)):
					palavras[j] = palavras[j]+ texto[i]				
				else:	
					palavras = palavras + [""]
					j = j+1
		i=i+1
	
	#verifica se o ultimo valor e vazio
	if (palavras[len(palavras)-1] == ""):
		del palavras[len(palavras)-1]
		j = j -1

	return palavras

#conta palavras	
def frequencia(p_frase,p_palavras):
	#varivaies
	texto = p_frase
	palavras = [""]
	palavras2 = p_palavras  #["",0]
	i = 0
	j = 0
	l = 0
	x = 0
	ctr = 0
	#separa em palavras
	palavras = separaPalavras(texto)
	j = len(palavras)-1

	#conta palavras
	if(len(palavras2) == 0):
		palavras2 = [["(total)",j+1],[palavras[0],1]] #recebea primeira palavra do texto
		i = 1
		x = 2	
	else:	
		palavras2[0][1] += j+1
		i = 0
		x = len(palavras2)
	ctr = 0
	while i<=j: 
		l = 1
		while l<x:
			#verifica se a palavra ja existe
			if (palavras[i] == palavras2[l][0]): 
				palavras2[l][1] = palavras2[l][1] + 1 	#soma +1 na palavra
				l = x 	#quebra o laço
				ctr = 0 
			else:
				ctr = 1 #ativa o controle
			l= l+1

		#adiciona palavra na lista
		if (ctr == 1):
			palavras2 = palavras2 + [[palavras[i],1]]
			x = x+1
			ctr = 0
		i = i+1
		
	#verifica se o ultimo valor e vazio
	if (palavras2[len(palavras2)-1] == ""):
		del palavras2[len(palavras2)-1]
		i = i-1
	return palavras2

#retorna a frequencia de palavras no texto solicitado
def freqNoTexto(p_palavra,p_lista):
	#Declaro e inicializo variaveis
	lista = [] #["palavra",freq] --> ["ab",0]
	palavra = ""
	freq = 0
	i = 0
	tam = 0
	
	#atualizo variaveis
	palavra = p_palavra
	lista = p_lista
	tam = len(lista)
	
	#procuro a palavra na lista
	while i<tam:
		if (palavra in lista[i]):
			freq = lista[i][1]
			i = tam
		i+=1
	#retorno a frequencia
	return freq

#le arquivo e gera tabela de frequencia
def read_arq_arg(arquivo):
	conteudo =""
	palavras=[]#[["(total)",freqTotal],["palavra",frequencia]] --> primeiro elemento é a freq total
	arq = open('./'+arquivo, 'rt',encoding="utf-8")
	conteudo = arq.readline()
	while conteudo != '':
		if(conteudo[-1] =='\n'):
			conteudo = conteudo[:-1] 
		palavras = frequencia(conteudo,palavras)
		conteudo = arq.readline()
	arq.close()
	return palavras

#calcula total de palavras em todos os textos
def calculaTotalPal(p_tabela):
	#variaveis
	total = 0
	tam = 0
	i = 0
	tabela = p_tabela
	tam = len(tabela)
	
	#percorro a tabela e calculo
	while(i<tam):
		total += tabela[i][1][0][1] #[[classe,[['(max)',freqmax],["p1",f1]]]]
		i+=1
		
	return total

#calcula quantidade de palavras por classe
def calculaPalClasse(p_tabela,p_dicClasses):
	#variaveis
	tam = 0
	i = 0
	classes = p_dicClasses #{classe:[quant,prob]}
	tabela = p_tabela
	
	#atualização de variaveis
	tam = len(tabela)
	
	while(i<tam):
		classes[tabela[i][0]][0] +=tabela[i][1][0][1]
		i+=1
	return classes

#Naïve Bayes --> calcula probabilidade de ser da classe (melhora no aumento da qt de textos)
def calculaProb(p_analisado,p_base,p_totalPal,p_totalPalClasse):
	#variaveis 
	a_palavras = [] #palavras
	c_palavras = [] #palavras
	totalClasse = {} #{classe:[quant,prob,classe]}
	classe = ""
	totalPal = 0
	freq = 0
	i = 0
	tam = 0
	prob = 1.0 # 1 nao interfere no valor total
	freqTexto = 0
	
	#atualização de variaveis
	a_palavras = p_analisado #[["palavra",freq]]
	c_palavras = p_base[1] #p_base-> [classe,[palavras]]
	classe = p_base[0]
	totalClasse = p_totalPalClasse
	totalPal = p_totalPal + totalClasse[classe][0]
	tam = len(a_palavras)
	
	while(i < tam):
		#calcula probabilidade individual e multiplica com as anteriores	
		prob = prob * (freqNoTexto(a_palavras[i][0],c_palavras) + a_palavras[i][1]) / totalPal
		i+=1
	
	totalClasse[classe][1] *= prob
	
	return totalClasse

#Calcula Prob Geral
def calculaProbGeral(p_analisado,p_tabela,p_dicClasses):
	#variaveis
	tabela=[] #[[classe,[["palavra1",freq1],["p2",f2]]]]
	analisado = []#[["palavra1",freq1],["p2",f2]]
	dicClasses = {} #{classe:[quant,prob,classe]}
	i = 0
	tam = 0
	totalPal = 0
	
	#atualização de variaveis
	tabela = p_tabela
	analisado = p_analisado
	dicClasses = calculaPalClasse(tabela,p_dicClasses)
	totalPal = calculaTotalPal(tabela)
	tam = len(tabela)
	
	#calcula a probabilidade baseado no texto tabela[i]
	while(i<tam):
		dicClasses = calculaProb(analisado,tabela[i],totalPal,dicClasses)
		i+=1
		
	return dicClasses

#imprime classes
def imprimeClasses(p_dicClasses):
	#variveis
	dicClasses = {} #{classe:[quant,prob,classe]}
	maior = 0.0
	chaveMaior = ""
	
	#atualizacao de variaveis
	dicClasses = p_dicClasses
	chaves = dicClasses.keys()
	tam = len(chaves)
	for chave in dicClasses:
		print("Probabilidade da classe "+chave+" : ",end="")
		print(dicClasses[chave][1])
		if(maior <= dicClasses[chave][1]):
			maior  = dicClasses[chave][1]
			chaveMaior = chave
	print("Portanto Pertence a classe: "+chave)
	return chave

#programa principal	
def main():
	#controle de tempo
	import time
	ini = time.time()
	#variaveis
	i = 0
	tabela=[] #[[classe,[["palavra1",freq1],["p2",f2]]]]
	analisado = []#[["palavra1",freq1],["p2",f2]]
	dicClasses = {} #{classe:[quant,prob]}
	
	#inicializações
	import sys
	argumento = sys.argv[1:]	
	analisado = read_arq_arg(argumento[0])

	#carrego os arquivos a serem analizados para memoria
	conteudo =""
	arq = open('./index.txt', 'rt',encoding="utf-8")
	conteudo = arq.readline()
	while conteudo != '':
		if(conteudo[-1] =='\n'):
			conteudo = conteudo[:-1] 
		dicClasses[conteudo[0]] = [0,1.0] #adiciono a classe no dicionario
		tabela.append([conteudo[0]]) #classe
		tabela[i].append(read_arq_arg(conteudo[1:]))# lista de palavras
		conteudo = arq.readline()
		i+=1
	arq.close()
	
	dicClasses = calculaProbGeral(analisado,tabela,dicClasses)
	
	classe = imprimeClasses(dicClasses)
	
	write_arq("index.txt",classe+""+argumento[0]) #escreve a classe no arquivo index
	fim = time.time()
	print("Tempo de execução: ",end="")
	print(fim-ini)
	
main()
