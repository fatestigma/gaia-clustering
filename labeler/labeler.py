import ipywidgets as widgets
from IPython.display import HTML, Javascript, display

class Labeler:
    def __init__(self, candidates, template1, template2=None, default=False):
        self.candidates = candidates
        self.labels = [default] * len(self.candidates)
        self.index = 0

        self.template1 = template1
        self.template2 = template2 if template2 else template1

        self.__create_view_components()

    @classmethod
    def load_ground_truth(cls, ds1, ds2, path, template1, template2=None):
        candidates = []
        labels = []
        with open(path) as f:
            for line in f.readlines():
                id1, id2, lbl = line.strip().split('\t')
                e1 = ds1.get_record(id1)
                e2 = ds2.get_record(id2)
                label = lbl == '1'
                candidates.append((e1, e2))
                labels.append(label)
        labeler = cls(candidates, template1, template2)
        labeler.labels = labels
        return labeler

    def build_view(self):
        self.__init_view_components()

        out_box = widgets.HBox([self.reference_out, self.label_out])
        nav_box = widgets.HBox([self.prev_button, self.nav_label, self.next_button])
        save_box = widgets.HBox([self.save_path, self.save_button], layout={'margin': '10px 0 0 0'})

        return widgets.VBox([nav_box, self.label_button, out_box, save_box])

    def __create_view_components(self):
        self.reference_out = widgets.Output(layout={'border': '1px solid black', 'width': '50%'})
        self.label_out = widgets.Output(layout={'border': '1px solid black', 'width': '50%'})

        self.label_button = widgets.ToggleButtons(options=[True, False])
        self.nav_label = widgets.Label(value="")
        self.prev_button = widgets.Button(description="Prev")
        self.next_button = widgets.Button(description="Next")

        self.save_path = widgets.Text(value='', placeholder='Save to ...', layout={'width': '150px'})
        self.save_button = widgets.Button(description="Save", button_style='danger')

    def __init_view_components(self):
        self.next_button.on_click(self.on_nav_button_clicked)
        self.prev_button.on_click(self.on_nav_button_clicked)
        self.save_button.on_click(self.on_save_button_clicked)
        self.label_button.observe(self.on_label_button_change, 'value')

        self.prev_button.disabled = True
        self.next_button.disabled = not self.__has_next()

        self.reference_out.clear_output()
        self.label_out.clear_output()
        with self.label_out:
            print("")
        with self.reference_out:
            print("")

        self.update_out()

    def update_out(self):
        self.reference_out.clear_output(wait=True)
        self.label_out.clear_output(wait=True)
        e1, e2 = self.candidates[self.index]
        self.reference_out.append_display_data(self.get_entity_html_description(e1, self.template1))
        self.label_out.append_display_data(self.get_entity_html_description(e2, self.template2))

        self.__update_nav_label()
        self.label_button.value = self.labels[self.index]

    def on_nav_button_clicked(self, b):
        if b.description == 'Next':
            if self.__has_next():
                self.index += 1
        else:
            if self.__has_prev():
                self.index -= 1
        self.next_button.disabled = not self.__has_next()
        self.prev_button.disabled = not self.__has_prev()
        self.update_out()

    def __has_next(self):
        return self.index < len(self.candidates) - 1

    def __has_prev(self):
        return self.index > 0

    def __update_nav_label(self):
        self.nav_label.value = "{}/{}".format(self.index+1, len(self.candidates))

    def on_save_button_clicked(self, b):
        if self.save_path.value:
            path = self.save_path.value
            self.save_labels(path)
        else:
            with self.label_out:
                display(Javascript("alert('Please fill filename!')"))
            self.update_out()

    def on_label_button_change(self, change):
        self.labels[self.index] = change['new']

    def save_labels(self, path):
        ground_truth = ['{}\t{}\t{}\n'.format(e1.id, e2.id, int(label))
                        for (e1, e2), label in zip(self.candidates, self.labels)]
        with open(path, 'w') as f:
            f.writelines(ground_truth)

    def get_entity_html_description(self, record, template):
        html_string = ''
        for title, attr in template:
            if isinstance(attr, str):
                content = getattr(record, attr)
            else:
                content = attr(record)
            if not content: continue
            html_string += '<b>{}</b>: {}<br />'.format(title, content)
        return HTML(html_string)

