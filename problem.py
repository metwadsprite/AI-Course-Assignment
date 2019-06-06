import objects as obj
from copy import deepcopy


class ProblemState:
    def __init__(self, track, pieces_qty):
        self.track = track
        self.pieces_qty = pieces_qty


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
            return True
        else:
            is_empty = True
            for val in state.pieces_qty:
                if state.pieces_qty[val] != 0:
                    is_empty = False

            return is_empty

    def h(self, state):
        return len(state.track.get_open_edges())


class TreeNode:
    
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

        print(self.depth)

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
    