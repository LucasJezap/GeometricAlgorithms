from data_structures import *
from events import *
from tree import *
from queue import PriorityQueue
import time
from math_helper import Math

class Voronoi:
    def __init__(self):
        # Pola do opisu diagramu Voronoi
        self.event_queue = PriorityQueue()
        self.beach_line = None
        self.sweep_line = float("inf")
        self.points = None
        self.edges = []
        self.vertices = []
        self.x0 = self.x1 = self.y0 = self.y1 = None
        self.bounding_poly = None

    def initialize(self, points):
        self.points = points
        # Tworzę obramowanie
        self.x0 = min(p.x for p in points)
        self.x1 = max(p.x for p in points)
        self.y0 = min(p.y for p in points)
        self.y1 = max(p.y for p in points)
        dx = (self.x1 - self.x0) / 4
        dy = (self.y1 - self.y0) / 4
        self.x0 -= dx
        self.x1 += dx
        self.y0 -= dy
        self.y1 += dy
        self.bounding_poly = Polygon(
            [(self.x0, self.y0), (self.x1, self.y0), (self.x1, self.y1), (self.x0, self.y1), (self.x0, self.y0)])

        # dodaje punkty do struktury zdarzeń
        for index, point in enumerate(points):
            site_event = SiteEvent(point=point)
            self.event_queue.put(site_event)

    def create_diagram(self, points):
        # Zmieniam liste tupli na liste obiektów
        points = [Point(x, y) for x, y in points]
        length=len(points)

        # Inicjalizuje strukture, zapisuje czas by móc policzyć czas trwania procedury
        time1 = time.time()
        self.initialize(points)

        # Główna pętla, przechodzi przez wszystkie punkty struktury zdarzeń
        index = 0
        genesis_point = None
        while not self.event_queue.empty():
            event = self.event_queue.get()
            genesis_point = genesis_point or event.point

            if isinstance(event, CircleEvent) and event.is_valid:
                self.sweep_line = event.y
                self.handle_circle_event(event)

            elif isinstance(event, SiteEvent):
                self.sweep_line = event.y
                self.handle_site_event(event)

        # "Zamykam" obramowanie
        self.edges = self.bounding_poly.finish_edges(self.edges)
        # Obliczam czas działania programu
        time2 = time.time()
        #print("For " + str(length) + " points it took " + str(time2 - time1) + "s time to calculate diagram")
        return time2-time1

    def handle_site_event(self, event):
        # Tworzę nową parabolę
        new_point = event.point
        new_arc = Arc(origin=new_point)

        # Jeśli drzewo jest puste, wsadzam nowy element i wracam
        if self.beach_line is None:
            self.beach_line = LeafNode(new_arc)
            return

        # Znajduje parabole powyżej obecnie przetwarzanego punktu
        arc_node_above_point = Tree.find_leaf_node(self.beach_line, key=new_point.x, sweep_line=self.sweep_line)
        arc_above_point = arc_node_above_point.get_value()

        # Usuwam "fałszywe" punkty zdarzeń (koła)
        if arc_above_point.circle_event is not None:
            arc_above_point.circle_event.remove()

        # Rozbijam liść na odpowiednie poddrzewo
        point_i = new_point
        point_j = arc_above_point.origin
        breakpoint_left = Breakpoint((point_j, point_i))
        breakpoint_right = Breakpoint((point_i, point_j))

        root = InternalNode(breakpoint_left)
        root.left = LeafNode(Arc(origin=point_j, circle_event=None))

        # Prawy Breakpoint ląduje w drzewie tylko jeżeli istnieje punkt przecięcia
        if breakpoint_right.does_intersect():
            root.right = InternalNode(breakpoint_right)
            root.right.left = LeafNode(new_arc)
            root.right.right = LeafNode(Arc(origin=point_j, circle_event=None))
        else:
            root.right = LeafNode(new_arc)

        self.beach_line = arc_node_above_point.replace_leaf(replacement=root, root=self.beach_line)

        # Tworzę odpowiednie półkrawędzie
        A, B = point_j, point_i
        AB = breakpoint_left
        BA = breakpoint_right

        AB.edge = HalfEdge(B, origin=AB)
        BA.edge = HalfEdge(A, origin=BA, twin=AB.edge)

        self.edges.append(AB.edge)

        B.first_edge = B.first_edge or AB.edge
        A.first_edge = A.first_edge or BA.edge

        # Sprawdzam czy istnieje punkt przecięcia
        if not breakpoint_right.does_intersect():
            return

        node_a, node_b, node_c = root.left.predecessor, root.left, root.right.left
        node_c, node_d, node_e = node_c, root.right.right, root.right.right.successor

        self.check_circles((node_a, node_b, node_c), (node_c, node_d, node_e))

        # Naprawa drzewa
        self.beach_line = Tree.balance_and_propagate(root)

    def handle_circle_event(self, event):
        # Usuwam odpowiedni liśc drzewa reprezentujący parabole
        arc_node = event.arc_pointer
        predecessor = arc_node.predecessor
        successor = arc_node.successor

        # Aktualizuje breakpointy
        self.beach_line, updated, removed, left, right = self.update_breakpoints(
            self.beach_line, self.sweep_line, arc_node, predecessor, successor)

        # Usuwam wszystkie zdarzenia kołowe związane z usuniętą parabolą
        def remove(neighbor_event):
            if neighbor_event is None:
                return None
            return neighbor_event.remove()

        remove(predecessor.get_value().circle_event)
        remove(successor.get_value().circle_event)

        # Tworze odpowiednie półkrawędzie
        convergence_point = event.center

        v = Vertex(point=convergence_point)
        self.vertices.append(v)
        # Łącze dwie stare krawędzie z nowym wierzchołkiem
        updated.edge.origin = v
        removed.edge.origin = v
        v.incident_edges.append(updated.edge)
        v.incident_edges.append(removed.edge)

        C = updated.breakpoint[0]
        B = updated.breakpoint[1]

        new_edge = HalfEdge(B, origin=updated, twin=HalfEdge(C, origin=v))
        v.incident_edges.append(updated.edge.twin)
        self.edges.append(new_edge)

        # Ustawiam odpowiednie wskaźniki
        left.edge.twin.set_next(new_edge.twin)
        right.edge.twin.set_next(left.edge)
        new_edge.set_next(right.edge)

        updated.edge = new_edge

        # Sprawdzam czy nie pojawiły się nowe zdarzenia kołowe związane z lewą i prawą parabolą usuniętej paraboli
        former_left = predecessor
        former_right = successor

        node_a, node_b, node_c = former_left.predecessor, former_left, former_left.successor
        node_d, node_e, node_f = former_right.predecessor, former_right, former_right.successor

        self.check_circles((node_a, node_b, node_c), (node_d, node_e, node_f))

    def check_circles(self, triple_left, triple_right):
        node_a, node_b, node_c = triple_left
        node_d, node_e, node_f = triple_right

        # Tworzę koła
        left_event = CircleEvent.create_circle_event(node_a, node_b, node_c, sweep_line=self.sweep_line)
        right_event = CircleEvent.create_circle_event(node_d, node_e, node_f, sweep_line=self.sweep_line)

        # Sprawdzam czy koło jest odpowiednie
        if left_event:
            point1 = node_a.get_value().origin
            point2 = node_b.get_value().origin
            point3 = node_c.get_value().origin
            if not Math.check_clockwise(node_a.data.origin, node_b.data.origin, node_c.data.origin,
                                        left_event.center):
                left_event = None

        # Jeżeli tak umieszczam je w strukturze zdarzeń
        if left_event is not None:
            self.event_queue.put(left_event)
            node_b.data.circle_event = left_event

        # Sprawdzam czy drugie koło jest odpowiednie
        if right_event:
            point1 = node_d.get_value().origin
            point2 = node_e.get_value().origin
            point3 = node_f.get_value().origin
            if not Math.check_clockwise(node_d.data.origin, node_e.data.origin, node_f.data.origin,
                                        right_event.center):
                right_event = None

        # Jeżeli tak umieszczam je w strukturze zdarzeń
        if right_event is not None and left_event != right_event:
            self.event_queue.put(right_event)
            node_e.data.circle_event = right_event

        return left_event, right_event

    def update_breakpoints(self, root, sweep_line, arc_node, predecessor, successor):
        # Jeżeli mamy do czynienia z lewym synem to ojciec jest right_breakpoint
        if arc_node.is_left_child():

            # Zamieniamy go z prawym synem
            root = arc_node.parent.replace_leaf(arc_node.parent.right, root)

            # Usuwamy right_breakpoint
            removed = arc_node.parent.data
            right = removed

            # Naprawa drzewa
            root = Tree.balance_and_propagate(root)

            # Znajduje left_breakpoint
            left_breakpoint = Breakpoint((predecessor.get_value().origin, arc_node.get_value().origin))
            query = InternalNode(left_breakpoint)
            compare = lambda x, y: hasattr(x, "breakpoint") and x.breakpoint == y.breakpoint
            breakpoint = Tree.find_value(root, query, compare, sweep_line=sweep_line)

            # Aktualizuje go
            if breakpoint is not None:
                breakpoint.data.breakpoint = (breakpoint.get_value().breakpoint[0], successor.get_value().origin)

            updated = breakpoint.data if breakpoint is not None else None
            left = updated

        # Jeżeli mamy do czynienia z prawym synem to ojciec jest left_breakpoint
        else:
            # Zamieniamy go z lewym synem
            root = arc_node.parent.replace_leaf(arc_node.parent.left, root)

            # Usuwamy left_breakpoint
            removed = arc_node.parent.data
            left = removed

            # Naprawa drzewa
            root = Tree.balance_and_propagate(root)

            # Znajduje right_breakpoint
            right_breakpoint = Breakpoint(breakpoint=(arc_node.get_value().origin, successor.get_value().origin))
            query = InternalNode(right_breakpoint)
            compare = lambda x, y: hasattr(x, "breakpoint") and x.breakpoint == y.breakpoint
            breakpoint = Tree.find_value(root, query, compare, sweep_line=sweep_line)

            # Aktualizuje go
            if breakpoint is not None:
                breakpoint.data.breakpoint = (predecessor.get_value().origin, breakpoint.get_value().breakpoint[1])

            updated = breakpoint.data if breakpoint is not None else None
            right = updated

        return root, updated, removed, left, right
