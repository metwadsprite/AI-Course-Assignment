import matplotlib.pyplot as plt
import search as src
import problem as pb

track_prob = pb.RailTrackProblem()
# final_state = src.bfs(track_prob)
final_state = src.best_first_search(track_prob)
final_state.state.track.plot()
plt.show()