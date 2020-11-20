import networkx as nx
import time
import sys
from data import checkData, readData, checkSol, writeSol, writeTrace


def Approximation(file_name):
  G = nx.MultiGraph()
  f = open('%s'%file_name,'r')
  content = f.readlines()
  num_vertices = int(content[0].split(" ")[0])

  for i in range (1, num_vertices+1):
    G.add_node(i, visited = False)
    edges = [int(item) for item in content[i].strip().split(" ")]
    for e in edges:
      G.add_edge(i,e)

  #Max Degree Greedy Algorithm 
  #Fran¸cois Delbot and Christian Laforest. Analytical and experimental comparison of six algorithms for the
  #vertex cover problem. Journal of Experimental Algorithmics (JEA), 15:1–4, 2010.
  start = time.time()
  vc = []
  degree_list = nx.degree(G)
  sorted_degree_list = sorted(degree_list, key=lambda x: x[1])
  max_idx = len(sorted_degree_list) - 1
  while(G.edges):
    max_degree_node = sorted_degree_list[max_idx][0]
    G.remove_node(max_degree_node)
    vc.append(max_degree_node)
    max_idx -= 1
  

  elapsed = str(time.time() - start)
  print(elapsed)
  print(len(vc))
  return vc


Approximation('data/Data/dummy1.graph')