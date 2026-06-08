from manim import *
import numpy as np


def corner_path(t, radius=1.5, start_x=-4, mid_y=0, end_y=4):
    """Parametric L-shaped path: horizontal then quarter-circle up."""
    if t <= 0.5:
        p = 2 * t
        x = start_x + (0 - start_x) * p
        y = 0
    else:
        p = 2 * (t - 0.5)
        # quarter circle from angle -pi/2 to 0 to pi/2
        angle = -PI / 2 + p * (PI / 2)
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
    return np.array([x, y, 0])


def tangent_angle(t, eps=1e-3):
    p1 = corner_path(max(0, t - eps))
    p2 = corner_path(min(1, t + eps))
    v = p2 - p1
    return np.arctan2(v[1], v[0])


def semicircle(radius=1.0, n_points=60):
    pts = []
    for a in np.linspace(PI, 2 * PI, n_points):
        pts.append([radius * np.cos(a), radius * np.sin(a), 0])
    # close back to center
    pts.append([0, 0, 0])
    m = VMobject()
    m.set_points_as_corners(pts + [pts[0]])
    m.close_path()
    m.set_fill(BLUE, opacity=0.8)
    m.set_stroke(BLUE_E, 2)
    return m


def cashew_like():
    # two overlapping circles with a small connector to look cashew-like
    c1 = Circle(radius=1.0).shift(LEFT * 0.5 + DOWN * 0.2)
    c2 = Circle(radius=0.7).shift(RIGHT * 0.7 + UP * 0.1)
    grp = VGroup(c1, c2)
    grp.set_fill(YELLOW, opacity=0.8)
    grp.set_stroke(YELLOW_D, 2)
    return grp


def gerver_approx():
    # rough approximation of Gerver's sofa via smoothed polygon
    pts = [
        [-1.8, -0.2, 0],
        [-1.0, -0.9, 0],
        [-0.2, -1.0, 0],
        [0.8, -0.6, 0],
        [1.4, 0.2, 0],
        [0.9, 1.1, 0],
        [0.1, 1.6, 0],
        [-0.9, 1.4, 0],
        [-1.6, 0.8, 0],
    ]
    poly = VMobject()
    poly.set_points_as_corners(pts + [pts[0]])
    poly.make_smooth()
    poly.set_fill(GREEN, opacity=0.9)
    poly.set_stroke(GREEN_D, 2)
    return poly


class MovingSofaDemo(Scene):
    def construct(self):
        # Corridor: horizontal left and vertical up, width 2
        horiz = Rectangle(width=6, height=2).shift(LEFT * 1.5)
        vert = Rectangle(width=2, height=6).shift(UP * 1.5)
        corridor = VGroup(horiz, vert)
        corridor.set_fill(GREY_E, opacity=0.6)
        corridor.set_stroke(GREY_BROWN, 2)

        title = Text("Moving Sofa: Trial Shapes demo").to_edge(UP)

        self.add(corridor, title)

        # Define shapes
        sq = Square(side_length=2).set_fill(ORANGE, opacity=0.9).set_stroke(ORANGE, 2)
        semi = semicircle(radius=1.0).scale(1.1)
        cashew = cashew_like()
        gerver = gerver_approx().scale(1.0)

        shapes = [sq, semi, cashew, gerver]
        labels = ["Square", "Semi-circle", "Cashew-like", "Gerver approx"]

        # Starting positions (stacked left)
        start_x = -5
        stack = VGroup()
        for i, s in enumerate(shapes):
            s_copy = s.copy()
            s_copy.move_to([start_x, 2 - i * 1.6, 0])
            lbl = Text(labels[i], font_size=24).next_to(s_copy, RIGHT)
            stack.add(VGroup(s_copy, lbl))
        self.play(FadeIn(stack, shift=LEFT))
        self.wait(0.6)

        # helper to animate a trial: move shape along path until fail_t then flash
        def run_trial(mob, fail_t=0.9, success=False, run_time=6):
            tracker = ValueTracker(0)

            def updater(m):
                t = tracker.get_value()
                if not success:
                    t = min(t, fail_t)
                pos = corner_path(t)
                ang = tangent_angle(t)
                m.move_to(pos)
                m.set_angle(ang)

            mob.add_updater(updater)

            # animate forward
            self.play(tracker.animate.set_value(1), run_time=run_time, rate_func=linear)
            if not success:
                # flash red to indicate collision
                self.play(mob.animate.set_fill(RED, opacity=0.9), run_time=0.25)
                self.wait(0.2)
                # retreat
                self.play(tracker.animate.set_value(0), run_time=run_time * 0.4)
                self.play(mob.animate.set_fill(mob.get_fill_color(), opacity=0.8), run_time=0.2)
            mob.remove_updater(updater)

        # Sequentially take each shape from stack and trial it
        for i, grp in enumerate(stack):
            shape_mob = grp[0]
            lbl = grp[1]
            # bring to front and scale for trial
            self.play(shape_mob.animate.scale(1.0).move_to([-4, 0, 0]), lbl.animate.next_to(shape_mob, RIGHT))
            self.wait(0.2)
            if i < 3:
                # failing shapes: set fail points progressively closer
                fail_t = 0.6 + 0.1 * i
                run_trial(shape_mob, fail_t=fail_t, success=False, run_time=4)
            else:
                # last shape - success
                run_trial(shape_mob, success=True, run_time=6)
            self.play(shape_mob.animate.scale(0.7).move_to([2.5, 2 - i * 0.9, 0]), lbl.animate.next_to(shape_mob, RIGHT))
            self.wait(0.2)

        # Final scene: show all four with annotations
        final_note = Text("From simple trials to best-known shape (approx)", font_size=28).to_edge(DOWN)
        self.play(FadeIn(final_note))
        self.wait(2)


if __name__ == "__main__":
    print("Run with: manim -pql moving_sofa_demo.py MovingSofaDemo")
