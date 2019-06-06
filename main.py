import objects as obj
import matplotlib.pyplot as plt
from copy import deepcopy
import random
from search import bfs
import problem as pb

track_prob = pb.RailTrackProblem()
final_state = bfs(track_prob)
final_state.state.track.plot()
plt.show()