import heapq
import itertools

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+')'

class Event:
    def __init__(self,x,p,a):
        self.x=x
        self.p=p
        self.a=a
        self.valid=True

class Parabole:
    def __init__(self,p,a=None,b=None):
        self.p=p
        self.prev=a
        self.next=b
        self.e=None
        self.s0=None
        self.s1=None

class LineSegment:
    def __init__(self,p):
        self.start=p
        self.end=None
        self.done=False

    def finish(self,p):
        if self.done:
            return
        self.end=p
        self.done=True

    def __str__(self):
        return str(self.start)+' -> '+str(self.end)

class PriorityQueue:
    def __init__(self):
        self.q=[]
        self.entry_finder={}
        self.counter=itertools.count()

    def push(self,item):
        if item in self.entry_finder:
            return
        count=next(self.counter)
        entry=[item.x,count,item]
        self.entry_finder[item]=entry
        heapq.heappush(self.q,entry)

    def remove_entry(self,item):
        entry=self.entry_finder.pop(item)
        entry[-1]='Removed'

    def pop(self):
        while self.q:
            priority, count, item = heapq.heappop(self.q)
            if item is not 'Removed':
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def top(self):
        while self.q:
            priority, count, item = heapq.heappop(self.q)
            if item is not 'Removed':
                del self.entry_finder[item]
                self.push(item)
                return item
        raise KeyError('top from an empty priority queue')

    def empty(self):
        return not self.q