import abstractions as abstr
import matplotlib.pyplot as plt
from copy import deepcopy
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
        piece_edges.append(abstr.Edge(edge.type, edge.angle, abstr.Point(edge.position.x, edge.position.y)))
    
    pieces.append(abstr.TrackPiece(piece_edges))
    piece_qty[pieces[-1]] = piece.count


track = abstr.Track()
track.plot()

plt.show()