##
p.96
In the edge algebra, the Org and Left rings of an edge e are the orbits under
Onext of e and e Onext Rot, respectively.
1. How we represent an orbit?

MakeEdge
 1. It takes no parameters,
and returns an edge e of a newly created data structure representing a subdivision
of the sphere (see Figure 9). Apart from orientation and direction, e will be the
only edge of the subdivision and will not be a loop; we have, eLeft
= e Right, e Lnext = e Rnext = e Sym, and e Onext = e Oprev = e
To construct a loop, we may use e <- MakeEdge[ ].Rot; then we will have eOrg = eDest, eLeft
2. e Org != e Dest, what does it mean? two different orbits?
3. Why  MakeEdge[].Rot create a loop?
4. Org and Dest are x and y coordinates?

p.97
1. What does it mean for aOrg = bOrg, aLeft != bLeft
My understanding: Origin is the orbit? not the vertex point?
2. So Org is node in a circular list?
3. So we have to traverse the whole list to compare?


## New question
1. The rot assignment in make_edge
2. What is the min_x,min_y;max_x,max_y of the random points
3. Stuck in the basel loop - what to do?

## Time
Runtime in seconds
Size | Dataset | Run 1 | Run 2 | Run 3
10000 | 2 | 3.2s | | |
100000 | 1 | 36.4 | 35.2 | 38.6 |
100000 | 1 | 41.0 | 41.0 | 41.3 |
1000000 | 1 | 6m43.9 |  | 6m43.8 | 6m30.4s
1000000 | 2 | 8m7.1 | 7m24.9 | 6m | 7m30.7



## Edge needed to draw:
Size | Dataset | Run 1 | Run 2 | Run 3
100000 | 1 | 290889 |
100000 | 2 | 290655 |
1000000 | 1 | 2854749 |
1000000 | 2 | 2855202 |


