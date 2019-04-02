class UnionFind:
    def __init__(self, n=None, elems=None):
        if n:
            self.parent = [*range(n)]
            self.count = n
        elif elems:
            self.parent = {e: e for e in elems}
            self.count = len(elems)
        else:
            self.parent = {}
            self.count = 0

    def add(self, elem):
        if isinstance(self.parent, list):
            self.parent = {i:e for i,e in enumerate(self.parent)}
        if elem not in self.parent:
            self.parent[elem] = elem
            self.count += 1

    def find(self, p):
        while p != self.parent[p]:
            p = self.parent[p]
        return p

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        root_p, root_q = self.find(p), self.find(q)
        if root_p == root_q: return
        self.parent[root_q] = self.parent[root_p]
        self.count -= 1


class WeightedQuickUnionUF(UnionFind):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = {e: 1 for e in self.parent}

    def add(self, elem):
        if elem not in self.parent:
            self.parent[elem] = elem
            self.count += 1
            self.size[elem] = 1

    def union(self, p, q):
        root_p, root_q = self.find(p), self.find(q)
        if root_p == root_q: return
        if self.size[root_p] < self.size[root_q]:
            root_p, root_q = root_q, root_p
        self.parent[root_q] = self.parent[root_p]
        self.size[root_p] += self.size[root_q]
        self.count -= 1

class WeightedQuickUnionPathCompressionUF(WeightedQuickUnionUF):
    def find(self, p):
        root = p
        while root != self.parent[root]:
            root = self.parent[root]
        while p != root:
            self.parent[p], p = root, self.parent[p]
        return p