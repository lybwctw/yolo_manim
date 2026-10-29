from manim import *
from utils.constants import *
from utils.general import *

SAMPLE_O_IDX = 8
SAMPLE_I_IDXS = [11, 12, 18, 19]

BEAMS_LENGTH = [3, 7, 6, 5]
BEAMS_UNIT = 0.4
DEFAULT_BEAM_CONFIG = {
    'stroke_width': 3,
    'stroke_color': WHITE,
    'stroke_opacity': 1.0,
}
DEFAULT_RES_BEAM_CONFIG = {
    'stroke_width': 3,
    'stroke_color': PURE_RED,
    'stroke_opacity': 1.0,
}
DEFAULT_BASE_CONFIG = {
    'stroke_width': 2,
    'stroke_color': WHITE,
    'stroke_opacity': 0.3,
}
DEFAULT_CONNECT_CONFIG = {
    'stroke_width': 2,
    'stroke_color': WHITE,
    'stroke_opacity': 0.3,
}
DEFAULT_FLASH_CONFIG = {
    'stroke_width': 2,
    'stroke_color': WHITE,
    'stroke_opacity': 0.3,
}
DEFAULT_DOT_CONFIG = {
    'radius': 0.05,
    'stroke_opacity': 0.0,
    'fill_color': PURE_RED,
    'fill_opacity': 1.0,
}

wt = SHORT_DURATION
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load mobs and torch module
        mobs = import_mobs('009')
        (
            cells_i,
            cells_o,
            dots_i,
            dots_o,
            dots_oi,
        ) = mobs

        self.set_camera_orientation(
            focal_distance=100,
        )
        self.add(
            mobs,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on 5 (4+1) dots',
            skip_animations=False,
        )
        # ************************************************************
        # remove other mobs
        other_i_idxs = [x for x in range(len(dots_i)) if x not in SAMPLE_I_IDXS]
        other_o_idxs = [x for x in range(len(dots_o)) if x != SAMPLE_O_IDX]
        self.play(AnimationGroup(
            *(FadeOut(dots_i[idx]) for idx in other_i_idxs),
            *(FadeOut(dots_oi[idx]) for idx in other_o_idxs),
            FadeOut(dots_o),
            FadeOut(cells_i),
            FadeOut(cells_o),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # focus on dots
        dot_ul = dots_i[SAMPLE_I_IDXS[0]]
        dot_ur = dots_i[SAMPLE_I_IDXS[1]]
        dot_dl = dots_i[SAMPLE_I_IDXS[2]]
        dot_dr = dots_i[SAMPLE_I_IDXS[3]]
        dot_mid = dots_oi[SAMPLE_O_IDX]
        dots = VGroup(dot_ul, dot_ur, dot_dl, dot_dr, dot_mid)

        dots.generate_target()
        dots.target.scale(6.0).center().shift(IN*1)
        for dot in dots.target:
            dot.scale(2/3)

        # focus on dots
        self.move_camera(
            phi=60*DEGREES,
            theta=-75*DEGREES,
            focal_distance=20,
            added_anims=[
                MoveToTarget(dots),
            ],
            run_time=wt,
        )
        # self.wait(wt)

        # prepare beams
        beam_ul = Line(start=dot_ul.get_center(), end=dot_ul.get_center()+BEAMS_LENGTH[0]*OUT*BEAMS_UNIT, **DEFAULT_BEAM_CONFIG)
        beam_ur = Line(start=dot_ur.get_center(), end=dot_ur.get_center()+BEAMS_LENGTH[1]*OUT*BEAMS_UNIT, **DEFAULT_BEAM_CONFIG)
        beam_dl = Line(start=dot_dl.get_center(), end=dot_dl.get_center()+BEAMS_LENGTH[2]*OUT*BEAMS_UNIT, **DEFAULT_BEAM_CONFIG)
        beam_dr = Line(start=dot_dr.get_center(), end=dot_dr.get_center()+BEAMS_LENGTH[3]*OUT*BEAMS_UNIT, **DEFAULT_BEAM_CONFIG)
        beams = VGroup(beam_ul, beam_ur, beam_dl, beam_dr)
        self.play(AnimationGroup(
            Write(beam_ul),
            Write(beam_ur),
            Write(beam_dl),
            Write(beam_dr),
            lag_ratio=0.5,
            run_time=wt,
        ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'up side interpolate',
            skip_animations=False,
        )
        # ************************************************************
        # show base and connection
        base_up = Line(start=dot_ul.get_center(), end=dot_ur.get_center(), **DEFAULT_BASE_CONFIG)
        connect_up = Line(start=beam_ul.get_end(), end=beam_ur.get_end(), **DEFAULT_CONNECT_CONFIG)
        self.play(AnimationGroup(
            Write(base_up),
            Write(connect_up),
            lag_ratio=0.5,
            run_time=wt,
        ))
        # self.wait(wt)

        x1, y1 = dot_ul.get_center()[:2]
        x2, y2 = dot_ur.get_center()[:2]
        z1, z2 = beam_ul.get_end()[2], beam_ur.get_end()[2]
        x, y = dot_mid.get_center()[:2]
        z = ((z2-z1)*x+x2*z1-x1*z2) / (x2-x1)

        p1 = dot_mid.get_center()
        p2_up = p1.copy()
        p2_up[1] = y1
        p3_up = p2_up.copy()
        p3_up[2] = z

        # show path into target joint
        path_up = VMobject(
            **DEFAULT_FLASH_CONFIG,
        ).set_points_as_corners([p1, p2_up, p3_up])
        self.play(AnimationGroup(
            Write(path_up),
            # Create(joint_up),
            # lag_ratio=0.8,
            run_time=wt,
        ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'down side interpolate',
            skip_animations=False,
        )
        # ************************************************************
        # show base and connection
        base_down = Line(start=dot_dl.get_center(), end=dot_dr.get_center(), **DEFAULT_BASE_CONFIG)
        connect_down = Line(start=beam_dl.get_end(), end=beam_dr.get_end(), **DEFAULT_CONNECT_CONFIG)
        self.play(AnimationGroup(
            Write(base_down),
            Write(connect_down),
            lag_ratio=0.5,
            run_time=wt,
        ))
        # self.wait(wt)

        x1, y1 = dot_dl.get_center()[:2]
        x2, y2 = dot_dr.get_center()[:2]
        z1, z2 = beam_dl.get_end()[2], beam_dr.get_end()[2]
        x, y = dot_mid.get_center()[:2]
        z = ((z2-z1)*x+x2*z1-x1*z2) / (x2-x1)

        p1 = dot_mid.get_center()
        p2_down = p1.copy()
        p2_down[1] = y1
        p3_down = p2_down.copy()
        p3_down[2] = z

        # show path into target joint
        path_down = VMobject(
            **DEFAULT_FLASH_CONFIG,
        ).set_points_as_corners([p1, p2_down, p3_down])
        self.play(AnimationGroup(
            Write(path_down),
            # Create(joint_down),
            # lag_ratio=0.8,
            run_time=wt,
        ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'mid side interpolate',
            skip_animations=False,
        )
        # ************************************************************
        # show base and connection
        connect = Line(start=p3_down, end=p3_up, **DEFAULT_CONNECT_CONFIG)
        self.play(AnimationGroup(
            Write(connect),
            run_time=wt,
        ))
        # self.wait(wt)

        p1 = dot_mid.get_center()
        y1, z1 = p3_up[1:]
        y2, z2 = p3_down[1:]
        y = p1[1]
        z = ((z2-z1)*y+y2*z1-y1*z2) / (y2-y1)
        p2 = p1.copy()
        p2[2] = z

        dot_final = Dot(
            **DEFAULT_DOT_CONFIG,
        ).move_to(p2)

        # show path into result
        beam_final = VMobject(
            **DEFAULT_RES_BEAM_CONFIG,
        ).set_points_as_corners([p1, p2])
        self.play(Write(beam_final, run_time=wt))
        self.play(Create(dot_final, run_time=wt))

        # new perspective
        self.move_camera(
            theta=-15*DEGREES,
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            Unwrite(path_down),
            Unwrite(path_up),
            Unwrite(connect),
            Unwrite(base_down),
            Unwrite(connect_down),
            Unwrite(base_up),
            Unwrite(connect_up),
            lag_ratio=0.1,
            run_time=wt
        ))
        # self.wait(wt)

        self.play(AnimationGroup(
            FadeOut(dot_final),
            Unwrite(beam_final),
            Unwrite(beam_ul),
            Unwrite(beam_ur),
            Unwrite(beam_dl),
            Unwrite(beam_dr),
            AnimationGroup(
                FadeOut(dot_mid),
                FadeOut(dot_ul),
                FadeOut(dot_ur),
                FadeOut(dot_dl),
                FadeOut(dot_dr),
            ),
            lag_ratio=0.1,
            run_time=wt,
        ))
        self.wait(wt)