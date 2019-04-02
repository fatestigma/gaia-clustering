from labeler.union_find import WeightedQuickUnionPathCompressionUF
from collections import defaultdict
import json


class LabelCluster(WeightedQuickUnionPathCompressionUF):
    def __init__(self, keep_singleton=True):
        super().__init__()
        self.keep_singleton=keep_singleton

    def find(self, p):
        if p not in self.parent:
            self.add(p)
        return super().find(p)

    def add_label_file(self, path):
        """
        Input tsv file that format in `id1\tid2\tlabel`, like `uri1 uri2    1`.
        """
        with open(path) as f:
            for line in f.readlines():
                id1, id2, lbl = line.strip().split('\t')
                label = lbl == '1'
                self.add_label(id1, id2, label)

    def add_label(self, id1, id2, label):
        if label:
            self.union(id1, id2)
        elif self.keep_singleton:
            self.add(id1)
            self.add(id2)

    def dump_clusters(self):
        clusters = defaultdict(list)
        for p in self.parent:
            clusters[self.find(p)].append(p)
        return list(clusters.values())

    def dump_clusters_json_lines(self, path):
        clusters = self.dump_clusters()
        clusters_json = [json.dumps(cluster) + '\n' for cluster in clusters]
        with open(path, 'w') as f:
            f.writelines(clusters_json)


if __name__ == '__main__':
    lc = LabelCluster()
    lc.union(1, 2)
    print(lc.parent)
    lc.union(2, 3)
    lc.union(4, 5)
    lc.add(6)
    print(lc.parent)
    print(lc.dump_clusters())
