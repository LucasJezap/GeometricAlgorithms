from random import random,seed
from voronoi import Voronoi

def randomFirst(n, left, right):
    pts = []
    seed(1)
    for i in range(0,n):
        pts.append((round(left+random()*(right-left),8),round(left+random()*(right-left),8)))
    return pts

left=int(input("Welcome to time complexity tester for generating Voronoi diagrams. "
               "Enter left border of number of points: "))
right=int(input("Now enter right border: "))
times=[]
for i in range(left,right):
    points=randomFirst(i,0,100)
    v=Voronoi()
    times.append((i,v.create_diagram(points)))
for t in times:
    print(t)
