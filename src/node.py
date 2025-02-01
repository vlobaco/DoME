
_operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }

class Node:

    def __init__(self, type, value = None):
        self._right_child = None
        self._left_child = None
        self.parent = None
        self.value = value
        self.type = type
        self.aes = None
        self.bs = None
        self.cs = None
        self.ds = None
        self.Ss = None
        self.semantics = None
        self.sme = None
        self._is_left_child = False
        if type in _operations.keys():
            operation = _operations[type]
            self._operation = lambda lefts, rights: [operation(left,right) for left, right in zip(lefts, rights)]
        
    def set_left_child(self, left_child):
        self._left_child = left_child
        left_child._is_left_child = True
        left_child.parent = self

    @property
    def left_child(self):
        return self._left_child
    
    def set_right_child(self, right_child):
        self._right_child = right_child
        right_child.parent = self

    @property
    def right_child(self):
        return self._right_child
        
    def update_semantics(self, observations):
        if self.type == "terminal":
            if isinstance(self.value, int) or isinstance(self.value, float):
                self.semantics = [self.value] * len(observations)
            else:
                self.semantics = observations
        else:
            if self.left_child and self.right_child:
                self.left_child.update_semantics(observations)
                self.right_child.update_semantics(observations)
                self.semantics = self._operation(
                    self.left_child.semantics,
                    self.right_child.semantics
                )
    
    def update_sme(self, targets):
        number_of_targets = len(targets)
        if self.parent:
            parent = self.parent
            parent_aes = parent.aes
            parent_bs = parent.bs
            parent_cs = parent.cs
            parent_ds = parent.ds
            parent_Ss = parent.Ss
            #if the node is the left child
            if self._is_left_child:
                ys = parent.right_child.semantics
                if parent.type == "+":
                    self.aes = parent_aes.copy()
                    self.bs = [parent_b - parent_a * y for parent_a, parent_b, y 
                                in zip(parent_aes, parent_bs, ys)]
                    self.cs = parent_cs.copy()
                    self.ds = [parent_d - parent_c * y for parent_c, parent_d, y 
                                in zip(parent_cs, parent_ds, ys)]
                    self.Ss = {tuple(s - y  for s, y in zip(parent_S, ys)) for parent_S in parent_Ss}
                elif parent.type == "-":
                    self.aes = parent_aes.copy()
                    self.bs = [parent_b + parent_a * y for parent_a, parent_b, y in zip(parent_aes, parent_bs, ys)]
                    self.cs = parent_cs.copy()
                    self.ds = [parent_d + parent_c * y for parent_c, parent_d, y in zip(parent_cs, parent_ds, ys)]
                    self.Ss = {tuple(s + y  for s, y in zip(parent_S, ys)) for parent_S in parent_Ss}
                elif parent.type == "*":
                    self.aes = [parent_a * y for parent_a, y in zip(parent_aes, ys)]
                    self.bs = parent_bs.copy()
                    self.cs = [parent_c * y for parent_c, y in zip(parent_cs, ys)]
                    self.ds = parent_ds.copy()
                    self.Ss = {tuple(s / y  for s, y in zip(parent_S, ys)) for parent_S in parent_Ss}
                elif parent.type == "/":
                    self.aes = parent_aes.copy()
                    self.bs = [parent_b * y for parent_b, y in zip(parent_bs, ys)]
                    self.cs = parent_cs.copy()
                    self.ds = [parent_d * y for parent_d, y in zip(parent_ds, ys)]
                    self.Ss = {tuple(s * y  for s, y in zip(parent_S, ys)) for parent_S in parent_Ss}
            #if the node is the right child
            else:
                xs = parent.left_child.semantics
                if parent.type == "+":
                    self.aes = parent_aes.copy()
                    self.bs = [parent_b - parent_a * x for parent_a, parent_b, x in zip(parent_aes, parent_bs, xs)]
                    self.cs = parent_cs.copy()
                    self.ds = [parent_d - parent_c * x for parent_c, parent_d, x in zip(parent_cs, parent_ds, xs)]
                    self.Ss = {tuple(s - x for s, x in zip(parent_S, xs)) for parent_S in parent_Ss}
                elif parent.type == "-":
                    self.aes = parent_aes.copy()
                    self.bs = [parent_a * x - parent_b for parent_a, parent_b, x in zip(parent_aes, parent_bs, xs)]
                    self.cs = parent_cs.copy()
                    self.ds = [parent_c * x - parent_d for parent_c, parent_d, x in zip(parent_cs, parent_ds, xs)]
                    self.Ss = {tuple(x - s for s, x in zip(parent_S, xs)) for parent_S in parent_Ss}
                elif parent.type == "*":
                    self.aes = [parent_a * x for parent_a, x in zip(parent_aes, xs)]
                    self.bs = parent_bs.copy()
                    self.cs = [parent_c * x for parent_c, x in zip(parent_cs, xs)]
                    self.ds = parent_ds.copy()
                    self.Ss = {tuple(s / x  for s, x in zip(parent_S, xs)) for parent_S in parent_Ss}
                elif parent.type == "/":
                    self.aes = parent_bs.copy()
                    self.bs = [parent_a * x for parent_a, x in zip(parent_aes, xs)]
                    self.cs = parent_ds.copy()
                    self.ds = [parent_c * x for parent_c, x in zip(parent_cs, xs)]
                    self.Ss = {tuple(x / s for s, x in zip(parent_S, xs)) for parent_S in parent_Ss}
                    self.Ss.add(tuple(0 for _ in range(number_of_targets)))
        else:
            # if the node is the root
            self.aes = [1] * number_of_targets
            self.bs = targets.copy()
            self.cs = [0] * number_of_targets
            self.ds = [-1] * number_of_targets
            self.Ss = set()
        
        self.sme = self._sme()
        if self.left_child:
            self.left_child.update_sme(targets)
        if self.right_child:
            self.right_child.update_sme(targets)
        
    def _sme(self):
        return 1/len(self.semantics)*sum(
                ((a * semantic - b) / (c * semantic - d)) ** 2
                for a, b, c, d, semantic in zip(self.aes, self.bs, self.cs, self.ds, self.semantics)
                )