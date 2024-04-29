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
        self.face_record = dict() #Contain the starting edge, the points of the faces
        self.current_face_id = 0

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

    '''
    Calculate the distance of a site s to a face by summing the vector norm of the point to three face sites
    '''
    def dist_to_face(self,s,face_id):
        record = self.face_record.get(face_id,None)
        if record == None:
            return 0
        e,points = record
        print(f"record: {e.get_coor()} - points dist: {points}")
        x,y = s.getXY()
        p0 = np.array([x,y])
        pa = np.array(list(points))
        # Find the center of the triangle
        center = np.sum(pa,axis=0)
        # dist = [np.linalg.norm(p-p0) for p in pa]
        # min_dist = min(dist)
        # print(f"dist: {dist}\n")
        dist = np.linalg.norm(center-p0)
        print(f"dist: {dist}\n")
        return dist

    def locate(self,x):
        print("\nlocate debug:")
        print(f"locate edge for: {x.getXY()}")
        chosen_edge = []
        seen_face = set()
        neg_face_record = {}
        neg_face_id = -2
        for face_id,record in self.face_record.items():
            if face_id in seen_face:
                continue
            e,_ = record
            print(f"starting edge: {e.get_coor()} - face: {e.face}")
            seen_edge = set()
            counter = 0
            while True:
                print(f"locate counter: {counter}")
                seen_edge.add(e)
                counter += 1
                eOnext = e.Onext()
                eDprev = e.Dprev()
                if e.face == -1:
                    points = set()
                    face_id = neg_face_id
                    e.face = face_id
                    neg_face_record[face_id] = (e,points)
                    self.traverse_left(face_id=face_id,update_face=True,face_record=neg_face_record)
                    neg_face_id -= 1

                if x == e.Org() or x == e.Dest():
                    print(f"I. chosen edge: {e.get_coor()} - face: {e.face}")
                    chosen_edge.append(e)
                    break
                    #return e
                elif right_of(x,e):
                    print(f"1. right of {self.make_key(e)}")
                    seen_face.add(e.face)
                    e = e.Sym()
                    print(f"starting edge: {e.get_coor()} - face: {e.face}")
                    counter = 0
                elif left_of(x, eOnext):
                    print(f"2. not right of {eOnext.get_coor()}")
                    e = eOnext
                elif left_of(x, eDprev):
                    print(f"3. not right of {eDprev.get_coor()}")
                    e = eDprev
                else:
                    print(f"II. chosen edge: {e.get_coor()} - {e.face}")
                    seen_face.add(e.face)
                    chosen_edge.append(e)
                    break
                    #return e
                #avoid stuck in the loop because the point is outside of the triangle
                # is it still work?
                if e in seen_edge:
                    print(f"stuck in the loop of face: {e.face}")
                    break
        for face_id, record in neg_face_record.items():
            self.face_record[face_id] = record

        print("Debug chosen edges:")
        min_dist = float('inf')
        result_edge = None
        for edge in chosen_edge:
            print(f"getting dist for face of edge: {edge.get_coor()} - face: {edge.face}")
            face_id = edge.face
            if face_id == -1:
                raise(Exception("Face_id of a chosen edge should not be negative:"))
            dist = self.dist_to_face(x,face_id=face_id)
            if dist < min_dist:
                min_dist = dist
                result_edge = edge
                print(f"dist: {dist} - edge: {result_edge.get_coor()} - face: {result_edge.face}")
        return result_edge
    
    def traverse_left(self,face_id,update_face=True,face_record = {}):
        if len(face_record) == 0:
            e,points = self.face_record[face_id]
        else:
            e,points = face_record[face_id]

        lnext = e.Lnext()
        while lnext != e:
            if update_face:
                lnext.face = face_id
            print(f"next: {lnext.get_coor()} -face: {lnext.face}")
            self.add_points(lnext,points)
            lnext = lnext.Lnext()

    def add_points(self,e,points=set()):
        c = e.get_coor()
        points.add(c[0])
        points.add(c[1])

    def mark_face(self):
        self.current_face_id = 0
        self.face_record = dict()
        for _, e in self.edge_store.items():
            #Traverse edges that has the same left face
            if self.face_record.get(e.face, None) != None:
                continue
            e.face = self.current_face_id
            points = set()
            self.add_points(e,points)
            self.face_record[self.current_face_id] = (e,points)
            self.traverse_left(face_id=self.current_face_id,update_face=True)
            self.current_face_id += 1
    
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
        max_loop = 40
        counter = 0
        while e.Dest() != first:
            baseSym = base.Sym()
            base = QuadEdge.Connect(e, baseSym)
            self.store_edge(e)
            self.store_edge(baseSym)
            self.store_edge(base)
            e = base.Oprev()
            if counter > max_loop:
                print(f"first: {first.getXY()}")
                raise(Exception("Stuck in loop"))
            counter += 1
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
        #S = DelaunayInc.prepare_data(S)

        for x in S:
            self.mark_face()
            print("\nFace Debug")
            for key, e in self.edge_store.items():
                print(f"{e.get_coor()} - {e.face}")
            print("\n")
            print("\nEdge face debug")
            for face_id, value in self.face_record.items():
                e, points = value
                print(f"start edge: {e.get_coor()} - face: {e.face}")
                self.traverse_left(face_id=face_id,update_face=False)
                print(f"face points: {points}")
            # for key, e in self.edge_store.items():
            #     if e.face in seen_face:
            #         continue
            #     print(f"start edge: {e.get_coor()} - face: {e.face}")
            #     self.traverse_left(e,e.face,set_face=False)
            #     seen_face.add(e.face)

            self.insert_site(x)
#update key
'''
TODO:
1. How to initialize with edges?
 + Wait for enough sites then create the first triangle?
 + Test to see if it works
 
'''
if __name__ == "__main__":
    def are_collinear(points):
        # Check if the slope between any pair of points is the same
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]
        
        # Calculate slopes
        slope1 = (y2 - y1) * (x3 - x2)
        slope2 = (y3 - y2) * (x2 - x1)
        
        # Check if slopes are equal (or almost equal due to floating point precision)
        print(f"slope 1: {slope1} - slope 2: {slope2}")
        return np.isclose(slope1, slope2)

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
    #
    print("Test harder case")
    S = [Site(-1.02,-8.55), Site(7.64,1.29),  Site(5.55,-1.01)]
    e = QuadEdge.Make_Edge(S[0],S[1])
    on_edge = site_on_edge(S[2],e)
    collinear = are_collinear([(-1.02,-8.55), (7.64,1.29), (5.55,-1.01)])
    print(f"collinear: {collinear}")
    #assert(on_edge == True)

    #
    print("Test edge case")
    S = [Site(5.28,-7.41), Site(40,-10), Site(3.11,-6.93)]
    e = QuadEdge.Make_Edge(S[0],S[1])
    on_edge = site_on_edge(S[2],e)
    collinear = are_collinear([(5.28,-7.41), (40,-10), (3.11,-6.93)])
    print(f"collinear: {collinear}")
    #assert(on_edge == True)
