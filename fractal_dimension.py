import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import random
import networkx as nx
import network as nk
import membINF as membINF
import membRENYI


#Box Covering algorithm №1
def memb(network, rb, boxing=False):
        # "How to calculate the fractal dimension of a complex network: the box covering algorithm"
        # by Chaoming Song et al

        graph = network.graph
        if rb == 0:
            boxes = [[node] for node in graph.nodes()]
#         elif lb == network.diameter         CHANGED FROM LB TO RB
#             boxes = [list(graph.nodes())]
        else:
            if not network.distance_dict:
                # print('computing shortest path data')
                network.get_dist_dict()
                
            distances = network.distance_dict # {node:{distance:set_of_nodes}}
            
            if not network.shortest_paths:
                # print('computing shortest path data')
                network.shortest_paths = dict(nx.all_pairs_shortest_path_length(graph)) 
            
            distance_dictionary = network.shortest_paths # {node1:{node2:dist12}}

            # (i) Initially,  all  the  nodes  are  marked  as  uncovered  and  non-centers
            uncovered = set(graph.nodes())
            non_center = set(graph.nodes())

            centers = set()
            unc_or_non_center = set(graph.nodes())
            c_dist = {}  # "central distance"
            c_id = {}  # box id's

            # first part
            # (iv) Repeat  steps  (ii)  and  (iii)  until  all  nodes  are  either  covered  or  centers.
            
            while unc_or_non_center: # 'and' would be better, wouldn't it? :)
                # if there were no ambiguity in unc_..., this could cause problems
                # but we are saved due to the fact that centers are covered too, opposed to the paper
                
                excluded_mass = {}  # dictionary of nodes excluded mass
                max_excluded_mass = 0
                p_node = 0
                
                # (ii) For all non-center nodes (including the already covered nodes) calculate the excluded mass,
                #      and select the node p with the maximum excluded mass as the next center.
                
                for node in non_center:
                    
                    # For a given radus rb, we define the excluded mass of a node as the number of uncovered nodes
                    # within a chemical distance less than rB
                    
                    excluded_mass[node] = len(network.ball_of_seed(node, rb).intersection(uncovered)) # ball contains node too
                    
                    if excluded_mass[node] > max_excluded_mass:
                        max_excluded_mass = excluded_mass[node]
                        p_node = node

                centers.add(p_node)
                # print("c",centers)
                non_center -= {p_node}
                uncovered -= network.ball_of_seed(p_node, rb)
                # print(uncovered)
                unc_or_non_center = uncovered.intersection(non_center) # ambiguity, every center is covered -> this is uncovered
                c_dist[p_node] = 0
                c_id[p_node] = p_node
                
# After everyone is covered, we sort non-center nodes to some approporiate center            
            
    # find the nearest-center distance
    
            for non_center_node in non_center:
                radius = 1
                while non_center_node not in c_dist:
                    if distances[non_center_node][radius].intersection(centers): #there is a center in radius distance 
                        c_dist[non_center_node] = radius
                    radius += 1
                    
            sorted_non_center = sorted(list(non_center), key=lambda x: c_dist[x]) 
            
    # in every iteration, one node is sorted to a center
    
            for node in sorted_non_center:
            
                neighbours = list(graph.neighbors(node)) # centers are included too
                random.shuffle(neighbours)
                
                for neigh in neighbours:
                    if c_dist[neigh] < c_dist[node]: # equivalent to c_dist[neigh]==c_dist[node]-1
                        
    # as we iterate over sorted_non_center, neigh is sorted to a center if this point is reached
    
                        c_id[node] = c_id[neigh]
                        break
             
            boxes = list(network.invert_dict_list(c_id).values()) # yields list of values of {c_id:list_of_nodes}
            
        # RN=[]
        # Links=[]
        # Edges= graph.edges()
        # for i in Edges:
        #     for j in boxes:
        #         if i[0] in j and i[1] not in j:
        #             RN.append(i[0])
        #             RN.append(i[1])
        #             Links.append(i)
                
               
        # RN1 = list(set(RN))

        # print(Edges)
        
            

        if boxing:
            return len(boxes)
        else:
            return boxes


#Box Covering algorithm №2
def CIE(network, g, rb):
        
    unburned = set(network.graph.nodes())
    
              
    if rb == 0:
            boxes = [[node] for node in network.graph.nodes()]
    else:    
                boxes = []
                    
            # if network.distance_dict==None:
            #     print('computation of shortest path data')
            #     network.get_dist_dict()
    
        
                  
                sp=dict(nx.shortest_path_length(g, weight='length'))
                
                # print('sp=',sp)
                #print(len(sp))
                b={i: sp[(i)][max(sp[(i)], key=sp[(i)].get)] for i in range(0,len(sp))}
                # print('b=',b)
                
                x1=[]    
                for i in range(0,len(b),1):
                    x1.append(float(b[(i)]))
                x1=np.array(x1)
                # print('x1=',x1)
                n=0
                
                y1=max(x1)
                # print('y1=',y1)
                j=np.where(x1>=max(x1-rb))
    
                while unburned:
                    
                    j=np.where(x1>=max(x1-rb))
                    # print('j=',j)
                    x3=x1[j]
                    # print('x3=',x3)
                    jj=np.argmin(x3)
                    # print('jj=',jj)
                    jjj=j[0][jj]
                    # print('jjj=',jjj)
                    
                    
                    
                    
                    
                    x2=np.array(list(b))
                    
                        
     
                    seed = int(x2[jjj])   
                    # print(seed)
                    
                    box = list(network.ball_of_seed(seed, rb).intersection(unburned))
        
                    if box:
                        boxes.append(box)
                        unburned -= set(box)
                    #x2=np.delete(x2, boxes[n])
                        x1[boxes[n]]=0
                        n+=1
    return len(boxes)

#Cutting data within Jcobi Radius
def cutJR(filename, JR, JRn, plotC=False):
    Data = np.genfromtxt(filename+".den", usecols=(1,2,3))
    
    d0=[0,0,0]
    t = KDTree(Data)
    k = t.query_ball_point(d0, JR*JRn)
    XYZ = Data[k]

    # np.savetxt(f"{filename}_{JRn}xJR.txt",XYZ)
    if plotC==True:
        plt.figure()
        plt.plot(Data[:,0],Data[:,1],"o")
        plt.plot(XYZ[:,0],XYZ[:,1], "ro")
    return XYZ
    
 
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

#Minimum Spanning Tree algorithm
def MST(filename, JR, JRn, plotC=False,  plotG=False):
    XYZ=cutJR(filename, JR, JRn, plotC)
    print(f"Generating MST of {filename}")
    x=XYZ[:,0]
    y=XYZ[:,1]
    z=XYZ[:,2]
    
    n = len(XYZ)
    
    data=np.zeros((len(x), 3))
    data[:,0]=x
    data[:,1]=y
    data[:,2]=z
    
    G = generate_random_3Dgraph(data,n,radius=1000000000000000000, seed=None)
    T = nx.minimum_spanning_tree(G) 
    
    # nx.write_gml(T, f"{filename}_{JRn}xJR.gml",stringizer=str)    
    if plotG==True:
        plt.figure()
        nx.draw(T)
    return T


def fractal_dimension(filename, JR, JRn, plotD=False, plotC=False,  plotG=False ):    
    G = MST(filename, JR, JRn, plotC,  plotG)
    print(f"Calculating D of {filename}")
    N=[len(G)]
    G = nk.network(G)
        
    r=[0.0000001]
    i=1 
    
    while N[-1]>3:
        print(N[-1])
        N.append(memb.memb(G,i, boxing=True))
        r.append(i) 
        i+=5
    
    N=N[1:]
    r=r[1:]
    
    lb=2*np.array(r)+1
    rb=np.log(lb)
    Nb=np.log(N)
    p=np.polyfit(rb, Nb, 1)
    a=np.polyval(p, rb)
    if plotD==True:    
        plt.figure()
        plt.plot(rb, Nb, "o")
        plt.plot(rb,a, "r--")
        plt.xlabel("log(r)")
        plt.ylabel("log(N)")
        plt.title(f"{filename} { JRn} Jacobi Radius")


    return p[0]


def information_dimension(filename, JR, JRn, plotI=False, plotC=False,  plotG=False):
 
    G = MST(filename, JR, JRn, plotC,  plotG)
    print(f"Calculating I of {filename}")
    N=[len(G)]
    G = nk.network(G)
        
    r=[0.0000001]
    i=1 
    ID=[]
    while N[-1]>3:
        I, Nj=membINF.information_dimension(G,i, N[0], boxing=False)
        print(N[-1])
        N.append(Nj)
        ID.append(I)
        r.append(i) 
        i+=5
    
    N=N[1:]
    r=r[1:]
    
    lb=2*np.array(r)+1
    rb=np.log(lb)
    Nb=ID
    p=np.polyfit(rb, Nb, 1)
    a=np.polyval(p, rb)
    if plotI==True:    
        plt.figure()
        plt.plot(rb, Nb, "o")
        plt.plot(rb,a, "r--")
        plt.xlabel("log(r)")
        plt.ylabel("I")
        plt.title(f"{filename} { JRn} Jacobi Radius")


    return p[0]


def renyi_dimension(alpha,filename, JR, JRn, plotI=False, plotC=False,  plotG=False):
    
    G = MST(filename, JR, JRn, plotC,  plotG)
    print(f"Calculating RD of {filename}")
    N=[len(G)]
    G = nk.network(G)
        
    r=[0.0000001]
    i=1 
    ID=[]
    while N[-1]>3:
        I, Nj=membRENYI.renyi_dimension(alpha, G,i, N[0], boxing=False)
        print(N[-1])
        N.append(Nj)
        ID.append(I)
        r.append(i) 
        i+=5
    
    N=N[1:]
    r=r[1:]
    
    lb=2*np.array(r)+1
    rb=np.log(lb)
    Nb=ID
    p=np.polyfit(rb, Nb, 1)
    a=np.polyval(p, rb)
    if plotI==True:    
        plt.figure()
        plt.plot(rb, Nb, "o")
        plt.plot(rb,a, "r--")
        plt.xlabel("log(r)")
        plt.ylabel("I")
        plt.title(f"{filename} { JRn} Jacobi Radius")


    return p[0]


def fractal_dimension_CIE(filename, JR, JRn, plotD=False, plotC=False,  plotG=False ):    
    G = MST(filename, JR, JRn, plotC,  plotG)
    print(f"Calculating D of {filename}")
    N=[len(G)]
    G1 = nk.network(G)
        
    r=[0.0000001]
    i=1 
    
    while N[-1]>3:
        print(N[-1])
        N.append(CIE.CIE(G1,G,i))
        r.append(i) 
        i+=5
    
    N=N[1:]
    r=r[1:]
    
    lb=2*np.array(r)+1
    rb=np.log(lb)
    Nb=np.log(N)
    p=np.polyfit(rb, Nb, 1)
    a=np.polyval(p, rb)
    if plotD==True:    
        plt.figure()
        plt.plot(rb, Nb, "o")
        plt.plot(rb,a, "r--")
        plt.xlabel("log(r)")
        plt.ylabel("log(N)")
        plt.title(f"{filename} { JRn} Jacobi Radius")


    return p[0]


#Fractal Dimension for weighted networks
def WFD(filename, JR, JRn, plotW=False, plotC=False,  plotG=False):
    G = MST(filename, JR, JRn, plotC,  plotG)
    print(f"Calculating RD of {filename}")
    D = WFDim.WFD(G, plotW )      
    
    return D     


