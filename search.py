import objects as obj
import problem as pb
from collections import deque
import json
from collections import namedtuple
import utils


with open('track_pieces.json') as track_pieces_file:
    json_string = track_pieces_file.read()
    track_pieces = json.loads(json_string, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

pieces = []
piece_qty = dict()

for piece in track_pieces:
    piece_edges = []
    
    for edge in piece.edges:
        piece_edges.append(obj.Edge(edge.type, edge.angle, obj.Point(edge.position.x, edge.position.y)))
    
    pieces.append(obj.TrackPiece(piece_edges))
    piece_qty[pieces[-1]] = piece.count


def bfs(problem):
    frontier = deque([pb.TreeNode(pb.ProblemState( obj.Track(), piece_qty ))])

    while frontier:
        node = frontier.popleft()
        if problem.end_test(node.state):
            return node
        
        frontier.extend(node.expand(problem))
    return None


def informed_bfs(problem, f):
    f = utils.memoize(f, 'f')
    node = pb.TreeNode(pb.ProblemState( obj.Track(), piece_qty ))

    if problem.end_test(node.state):
        return node
    
    frontier = utils.PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.end_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None


def astar(problem, h=None):
    h = utils.memoize(h or problem.h, 'h')
    return informed_bfs(problem, lambda  n: n.depth + h(n.state))
