import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import time


def isSuffAndPostf(code, substr):  # substr - для каждого слова word[:i]
    isSuf = False
    isPostf = False

    for word in code:
        if word.startswith(substr, 0, -1) == True:
            isSuf = True
        if word.endswith(substr, 1) == True:
            isPostf = True
    
    if isSuf == True and isPostf == True:
        return True
    else:
        return False
    


def findElementaryDecompositions(target, arr, flag, prefix="", result=[], count=0):
    if not target:
        result.append(prefix)
        if count > 1: 
            flag[0] = True
        return
    for word in arr:
        if target.startswith(word):
            findElementaryDecompositions(target[len(word):], arr, flag, prefix + word, result, count+1)
            







def markov_alg(Code):
    flag = 0
    
    V = Code.replace(',', '').split(' ')
    print(V)


    start_time = time.perf_counter()
    S1 = []
    for code in V:
        n = len(code)
        for i in range(1,n):
            substr = code[:i]   
            if substr not in S1 and isSuffAndPostf(V, substr):
                S1.append(substr)
    end_time = time.perf_counter()
    print(f"S_creation time: {end_time - start_time:.6f} seconds")

                
    Sl = S1 + ['λ']
    S = S1 + ['']
    print("S = {", Sl, "}")

    G = nx.DiGraph()

    for each in Sl:
        G.add_node(each)


    start_time2 = time.perf_counter()
    for word in V:
        for start in S:
            for end in S:
                if start != '' and end != '' and start + end == word:
                    G.add_edge(start, end, name='λ', color='black')
                elif word.startswith(start, 0, len(word)-1) and word.endswith(end, 1):
                    counter = 0
                    nameOfEdge = []
                    flag2 = [False]
                    findElementaryDecompositions(word[len(start):len(word)-len(end)], V, flag2, "", nameOfEdge, counter)
                    if len(nameOfEdge) != 0 and nameOfEdge[0] != '':    
                        if start == end and start != '':
                            G.add_edge(start, end, name = nameOfEdge[0], color='black')
                        elif start == '' and start == end:
                            if flag2[0]:
                                G.add_edge('λ', 'λ', name=nameOfEdge[0], color='black')
                        else:
                            if start == '':
                                G.add_edge('λ', end, name=nameOfEdge[0], color='black')
                            elif end == '':
                                G.add_edge(start, 'λ', name=nameOfEdge[0], color='black')
                            else:
                                G.add_edge(start, end, name=nameOfEdge[0], color='black')
    end_time2 = time.perf_counter()
    print(f"Edge_adding_time: {end_time2 - start_time2:.6f} seconds")                        


    start_time3 = time.perf_counter()            
    cycles = nx.simple_cycles(G)
    end_time3 = time.perf_counter()
    print(f"Cycles_finding_time: {end_time3 - start_time3:.6f} seconds")  
    # print(sorted(nx.simple_cycles(G)))

    cycleThrowLambda = None
    lenmax = 10000

    for cycle in cycles:
        if 'λ' in cycle:
            if len(cycle) < lenmax:
                cycleThrowLambda = cycle
                lenmax = len(cycle)


    start_time4 = time.perf_counter() 
    if cycleThrowLambda != None:
        ind = cycleThrowLambda.index('λ')
        ctlt = deque(cycleThrowLambda)
        ctlt.rotate(len(cycleThrowLambda) - ind)            
        cycleThrowLambda = list(ctlt)
        print("Найден цикл:", cycleThrowLambda)

    
    else: 
        flag = 1
    
    end_time4 = time.perf_counter()
    print(f"Cycle_through_lambda_finding_time: {end_time4 - start_time4:.6f} seconds")




    word = ""
    edge_labels = nx.get_edge_attributes(G, 'name')

    
    if flag == 0:
        n = len(cycleThrowLambda)

        if n != 2:
            word += cycleThrowLambda[0]
            for i in range(0, n-1):
                word += edge_labels[(cycleThrowLambda[i], cycleThrowLambda[i+1])] + cycleThrowLambda[i+1]

            word += edge_labels[(cycleThrowLambda[n-1], cycleThrowLambda[0])]

        else:
            word += cycleThrowLambda[0] + edge_labels[(cycleThrowLambda[0], 
                                                       cycleThrowLambda[1])] + cycleThrowLambda[1] + edge_labels[(cycleThrowLambda[1],
                                                                                                                   cycleThrowLambda[0])]
    word = word.replace('λ', '')
        

    

    
    curveEdges = []
    straightEdges = []

    for u,v in G.edges():
        if (u,v) in G.edges() and (v,u) in G.edges() and edge_labels[(u,v)] != edge_labels[(v,u)]:
            if (u,v) not in curveEdges:
                curveEdges.append((u,v))
            if (v,u) not in curveEdges:
                curveEdges.append((v,u))
        elif (u,v) in G.edges():
            if (u,v) not in straightEdges:
                straightEdges.append((u,v))
        elif (v,u) in G.edges():
            if (v,u) not in straightEdges:
                straightEdges.append((v,u))

            

   
   
   

    if flag == 0:
        edge_colors1 = ['blue' if u in cycleThrowLambda and v in cycleThrowLambda 
                        and u!= v and ((u,v) in curveEdges or (v,u) in curveEdges) 
                        else 'black' for (u, v) in curveEdges]
        edge_colors2 = ['blue' if u in cycleThrowLambda and v in cycleThrowLambda 
                        and u!= v and ((u,v) in straightEdges or (v,u) in straightEdges) 
                        else 'black' for (u, v) in straightEdges]
    else:
        edge_colors1 = ['black' for (u, v) in curveEdges]
        edge_colors2 = ['black' for (u, v) in straightEdges]

    
    return G, flag, Sl, curveEdges, straightEdges, edge_colors1, edge_colors2, edge_labels, word





  

    
        