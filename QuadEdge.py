# is used to reprenset a subdivision S 
'''
p.92

The group of edges containing e is represented in the data structure by one
edge record e, divided into four parts e [0] through e [3]. Part e [r] corresponds
to the edge e. Rot’. See Figure 7a. A generic edge e = e. Rot’Flipf is represented
by the triplet (e r, f ), called an edge reference. We may think of this triplet as a
pointer to the “quarter-record” e[r] plus a bit f that tells whether we should look
at it from “above” or from “below.”
Each part e [r] of an edge record contains two fields, Data and Next. The
Data field is used to hold geometrical and other nontopological information
about the edge e. Rot’. This field neither affects nor is affected by the topological
operations that we will describe, so its contents and format are entirely dependent
on the application.

The Next field of e [r] contains a reference to the edge e0Rot(r)Onext. Given an
arbitrary edge reference (e, r, f ), the three basic edge functions Rot, Flip, and
Onext are given by the formulas

The quad-edge data structure contains no separate records for vertice or faces;
a vertex is implicitly defined as a ring of edges, and the standard
way to refer to it is to specify one of its outgoing edges.

The standard way of referring to a connected component of the edge structure 
is by giving one of its directed edges.
'''
from enum import Enum

class EdgeType(Enum):
    NORMAL = "normal"
    CROSS = "cross"
class QuadEdge:
    name_id = 1
    def __init__(self):
        self.Name = QuadEdge.name_id
        QuadEdge.name_id += 1
        self.next = self
        self.rot = None
        self.org = None
        self.dest = None
        #self.Sym = self - not making any sense at the moment?
        # Lnext = Rnext = Sym ? are they pointing to self? 
       # self.Lnext = self # p.84 = eRotInverse.Onext.Rot
        #self.Rnext = self # p.84 = eRot.Onext.RotInverse
        #self.Dnext = self # p.84 = eSym.Onext.Sym
        #self.Oprev = self # p.84 = eRot.Onext.Rot
        #self.Lprev = self # p.84 = eRot.Onext.Sy,
       # self.Rprev = self # p.84 = eRot.Sym.Onext
       # self.Dprev = self # p.84 = eRot.RotInverse.Onext.RotInverse
       # self.Left = self # p.85 = eRotInverse.Org
        #self.Right = self # p.85 = eRotInverse.Org
        #self.Org = None # p.85 an edge algebra as the orbit of e under Onext, that is the cyclic sequence of edges
        # orbit: <..., e, eOnext, eOnext2,...,eOnext-1,e,...>
       # self.Dest = None # p.85 = e.Sym.Org
        
       # self.Edges = [Edge(self.Org,self.Dest,self)]*4
        #self.edge_index = 0
        self.active = True
        self.type = EdgeType.NORMAL

    def debug(self):
        print(f"name - active - type: {self.Name} - {self.active} - {self.type}")

    @staticmethod
    def Make_Edge(a, b):
        #print(f"\Make_Edge - create edge: {QuadEdge.name_id} ")
        quad_edges = []
        for _ in range(4):
            new_qe = QuadEdge()
            new_qe.org = a
            new_qe.dest = b
            quad_edges.append(new_qe)
            
        quad_edges[0].rot = quad_edges[1]
        quad_edges[1].rot = quad_edges[2]
        quad_edges[2].rot = quad_edges[3]
        quad_edges[3].rot = quad_edges[0]

        quad_edges[0].Sym().org = quad_edges[0].dest
        quad_edges[0].Sym().dest = quad_edges[0].org

        quad_edges[1].Sym().org = quad_edges[1].dest
        quad_edges[1].Sym().dest = quad_edges[1].org

        # Why is this the case?
        # Why intialize like this?
        quad_edges[0].next = quad_edges[0]
        quad_edges[1].next = quad_edges[3]
        quad_edges[2].next = quad_edges[2]
        quad_edges[3].next = quad_edges[1]

        return quad_edges[0]

    '''
    Splice[a, b] and takes as parameters two
    edges a and b, returning no value. 
    This operation affects the two edge rings a Org
    and b Org and, independently, the two edge rings a Left and b Left. In each case,
    (a) if the two rings are distinct, Splice will combine them into one;
    (b) if the two are exactly the same ring, Splice will break it in two separate
    pieces;
    (c) if the two are the same ring taken with opposite orientations, Splice will
    Flip (and reverse the order) of a segment of that ring.

    The parameters a and b determine the place where the edge rings will be cut
    and joined. For the rings a Org and b Org, the cuts will occur immediately after a
    and b (in counterclockwise order); for the rings aLeft and bLeft, the cut will
    occur immediately before a Rot and b Rot.
    '''
    @staticmethod
    def Splice(a,b):
        #print("\n---BEGIN SPLICE---")
        alpha = a.Onext().Rot() # Onext(a).Rot() --> return the underlying edge
        beta = b.Onext().Rot() # Onext(a).Rot()--> return the underlying edge
        #Ref: L.Guibas and J. Stolfi, p.102
        #precompute right hand side
        bOnext = b.Onext() # QuadEdge
        aOnext = a.Onext() # QuadEdge
        betaOnext = beta.Onext() # QuadEdge
        alphaOnext = alpha.Onext() # QuadEdge
        # assign to the left hand
        # print("\n---Before update---")
        # print(f"bOnext: {bOnext.Name}")
        # print(f"aOnext: {aOnext.Name}")
        # print(f"betaOnext: {betaOnext.Name}")
        # print(f"alphaOnext: {alphaOnext.Name}")

        a.next = bOnext
        b.next = aOnext
        alpha.next = betaOnext
        beta.next = alphaOnext

        # print("\n---After update---")
        # print(f"bOnext: {b.Onext().Name}")
        # print(f"aOnext: {a.Onext().Name}")
        # print(f"betaOnext: {beta.Onext().Name}")
        # print(f"alphaOnext: {alpha.Onext().Name}")
        # print("\n---END SPLICE---")
        return None
    
    '''
    The operation Connett[a, b] will add a new edge e 
    connecting the destination of a to the origin of
    b, in such a way that a Left = e Left = b Left after the connection is complete. 
    For added convenience it will also set the Org and Dest fields of the new edge to
    a.Dest and b.Org, respectively.
    '''
    @staticmethod
    def Connect(a,b):
        #print(f"\Connect - will create edge: {QuadEdge.name_id} ")
        e = QuadEdge.Make_Edge(a.Dest(),b.Org())
        e.type = EdgeType.CROSS
        QuadEdge.Splice(e, a.Lnext())
        QuadEdge.Splice(e.Sym(), b)
        return e
    
    # Check the delete_edge - does it only disconnect but not actually delete anything
    @staticmethod
    def DeleteEdge(e):
        #print(f"Delete edge: {e.Name}")
        QuadEdge.Splice(e, e.Oprev())
        QuadEdge.Splice(e.Sym(), e.Sym().Oprev())
        e.Delete()
    
    @staticmethod
    def Swap(e):
        #print(f"Delete edge: {e.Name}")
        a = e.Oprev()
        b = e.Sym().Oprev()
        QuadEdge.Splice(e, a)
        QuadEdge.Splice(e.Sym(),b)
        QuadEdge.Splice(e, a.Lnext())
        QuadEdge.Splice(e.Sym(), b.Lnext())
        e.org = a.Dest()
        e.dest = b.Dest()

    def Org(self):
        return self.org
    
    def Dest(self):
        return self.dest
    
    # What do we return after Rot? self?
    def Rot(self):
        return self.rot
    
    def Sym(self):
        return self.rot.rot
    
    def RotInverse(self):
        return self.rot.Sym()

    def Lnext(self):
        return self.RotInverse().Onext().Rot()

    def Lprev(self):
        return self.next.Sym()
    
    def Rnext(self):
        return self.rot.next.RotInverse()
    
    def Rprev(self):
        return self.Sym().Onext()
    
    def Onext(self):
        return self.next
    
    def Oprev(self):
        return self.rot.next.rot
    
    def Dnext(self):
        return self.Sym().Onext().Sym()
    
    def Dprev(self):
        return self.RotInverse().Onext().RotInverse()
    
    # Deactivate the edge but not actually delete it
    # What to do when a cross-edge is removed?
    def Delete(self):
        self.active = False
        # other = self.rot
        # while other != self:
        #     print(f"deactivate: {other.Name}")
        #     other.active = False
        #     other = other.rot
