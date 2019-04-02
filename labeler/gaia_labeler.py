from IPython.display import Javascript, display
from labeler.labeler import Labeler
from labeler.label_cluster import LabelCluster


class GAIALabeler(Labeler):
    def __init__(self, base_entity, candidates, template, default=False):
        pair_candidates = [(base_entity, candidate) for candidate in candidates]
        super().__init__(pair_candidates, template, default=default)
        self.path_prefix = '/lfs1/jupyterhub_data_dir/share/'
        self.save_path.description = self.path_prefix
        self.save_path.style.description_width = 'initial'
        self.save_path.layout.width = '350px'

    def on_save_button_clicked(self, b):
        self.labels[self.index] = self.label_button.value

        if self.save_path.value:
            path = self.path_prefix + self.save_path.value
            self.save_labels(path)
        else:
            with self.label_out:
                display(Javascript("alert('Please fill filename!')"))
            self.update_out()

    def __dump_label_cluster(self, keep_singleton=False):
        lc = LabelCluster(keep_singleton)
        for (e1, e2), label in zip(self.candidates, self.labels):
            lc.add_label(e1.id, e2.id, label)
        return lc

    def dump_clusters(self, keep_singleton=False):
        lc = self.__dump_label_cluster(keep_singleton)
        return lc.dump_clusters()

    def dump_json_lines(self, path, keep_singleton=False):
        lc = self.__dump_label_cluster(keep_singleton)
        lc.dump_clusters_json_lines(path)

    @staticmethod
    def parse_label_files(paths, keep_singleton=False):
        if isinstance(paths, str):
            paths = [paths]
        lc = LabelCluster(keep_singleton)
        for path in paths:
            lc.add_label_file(path)
        return lc

