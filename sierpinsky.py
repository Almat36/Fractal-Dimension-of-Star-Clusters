
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



# G=nx.balanced_tree(2,2)


# pos=dict()

# for i in range(len(G)):
#     pos[i]=(i,i)

# # pos = {0: (0, 0), 1: (50, 1), 2: (40, -20), 3: (60, -20), 4:(100,0)} 




import turtle
turtle.tracer(100, 0) # Increase the first argument to speed up the drawing.
turtle.setworldcoordinates(0, 0, 700, 700)
turtle.hideturtle()

MIN_SIZE = 100 # Try changing this to decrease/increase the amount of recursion.

def midpoint(startx, starty, endx, endy):
    # Return the x, y coordinate in the middle of the four given parameters.
    xDiff = abs(startx - endx)
    yDiff = abs(starty - endy)
    return (min(startx, endx) + (xDiff / 2.0), min(starty, endy) + (yDiff / 2.0))

def isTooSmall(ax, ay, bx, by, cx, cy):
    # Determine if the triangle is too small to draw.
    width = max(ax, bx, cx) - min(ax, bx, cx)
    height = max(ay, by, cy) - min(ay, by, cy)
    return width < MIN_SIZE or height < MIN_SIZE

def drawTriangle(ax, ay, bx, by, cx, cy, G, pos):
    if isTooSmall(ax, ay, bx, by, cx, cy):
        # BASE CASE
        return
    else:
        # RECURSIVE CASE
        # Draw the triangle.
        turtle.penup()
        turtle.goto(ax, ay)
        turtle.pendown()
        turtle.goto(bx, by)
        turtle.goto(cx, cy)
        turtle.goto(ax, ay)
        turtle.penup()

        # Calculate midpoints between points A, B, and C.
        mid_ab = midpoint(ax, ay, bx, by)
        mid_bc = midpoint(bx, by, cx, cy)
        mid_ca = midpoint(cx, cy, ax, ay)
        
        # mido=(mid_ab+mid_bc+mid_ca)/3
        print(ax)
        
        
        G.add_edge((ax,ay), (mid_ab))
        G.add_edge((ax,ay), (mid_ca))
        G.add_edge((mid_ab), (mid_ca))
        pos[(ax,ay)]=(ax,ay)
        pos[(mid_ab)]=(mid_ab)
        pos[(mid_ca)]=(mid_ca)
        
        G.add_edge((mid_ab), (bx, by))
        G.add_edge((bx, by), (mid_bc))
        G.add_edge((mid_ab), (mid_bc))
        pos[(bx,by)]=(bx,by)
        pos[(mid_bc)]=(mid_bc)
        
        G.add_edge((mid_ca), (mid_bc))
        G.add_edge((mid_bc), (cx,cy))
        G.add_edge((mid_ca), (cx,cy))
        
        pos[(mid_ca)]=(mid_ca)
        pos[(cx,cy)]=(cx,cy)

        # Draw the three inner triangles.
        # print(ax, ay, mid_ab[0], mid_ab[1], mid_ca[0], mid_ca[1])
        drawTriangle(ax, ay, mid_ab[0], mid_ab[1], mid_ca[0], mid_ca[1], G, pos)
        drawTriangle(mid_ab[0], mid_ab[1], bx, by, mid_bc[0], mid_bc[1], G, pos)
        drawTriangle(mid_ca[0], mid_ca[1], mid_bc[0], mid_bc[1], cx, cy, G, pos)
        return G, pos
G=nx.Graph() 
pos=dict()
# Draw an equilateral Sierpinski triangle.
G,pos=drawTriangle(0, 0, 300, 600, 600, 0, G, pos)

# Draw a skewed Sierpinski triangle.
#drawTriangle(30, 250, 680, 600, 500, 80)

Edges=G.edges()
Dist=[]

for j in Edges:
    # print(j[0], j[1])
    dist=np.sqrt((pos[j[0]][0]-pos[j[1]][0])**2+(pos[j[0]][1]-pos[j[1]][1])**2)
    Dist.append(round(dist,2))
    
    
k=0
for j in Edges:
    G.add_edge(j[0], j[1], weight=Dist[k])
    k=k+1
    

    
# nx.draw_networkx(G, pos=pos, with_labels=True)

mapping = {}
Nodes=G.nodes()
k=0
for j in Nodes:
    mapping[j]=k
    k=k+1





H=nx.Graph() 



H = nx.relabel_nodes(G, mapping)
k=0
pos0=dict()
for j in pos:
    pos0[k]=j
    k+=1
    


x=0
nx.set_node_attributes(G, x, "x")
y=0
nx.set_node_attributes(G, y, "y")

for ix in range(0,len(H)):
    H.nodes[ix]["x"]=pos0[ix][0]
    H.nodes[ix]["y"]=pos0[ix][1]



nx.draw_networkx(H,pos0, with_labels=True)

nx.write_gml(H, "test.gml")

turtle.exitonclick()