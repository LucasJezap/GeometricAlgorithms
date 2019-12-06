import math
import time
from DataStructures import *
from line_clipping import cohenSutherlandClip

# Źródło http://www.cs.hmc.edu/~mbrubeck/voronoi.html (C++)

class Voronoi:
    def __init__(self,points):
        self.result=[]
        self.root=None
        self.point_events=PriorityQueue()
        self.circle_events=PriorityQueue()
        self.x0=min(points, key=lambda t:t.x).x
        self.x1=max(points, key=lambda t:t.x).x
        self.y0=min(points, key=lambda t:t.y).y
        self.y1=max(points, key=lambda t:t.y).y

        for point in points:
            self.point_events.push(point)
        dx=(self.x1-self.x0+1)/5
        dy=(self.y1-self.x0+1)/5
        self.x0-=dx
        self.x1+=dx
        self.y0-=dy
        self.y1+=dy

    def find(self):
        time1=time.time()
        while not self.point_events.empty():
            if not self.circle_events.empty() and (self.circle_events.top().x<=self.point_events.top().x):
                self.process_circle()
            else:
                self.process_point()

        while not self.circle_events.empty():
            self.process_circle()

        self.close_edges()
        self.adjust_lines()
        time2=time.time()
        print("It took "+str(time2-time1)+"s to find diagram")

    def process_point(self):
        p=self.point_events.pop()
        self.front_insert(p)

    def intersect(self, p, i):
        if i is None:
            return False, None
        if i.p.x==p.x:
            return False, None
        a,b=0,0
        if i.prev is not None:
            a=(self.intersection(i.prev.p,i.p,p.x)).y
        if i.next is not None:
            b=(self.intersection(i.p,i.next.p,p.x)).y

        if (((i.prev is None) or (a<=p.y)) and ((i.next is None) or (p.y<=b))):
            res=Point(((i.p.x)**2 + (i.p.y-p.y)**2 - p.x**2) / (2*i.p.x - 2*p.x),p.y)
            return True,res
        return False,None

    def intersection(self,p0,p1,l):
        res=Point(0,0)
        p=p0
        if p0.x==p1.x:
            res.y=(p0.y+p1.y)/2
        elif p1.x==l:
            res.y=p1.y
        elif p0.x==l:
            res.y=p0.y
            p=p1
        else:
            z0=2*(p0.x-l)
            z1=2*(p1.x-l)
            a=1/z0-1/z1
            b=(-2)*(p0.y/z0-p1.y/z1)
            c=(p0.y**2+p0.x**2-l**2)/z0-(p1.y**2+p1.x**2-l**2)/z1
            res.y=(-b-math.sqrt(b*b-4*a*c))/(2*a)
        res.x=(p.x**2+(p.y-res.y)**2-l**2)/(2*p.x-2*l)
        return res

    def front_insert(self,p):
        if self.root is None:
            self.root = Parabole(p)
        else:
            i=self.root
            while i is not None:
                flag,z=self.intersect(p,i)
                if flag:
                    flag,zz=self.intersect(p, i.next)
                    if (i.next is not None) and (not flag):
                        i.next.prev=Parabole(i.p,i,i.next)
                        i.next=i.next.prev
                    else:
                        i.next=Parabole(i.p,i)
                    i.next.s1=i.s1
                    i.next.prev=Parabole(p,i,i.next)
                    i.next=i.next.prev
                    i=i.next
                    segment=LineSegment(z)
                    self.result.append(segment)
                    i.prev.s1=i.s0=segment
                    segment=LineSegment(z)
                    self.result.append(segment)
                    i.next.s0=i.s1=segment
                    self.check_event(i,p.x)
                    self.check_event(i.prev,p.x)
                    self.check_event(i.next,p.x)
                    return
                i=i.next
            i=self.root
            while i.next is not None:
                i=i.next
            i.next=Parabole(p,i)
            start=Point(self.x0,(i.next.p.y+i.p.y)/2)
            segment=LineSegment(start)
            i.s1=i.next.s0=segment
            self.result.append(segment)

    def process_circle(self):
        c=self.circle_events.pop()
        if c.valid:
            segment=LineSegment(c.p)
            self.result.append(segment)
            a=c.a
            if a.prev is not None:
                a.prev.next=a.next
                a.prev.s1=segment
            if a.next is not None:
                a.next.prev=a.prev
                a.next.s0=segment

            if a.s0 is not None:
                a.s0.finish(c.p)
            if a.s1 is not None:
                a.s1.finish(c.p)

            if a.prev is not None:
                self.check_event(a.prev,c.x)
            if a.next is not None:
                self.check_event(a.next,c.x)

    def check_event(self,i,x0):
        if (i.e is not None) and (i.e.x != x0):
            i.e.valid=False
        i.e=None
        if (i.prev is None) or (i.next is None):
            return
        flag,x,o=self.find_circle(i.prev.p,i.p,i.next.p)
        if flag and (x>x0):
            i.e=Event(x,o,i)
            self.circle_events.push(i.e)

    def find_circle(self,p,q,r):
        if ((q.x-p.x)*(r.y-p.y)-(r.x-p.x)*(q.y-p.y))>0:
            return False,None,None
        A=q.x-p.x
        B=q.y-p.y
        C=r.x-p.x
        D=r.y-p.y
        E=A*(p.x+q.x)+B*(p.y+q.y)
        F=C*(p.x+r.x)+D*(p.y+r.y)
        G=2*(A*(r.y-q.y)-B*(r.x-q.x))
        if G==0:
            return False,None,None
        o=Point((D*E-B*F)/G,(A*F-C*E)/G)
        x=o.x+math.sqrt((p.x-o.x)**2+(p.y-o.y)**2)
        return True,x,o

    def close_edges(self):
        l=self.x1+(self.x1-self.x0)+(self.y1-self.y0)
        i=self.root
        while i.next is not None:
            if i.s1 is not None:
                p=self.intersection(i.p,i.next.p,l*2)
                i.s1.finish(p)
            i=i.next

    def adjust_lines(self):
        tmp=[]
        for line in self.result:
            if cohenSutherlandClip(line.start,line.end,self.x0,self.y0,self.x1,self.y1):
                tmp.append(line)
        self.result=tmp


    def get_result(self):
        res=[(self.x0,self.y0,self.x1,self.y0),(self.x1,self.y0,self.x1,self.y1),(self.x1,self.y1,self.x0,self.y1),(self.x0,self.y1,self.x0,self.y0)]
        for line in self.result:
            p0=line.start
            p1=line.end
            res.append((p0.x,p0.y,p1.x,p1.y))
        return res
