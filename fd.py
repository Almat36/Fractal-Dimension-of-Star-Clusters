import fractal_dimension as fd
import numpy as np
import matplotlib.pyplot as plt

SFE =["0.15"]
# SFE =["0.15", "0.17", "0.20", "0.25"]
# T = ["000285", "000855", "001014" , "001033", "001053", "001072", "001091",  "001110", "001129", "001148" ]
T = ["001072"]
JRn = 1

DD=[]
for j in SFE: 
    D = []
    for i in T:
        filename = f"./{j}/{i}"
        r = np.genfromtxt(f"./{j}/def-dc {j}.dat", usecols=(8))    
        JR = r[int(i)]
        R = fd.cutJR(filename,JR,JRn,plotC=False)
        D.append(fd.fractal_dimension(filename, JR, JRn, plotD=True, plotC=False, plotG=False))
    DD.append(D)

print(DD)
# t =[1000,1500,2000,2500]

# plt.figure()
# plt.plot(t ,np.abs(DD[0]), "o-" , label='SFE 0.15')
# plt.plot(t, np.abs(DD[1]), "r^-", label='SFE 0.17')
# plt.plot(t, np.abs(DD[2]), "x-", label='SFE 0.20')
# plt.plot(t, np.abs(DD), "g*-", label='SFE 0.25')

# plt.xlabel("$Time (Myr)$")
# plt.ylabel("$Fractal dimension$")
# plt.legend()
# plt.xticks(t)
# plt.title(f"{JRn} Jacobi Radius")
# plt.savefig(f"{JRn} JR.png")


