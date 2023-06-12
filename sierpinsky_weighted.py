import numpy as np
from PIL import Image
import math
import networkx as nx
def plot_line(from_coordinates, to_coordinates, thickness, colour, pixels):

    # Figure out the boundaries of our pixel array
    max_x_coordinate = len(pixels[0])
    max_y_coordinate = len(pixels)

    # The distances along the x and y axis between the 2 points
    horizontal_distance = to_coordinates[1] - from_coordinates[1]
    vertical_distance = to_coordinates[0] - from_coordinates[0]

    # The total distance between the two points
    distance =  math.sqrt((to_coordinates[1] - from_coordinates[1])**2 \
                + (to_coordinates[0] - from_coordinates[0])**2)

    # How far we will step forwards each time we colour in a new pixel
    horizontal_step = horizontal_distance/distance
    vertical_step = vertical_distance/distance

    # At this point, we enter the loop to draw the line in our pixel array
    # Each iteration of the loop will add a new point along our line
    for i in range(round(distance)):
        
        # These 2 coordinates are the ones at the center of our line
        current_x_coordinate = round(from_coordinates[1] + (horizontal_step*i))
        current_y_coordinate = round(from_coordinates[0] + (vertical_step*i))

        # Once we have the coordinates of our point, 
        # we draw around the coordinates of size 'thickness'
        for x in range (-thickness, thickness):
            for y in range (-thickness, thickness):
                x_value = current_x_coordinate + x
                y_value = current_y_coordinate + y

                if (x_value > 0 and x_value < max_x_coordinate and \
                    y_value > 0 and y_value < max_y_coordinate):
                    pixels[y_value][x_value] = colour



def draw_triangle(center, side_length, degrees_rotate, thickness, colour, \
                  pixels, shrink_side_by, iteration, max_depth, old_center, G, pos):
    
    # The height of an equilateral triangle is, h = ½(√3a) 
    # where 'a' is the side length
    triangle_height = side_length * math.sqrt(3)/2

    # The top corner
    top = [center[0] - 2/3*triangle_height, center[1]]
    # print(top)

    # Bottom left corner
    bottom_left = [center[0] + 1/3*triangle_height, center[1] - side_length/2]

    # Bottom right corner
    bottom_right = [center[0] + 1/3*triangle_height, center[1] + side_length/2]


    # Coordinates between each edge of the triangle
    

    

    
    line_number = 0
    lines = [[top, bottom_left],[bottom_right,top],[bottom_left, bottom_right],[center, top],\
               [center, top],[center, bottom_left],[center, bottom_right], \
                [[500,500], top],[[500,500], bottom_left],[[500,500],bottom_right],
                [old_center, top],  [old_center, bottom_left],[old_center, bottom_right]]
    
    # lineso = []
    # for lineo in lineso:
    #         plot_line(lineo[0], lineo[1], thickness, colour, pixels)
    
    for line in lines:
        line_number += 1
        plot_line(line[0], line[1], thickness, colour, pixels)
        # print(line[0][0])
        G.add_edge(str(line[1]), str(line[0]))
        pos[str(line[1])]=(line[1][0],line[1][1])
        pos[str(line[0])]=(line[0][0],line[0][1])
        
    
    # # if iteration>0:
       
        

            
    # centers=([top, bottom_left, bottom_right, center])

    # Draw a line between each corner to complete the triangle
    
    # for cen in centers:
        

            # plot_line([line[0][0]/3,line[0][1]/3], line[1], thickness, colour, pixels)
    
        # If we haven't reached max_depth, draw some new triangles
        if (iteration < max_depth and (iteration < 1 or line_number < 5)):
           

            new_side_length = side_length*shrink_side_by



            new_center = line[0]
            old_center=center
            new_rotation = degrees_rotate



            draw_triangle(new_center, new_side_length, new_rotation, \
                          thickness, colour, pixels, shrink_side_by, \
                          iteration+1, max_depth, old_center, G, pos)
    return G, pos

# # Define the size of our image
pixels = np.zeros( (1000,1000,3), dtype=np.uint8 )    
    


# draw_triangle(center, side_length, degrees_rotate, thickness, colour, \
#                   pixels, shrink_side_by, iteration, max_depth):

G=nx.Graph() 
pos=dict()   

draw_triangle([500,500], 600, 0, 1, [250,200,0], pixels, 1/3, 0, 2, [500,500], G, pos)

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
    print(j)
    pos0[k]=pos[j]
    k+=1
    


x=0
nx.set_node_attributes(G, x, "x")
y=0
nx.set_node_attributes(G, y, "y")

for ix in range(0,len(H)):
    H.nodes[ix]["x"]=pos0[ix][0]
    H.nodes[ix]["y"]=pos0[ix][1]



nx.draw_networkx(H, pos0, with_labels=True)
    
    
nx.write_gml(H, "serp.gml")    
    
    
# nx.draw_networkx(G, pos, with_labels=True)

# # Turn our pixel array into a real picture
img = Image.fromarray(pixels)

# # Show our picture, and save it
img.show()
# img.save('Line.png')

