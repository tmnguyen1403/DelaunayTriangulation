
def delaunay_dc(S):
    length_S = len(S)
    if length_S == 2:
        s1,s2 = S[0],S[1]
        a = make_edge()
        a.Org = s1
        a.dest = s2
        return (a,a.Sym)
    elif length_S == 3:
        s1,s2,s3 = S[0],S[1],S[2]
        # Create edges a connecting s1 to s2 
        # and b connecting s2 to s3
        a = make_edge()
        b = make_edge()
        splice(a.Sym,b)
        a.Org = s1
        a.Dest = b.Org = s2
        b.Dest = s3
        #Close the triangle
        if ccw(s1,s2,s3):
            c = connect(b,a)
            return (a,b.Sym)
        elif ccw(s1,s3,s2):
            c = connect(b,a)
            return (c.Sym,c)
        else:
            return (a,b.Sym)
    elif length_S >= 4:
        L,R = S[:length_S//2],S[length_S//2:]
        ldo,ldi = delaunay_dc(L)
        rdi,rdo = delaunay_dc(R)
        #Compute the lower common tangent of L and R
        while True:
            if left_of(rdi.Org,ldi):
                ldi = ldi.Lnext
            elif right_of(ldi.Org,rdi):
                rdi = rdi.Rprev
            else:
                print("Finish compute the lower common tangent of L and R")
                break
        #Create a first cross edge basel from rdi.Org to ldi.Org
        basel = connect(rdi.Sym,ldi)
        if ldi.Org == ldo.Org:
            ldo = basel.Sym
        if rdi.Org == rdo.Org:
            rdo = basel
        #Merge loop
        while True:
            #Locate the first L point (lcand.Dest) to be encoutered by the rising bubble
            #and delete Ledges out of basel.Dest that fail the circle test
            lcand = basel.Sym.Onext
            if valid(lcand):
                while incircle(basel.Dest, basel.Org, lcand.Dest, lcand.Onext.Dest):
                    t = lcand.Onext
                    delete_edge(lcand)
                    lcand = t
            #End if
            #Symmetrically locate the first R point to be hit, and delete R edges
            rcand = basel.Oprev
            if valid(rcand):
                while incircle(basel.Dest, basel.Org, rcand.Dest, rcand.Oprev.Dest):
                    t = rcand.Oprev
                    delete_edge(rcand)
                    rcand = t
            #End if
            #If both lcand and rcand are invalid, then basel is the upper common tangent
            if not valid(lcand) and not valid(rcand):
                print("Both lcand and rcand are invalid")
                break
            #if both are valid, then choose the approriate one using the incircle test
            if not valid(lcand) or (valid(rcand) and incircle(lcand.Dest, lcand.Org, rcand.Org, rcand.Dest)):
                #add cross edge basel from rcand.Dest to basel.Dest
                basel = connect(rcand, basel.Sym)
            else:
                #add cross edge basel from basel.Org to lcand.Dest
                basel = connect(basel.Sym, lcand.Sym)
            #end if
        #End loop
        return (ldo, rdo)
    #End delaunay_dc 
