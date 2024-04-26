#Divide and conquer
from QuadEdge import QuadEdge
from AlgebraUtils import *
class DelaunayDC:
    def __init__(self):
        self.edge_key = set()
        self.edge_store = set()
        self.sorted_s = None
        self.enable_save_edge = False

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
    
    def store_edge(self,edge):
        key1 = (edge.Org().getXY(),edge.Dest().getXY())
        key2 = (key1[1],key1[0])

        if key1 not in self.edge_key and key2 not in self.edge_key:
            self.edge_store.add(edge)
            self.edge_key.add(key1)

    def start_solve(self, S):
        print("preparing data")
        sorted_s = DelaunayDC.prepare_data(S)
        self.sorted_s = sorted_s
        self.edge_store = set()
        print(f"finish preparing data - length: {len(self.sorted_s)}")
        return self.solve(sorted_s)
    
    def solve(self, S):
        length_S = len(S)
        if length_S == 2:
            s1,s2 = S[0],S[1]
            a = QuadEdge.Make_Edge(s1,s2)
            return (a,a.Sym())
        elif length_S == 3:
            s1,s2,s3 = S[0],S[1],S[2]
            # Create edges a connecting s1 to s2 
            # and b connecting s2 to s3
            a = QuadEdge.Make_Edge(s1,s2)
            b = QuadEdge.Make_Edge(s2,s3)
            QuadEdge.Splice(a.Sym(),b)
            #Close the triangle
            if ccw(s1,s2,s3):
                c = QuadEdge.Connect(b,a)
                if self.enable_save_edge:
                    self.store_edge(a)
                    self.store_edge(b)
                    self.store_edge(c)
                return (a,b.Sym())
            elif ccw(s1,s3,s2):
                c = QuadEdge.Connect(b,a)
                if self.enable_save_edge:
                    self.store_edge(a)
                    self.store_edge(b)
                    self.store_edge(c)
                return (c.Sym(),c)
            else:
                #print("the three points are collinear")
                return (a,b.Sym())
        elif length_S >= 4:
            L,R = S[:length_S//2],S[length_S//2:]
            ldo,ldi = self.solve(L)
            rdi,rdo = self.solve(R)
            #Compute the lower common tangent of L and R
            while rdi != None and ldi != None:
                if left_of(rdi.Org(),ldi):
                    ldi = ldi.Lnext()
                elif right_of(ldi.Org(),rdi):
                    rdi = rdi.Rprev()
                else:
                    break
               
            #Create a first cross edge basel from rdi.Org to ldi.Org
            basel = QuadEdge.Connect(rdi.Sym(),ldi)
            if self.enable_save_edge:
                self.store_edge(rdi.Sym())
                self.store_edge(ldi)
                self.store_edge(basel)
            if ldi.Org() == ldo.Org():
                ldo = basel.Sym()
            if rdi.Org() == rdo.Org():
                rdo = basel
            #Merge loop
            while True:
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

                if not lcand_valid or (rcand_valid and in_circle(lcand.Dest(), lcand.Org(), rcand.Org(), rcand.Dest())):
                    #print("add cross edge basel from rcand.Dest to basel.Dest")
                    baselSym = basel.Sym()
                    basel = QuadEdge.Connect(rcand,baselSym)
                    if self.enable_save_edge:
                        self.store_edge(basel)
                        self.store_edge(rcand)
                        self.store_edge(baselSym)   
                else:
                    #print("add cross edge basel from basel.Org to lcand.Dest")
                    baselSym = basel.Sym()
                    lcandSym = lcand.Sym()
                    basel = QuadEdge.Connect(baselSym, lcandSym)
                    if self.enable_save_edge:
                        self.store_edge(basel)
                        self.store_edge(lcandSym)
                        self.store_edge(baselSym)
                #end if
            #End loop
            return (ldo, rdo)
        #End delaunay_dc 