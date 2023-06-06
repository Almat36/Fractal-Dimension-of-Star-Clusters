import networkx as nx
import numpy as np
import random


def generate_random_3Dgraph(data, n_nodes, radius, seed=None):

    if seed is not None:
        random.seed(seed)
    x=data[:,0]
    y=data[:,1]
    z=data[:,2]
    
    # Generate a dict of positions
    pos = {i: (x[i],y[i], z[i]) for i in range(n_nodes)}
    
    # Create random 3D network
    G = nx.random_geometric_graph(n_nodes, radius, pos=pos)
    for i in G.edges():

        G[i[0]][i[1]]['weight'] =np.sqrt((x[i[0]]-x[i[1]])**2+(y[i[0]]-y[i[1]])**2+(z[i[0]]-z[i[1]])**2)

    return G


dat = np.genfromtxt("filename", usecols=(0,1,2))
x=dat[:,0]
y=dat[:,1]
z=dat[:,2]

n = len(dat)

data=np.zeros((len(x), 3))
data[:,0]=x
data[:,1]=y
data[:,2]=z

G = generate_random_3Dgraph(data,n,radius=1000000000000000000, seed=None)
T = nx.minimum_spanning_tree(G) 

nx.write_gml(T, "filename",stringizer=str)
# nx.draw(T)

