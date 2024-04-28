import numpy as np

def det2(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return x1*y2 - x2*y1

def det3(p1,p2,p3):
    x1,y1,z1 = p1
    x2,y2,z2 = p2
    x3,y3,z3 = p3
    det = x1*det2((y2,z2),(y3,z3)) - y1*det2((x2,z2),(x3,z3)) + z1*det2((x2,y2),(x3,y3))
    #print(f"det3: {det}")
    return det

def det4(p1,p2,p3,p4):
    x1,y1,z1,h1 = p1
    x2,y2,z2,h2 = p2
    x3,y3,z3,h3 = p3
    x4,y4,z4,h4 = p4
    detN = x1*det3((y2,z2,h2),(y3,z3,h3),(y4,z4,h4)) - y1*det3((x2,z2,h2),(x3,z3,h3),(x4,z4,h4))
    detM = z1*det3((x2,y2,h2),(x3,y3,h3),(x4,y4,h4)) - h1*det3((x2,y2,z2),(x3,y3,z3),(x4,y4,z4))
    return detN + detM

def left_of(X,e):
    return ccw(X,e.Org(),e.Dest())

def right_of(X,e):
    return ccw(X,e.Dest(),e.Org())

def valid(e, basel):
    return right_of(e.Dest(),basel)

def ccw(s1,s2,s3):
    #Calculate normaly
    xa,ya = s1.x,s1.y
    xb,yb = s2.x,s2.y
    xc,yc = s3.x,s3.y
    detT = det3((xa,ya,1),(xb,yb,1),(xc,yc,1)) 
    #detN = xa*(yb-yc) - ya*(xb-xc) + (xb*yc-xc*yb)
    #print(f"detT: {detT}")
    #print(f"detT: {detN}")

    #TODO: remove after done
    # calculate with numpy
    #matrix = np.array([[xa,ya,1],[xb,yb,1],[xc,yc,1]])
    #detM = np.linalg.det(matrix)
    # print(f"detN: {detN}")
    # print(f"detM: {detM}")
    #assert(round(detM) == round(detN))

    return detT > 0

def create_4D(s):
    x,y = s.x,s.y
    return [x,y,x*x+y*y,1]

def in_circle(s1,s2,s3,s4,debug=False):
    p1 = create_4D(s1)
    p2 = create_4D(s2)
    p3 = create_4D(s3)
    p4 = create_4D(s4)
    #detN = det4(p1,p2,p3,p4)

    #TODO: remove after done
    # calculate with numpy
    matrix = np.array([p1,p2,p3,p4])
    detM = np.linalg.det(matrix)
    #print(f"detN4: {detN}")
    #print(f"detM4: {detM}")
    #assert(round(detN,0) == round(detM,0))
    # if debug:
    #     with open("debug_in_circle1.txt","a") as f:
    #         f.write(f"{p1};{p2};{p3};{p4};{detN};{detM}\n")
    return detM > 0

def site_on_edge(s,e):
    a = ccw(s,e.Org(),e.Dest())
    b = ccw(s,e.Dest(),e.Org())
    return not a and not b

# Close to 0 case
#[-440.53, -978.69, 1151900.797, 1];[-432.78, -781.5, 798040.7784, 1];[-432.78, -781.5, 798040.7784, 1];[-440.53, -978.69, 1151900.797, 1];1.5050377784064035e-05;0.0