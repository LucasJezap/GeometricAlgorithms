from random import seed,random
import heapq
import bisect
from rb_tree import *
from rb_tree2 import *

from random import seed,random
import heapq
import bisect

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self,other):
        return isinstance(other,self.__class__) and self.x==other.x and self.y==other.y

    def __lt__(self,other):
        return self.x<other.x or (self.x==other.x and self.y<other.y)

    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+')'

    def __hash__(self):
        return hash((self.x,self.y))

def det(a,b,c):
    return a.x*b.y + a.y*c.x + b.x*c.y - b.y*c.x - a.y*b.x - a.x*c.y

def orientation(x,line):
    c_det = det(line.s,line.e,x)
    if c_det>1e-7:
        return 1
    elif c_det<-1e-7:
        return -1
    else:
        return 0

class Line:
    def __init__(self,s,e):
        self.s=s
        self.e=e
        self.orientation=self.s

    def __eq__(self,other):
        return isinstance(other,self.__class__) and self.s==other.s and self.e==other.e
    def __lt__(self,other):
        c_orientation = None
        if self.orientation.x>=other.orientation.x:
            c_orientation = orientation(self.orientation, other)
        else:
            c_orientation = -orientation(other.orientation, self)
        return (c_orientation==1) or (c_orientation==0 and orientation(self.e,other)==1)

    def __str__(self):
        return 'Line segment from '+str(self.s)+ ' to ' +str(self.e)

def generate_random_lines():
    lines=[]
    points=set()                                # to check if they don't meet at the ends
    number=int(input("Enter the number of lines you want to generate randomly: "))
    l=int(input("Enter first bound of x and y: "))
    r=int(input("Enter second bound of x and y: "))
    seed()
    while(number>0):
        x1=l+random()*(r-l)
        x2=l+random()*(r-l)
        while(x2==x1):
            seed()
            x2=l+random()*(r-l)
        y1=l+random()*(r-l)
        y2=l+random()*(r-l)
        start=Point(round(x1,10),round(y1,10))
        end=Point(round(x2,10),round(y2,10))
        if start in points or end in points:
            continue
        if start.x<end.x:
            lines.append(Line(start,end))
        else:
            lines.append(Line(end,start))
        points.add(start)
        points.add(end)
        number -=1
    return lines

# checks if lines ab and cd intersects and returns intersection point
def intersect(line1,line2):
    r = (line1.e.x-line1.s.x, line1.e.y-line1.s.y)
    s = (line2.e.x-line2.s.x, line2.e.y-line2.s.y)

    rxs = r[0]*s[1] - r[1]*s[0] #if rxs = 0 then lines colinear

    if(rxs > 1e-7 or rxs < -1e-7):
        q_p = (line2.s.x - line1.s.x, line2.s.y - line1.s.y)
        t = (q_p[0]*s[1] - q_p[1]*s[0]) / rxs
        u = (q_p[0]*r[1] - q_p[1]*r[0]) / rxs

        if((t >= 0. and t<=1.) and (u >= 0. and u <= 1.)):
            return (round(line1.s.x + t*r[0], 10), round(line1.s.y + t*r[1], 10))
        else:
            return None
    else:
        return None

# print all lines
def printLines(lines):
    for i in range(len(lines)):
        print(lines[i])

def copy(lines):
    tmp=[]
    for line in lines:
        tmp.append(Line(line.s,line.e))
    return tmp

def look_intersection(line1,line2):
    intersection=intersect(line1,line2)
    if not intersection is None:
        print("The first detected intersection point is ", intersection)
        return True
    return False

def any_lines_intersects(lines):
    T=RedBlackTree()                          # T is a RB-Tree, all operations in O(logn)
    Q=[]                                      # normal list, sorted in O(nlogn)
    for line in lines:
        Q.append((line.s,-1,line))   # start point of line symbolized by -1
        Q.append((line.e,1,line))    # end point of line symbolized by 1
    Q=sorted(Q)
    for p in Q:
        if p[1]==-1:
            T.add(p[2])
            prd=T.predecessor(p[2]).line
            if prd:
                if look_intersection(p[2],prd):
                    return (True, steps)
            suc=T.successor(p[2]).line
            if suc:
                if look_intersection(p[2],suc):
                    return (True, steps)
        elif p[1]==1:
            prd=T.predecessor(p[2]).line
            suc=T.successor(p[2]).line
            if prd and suc:
                if look_intersection(prd,suc):
                    return (True, steps)
            T.delete(p[2])
    return (False,steps)

def look_intersection2(line1,line2,P,Q,duplicates):
    intersection=intersect(line1,line2)
    if not intersection is None and intersection in P:
        duplicates.append(intersection)
    if not intersection is None and intersection not in P:
        Q.add((Point(intersection[0],intersection[1]),0,line1,line2))
        P.add(intersection)
        print(line1, " and ", line2, " intersect at the point ", intersection, "\n")

def every_lines_intersections(lines):         #TODO: color lines which are in T
    T=RedBlackTree()                          # T is a RB-Tree, all operations in O(logn)
    Q=RedBlackTree2()                         # Q is also a RB-Tree, but containing points
    P=set()                                   # P is a set
    duplicates=[]
    for line in lines:
        Q.add((line.s,-1,line,None))   # start point of line symbolized by -1
        Q.add((line.e,1,line,None))    # end point of line symbolized by 1
    while Q.size>0:
        p = Q.minimum().point
        Q.delete(p)
        if p[1]==-1:
            T.add(p[2])
            prd=T.predecessor(p[2])
            suc=T.successor(p[2])
            if prd:
                look_intersection2(p[2],prd.line,P,Q,duplicates)
            if suc:
                look_intersection2(p[2],suc.line,P,Q,duplicates)
        elif p[1]==1:
            prd=T.predecessor(p[2])
            suc=T.successor(p[2])
            if prd and suc:
                look_intersection2(prd.line,suc.line,P,Q,duplicates)
            T.delete(p[2])
        elif p[1]==0:
            T.delete(p[2])
            T.delete(p[3])
            p[2].orientation=Point(p[0].x,p[0].y)
            p[3].orientation=Point(p[0].x,p[0].y)
            T.add(p[2])
            T.add(p[3])
            upper1=p[2]
            lower1=p[2]
            prd=T.predecessor(upper1)
            suc=T.successor(lower1)
            if prd:
                look_intersection2(upper1,prd.line,P,Q,duplicates)
            if suc:
                look_intersection2(lower1,suc.line,P,Q,duplicates)
            upper2=p[3]
            lower2=p[3]
            prd2=T.predecessor(upper2)
            suc2=T.successor(lower2)
            if prd2:
                look_intersection2(upper2,prd2.line,P,Q,duplicates)
            if suc2:
                look_intersection2(lower2,suc2.line,P,Q,duplicates)
    points=[]
    for p in P:
        points.append((p[0],p[1]))

    print("There are " + str(len(points)) + " intersecting points ")
    if(len(points)!=0):
        print("How many times were each point averagely found?", str((len(duplicates)+len(points))/len(points)))
    return P

lines=generate_random_lines()
P=every_lines_intersections(lines)
for point in P:
    print("Intersection point ", point)
