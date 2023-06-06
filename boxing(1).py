import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import memb
import network as nk

t = ["000057", "000114", "000285", "000570", "000855", "001140"]
D = []
for i in t:
    
    G=nx.read_gml(f"{i}_1xJR.gml")
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
    
    NR=np.zeros((len(N), 2))
    NR[:,0]=N
    NR[:,1]=r
    # np.savetxt(f"{i}_1xJR_1.txt",NR)
    lb=2*np.array(r)+1
    rb=np.log(lb)
    Nb=np.log(N)
    p=np.polyfit(rb, Nb, 1)
    D.append(p[0])
    # a=np.polyval(p, rb)
    
    # plt.plot(rb, Nb, "o")
    # plt.plot(rb,a, "r--")
    # plt.xlabel("log(r)")
    # plt.ylabel("log(N)")
    # plt.title("SFE=0.15  20 Myr 1JR")

