from math import pi,cos,sin
from random import seed,random

def randomFirst(n):
    points = []
    seed(1)
    for i in range(0,n):
        points.append((-1000+random()*2000,-1000+random()*2000))
    return points
def randomSecond(n):
    points = []
    seed(1)
    for i in range(0,n):
        points.append((-10**14+random()*2*10**14,-10**14+random()*2*10**14))
    return points
def randomThird(n):
    points = []
    seed(1)
    for i in range(0,n):
        angle = 2*pi*random()
        points.append((cos(angle)*100,sin(angle)*100))
    return points
def randomFourth(n):
    a = 0.05
    b = 0.05                  # y=ax+b
    points = []
    seed(1)
    for i in range(0,n):
        x = -1000+random()*2000
        points.append((x,a*x+b))
    return points

points1=randomFirst(10)
points2=randomSecond(10)
points3=randomThird(10)
points4=randomFourth(10)

def dividePointsFirst(points,eps):
    a = (-1.0,0.0)
    b = (1.0, 0.1)
    left = []
    right = []
    middle = []
    placed = []
    l = r = m = 0
    for point in points:
        det = a[0]*b[1]+a[1]*point[0]+b[0]*point[1]-b[1]*point[0]-a[0]*point[1]-a[1]*b[0]
        print(det)
        if det > eps:
            left.append(point)
            l += 1
            placed.append(1)
        elif det < -eps:
            right.append(point)
            r += 1
            placed.append(-1)
        else:
            middle.append(point)
            m += 1
            placed.append(0)
    print("Method 1: The number of points in list LEFT is {}, in list RIGHT is {} and in list MIDDLE is {}".format(l,r,m))
    return placed
def dividePointsSecond(points, eps):
    a = (-1.0,0.0)
    b = (1.0, 0.1)
    left = []
    right = []
    middle = []
    placed = []
    l = r = m = 0
    for point in points:
        det = (a[0]-point[0])*(b[1]-point[1])-(b[0]-point[0])*(a[1]-point[1])
        print(det)
        if det > eps:
            left.append(point)
            l += 1
            placed.append(1)
        elif det < -eps:
            right.append(point)
            r += 1
            placed.append(-1)
        else:
            middle.append(point)
            m += 1
            placed.append(0)
    print("Method 2: The number of points in list LEFT is {}, in list RIGHT is {} and in list MIDDLE is {}".format(l,r,m))
    return placed
def dividePointsThird(points,eps):
    left = []
    right = []
    middle = []
    placed = []
    l = r = m = 0
    for point in points:
        a = np.array([[-1,0,1],[1,0.1,1],[point[0],point[1],1]])
        det = np.linalg.det(a)
        print(det)
        if det > eps:
            left.append(point)
            l += 1
            placed.append(1)
        elif det < -eps:
            right.append(point)
            r += 1
            placed.append(-1)
        else:
            middle.append(point)
            m += 1
            placed.append(0)
    print("Method 3: The number of points in list LEFT is {}, in list RIGHT is {} and in list MIDDLE is {}".format(l,r,m))
    return placed
def dividePointsFourth(points,eps):
    left = []
    right = []
    middle = []
    placed = []
    l = r = m = 0
    for point in points:
        a = np.array([[-1.0-point[0],0-point[1]],[1.0-point[0],0.1-point[1]]])
        det=np.linalg.det(a)
        print(det)
        if det > eps:
            left.append(point)
            l += 1
            placed.append(1)
        elif det < -eps:
            right.append(point)
            r += 1
            placed.append(-1)
        else:
            middle.append(point)
            m += 1
            placed.append(0)
    print("Method 4: The number of points in list LEFT is {}, in list RIGHT is {} and in list MIDDLE is {}".format(l,r,m))
    return placed
def calculateDiff(result1, result2,a,b):
    j = 0
    for i in range(0,len(result1)):
        if result1[i] != result2[i]:
            j += 1
    print("The number of points that were placed different between method {} and method {} is {} ".format(a,b,j))
dividePointsFirst(points1,0)
dividePointsSecond(points1,0)
dividePointsThird(points1,0)
dividePointsFourth(points1,0)