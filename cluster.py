import random
from collections import defaultdict
import numpy as np

# CLUSTERIZADOR NÃO SUPERVISIONADO - CLOPE

# classes e funções da clusterização com CLOPE

class Cluster:

    def __init__(self):
        # Largura do histograma (em termos de número de elementos)
        self.width = 0.0
        # Número de transações
        self.ntrans = 0
        # Histograma
        self.histogram = {}
        # self.trans_id = []

    '''
    Adicione uma transação ao cluster. Iterar sobre todos os elementos do histograma, completar o histograma
     parâmetros de entrada:
     transação -- fatia com objetos (transação)
    '''
    def add_transaction(self, transaction):
        # Iterar por todos os elementos do histograma um por um e adicionar à coluna correspondente do histograma. 
        # Se não há elemento em questão, então adicione uma nova coluna ao histograma
        for item in transaction:
            if not (item in self.histogram):
                self.histogram[item] = 1 # adiciona novo elemento ao histograma
            else:
                self.histogram[item] += 1 # incrementa o numero do elemento existente no histograma
        # Calcular a largura do histograma (o número de objetos diferentes)
        self.width = float(len(self.histogram))
        # incrementa o número de transações no cluster
        # self.trans_id.append(id)
        # self.ntrans = len(self.trans_id)
        self.ntrans+=1

    '''
    Excluir transação do cluster. Passamos por todos os elementos do histograma, removemos todos os elementos da transação de
     histogramas
    
     parâmetros de entrada:
     transação -- fatia com objetos (transação)
     valores retornados:
     valor gradiente G (transação) # sem sentido 
    
     Dentro da classe, não há rastreamento de quais transações são adicionadas, quais são excluídas, portanto, se em
     o processo de modificação excluirá uma transação que não foi adicionada ao cluster correspondente, o algoritmo
     vai dar resultado errado    
     '''
    
    def remove_transaction(self, transaction):
        
        for item in transaction:
            if self.histogram[item] > 0: # new
                self.histogram[item] -= 1 # new
            if self.histogram[item] == 0:
                # print("deletando item",item,"do histograma ao tira a transação",transaction)
                del self.histogram[item]
        # Calcular a largura do histograma (o número de objetos diferentes)        
        self.width = float(len(self.histogram))
        self.ntrans -= 1
        # print("id2rem",id,"lst of ids",self.trans_id)
        # self.trans_id.remove(id)


###################### teste somente com a classe cluster

transactions = [
    ["apple", "banana", "milk"],
    ["apple", "milk", "banana"],
    ["banana", "milk", "beer"],
    ["apple", "banana", "milk"],
    ["milk", "bread", "rice"],
    ["apple", "bread", "milk"],
    ["milk", "bread", "rice"],
    ["apple", "bread", "milk"],
    ["banana", "bread", "bread"],
    ["chocolate", "milk", "apple"],
    ["banana", "honey", "milk"],
    ["rice", "bread", "milk"],
    ["cheese", "apple", "crackers"],
    ["yogurt", "banana", "granola"],
    ["juice", "bread", "apple"],
    ["beer", "chips", "salsa"],
    ["pasta", "tomato", "basil"],
    ["milk", "cookie", "chocolate"],
    ["fish", "chips", "lemon"],
    ["beef", "carrot", "potato"],
    ["lettuce", "tomato", "cucumber"],
    ["orange", "apple", "banana"],
    ["water", "lime", "mint"],
    ["tea", "honey", "lemon"],
    ["egg", "bacon", "toast"],
    ["rice", "bean", "corn"],
    ["peanut butter", "jelly", "bread"],
    ["chicken", "rice", "broccoli"],
    ["salmon", "asparagus", "lemon"],
    ["milk", "banana", "peanut butter"]
]




