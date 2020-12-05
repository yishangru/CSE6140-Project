'''
Branch and Bound Algorithms
Implement using DFS and backtracking in networkx
To Run, try: python solution/bnb.py -inst ./data/DATA/<filename> -alg BnB -time 600 -seed 100
'''
import networkx as nx
import operator
import argparse
import time
import os


def parse(datafile):
	adjList = []
	graph = nx.Graph()
	with open(datafile) as f:
		vertices, edges, weighted = map(int, f.readline().split())
		for i in range(vertices):
			adjList.append(map(int, f.readline().split()))
	for i in range(len(adjList)):
		for j in adjList[i]:
			graph.add_edge(i + 1, j)
	return graph

def Lowerbound(graph):
	lb=graph.number_of_edges() / maxDdeg(graph)[1]
	if(lb> int(lb)):
		return int(lb)+1
	else:
		return int(lb)

def maxDeg(g):
    deglist_sorted=sorted(g.degree,key = lambda x:x[1],reverse=True)
    v = deglist_sorted[0]
    return v
    

def VCsize(VC):
	size = 0
	for element in VC:
		size = size + element[1]
	return size

def bnb(G, T):

	start=time.time()
	end=start
	timeBlock=end - start
	times=[]

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

		end=time.time()
		timeBlock=end-start
		if timeBlock>T:
			print('Time reached')

	return optVC,times


def main(inputfile, output_dir, cutoff, randSeed):
	g = parse(inputfile)

	print('Number of Nodes:', g.number_of_nodes(),
		  '\nNumber of Edges', g.number_of_edges())
	OptVC,times = bnb(g, cutoff)

	for element in OptVC:
		if element[1]==0:
			OptVC.remove(element)
			
	indir, infile = os.path.split(args.inst)

	with open('.\result\\' + infile.split('.')[0] + '_bnb_'+str(cutoff)+'.sol', 'w') as f:
	    f.write('%i\n' % (len(OpteVC)))
	    f.write(','.join([str(x[0]) for x in OptVC]))

	with open('.\result\\' + infile.split('.')[0] + '_bnb_'+str(cutoff)+'.trace', 'w') as f:
	    for t in times:
	        f.write('%.2f,%i\n' % ((t[1]),t[0]))

if __name__ == '__main__':
	parser=argparse.ArgumentParser(description='Input parser for BnB')
	parser.add_argument('-inst',action='store',type=str,required=True,help='Put Data File here')
	parser.add_argument('-alg',action='store',default=1000,type=str,required=True,help='Name of algorithm')
	parser.add_argument('-time',action='store',default=1000,type=int,required=True,help='Time limit reaches')
	parser.add_argument('-seed',action='store',default=1000,type=int,required=False,help='Select Random Seed')
	args=parser.parse_args()

	graphFile = args.inst
	algorithm = args.alg
	output_dir = 'result/'
	rSeed = args.seed
	cutoffTime = args.time
	main(graphFile, output_dir, cutoffTime, rSeed)