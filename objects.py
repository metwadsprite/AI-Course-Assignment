import math
from utils import is_intersect
import matplotlib.pyplot as plt


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Edge():
    def __init__(self, t, angle, position):
        self.type = t
        self.angle = angle
        self.position = position


class TrackPiece():
    def __init__(self, edges):
        self.edges = edges
        self.position = Point(0, 0)
        self.angle = 0
        
        self.connected = dict()

        for edge in self.edges:
            self.connected[edge] = None

    def rotate(self, deg):
        """
        Rotates the trackpiece by given number of degrees.
        """
        self.angle += deg
        pivot = (65, 15)

        for edge in self.edges:
            edge.position.x -= pivot[0]
            edge.position.y -= pivot[1]

            new_x = (edge.position.x * math.cos(math.radians(deg))) - \
                (edge.position.y * math.sin(math.radians(deg)))
            new_y = (edge.position.x * math.sin(math.radians(deg))) + \
                (edge.position.y * math.cos(math.radians(deg)))

            edge.position.x = new_x + pivot[0]
            edge.position.y = new_y + pivot[1]

            edge.angle += deg
    
    def move(self, distance):
        """
        Moves the trackpiece by given distance as a vector.
        """
        for edge in self.edges:
            edge.position.x += distance[0]
            edge.position.y += distance[1]

    def move_to_con(self, edge, piece, edge_to_connect = None):
        """
        edge - Point on the other piece to connect to.\n
        piece - Other piece.\n
        edge_to_connect(optional) - Point of connection on this piece.\n

        Moves the trackpiece in position to connect to another piece.
        """
        if edge_to_connect == None:
            for con_edge in piece.edges:
                if con_edge.type != edge.type and piece.connected[con_edge] == None:
                    edge_to_connect = con_edge

        rotate_deg = edge.angle - edge_to_connect.angle
        piece.rotate(rotate_deg)

        move_dist = (edge.position.x - edge_to_connect.position.x, \
            edge.position.y - edge_to_connect.position.y)

        piece.move(move_dist)

    def connect(self, edge, piece, edge_to_connect):
        """
        Connects the given points on this trackpiece and the other given.
        """
        self.connected[edge] = piece
        piece.connected[edge_to_connect] = self


class Track():
    def __init__(self):
        self.start = None

    def is_overlap(self, piece):
        """
        Checks whether the piece will overlap with any of the existing ones
        on the track.
        """
        queue = [self.start]
        visited = []

        while len(queue):
            cur_node = queue.pop()
            visited.append(cur_node)
           
            A, B, C, D = [], [], [], []
            
            for edge in cur_node.edges:
                if edge.type == 'female':
                    A.append(edge.position)
                else:
                    B.append(edge.position)

                if cur_node.connected[edge] != None and cur_node.connected[edge] not in visited:
                    queue.append(cur_node.connected[edge])

            for edge in piece.edges:
                if edge.type == 'female':
                    C.append(edge.position)
                else:
                    D.append(edge.position)

            for a in A:
                for b in B:
                    for c in C:
                        for d in D:
                            if is_intersect(a, b, c, d):
                                return True
        return False
    
    def add_piece(self, con_piece, con_edge_id, new_piece, newpc_edge_con_id = None):
        """
        con_piece - Piece on track to connect to.\n
        con_edge_id - Point on the piece to connect to.\n
        new_piece - Piece to be added to the track.\n
        newpc_edge_con_id - Point on the new piece to connect.\n

        Adds a new piece to the track. Returns 'True' if successful, 'False'
        otherwise.
        """
        if self.start == None:
            self.start = new_piece
            return

        con_edge = con_piece.edges[con_edge_id]
        if con_piece.connected[con_edge] != None:
            return

        con_piece.move_to_con(con_edge, new_piece, newpc_edge_con_id)
        
        if self.is_overlap(new_piece):
            return False
        
        self.merge_branches(new_piece)

        return True


    def plot(self):
        """
        Plots the current track in a two-dimensional system of coordinates
        using pyplot from matplotlib.
        """
        if self.start == None:
            return

        queue = [self.start]
        visited = []

        while len(queue):
            cur_node = queue.pop()
            visited.append(cur_node)

            A, B = [], []

            for edge in cur_node.edges:
                if edge.type == 'female':
                    A.append(edge.position)
                else:
                    B.append(edge.position)
                
                if cur_node.connected[edge] != None and cur_node.connected[edge] not in visited:
                    queue.append(cur_node.connected[edge])

            for a in A:
                for b in B:
                    plt.plot([a.x, b.x], [a.y, b.y], 'ro-')
        
    def merge_branches(self, piece):
        """
        Makes the connections when points from given piece overlap with already existing
        points on the track.
        """
        queue = [self.start]
        visited = []

        while len(queue):
            cur_node = queue.pop()
            visited.append(cur_node)

            for edge in cur_node.edges:
                b = edge.position

                for check_edge in piece.edges:
                    a = check_edge.position
                    if a.x == b.x and a.y == b.y and edge.type != check_edge.type:
                        cur_node.connect(edge, piece, check_edge)
            
                if cur_node.connected[edge] != None and cur_node.connected[edge] not in visited:
                    queue.append(cur_node.connected[edge])


    def get_open_edges(self):
        """
        Returns the list of points currently 'in air' on the track.
        """
        if self.start == None:
            return [(self.start, 0)]

        queue = [self.start]
        visited = []

        edge_list = []

        while len(queue):
            cur_node = queue.pop()
            visited.append(cur_node)

            for edge in cur_node.edges:
                if cur_node.connected[edge] == None:
                    edge_list.append((cur_node, cur_node.edges.index(edge)))
            
                if cur_node.connected[edge] != None and cur_node.connected[edge] not in visited:
                    queue.append(cur_node.connected[edge])
        
        return edge_list


