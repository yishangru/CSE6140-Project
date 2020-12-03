'''
Executable: python Code/BnB_group_25.py -inst Data/karate.graph -alg BnB -time 600 -seed 100 
'''
import networkx as nx
import operator
import argparse
import time
import os

def create_graph(adj_list):
	G = nx.Graph()
	for i in range(len(adj_list)):
		for j in adj_list[i]:
			G.add_edge(i + 1, j)
	return G

def parse(datafile):
	adj_list = []
	with open(datafile) as f:
		num_vertices, num_edges, weighted = map(int, f.readline().split())
		for i in range(num_vertices):
			adj_list.append(map(int, f.readline().split()))
	return adj_list

def BnB(G, T):
	#RECORD START TIME
	start_time=time.time()
	end_time=start_time
	delta_time=end_time-start_time
	times=[]
	OptVC = []
	CurVC = []
	Frontier = []
	neighbor = []
	UpperBound = G.number_of_nodes()
	print('Initial UpperBound:', UpperBound)

	CurG = G.copy()
	v = find_maxdeg(CurG)
	Frontier.append((v[0], 0, (-1, -1)))
	Frontier.append((v[0], 1, (-1, -1)))

	while Frontier!=[] and delta_time<T:
		(vi,state,parent)=Frontier.pop()
		backtrack = False
		if state == 0:
			neighbor = CurG.neighbors(vi)
			for node in list(neighbor):
				CurVC.append((node, 1))
				CurG.remove_node(node)
		elif state == 1:
			CurG.remove_node(vi)
		else:
			pass

		CurVC.append((vi, state))
		CurVC_size = VC_Size(CurVC)
		if CurG.number_of_edges() == 0:
			if CurVC_size < UpperBound:
				OptVC = CurVC.copy()
				print('Current Opt VC size', CurVC_size)
				UpperBound = CurVC_size
				times.append((CurVC_size,time.time()-start_time))
			backtrack = True
				
		else:
			CurLB = Lowerbound(CurG) + CurVC_size
			if CurLB < UpperBound:
				vj = find_maxdeg(CurG)
				Frontier.append((vj[0], 0, (vi, state)))
				Frontier.append((vj[0], 1, (vi, state)))
			else:
				backtrack=True


		if backtrack==True:
			if Frontier != []:
				nextnode_parent = Frontier[-1][2]
				if nextnode_parent in CurVC:
					
					id = CurVC.index(nextnode_parent) + 1
					while id < len(CurVC):
						mynode, mystate = CurVC.pop()
						CurG.add_node(mynode)
						curVC_nodes = list(map(lambda t:t[0], CurVC))
						for nd in G.neighbors(mynode):
							if (nd in CurG.nodes()) and (nd not in curVC_nodes):
								CurG.add_edge(nd, mynode)

				elif nextnode_parent == (-1, -1):
					CurVC.clear()
					CurG = G.copy()
				else:
					print('error in backtracking step')

		end_time=time.time()
		delta_time=end_time-start_time
		if delta_time>T:
			print('Cutoff time reached')

	return OptVC,times

#TO FIND THE VERTEX WITH MAXIMUM DEGREE IN REMAINING GRAPH
def find_maxdeg(g):
    deglist_sorted=sorted(g.degree,key = lambda x:x[1],reverse=True)
    v = deglist_sorted[0]
    return v

def Lowerbound(graph):
	lb=graph.number_of_edges() / find_maxdeg(graph)[1]
	lb=cl(lb)
	return lb


def cl(d):
    """
        return the minimum integer that is bigger than d
    """ 
    if d > int(d):
        return int(d) + 1
    else:
        return int(d)
    

def VC_Size(VC):
	# VC is a tuple list, where each tuple = (node_ID, state, (node_ID, state)) vc_size is the number of nodes which has state == 1

	vc_size = 0
	for element in VC:
		vc_size = vc_size + element[1]
	return vc_size


def main(inputfile, output_dir, cutoff, randSeed):
	adj_list = parse(inputfile)	
	g = create_graph(adj_list)

	print('No of nodes in G:', g.number_of_nodes(),
		  '\nNo of Edges in G:', g.number_of_edges())

	Sol_VC,times = BnB(g, cutoff)
	for element in Sol_VC:
		if element[1]==0:
			Sol_VC.remove(element)
	inputdir, inputfile = os.path.split(args.inst)

	with open('.\Output\\' + inputfile.split('.')[0] + '_BnB_'+str(cutoff)+'.sol', 'w') as f:
	    f.write('%i\n' % (len(Sol_VC)))
	    f.write(','.join([str(x[0]) for x in Sol_VC]))

	with open('.\Output\\' + inputfile.split('.')[0] + '_BnB_'+str(cutoff)+'.trace', 'w') as f:
	    for t in times:
	        f.write('%.2f,%i\n' % ((t[1]),t[0]))

if __name__ == '__main__':
	parser=argparse.ArgumentParser(description='Input parser for BnB')
	parser.add_argument('-inst',action='store',type=str,required=True,help='Put Data File here')
	parser.add_argument('-alg',action='store',default=1000,type=str,required=True,help='Name of algorithm')
	parser.add_argument('-time',action='store',default=1000,type=int,required=True,help='Time limit reaches')
	parser.add_argument('-seed',action='store',default=1000,type=int,required=False,help='Select Random Seed')
	args=parser.parse_args()

	algorithm = args.alg
	graph_file = args.inst
	output_dir = 'Output/'
	cutoff = args.time
	randSeed = args.seed
	main(graph_file, output_dir, cutoff, randSeed)