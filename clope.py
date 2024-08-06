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

class CLOPE:

    def __init__(self, print_step=1000, random_seed=None, repulsion = 2): 
        
        if random_seed is not None:
            self.random_seed = random_seed
        else:
            self.random_seed = random.randint(0, 65536 + 1)
        
        # Lista de clusters
        self.clusters = {}  # CCluster
        # Números de transações
        self.ntrans = 0
        # Número da iteração
        self.iteration = 0
        # inicializa dicionário: número da transação/número do cluster
        self.cluster_of_trans = {}
        # máxinmo número de clusters => o numero de clusters pode ser menor, pq algum cluster pode ter sido deletado e 
        # não reordeno a numeração dos clusters para economia de tempo=> teria que atualizar cluster_of_trans 
        self.K = 0
        # passo para imprimir - debugging 
        self.print_step = print_step
        # parametro de repulsão
        self.repulsion = repulsion

    '''
     Cálculo da função objetivo para 1 clusters 
    '''
    def get_cluster_value(self, k, cluster):
        if cluster.width == 0:
            print("DEBB: found empty clusters >>>>>>>>>>>>>>>>>>>>>>> ",k)
            return 0
        else:
            return float(cluster.ntrans) ** 2 / (cluster.width ** self.repulsion) 
    
    '''
    Cálculo da função objetivo para todos os clusters já formados
     Usado ao modificar clusters ou inicializá-los
     parâmetros de entrada:
     r -- número real denotando repulsão de cluster no sentido de CLOPE
     valor retornado:
     Retorna o valor da função objetivo
    '''
    def get_goal_function(self):
        Profit = 0.0
        # Percorremos todos os clusters e para cada um calculamos seu peso. 
        # Todos os pesos são resumidos em uma métrica comum
        for k in self.clusters:
            Profit += get_cluster_value(self, k, cluster)
        return Profit / float(self.ntrans)


    '''
     A mudança de valor que a função objetivo receberá ao criar um novo cluster k.
    '''
    def get_delta_new(self, transaction):
        
        return 1 / len(transaction) ** self.repulsion
        
    '''
     A mudança de valor que a função objetivo receberá ao adicionar transaction ao cluster k é calculada.
    '''
    def get_delta_add(self, transaction, k):
       
        # copio o histograma dos itens no cluster
        histo = self.clusters[k].histogram.copy()
       
        for item in transaction:
            if not (item in histo): # histogram tem a lista de objetos no cluster
                histo[item] = 1
                
        width = float(len(histo))  # cálculo da largura do cluster

        # self.clusters[k].histogram = histo
        
        return (self.clusters[k].ntrans+1) ** 2 / (width ** self.repulsion) - self.clusters[k].ntrans ** 2 / (self.clusters[k].width ** self.repulsion)

    '''
     A mudança de valor que a função objetivo receberá ao remover transaction do cluster k é calculada.
    '''
    def get_delta_rem(self, transaction, k):
        
        # copio o histograma dos itens no cluster
        histo = self.clusters[k].histogram.copy()
        
        # Removendo itens da transação do histograma
        for item in transaction:
            histo[item] -= 1  # Decrementa a contagem do item no histograma
            if histo[item] == 0:  # Se a contagem do item chegar a zero
                del histo[item]  # Remove o item do histograma
        
        # Calculando a largura do cluster após remover a transação
        width = float(len(histo))  # A largura é o número de itens únicos restantes no histograma

        current_value =   self. get_cluster_value(k, self.clusters[k]) # self.clusters[k].ntrans ** 2 / (self.clusters[k].width ** self.repulsion)
        
        if width > 0:
            return (self.clusters[k].ntrans-1) ** 2 / (width ** self.repulsion) - current_value
        else:
            return -current_value

    # '''
    #  Adicionando de forma forçada uma transação outlier ao cluster menos pior !!!
    # '''
    
    # def Force(self, data, id): #, max_count_clusters=None):

    #     transaction = data[id]
        
    #     max_value = None
    #     max_value_index = None
        
    #     # Estamos procurando um cluster no qual o valor máximo da mudança na função objetivo seja alcançado
    #     for k in self.clusters:
    #         if k != self.cluster_of_trans[id]:
    #             delta = self.get_delta_add(transaction, k)
    #             if max_value is None or delta > max_value:
    #                 max_value_index = k
    #                 max_value = delta

    #     if max_value is not None:
    #         # adiciona a transação ao melhor cluster max_value_index
    #         self.cluster_of_trans[id] = max_value_index
    #         #Adicionando uma transação ao cluster necessário
    #         self.clusters[max_value_index].add_transaction(transaction)
    #     else:
    #         print("DEBB: TRANSACTION",id,"COULD NOT BE FORCED IN ANY EXISTING CLUSTER ... CALL DIEGO!")

    #     return max_value_index


    '''
     Adicionando pela primeira vez uma transação
     Retorna o número do cluster ao qual a transação atual foi adicionada
    '''
    def first_move(self, transaction, id): #, max_count_clusters=None):
        
        max_value = None
        max_value_index = None
        
        # Estamos procurando um cluster no qual o valor máximo da mudança na função objetivo seja alcançado
        for k in self.clusters:
            delta = self.get_delta_add(transaction, k)
            if (delta > 0) and (max_value is None or delta > max_value):
                max_value_index = k
                max_value = delta

        new_value = self.get_delta_new(transaction)

        if (max_value is None) or (new_value > max_value):
            # cria um novo cluster
            self.clusters[self.K] = Cluster()
            max_value_index = self.K
            self.K += 1
        
        # adiciona a transação ao melhor cluster max_value_index
        self.cluster_of_trans[id] = max_value_index
        #Adicionando uma transação ao cluster necessário
        self.clusters[max_value_index].add_transaction(transaction)

        return max_value_index

    '''
     Trnasferindo transações entre clusters ou para cluster novo
     Retorna o número do cluster ao qual a transação atual foi adicionada
    '''
    
    def move_transaction(self, transaction, id, orig_cluster): #, max_count_clusters=None):

        # ponto de partida: a sequencia no seu cluster
        max_value_index = orig_cluster
        max_value = 0 # mover para ele mesmo nem ganha nem perde
        
        # Estamos procurando um cluster no qual o valor máximo da mudança na função objetivo seja alcançado
        delta_rem = self.get_delta_rem(transaction, orig_cluster)
        for k in self.clusters:
            if k != self.cluster_of_trans[id]:
                delta = self.get_delta_add(transaction, k) + delta_rem
                if delta > max_value:
                    max_value_index = k
                    max_value = delta

        # Adicione uma transação a um novo cluster e veja o resultado - registre o cluster com maior valor
        delta_new = self.get_delta_new(transaction) + delta_rem
        
        if delta_new > max_value: 
            self.clusters[self.K] = Cluster() # cria novo cluster
            max_value_index = self.K
            self.K += 1

        if max_value_index != orig_cluster:
            #Removendo uma transação do cluster original
            self.clusters[orig_cluster].remove_transaction(transaction)
            if self.clusters[orig_cluster].ntrans <= 0:
            # deletando cluster",orig_cluster,"por ficar vazio"
                del self.clusters[orig_cluster]
            #Adicionando uma transação ao cluster encontrado
            self.clusters[max_value_index].add_transaction(transaction)
             # Atualizamos o cluster no qual está a transação
            self.cluster_of_trans[id] = max_value_index
        
        return max_value_index
        
    '''
    Inicialização do cluster
    parâmetros de entrada:
    dados -- fatia com transações
    isPrint -- se deve imprimir informações de progresso (0 -- não é necessário, se > 0 -- imprimir a cada isPrint time)
    repulsão -- número real, denotando repulsão de clusters no sentido de CLOPE
    '''
    def init_clusters(self, data): #, max_count_clusters=None):
        
        # keys = sorted(data.keys()) # ordena
        keys = sorted(data.keys()) # pega as chaves
        np.random.seed(self.random_seed)
        np.random.shuffle(keys) # bagunça as chaves
        for item in keys:
            self.first_move(data[item], item)
            if self.print_step > 0 and self.ntrans % self.print_step == 0:
                # print("TRANSAÇÃO", self.ntrans, ". NÚMERO DE CLUSTERS: ", len(self.clusters))
                pass
            self.ntrans += 1
            
        self.iteration = 1

    '''
    Execução do algoritmo. Dando o próximo passo
    parâmetros de entrada:
    dados -- fatia com transações
    isPrint -- se deve imprimir informações de progresso (0 -- não é necessário, se > 0 -- imprimir a cada isPrint time)
    repulsão -- número real, denotando repulsão de clusters no sentido de CLOPE
    parâmetro retornado:
    Retorna o número de operações para transferir uma transação de cluster para cluster
    '''
    def next_step(self, data): #, is_noise_reduction=-1, noise_median_threshold=0.75, max_count_clusters=None):

        # # Remova todos os clusters vazios (ou ruído, se isNoiseReduction > 0)
        # if is_noise_reduction < 0:
        #     is_noise_reduction = self.get_noise_limit(noise_median_threshold)
        # self.noise_reduction(is_noise_reduction)

        nt = 0
        # O número de transações que foram transferidas
        moves = 0
        keys = sorted(data.keys())
        np.random.seed(self.random_seed)
        np.random.shuffle(keys)
        for id in keys: # loop por transações ordenadas de forma aleatória
            # print("id",id,"clusters",self.cluster_of_trans)
            # Nós olhamos onde esta transação está agora
            curr_k = self.cluster_of_trans[id]
            # print("id",id,"current k",curr_k,)
            # print("histo",self.clusters[curr_k].histogram)
            if curr_k in self.clusters:
                new_k = self.move_transaction(data[id], id, curr_k)
            else:
                print("ERROR: TRANSACTION",id,"ASSIGNED TO A CLUSTER",curr_k,"THAT WAS DELETED ...CALL DIEGO!")
            nt += 1
            if self.print_step is not None and self.print_step > 0 and nt % self.print_step == 0:
#                 print("Итерация: ", self.iteration, ". Номер шага", index, ". Число кластеров: ", len(self.clusters))
                # print("ITERAÇÃO: ", self.iteration, ". TRANSAÇÃO:", nt, ". CURR. K:", curr_k,"NEW K:",new_k, "NÚMERO DE CLUSTERS:", len(self.clusters))
                pass

        print(self.cluster_of_trans)
        self.iteration += 1
        
        return moves

    def FindOutliers(self, thres):

        if thres<1:
            nClusters = len(self.clusters)
            unif_cluster_sz =  int(self.ntrans / nClusters)
            sz_thres = int(thres*unif_cluster_sz)
        else:
            sz_thres = thres
            
        print("Disintegrating clusters with less than",sz_thres+1,"transactions")
        SEQS = []    
        if sz_thres >= 1:
            
            for cluster in self.clusters: # pego apens o key do dict clusters <=== aprendi!!
                # Listando os IDs das entradas no cluster k
                ids_in_cluster = [id for id, clust in self.cluster_of_trans.items() if clust == cluster]
                # Contando quantos IDs estão no cluster k
                trans_in_cluster = len(ids_in_cluster)
                if trans_in_cluster <= sz_thres:
                    # print("cluster",cluster,"with", self.clusters[cluster].ntrans,"sequence(s) seems to be an outlier cluster")
                    # print("It contains sequences with ordinal Ids:")
                    seqs = []
                    for id in ids_in_cluster:
                        seqs.append(id)
                    # print(seqs)
                    SEQS += seqs
        return SEQS
        

    def ClusterizeOutliers(self, Data, OutList):

        for id in OutList:
            transaction =  Data[id]
            # ponto de partida: a sequencia no seu cluster
            max_value_index = None
            max_value = 0 # mover para ele mesmo nem ganha nem perde
            
            for k in self.clusters:
                if k != self.cluster_of_trans[id]:
                    delta = self.get_delta_add(transaction, k)
                    if delta > max_value:
                        max_value_index = k
                        max_value = delta
            if max_value_index is not None:
                # adiciona a transação ao melhor cluster max_value_index
                self.cluster_of_trans[id] = max_value_index
                #Adicionando uma transação ao cluster necessário
                self.clusters[max_value_index].add_transaction(transaction)
                print("transaction id",id,"transfered to cluster",max_value_index)
            else:
                print("DEBB: TRANSACTION",id,"COULD NOT BE FORCED IN ANY EXISTING CLUSTER ... CALL DIEGO!")

##     ------------------------            MAIN           -------------------------------------------------
# Example usage
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

Data = {}  # usamos um dicionario para os dados com as features indexadas por posição
trans_len = len(transactions[0])

for trans_nmb in range(0, len(transactions)):
    # inicializa a transação efetiva
    Data[trans_nmb] = [''] * trans_len # cria string vazia do tamanho da transação
    fst = 0  # 
    missing = []
    for index in range(fst, len(transactions[trans_nmb])):
        # adicionando a posição (coluna) da feature se não for missing
        if transactions[trans_nmb][index] != '?':
            Data[trans_nmb][index] = str(index) + ":"+transactions[trans_nmb][index].replace(" ", "")  # add feature position
        else:  # counting missings
            missing.append(index)
        if len(missing) > 0:
            if verbose:
                print("WARNING: there were ", len(missing), " missing features in transaction ", trans_nmb, " at positions:\n", missing)
            pass

for rep in range(100):

    print("REP#",rep+1)
    # criamos um novo clusterizador
    seed = np.random.seed()
    # seed = 456 # during test only
    
    repulsion = 1
    clope = CLOPE(print_step = 1, random_seed=seed, repulsion = repulsion)
    
    # Dados iniciais # Inicializamos o algoritmo
    
    clope.init_clusters(Data)
    # print(transactions,clope.ntrans,clope.cluster_of_trans)
    
    # Iteramos até o metodo de clusterização não supervisionado convergir
    
    ctr = 0
    while clope.next_step(Data) > 0:
        ctr += 1
        print("iteração",ctr+1)
    
    print("clope iterations: ",
          ctr, " number of clusters: ", len(clope.clusters)," max cluster nmb",clope.K)
    
    thres = 0.2
    outliers = clope.FindOutliers(thres)
    print("Outlier sequences have ordinal Ids:",outliers)
    
    if len(outliers)>0:
        print('Reallocation needed')
        clope.ClusterizeOutliers(Data, outliers)    