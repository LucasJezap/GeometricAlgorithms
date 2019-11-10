from math import pi,cos,sin,sqrt
from random import seed,random
from functools import reduce
import time

def randomFirst(n, left, right):
    points = []
    seed(1)
    for i in range(0,n):
        points.append((left+random()*(right-left),left+random()*(right-left)))
    return points
def randomSecond(n, radius, x, y):
    points = []
    seed(1)
    for i in range(0,n):
        angle = 2*pi*random()
        points.append((cos(angle)*radius+x,sin(angle)*radius+y))
    return points

def findPoint(a,b,length):
    side = sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
    v = ((b[0]-a[0])/side,(b[1]-a[1])/side)
    result = (a[0]+length*v[0],a[1]+length*v[1])
    return result

def randomThird(n,a,b,c,d):
    points = []
    seed(1)
    side1 = sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
    side2 = sqrt((c[0]-b[0])**2+(c[1]-b[1])**2)
    perimeter = 2*side1+2*side2
    for i in range(0,n):
        tmp=random()*perimeter
        if (tmp<side1):
            (x,y)=findPoint(a,b,tmp)
        elif(tmp>side1 and tmp<side1+side2):
            (x,y)=findPoint(b,c,tmp%side1)
        elif(tmp>side1+side2 and tmp<side1*2+side2):
            (x,y)=findPoint(c,d,tmp%(side1+side2))
        else:
            (x,y)=findPoint(d,a,tmp%(2*side1+side2))
        points.append((x,y))
    return points

def randomFourth(n1,n2,a,b,c,d):           # lets say there are points on left and bottom sides, may not include axes
    points = [a,b,c,d]
    seed(1)
    side = sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
    for i in range(0,n1):
        tmp=random()*2*side
        if (tmp<side):
            (x,y)=findPoint(d,a,tmp)
        else:
            (x,y)=findPoint(a,b,tmp%side)
        points.append((x,y))
    diagonal = sqrt((c[0]-a[0])**2+(c[1]-a[1])**2)
    for i in range(0,n2):
        tmp=random()*2*diagonal
        if (tmp<diagonal):
            (x,y)=findPoint(a,c,tmp)
        else:
            (x,y)=findPoint(d,b,tmp%diagonal)
        points.append((x,y))
    return points

def firstPoint(points):
    min=0
    for i in range(0,len(points)):
        if(points[i][1]<points[min][1]):
            min=i
        elif (points[i][1]==points[min][1]):
            if(points[i][0]<points[min][0]):
                min=i
    return min

def orientation(a,b,c):
    det = ((b[1]-a[1])*(c[0]-b[0])-(b[0]-a[0])*(c[1]-b[1]))
    if det==0:
        return 0
    elif det>0:
        return 1
    else:
        return -1                    #

def dist(points,a,b):
    return sqrt((points[b][0]-points[a][0])**2+(points[b][1]-points[a][1])**2)

def Jarvis(points):
    time1 = time.time()
    if len(points) < 3:
        return []
    first = firstPoint(points)
    convex = []
    a = first
    while(True):
        convex.append(points[a])
        b = (a+1) % len(points)
        for i in range(len(points)):
            orient = orientation(points[a],points[i],points[b])
            if orient==-1 or (orient==0 and dist(points,a,i)>dist(points,a,b)):
                b = i
        a = b
        if a==first:
            convex.append(points[a])
            break
    time2 = time.time()
    print("It took ", time2-time1, "s time to find hull convex")
    print(convex)
    return convex

def orientation2(a,b,c):
    det = ((b[1]-a[1])*(c[0]-b[0])-(b[0]-a[0])*(c[1]-b[1]))
    if det==0:
        if dist2(a,b)<dist2(a,c):
            return 1
        else:
            return -1
    elif det>0:
        return 1
    else:
        return -1              # 1 - clockwise, -1 - counterclockwise

def dist2(a,b):
    return sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)

def slope(a,b):
    return 1.0*(b[0]-a[0])/(b[1]-a[1]) if b[1]!=a[1] else float('inf')

def Graham(points):
    time1 = time.time()
    if len(points) < 3:
        return []
    first=firstPoint(points)
    points[0],points[first]=points[first],points[0]
    tmpPoints = []
    sortedPoints = []
    for p in points:
        tmpPoints.append((p[0],p[1],slope(points[0],p),dist2(points[0],p)))
    tmpPoints[1:]=sorted(tmpPoints[1:],key=lambda t:t[3])
    tmpPoints[1:]=sorted(tmpPoints[1:],key=lambda t:t[2], reverse=True)
    for p in tmpPoints:
        sortedPoints.append((p[0],p[1]))
    stack = []
    for p in sortedPoints:
        while(len(stack)>1 and orientation(stack[-2],stack[-1],p) != -1):
            stack.pop(-1)
        stack.append(p)
    stack.append(points[0])
    time2 = time.time()
    print("It took ", time2-time1, "s time to find hull convex")
    print("The convex consists of points: " , stack)
    print("\n")
    return stack

points=randomFirst(10,-10,20)
convex = Graham(points)
convex2 = Jarvis(points)
print(convex)
print(convex2)