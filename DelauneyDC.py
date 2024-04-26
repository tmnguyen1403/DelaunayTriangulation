#Divide and conquer
from QuadEdge import QuadEdge
from AlgebraUtils import *
class DelaunayDC:
    def __init__(self):
        self.edge_store = []
        self.sorted_s = None

    @staticmethod
    def prepare_data(S):
        if len(S) < 2:
            return S
        #1. Sort by x
        #2. Sort by y
        sorted_y = sorted(S, key = lambda s: s.y)
        sorted_xy = sorted(sorted_y, key = lambda s: s.x)
        
        #3. Remove duplicate points
        i = 0
        while i < len(sorted_xy)-1:
            if sorted_xy[i].equal(sorted_xy[i+1]):
                #delete i+1
                sorted_xy.pop(i+1)
            else:
                i = i +1
        # for site in sorted_xy:
        #     site.debug()
        return sorted_xy
    
    def start_solve(self, S):
        print("preparing data")
        sorted_s = DelaunayDC.prepare_data(S)
        self.sorted_s = sorted_s
        print(f"finish preparing data - length: {len(self.sorted_s)}")
        return self.solve(sorted_s)
    
    def solve(self, S):
        length_S = len(S)
        if length_S == 2:
            s1,s2 = S[0],S[1]
            a = QuadEdge.Make_Edge(s1,s2)
            self.edge_store.append(a)
            #How do we return two edges if we only make one quad edge?
            # Which one is edge, which one is quad edge? Are they all edges only, or they are all quad edge
            return (a,a.Sym())
        elif length_S == 3:
            s1,s2,s3 = S[0],S[1],S[2]
            # Create edges a connecting s1 to s2 
            # and b connecting s2 to s3
            a = QuadEdge.Make_Edge(s1,s2)
            b = QuadEdge.Make_Edge(s2,s3)
            self.edge_store.append(a)
            self.edge_store.append(b)
            #print("\nsplice(a.Sym(),b)")
            QuadEdge.Splice(a.Sym(),b)
            #Close the triangle
            if ccw(s1,s2,s3):
                #print("\nccw(s1,s2,s3)")
                #print("connect(b,a)")
                c = QuadEdge.Connect(b,a)
                self.edge_store.append(c)
                return (a,b.Sym())
            elif ccw(s1,s3,s2):
                #print("\nccw(s1,s3,s2)")
                #print("connect(b,a)")
                c = QuadEdge.Connect(b,a)
                self.edge_store.append(c)
                return (c.Sym(),c)
            else:
                #print("the three points are collinear")
                return (a,b.Sym())
        elif length_S >= 4:
            L,R = S[:length_S//2],S[length_S//2:]
            ldo,ldi = self.solve(L)
            rdi,rdo = self.solve(R)
            #Compute the lower common tangent of L and R
            max_loop = 10
            counter = 0
            while rdi != None and ldi != None:
                print(f"lr loop: {counter}")
                counter += 1
                # print(f"ldi:")
                # ldi.Org().debug()
                # ldi.Dest().debug()

                # print(f"rdi:") 
                # rdi.Org().debug()
                # rdi.Dest().debug()

                if left_of(rdi.Org(),ldi):
                    ldi = ldi.Lnext()
                elif right_of(ldi.Org(),rdi):
                    rdi = rdi.Rprev()
                else:
                   # print("Finish compute the lower common tangent of L and R")
                    break
                # counter += 1
                # if counter > max_loop:
                #     print("Stuck in the loop")
                #     return None
            #Create a first cross edge basel from rdi.Org to ldi.Org
            basel = QuadEdge.Connect(rdi.Sym(),ldi)
            # print("cross edge I:")
            # basel.Org().debug()
            # basel.Dest().debug()
            self.edge_store.append(basel)
            if ldi.Org() == ldo.Org():
                ldo = basel.Sym()
            if rdi.Org() == rdo.Org():
                rdo = basel
            #Merge loop
            counter = 0
            while True:
                print(f"basel loop: {counter}")
                counter += 1
                #Locate the first L point (lcand.Dest) to be encoutered by the rising bubble
                #and delete Ledges out of basel.Dest that fail the circle test
                lcand = basel.Sym().Onext()
                lcand_valid = valid(lcand,basel)
                if lcand_valid:
                    while in_circle(basel.Dest(), basel.Org(), lcand.Dest(), lcand.Onext().Dest()):
                        t = lcand.Onext()
                        QuadEdge.DeleteEdge(lcand)
                        lcand = t
                #End if
                #Symmetrically locate the first R point to be hit, and delete R edges
                rcand = basel.Oprev()
                rcand_valid = valid(rcand, basel)
                if rcand_valid:
                    while in_circle(basel.Dest(), basel.Org(), rcand.Dest(), rcand.Oprev().Dest()):
                        t = rcand.Oprev()
                        QuadEdge.DeleteEdge(rcand)
                        rcand = t
                #End if
                #If both lcand and rcand are invalid, then basel is the upper common tangent
                lcand_valid = valid(lcand,basel)
                rcand_valid = valid(rcand, basel)
                if not lcand_valid and not rcand_valid:
                    #print("Both lcand and rcand are invalid")
                    break
                #if both are valid, then choose the approriate one using the incircle test
                #print(f"lcand_valid: {lcand_valid}")
                #print(f"rcand_valid: {rcand_valid}")

                if not lcand_valid or (rcand_valid and in_circle(lcand.Dest(), lcand.Org(), rcand.Org(), rcand.Dest())):
                    #print("add cross edge basel from rcand.Dest to basel.Dest")
                    basel = QuadEdge.Connect(rcand, basel.Sym())
                    #print("cross edge II:")
                    # basel.Org().debug()
                    # basel.Dest().debug()
                    self.edge_store.append(basel)
                else:
                    #print("add cross edge basel from basel.Org to lcand.Dest")
                    basel = QuadEdge.Connect(basel.Sym(), lcand.Sym())
                    #print("cross edge III:")
                    # basel.Org().debug()
                    # basel.Dest().debug()
                    self.edge_store.append(basel)
                #end if
            #End loop
            return (ldo, rdo)
        #End delaunay_dc 