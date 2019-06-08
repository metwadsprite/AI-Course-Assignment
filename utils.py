import heapq

class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []

        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("order must be either 'min' or max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.heap.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, item):
        """Return True if item in PriorityQueue."""
        return (self.f(item), item) in self.heap

    def __getitem__(self, key):
        for _, item in self.heap:
            if item == key:
                return item

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        self.heap.remove((self.f(key), key))
        heapq.heapify(self.heap)


def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn


def distance(A, B):
    return ((B.x - A.x)**2 + (B.y - A.y)**2)**0.5

def is_on_segment(A, B, point):
    if B.x <= max(A.x, point.x) and B.x >= min(A.x, point.x) and \
        B.y <= max(A.y, point.y) and B.y >= min(A.y, point.y):
        return True
    return False


def orientation(A, B, C):
    """
    Given 3 points (A, B, C) the function returns:
    0 If the points are colinear
    1 If the points are clockwise
    2 If the points are counter-clockwise
    """
    value = (B.y - A.y) * (C.x - B.x) - (B.x - A.x) * (C.y - B.y)

    return 0 if value == 0 else 1 if value > 0 else 2


def is_intersect(A, B, C, D):
    if A.x == C.x and A.y == C.y:
        return False
    if A.x == D.x and A.y == D.y:
        return False
    if B.x == C.x and B.y == C.y:
        return False
    if B.x == D.x and B.y == D.y:
        return False

    orient1 = orientation(A, B, C)
    orient2 = orientation(A, B, D)
    orient3 = orientation(C, D, A)
    orient4 = orientation(C, D, B)

    if orient1 != orient2 and orient3 != orient4:
        return True

    if orient1 == 0 and is_on_segment(A, B, C):
        return True
    if orient2 == 0 and is_on_segment(A, B, D):
        return True
    if orient3 == 0 and is_on_segment(C, D, A):
        return True
    if orient4 == 0 and is_on_segment(C, D, B):
        return True

    return False
