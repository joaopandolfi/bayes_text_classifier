# Classificador de textos
Classficador de textos Bayseano

## Funcionamento
 >Classifica o exto inserido de acordo com a base de dados atual
 >Classes definidas previamente

## Características
Algoritmo de aprendizado não supervisionado

 >Implementado em Python 3.X


## Utilização
```
python3 bayes.py <novo_arquivo_de_entrada>

Exemplo:

python3 bayes.py novo_texto.txt
```

## Arquivos necessários para funcionamento
 >conectores.txt

Elementos conectores entre palavras

 >separadores.txt

Elementos separadores de palavras

 >index.txt

Arquivo de index das classes
```
<classe> <arquivo>
Exemplo:
1 sportv.txt
1 sportnews.txt
2 rural.txt
3 leucemia.txt
2 mandioca.txt
3 celulas_tronco.txt
```
