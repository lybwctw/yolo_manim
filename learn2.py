from manim import *
import numpy as np

def create(n=5):
    data = np.random.randn(n, 4)
    table = DecimalTable(
            data,
            col_labels=[
                Text('first'),
                Text('second'),
                Text('third'),
                Text('forth'),
            ],
            element_to_mobject_config={
                'num_decimal_places': 2,
            },
            include_outer_lines=True,
        ).scale(0.5)
    table.remove(*table.get_vertical_lines())
    for i, line in enumerate(table.get_horizontal_lines()):
        if i not in (0, 1, 2, len(table.get_horizontal_lines())):
            table.remove(line)
            # line.set_opacity(0.)
        else:
            line.set_stroke(width=2)

    mobs = table.get_entries()
    mobs.set_opacity(0.3)
    return table

class TableExamples(Scene):
    def construct(self):
        m1 = create(5)
        m2 = create(7)

        self.add(m1)
        self.wait()
        self.play(TransformMatchingShapes(m1, m2))
        self.wait()