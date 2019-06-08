import objects as obj
import utils
from copy import deepcopy


class ProblemState:
    def __init__(self, track, pieces_qty):
        self.track = track
        self.pieces_qty = pieces_qty

    def __lt__(self, state):
        sum_this = 0
        sum_comp = 0
        
        for piece in self.pieces_qty:
            sum_this += self.pieces_qty[piece]
        
        for piece in state.pieces_qty:
            sum_comp += state.pieces_qty[piece]

        return sum_this < sum_comp


class RailTrackProblem:

    def actions(self, state):
        action_list = []

        if state.track.start == None:
            for piece in state.pieces_qty:
                if state.pieces_qty[piece] != 0:
                    state.pieces_qty[piece] -= 1
                    new_state = deepcopy(state)
                    new_state.track.start = deepcopy(piece)
                    state.pieces_qty[piece] += 1

                    action_list.append(new_state)
        else:
            edges = state.track.get_open_edges()

            while len(edges):
                edge = edges.pop()

                for piece in state.pieces_qty:
                    if state.pieces_qty[piece] != 0:
                        state.pieces_qty[piece] -= 1
                        new_state = deepcopy(state)
                        state.pieces_qty[piece] += 1

                        if new_state.track.add_piece(edge[0], edge[1], deepcopy(piece)):
                            action_list.append(new_state)

        return action_list

    def end_test(self, state):
        if len(state.track.get_open_edges()) == 0:
            ret_value = True
            for val in state.pieces_qty:
                if state.pieces_qty[val] != 0:
                    ret_value = False

            return ret_value

    def h(self, state):
        edges = state.track.get_open_edges()
        origin = obj.Point(0, 0)
        sum_dist = 0

        for edge in edges:
            if edge[0] == None:
                return 1
            sum_dist += utils.distance(edge[0].position, origin)
        
        return len(edges) + sum_dist


class TreeNode:
    
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [self.child_node(problem, action) for action in problem.actions(self.state)]
    
    def child_node(self, problem, action):
        return TreeNode(action, self, action)

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    