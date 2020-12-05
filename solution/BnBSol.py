import time
from solution.solution import Solution
import networkx as nx
import operator

class BnBSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        # Initialize 
        G = self.graph

	    print('Initial Global Upper Bound:', G.number_of_nodes())
	    leftG = G.copy() #frist with entire graph

        optVC = []
        CurVC = []
        Frontier = []
        expand = []
        v = maxDeg(leftG)

        Frontier.append((v[0], 0, (-1, -1)))
        Frontier.append((v[0], 1, (-1, -1)))

        bk = False
        while Frontier!=[] and timeBlock<T:
            bk = False
            (vi, state, src) = Frontier.pop()
            if state == 1:
                leftG.remove_node(vi)
            elif state == 0:
                expand = leftG.neighbors(vi)
                for node in list(expand):
                    leftG.remove_node(node)
                    CurVC.append((node, 1))
                    
            else:
                pass

            CurVC.append((vi, state))
            curSize = VCsize(CurVC)

            if leftG.number_of_edges() == 0:
                if VCsize(CurVC) < UpperBound:
                    optVC = CurVC.copy()
                    UpperBound = VCsize(CurVC)
                    print('Current Opt VC size', curSize)
                    times.append((curSize,time.time()-start))
                bk = True
                    
            else:
                if Lowerbound(leftG) + curSize < UpperBound:
                    vii = maxDeg(leftG)
                    Frontier.append((vii[0], 0, (vi, state)))
                    Frontier.append((vii[0], 1, (vi, state)))
                else:
                    bk=True

            if bk==True:
                if Frontier != []:
                    nodeParent = Frontier[-1][2]
                    if nodeParent in CurVC:
                        id = CurVC.index(nodeParent) + 1
                        while id < len(CurVC):
                            nodei, statei = CurVC.pop()
                            curNodes = list(map(lambda t:t[0], CurVC))
                            leftG.add_node(nodei)
                            for ndi in G.neighbors(nodei):
                                if (ndi in leftG.nodes()) and (ndi not in curNodes):
                                    leftG.add_edge(ndi, nodei)

                    elif nodeParent == (-1, -1):
                        leftG = G.copy()
                        CurVC.clear()
                    else:
                        print('Backtracking Error')
        #return opt
        ################################################
        self.updateVertexSet(optVC)
        self.updateTrace(len(optVC))
        #time.sleep(1)
    
    def Lowerbound(graph):
	    lb=graph.number_of_edges() / maxDdeg(graph)[1]
	    if(lb> int(lb)):
		    return int(lb)+1
	    else:
		    return int(lb)	    

    def VCsize(vc):
        size = 0
	    for element in VC:
            size = size + element[1]
	    return size

    def maxDeg(g):#Sort the vertices with max degree in desc order
         deglist_sorted=sorted(g.degree,key = lambda x:x[1],reverse=True)
         v = deglist_sorted[0]
         return v   
