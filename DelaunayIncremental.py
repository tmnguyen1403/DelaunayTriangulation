#Divide and conquer
from QuadEdge import QuadEdge,EdgeType
from Site import Site
from AlgebraUtils import *
class DelaunayInc:
    def __init__(self):
        self.edge_store = dict()
        self.enable_save_edge = False
        self.min_x = -10001
        self.max_x = 10001
        self.min_y = self.min_x
        self.max_y = self.max_x
        self.dummy_sites = []

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

    def get_store_edges(self):
        return set(self.edge_store.values())
    
    # Dummy triangle is used to 
    def create_dummy_triangle(self):
        self.dummy_sites = [Site(self.min_x,self.min_y),
                            Site(self.min_x,2*self.max_y),
                            Site(2*self.max_x,self.min_y)]
        S = self.dummy_sites
        s1,s2,s3 = S[0],S[1],S[2]
        # Create edges a connecting s1 to s2 
        # and b connecting s2 to s3
        a = QuadEdge.Make_Edge(s1,s2)
        b = QuadEdge.Make_Edge(s2,s3)
        QuadEdge.Splice(a.Sym(),b)
        #Close the triangle
        if ccw(s1,s2,s3) or ccw(s1,s3,s2):
            c = QuadEdge.Connect(b,a)
            self.store_edge(a)
            self.store_edge(b)
            self.store_edge(c)
        else:
            print("the three points are collinear. Not able to work it out")
            print("Error: Cannot create dummy_triangle")

    def edge_filter_dummy(self, edges):
        filter_xy = [s.getXY() for s in self.dummy_sites]
        new_edges = []
        for e in edges:
            start,end = e.get_coor()
            if start not in filter_xy and end not in filter_xy:
                new_edges.append(e)
        return new_edges

    def locate(self,x):
        print("locate debug:")
        print(f"locate edge for: {x.getXY()}")
        chosen_edge = []
        for key,e in self.edge_store.items():
            counter = 0
            print(f"starting edge: {key}")
            seen_edge = set()
            while True:
                #print(f"locate counter: {counter}")
                seen_edge.add(e)
                counter += 1
                eOnext = e.Onext()
                eDprev = e.Dprev()
                # print(f"e: {e.get_coor()}")
                # print(f"eOnext: {eOnext.get_coor()}")
                # print(f"eDprev: {eDprev.get_coor()}")

                if x == e.Org() or x == e.Dest():
                    #print(f"I. chosen edge: {e.get_coor()}")
                    chosen_edge.append(e)
                    break
                    #return e
                elif right_of(x,e):
                    #print(f"1. right of {self.make_key(e)}")
                    e = e.Sym()
                elif left_of(x, eOnext):
                    #print(f"2. not right of {eOnext.get_coor()}")
                    e = eOnext
                elif left_of(x, eDprev):
                    #print(f"3. not right of {eDprev.get_coor()}")
                    e = eDprev
                else:
                    #print(f"II. chosen edge: {e.get_coor()}")
                    chosen_edge.append(e)
                    break
                    #return e
                #avoid stuck in the loop because the point is outside of the triangle
                # is it still work?
                if e in seen_edge:
                    break
        print("Debug chosen edges:")
        # Keep track of largest points beside the dummy 
        #TODO: Improve this to remove the dummy edges
        # Chose the edge that has smallest distance to the point?
        # Test if picking any edges in a face, will it make any difference
        candidate_edges = self.edge_filter_dummy(chosen_edge)
        #candidate_edges = []
        if len(candidate_edges) > 0:
            print("Candidate edges")
            for edge in candidate_edges:
                print(f"{edge.get_coor()}")
            print(f"\nFinal candidate edge: {candidate_edges[0].get_coor()}\n")
            if candidate_edges[0].get_coor() == ((2,2),(4,0)):
                print("Chosen edges")
                for edge in chosen_edge:
                    print(f"{edge.get_coor()}")
                print(f"Final chosen edge: {chosen_edge[0].get_coor()}")
                print(f"\n---Done Chosen Edges---\n")
                #return chosen_edge[0]
                print(f"\nFinal candidate edge: (6,2),(2,2)\n")
                return chosen_edge[0]
            return candidate_edges[0]
        else:
            print("Chosen edges")
            for edge in chosen_edge:
                print(f"{edge.get_coor()}")
            print(f"Final chosen edge: {chosen_edge[0].get_coor()}")
            print(f"\n---Done Chosen Edges---\n")
            return chosen_edge[0]
        
    
    def insert_site(self,x):
        e = self.locate(x)
        if x == e.Org() or x == e.Dest():
            return
        elif site_on_edge(x,e):  #X is on e
            t = e.Oprev()
            print(f"delete edge: {e.get_coord()}")
            QuadEdge.DeleteEdge(e)
            self.remove_edge_from_store(e)
            # Do we perform e.Oprev() before or after the deleteEdge e?
            e = t
        # connect X to vertices around it
        first = e.Org()
        base = QuadEdge.Make_Edge(first,x)

        QuadEdge.Splice(base,e)
        while e.Dest() != first:
            baseSym = base.Sym()
            base = QuadEdge.Connect(e, baseSym)
            self.store_edge(e)
            self.store_edge(baseSym)
            self.store_edge(base)
            e = base.Oprev()
        e = base.Oprev()
        # The suspect edges (from top to bottom) are e(.Onext.Lprev)k for k = 0,1,...
        # The bottom edge has .Org = first.
        while True:
            t = e.Oprev()
            if right_of(t.Dest(),e) and in_circle(e.Org(),t.Dest(),e.Dest(),x):
                #use for update the edge key
                old_key = self.make_key(e)
                self.remove_edge_from_store(e)
                QuadEdge.Swap(e)
                self.store_edge(e)
                #self.store_swap_edge(e,old_key=old_key)
                e = t
            elif e.Org() == first:
                # no more suspect edges
                return
            else:
                e = e.Onext().Lprev()
    
    def make_key(self,edge):
        return (edge.Org().getXY(),edge.Dest().getXY())
    
    def remove_edge_from_store(self,e):
        key = self.make_key(e)
        print(f"Removing edge from store: {e.Name} - {key}")
        e_val = self.edge_store.get(key,None)
        if e_val != None:
            e_key = self.make_key(e_val)
            print(f"Removing edge: {e_val} - {e_key} success")
            self.edge_store.pop(key)
        else:
            print(f"Cannot find {key} to remove edge: {e.Name}")
            key2 = self.make_key(e.Sym())
            print(f"Using e.Sym() - {key2}")
            e_val = self.edge_store.get(key2,None)
            if e_val != None:
                e_key = self.make_key(e_val)
                print(f"Removing edge: {e_val} - {e_key} success")
                self.edge_store.pop(key2)
            else:
                print(f"Cannot find {key2} of e.Sym()")
                print("Investigate this issue.")

    # def store_swap_edge(self,edge,old_key):
    #     if old_key not in self.edge_key:
    #         print("Error: The old edge key should be stored already")
    #         print(f"Error: Cannot not store swapped edge: {self.make_key(edge)} - {edge.type}")
    #         edge.type = EdgeType.NORMAL
    #         self.store_edge(edge)
    #         #self.store_edge(edge)
    #         return
    #     if old_key in self.edge_key and edge in self.edge_store:
    #         self.edge_key.remove(old_key)
    #         self.edge_store.remove(edge)
    #         #edge.type = EdgeType.NORMAL
    #         self.store_edge(edge)
    #     else:
    #         print(f"Cannot not store swapped edge: {self.make_key(edge)} - {edge.type}")

    def store_edge(self,edge):
        key1 = self.make_key(edge)
        key2 = (key1[1],key1[0])
        e_val = self.edge_store.get(key1,None)
        if e_val != None:
            print(f"{key1} is already stored in edge {e_val.Name}")
            print(f"edge {edge.Name} will not be stored")
            return
            
        e_val = self.edge_store.get(key2,None)
        if e_val != None:
            print(f"{key2} is already stored in edge {e_val.Name}")
            print(f"edge {edge.Name} will not be stored")
            return
        
        self.edge_store[key1] = edge
        # key2 = (key1[1],key1[0])
        # print(f"storing edge: {key1}")
        # if key1 not in self.edge_key and key2 not in self.edge_key:
        #     self.edge_store.add(edge)
        #     self.edge_key.add(key1)
        print(f"store edge success: {key1}")


    def init_state(self):
        self.edge_store = dict()

    def start_solve(self, S):
        # TODO: Need to preprocess the points to remove duplicate
        print("preparing data for incremental")
        length_s = len(S)
        if length_s < 2:
            print(f"Size of S {len(S)} is too small to do anything")
            return
        self.init_state()
        self.create_dummy_triangle()
        if len(self.edge_store) == 0:
            print("Check dummy_triangle creation")
            return
        S = DelaunayInc.prepare_data(S)

        for x in S:
            self.insert_site(x)
#update key
'''
TODO:
1. How to initialize with edges?
 + Wait for enough sites then create the first triangle?
 + Test to see if it works
 
'''
if __name__ == "__main__":
    S = [Site(0,0), Site(1,1)]
    e = QuadEdge.Make_Edge(S[0],S[1])
    #collinear test
    for i in range(5):
        x = Site(i,i)
        on_edge = site_on_edge(x,e)
        assert(on_edge == True)
    #not collinear test
    for i in range(5):
        x = Site(i+0.2,i-0.3)
        on_edge = site_on_edge(x,e)
        assert(on_edge == False)
    dinc = DelaunayInc()
