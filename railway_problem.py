import abstractions as abstr
import matplotlib.pyplot as plt
from copy import deepcopy
import json
from collections import namedtuple
import random

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
track.start = deepcopy(pieces[3])

while sum(piece_qty.values()) != 0:
    a = track.get_open_edges()

    while len(a):
        b = a.pop()
        piece = pieces[random.randint(0, 3)]
        if piece_qty[piece] == 0:
            continue
        
        if track.add_piece(b[0], b[1], deepcopy(piece)):
            piece_qty[piece] -= 1

track.plot()
plt.show()