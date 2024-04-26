import matplotlib.pyplot as plt
import numpy as np

def generate_random_points(num_points, min_xy, max_xy):
    # Generate random x and y coordinates
    x_coords = np.random.uniform(min_xy, max_xy, num_points)
    y_coords = np.random.uniform(min_xy, max_xy, num_points)

    # Combine x and y coordinates to form points
    points = np.column_stack((x_coords, y_coords))
    return points

def read_data_file(file_name):
    data = np.loadtxt(file_name,delimiter=",",dtype=float)
    return data

def save_sites(S,output_file):
    with open(output_file,"w") as f:
        for s in S:
            f.write(f"{s.x},{s.y}\n")
    
def debug_edges(edges):
    for edge in edges:
        edge.debug()

def generate_anotation(sites):
    anotate = {}
    for i,p in enumerate(sites):
        anotate[i+1] = (p.x,p.y)
    return anotate

def draw_edges(edge_store, annotate_data,x_limit=(-4,8),y_limit=(-4,8)):
    for edge in edge_store:
        #print(f"Edge: {edge.Name}")
        Org = edge.Org()
        Dest = edge.Dest()
        org = Org.getXY()
        v = Dest.minus(Org).getXY()
        plt.quiver(*org,*v,scale=1,scale_units='xy', angles='xy', color='b', width=0.005)
    offset_text = (-0.1,0.1) 
    for key,value in annotate_data.items():
        offset_value = (value[0] + offset_text[0],value[1] + offset_text[1])
        plt.text(*offset_value, key, color='r', fontsize=8, ha='center', va='center')

    # Set plot limits
    plt.xlim(*x_limit)
    plt.ylim(*y_limit)

    # Show plot
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()