import objects as obj
import problem as pb
from collections import deque
import json
from collections import namedtuple

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