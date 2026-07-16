from manim import *
from utils.mtensor import MCube, MTensor_4D
from utils.show_shape import HideShape
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.general import import_mobs, export_mobs
from utils.layers_fake import LayersFake
from utils.arrow_comment import ArrowComment
from utils.constants_3d import *

BUFF_LAYER_2D = 0.08
BUFF_LAYER_3D = 0.13
BUFF_MOB_H = 0.6
BUFF_MOB_W = 0.8

CENTER_MOB = RIGHT*0.6

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # TODO, introduce top-left corner image as reference
        # ************************************************************
        self.next_section(
            'init mobs from 2d version',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('025')
        (
                            t8_distrib,  t8_prob,
        tin_norm, act_game, t16_distrib, t16_prob,
                            t32_distrib, t32_prob,
        ) = mobs

        t16_distrib = LayersFake(
            n=8,
            ref=t16_distrib,
            expanded=True,
            buff=BUFF_LAYER_2D,
            width_nominal=40,
            height_nominal=40,
            depth_nominal=64,
        ).center()
        t8_distrib = LayersFake(
            n=8,
            ref=t8_distrib,
            expanded=True,
            buff=BUFF_LAYER_2D,
            width_nominal=80,
            height_nominal=80,
            depth_nominal=64,
        ).next_to(t16_distrib, UP, buff=BUFF_MOB_H)
        t32_distrib = LayersFake(
            n=8,
            ref=t32_distrib,
            expanded=True,
            buff=BUFF_LAYER_2D,
            width_nominal=20,
            height_nominal=20,
            depth_nominal=64,
        ).next_to(t16_distrib, DOWN, buff=BUFF_MOB_H)

        act_game = ArrowComment(
            double=False,
            direction=RIGHT,
            comment='?',
            arrow_config={},
        ).scale(0.5).next_to(t16_distrib, LEFT, buff=BUFF_MOB_W)

        tin_norm = LayersFake(
            n=3,
            ref=tin_norm,
            expanded=True,
            buff=0.08,
            width_nominal=640,
            height_nominal=640,
            depth_nominal=3,
        ).next_to(act_game, LEFT, buff=BUFF_MOB_W)

        t8_prob = LayersFake(
            n=8,
            ref=t8_prob,
            expanded=True,
            buff=BUFF_LAYER_2D,
            width_nominal=80,
            height_nominal=80,
            depth_nominal=3,
        ).next_to(t8_distrib, RIGHT, BUFF_MOB_W)

        t16_prob = LayersFake(
            n=8,
            ref=t16_prob,
            expanded=True,
            buff=BUFF_LAYER_2D,
            width_nominal=40,
            height_nominal=40,
            depth_nominal=3,
        ).next_to(t16_distrib, RIGHT, BUFF_MOB_W)

        t32_prob = LayersFake(
            n=8,
            ref=t32_prob,
            expanded=True,
            buff=BUFF_LAYER_2D,
            width_nominal=20,
            height_nominal=20,
            depth_nominal=3,
        ).next_to(t32_distrib, RIGHT, BUFF_MOB_W)

        mobs = VGroup(
                                t8_distrib,  t8_prob,
            tin_norm, act_game, t16_distrib, t16_prob,
                                t32_distrib, t32_prob,
        ).shift(CENTER_MOB)
        t_mobs = VGroup(
                      t8_distrib,  t8_prob,
            tin_norm, t16_distrib, t16_prob,
                      t32_distrib, t32_prob,
        )

        self.add(mobs)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'another perspective',
            skip_animations=False,
        )
        # ************************************************************
        for mob in mobs:
            mob.generate_target()
        
        t16_distrib.target.rects.arrange(IN, buff=BUFF_LAYER_3D).shift(CENTER_MOB)
        t8_distrib.target.rects.arrange(IN, buff=BUFF_LAYER_3D).next_to(t16_distrib.target, OUT, buff=BUFF_MOB_H*2)
        t32_distrib.target.rects.arrange(IN, buff=BUFF_LAYER_3D).next_to(t16_distrib.target, IN, buff=BUFF_MOB_H*2)
        act_game.target.rotate(90*DEGREES, axis=RIGHT).next_to(t16_distrib.target, LEFT, buff=BUFF_MOB_W*1.5)
        # act_game.target.shift(DOWN*0.3)
        tin_norm.target.rects.arrange(IN, buff=BUFF_LAYER_3D).next_to(act_game.target, LEFT, buff=BUFF_MOB_W*1.5)
        # tin_norm.target.shift(DOWN*0.3)
        t16_prob.target.rects.arrange(IN, buff=BUFF_LAYER_3D).next_to(t16_distrib.target, RIGHT, buff=BUFF_MOB_W*1.5)
        # t16_prob.target.shift(UP*0.3)
        t8_prob.target.rects.arrange(IN, buff=BUFF_LAYER_3D).next_to(t16_prob.target, OUT, buff=BUFF_MOB_H*2)
        t32_prob.target.rects.arrange(IN, buff=BUFF_LAYER_3D).next_to(t16_prob.target, IN, buff=BUFF_MOB_H*2)
        
        self.move_camera(
            **VIEW_INTRO,
            added_anims=[AnimationGroup(
                *(MoveToTarget(mob) for mob in mobs),
                lag_ratio=0.0,
                run_time=wt,
            )],
            run_time=wt,
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'shapes',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(ShowShape3D(
                self,
                mob,
                aargs={'lag_ratio': 0.5},
            ) for mob in t_mobs),
             lag_ratio=0.0,
             run_time=wt,
        ))
        self.wait(wt)

        self.play(AnimationGroup(
            *(HideShape(
                mob,
                aargs={'lag_ratio': 0.0},
            ) for mob in t_mobs),
             lag_ratio=0.0,
             run_time=wt,
        ))
        self.wait(wt)