#Helper function
def make_edge():
    return QuadEdge()

def splice(a,b):
    return None

def prepare_data(S):
    if len(S) < 2:
        return S
    #1. Sort by x
    #2. Sort by y
    sort_x = sorted(S, key = lambda s: s.x)
    sorted_S = sorted(sort_x, key = lambda s: s.y)
    #3. Remove duplicate points
    i = 0
    while i < len(sorted_S)-1:
        if sorted_S[i].equal(sorted_S[i+1]):
            #delete i+1
            sorted_S.pop(i+1)
        else:
            i = i +1
    return sorted_S

def ccw(s1,s2,s3):
    return True

def connect(a,b):
    return None

def left_of(a,b):
    return None

def right_of(a,b):
    return None

# Test prepare_data
def test_prepare_data(S,expect_S,func,msg=""):
    print(f"{msg}")
    result_S = func(S)
    #print(f"result_S: {result_S}")
    assert(len(expect_S) == len(result_S))
    for i,result in enumerate(result_S):
        assert(result.equal(expect_S[i]))
#Test case
#1.
S = [Site(0,0)]
expect_S = [Site(0,0)]
test_prepare_data(S,expect_S,prepare_data,"Test with 1 site")
#2.
S = [Site(0,0),Site(0,0)]
expect_S = [Site(0,0)]
test_prepare_data(S,expect_S,prepare_data,"Test with 2 site")

#3.
S = [Site(0,0),Site(0,0),Site(0,0)]
expect_S = [Site(0,0)]
test_prepare_data(S,expect_S,prepare_data,"Test with 3 site")

#4.
S = [Site(0,0),Site(1,1),Site(2,2)]
expect_S = [Site(0,0),Site(1,1),Site(2,2)]
test_prepare_data(S,expect_S,prepare_data,"Test with 3 different sites")

#5.
S = [Site(0,0),Site(1,3),Site(1,1),Site(1,1),Site(1,2)]
expect_S = [Site(0,0),Site(1,1),Site(1,2),Site(1,3)]
test_prepare_data(S,expect_S,prepare_data,"Test with 4 different sites, 1 duplicate")

#6.
S = [Site(0,0),Site(1,3),Site(1,1),Site(1,1),Site(1,2),Site(-2,-6),Site(-2,-7)]
expect_S = [Site(-2,-7),Site(-2,-6),Site(0,0),Site(1,1),Site(1,2),Site(1,3)]
test_prepare_data(S,expect_S,prepare_data,"Test with 6 different sites, 1 duplicate")