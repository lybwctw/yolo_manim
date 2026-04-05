from manim import *
from utils.explainer_bbox import ExplainerBbox


class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=False,
        )
        # ************************************************************
        background = load_background()
        explainer_bbox = ExplainerBbox()
        bbox_system = Group(background, explainer_bbox)

        # ************************************************************
        self.next_section(
            'anchor points capture thinking',
            skip_animations=False,
        )
        # ************************************************************
        # create grid
        self.play(explainer_bbox.create_grid())
        self.wait()

        # create anchor points, remove grid
        self.play(explainer_bbox.create_anchor_points())
        self.play(explainer_bbox.remove_grid())
        self.wait()

        # anchor points capture
        self.play(explainer_bbox.to_rects())
        self.wait()
        self.play(explainer_bbox.to_dots())
        self.wait()

        # show annotation
        self.play(explainer_bbox.create_annotation())
        self.wait()

        # FIXME, inside anchor points capture
        explainer_bbox.save_state()
        self.play(explainer_bbox.highlight_key_aps())
        self.wait()
        self.play(explainer_bbox.key_to_rects())
        self.wait()
        self.play(explainer_bbox.animate.restore())
        self.wait()

        # ************************************************************
        self.next_section(
            'sample, from distance to position',
            skip_animations=False,
        )
        # ************************************************************
        # focus on sample anchor point
        
        # distance to position

        # digit counterpart

        # loop through several samples

        # ************************************************************
        self.next_section(
            'global, from distance to position',
            skip_animations=False,
        )
        # ************************************************************
        # sync, distance generation

        # sync, position generation

        # to thunbnail