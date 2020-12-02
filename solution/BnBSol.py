import time
from solution.solution import Solution
import networkx as nx
import operator

""" 
Steps:
1. choose node vi by the rank of degrees, append (vi,state=1) and (vi,state=0) to candiate list
2. If state=1, remove the node from the original graph. If state=0, remove from original graph, and add all neighbors into list.
3. Check the original graph. 
-If there's no egdes left in the original graph: 
    - if current VC is less than the optimal VC, make it to new optimal.
    - else #backtrack
-If there are edges left:
    - If lowerbound if greater than upperbound, pruning from the original graph, #backtrack. 
    - If lowerbound<upperbound, append next max degree node.
4. BackTracking
"""

class BnBSol(Solution):
    def __init__(self, graph, randomSeed, startTime, parameterDict):
        super().__init__(graph, randomSeed, startTime)
        self.parameterDict = parameterDict

    # override parent method
    def run(self):
        # Initialize 
        g = self.graph
        optVC=[] #optimal vertex cover to return
        curVC=[] #current VC found
        lists = []#set of candidate for subProblem
        neighbor =[]
        backtracking = False
        #set the upperbound first
        upperBound = g.number_of_nodes()
        print('Initial UpperBound',upperBound)

        curG = g.copy() #initial CurG  before any removement
        v = findMaxDegree(curG)

        #add initial values to the stack
        #tuples of node,state,(parent vertex,parent vertex state)
        # State: 0 is not in the VC, 1 is in the VC
        lists.append((v[0],0,(-1,-1)))
        lists.append((v[0],0,(-1,-1)))
        #print(lists)

        #dfs
        while lists !=[]:
            (vi,state,parent)=lists.pop()
            print("in dfs ==0 ")
            if state == 0:  # if vi is not selected, state of all neighbors=1
                neighbor = curG.neighbors(vi)  # store all neighbors of vi
                for node in lists(neighbor):
                    curVC.append((node, 1))
                    curG.remomve_node(node)
            elif state==1:
                CurG.remomve_node(vi)
            else:
                pass
            
            
            curVC.append((vi, state))
            curVC_size = VC_Size(curVC)

            #check solutions:
            if curG.number_of_edges() == 0:  # end of exploring, solution found
                if curVC_size < upperBound:
                    optVC = curVC.copy()
                    #print('Curr Vertex Cover Size', curVC_size)
                    upperBound = curVC_size
                backtracking=True
                
            else:
                    curLB = Lowerbound(curG) + curVC_size
                    if curLB < upperBound:  # worth exploring
                        vj = find_maxdeg(curG)
                        lists.append((vj[0], 0, (vi, state)))#(vi,state) is parent of vj
                        lists.append((vj[0], 1, (vi, state)))
                    else:
                        #backtrack
                        backtracking=True

            if backtracking==True:
            	if lists != []:	#otherwise no more candidates to process
                    nextnode_parent = lists[-1][2]	#parent of last element in Frontier (tuple of (vertex,state))
                    if nextnode_parent in curVC:
                        id = curVC.index(nextnode_parent) + 1
                        while id < len(curVC):	#undo changes from end of CurVC back up to parent node
                            mynode, mystate = curVC.pop()	#undo the addition to CurVC
                            curG.add_node(mynode)	#undo the deletion from CurG
                            
                            # find all the edges connected to vi in Graph G
                            # or the edges that connected to the nodes that not in current VC set.
                            
                            curVC_nodes = list(map(lambda t:t[0], curVC))
                            for nd in g.neighbors(mynode):
                                if (nd in curG.nodes()) and (nd not in curVC_nodes):
                                    curG.add_edge(nd, mynode)	#this adds edges of vi back to CurG that were possibly deleted

                    elif nextnode_parent == (-1, -1):
                        # backtrack to the root node
                        curVC.clear()
                        curG = g.copy()
                    else:
                        print('error in backtracking step')
        #return opt
        ################################################
        self.updateVertexSet(optVC)
        self.updateTrace(len(optVC))
        #time.sleep(1)
    
    def Lowerbound(graph):
	    return graph.number_of_edges() / find_maxdeg(graph)[1]

    def VC_Size(vc):
        vc_size = 0
        for element in vc:
            vc_size = vc_size + element[1]
        return vc_size

    def findMaxDegree(g):#Sort the vertices with max degree in desc order
        degrees = g.degree()
        sorted = sorted(degrees.items(),reverse=True,key=operator.itemgetter(1))
        v= sorted[0]
        return v
