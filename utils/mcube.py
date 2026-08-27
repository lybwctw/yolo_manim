from __future__ import annotations

from manim import *

DEFAULT_CUBE_CONFIG = {
    'fill_color': BLACK,
    'fill_opacity': 0.8,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
TARNISH_CUBE_CONFIG = {
    'fill_opacity': 0.0,
    'stroke_width': 1.0,
    'stroke_opacity': 0.05,
}

DEFAULT_SQUARE_CONFIG = {
    'fill_color': BLACK,
    'fill_opacity': 0.8,
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
TARNISH_SQUARE_CONFIG = {
    'fill_opacity': 0.0,
    'stroke_width': 1.0,
    'stroke_opacity': 0.05,
}

DEFAULT_DECIMAL_CONFIG = {
    'fill_opacity': 1.0,
    'num_decimal_places': 2,
    'mob_class': MathTex,
    'include_sign': True,
    'align_to_dot': True,
}
DEFAULT_INFINITY_CONFIG = {
    'fill_opacity': 1.0,
}

TARNISH_DECIMAL_CONFIG = {
    'fill_opacity': 0.3,
}

# cube update related
MID_SCALE = 0.5

class MCube(VMobject):
    def __init__(
        self,
        value: float = 0.0,
        mode: str = 'cube',
        z_index: float = 0.0,
        side_length: float = 0.5,
        font_size: float = 18,
        cube_config: dict = {},
        square_config: dict = {},
        decimal_config: dict = {},
        infinity_config: dict = {},
    ):
        super().__init__()
        self.value = value
        self.mode = mode
        self.z_index = z_index

        self.side_length = side_length
        self.font_size = font_size

        self.cube_config = {**DEFAULT_CUBE_CONFIG, **cube_config}
        self.square_config = {**DEFAULT_SQUARE_CONFIG, **square_config}
        self.decimal_config = {**DEFAULT_DECIMAL_CONFIG, **decimal_config}
        self.infinity_config = {**DEFAULT_INFINITY_CONFIG, **infinity_config}

        self.tarnished = False

        if mode == 'cube':
            cube_config = {**self.cube_config, 'side_length': self.side_length}
            mob = Cube(**cube_config)
            mob.set_z_index(self.z_index)
        elif mode == 'card':
            square_config = {**self.square_config, 'side_length': self.side_length}
            decimal_config = {**self.decimal_config, 'font_size': self.font_size}
            infinity_config = {**self.infinity_config, 'font_size': self.font_size}

            mob_square = Square(**square_config)
            if np.isposinf(self.value):
                mob_value = MathTex(r"\infty", **infinity_config)
            elif np.isneginf(self.value):
                mob_value = MathTex(r"-\infty", **infinity_config)
            else:
                mob_value = DecimalNumber(self.value, **decimal_config),
            mob = VGroup(
                mob_square,
                mob_value,
            )

            mob[0].set_z_index(self.z_index)
            mob[1].set_z_index(self.z_index+0.1)

        self.mob = mob
        self.add(self.mob)

    def _switch(
        self,
    ):
        """Instant switch without animation.
        """
        if self.mode == 'card':
            self.mode = 'cube'
            stroke_color = self.mob[0].stroke_color # stroke color from square
            cube_config = {
                **self.cube_config,
                'side_length': self.mob.width,
                'stroke_color': stroke_color,       # keep stroke color
            }
            new_mob = Cube(**cube_config).move_to(self.mob)
            new_mob.set_z_index(self.z_index)
            if self.tarnished:
                new_mob.set_style(**TARNISH_CUBE_CONFIG)
        elif self.mode == 'cube':
            self.mode = 'card'
            stroke_color = self.mob.stroke_color   # stroke color from cube
            square_config = {
                **self.square_config,
                'side_length': self.side_length,
                'stroke_color': stroke_color,      # keep stroke color
            }
            decimal_config = {**self.decimal_config, 'font_size': self.font_size}
            infinity_config = {**self.infinity_config, 'font_size': self.font_size}

            mob_square = Square(**square_config)
            if np.isposinf(self.value):
                mob_value = MathTex(r"\infty", **infinity_config)
            elif np.isneginf(self.value):
                mob_value = MathTex(r"-\infty", **infinity_config)
            else:
                mob_value = DecimalNumber(self.value, **decimal_config),
            new_mob = VGroup(
                mob_square,
                mob_value,
            ).move_to(self.mob)

            new_mob[0].set_z_index(self.z_index)
            new_mob[1].set_z_index(self.z_index+0.1)
            if self.tarnished:
                new_mob[0].set_style(**TARNISH_SQUARE_CONFIG)
                new_mob[1].set_style(**TARNISH_DECIMAL_CONFIG)
        old_mob = self.mob
        self.mob = new_mob
        self.remove(old_mob)
        return old_mob

    def switch_instant(
        self,
    ):
        self._switch()
        self.add(self.mob)
    
    def switch(
        self,
        **aargs,
    ) -> Animation:
        old_mob = self._switch()
        return AnimationGroup(
            Unwrite(old_mob),
            Write(self.mob),
            _on_finish=lambda _: self.add(self.mob),
            **aargs,
        )

    def tarnish(
        self,
        **aargs,
    ) -> Animation:
        self.tarnished = True
        if self.mode == 'cube':
            anim = self.mob.animate(
                **aargs,
            ).set_style(**TARNISH_CUBE_CONFIG)
        elif self.mode == 'card':
            anim = AnimationGroup(
                self.mob[0].animate.set_style(
                    **TARNISH_SQUARE_CONFIG,
                ),
                self.mob[1].animate.set_style(
                    **TARNISH_DECIMAL_CONFIG,
                ),
            )
        return anim

    def lightup(
        self,
        **aargs,
    ) -> Animation:
        self.tarnished = False
        if self.mode == 'cube':
            anim = self.mob.animate(
                **aargs,
            ).set_style(**self.lightup_cube_config)
        elif self.mode == 'card':
            anim = AnimationGroup(
                self.mob[0].animate.set_style(
                    **self.lightup_square_config,
                ),
                self.mob[1].animate.set_style(
                    **self.lightup_decimal_config,
                ),
            )
        return anim

    def update_value(
        self,
        value: float | None = None,
        **aargs,
    ) -> Animation:
        assert self.mode == 'card', "update_value only works in 'card' mode"
        if value is None:
            value = np.random.randn()
        self.value = value

        anim = ChangeDecimalToValue(
            self.mob[1],
            self.value,
            **aargs,
        )
        return anim

    def _af_translate(
        self,
        mob,
        alpha,
    ):
        if hasattr(mob, 'saved_state'):
            mob.restore()
        else:
            mob.save_state()

        target_scale = 1.0 + (MID_SCALE-1.0)*there_and_back(alpha)

        mob.scale(target_scale)
        mob.rotate(90 * DEGREES * smooth(alpha), OUT)

    def translate(
        self,
        **aargs,
    ) -> Animation:
        assert self.mode == 'cube', "translate only works in 'cube' mode"
        anim = UpdateFromAlphaFunc(
            self.mob,
            self._af_translate,
            **aargs,
        )
        return anim

    def breath(
        self,
        **aargs,    # run_time
    ) -> Animation:
        assert self.mode == 'cube', "breath only works in 'cube' mode"
        anim = self.mob.animate(
            rate_func=rate_functions.there_and_back,
            **aargs,
        ).scale(0.8)
        return anim

    @property
    def lightup_cube_config(self):
        return {
            k: self.cube_config[k] for k in [
                'fill_opacity',
                'stroke_width',
                'stroke_opacity',
            ]
        }

    @property
    def lightup_square_config(self):
        return {
            k: self.square_config[k] for k in [
                'fill_opacity',
                'stroke_width',
                'stroke_opacity',
            ]
        }

    @property
    def lightup_decimal_config(self):
        return {
            k: self.decimal_config[k] for k in [
                'fill_opacity',
            ]
        }

class DemoMC(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=60*DEGREES,
            theta=-75*DEGREES,
        )

        cube = MCube(
            value=0.55,
            size=1.5,
            mode='cube',
            square_config={
                'stroke_width': 1,
            },
            decimal_config={
                'font_size': 54,
                'align_to_dot': True,
                # 'stroke_width': 3,
            },
        )
        self.play(Write(cube))
        self.wait()

        self.play(cube.switch(
            run_time=1.0,
        ))
        self.wait()

        self.play(cube.tarnish(
            run_time=1.0,
        ))
        self.wait()

        self.play(cube.update_value(
            -9.32,
            run_time=1.0,
        ))
        self.wait()

        self.play(cube.switch(
            run_time=1.0,
        ))
        self.wait()

        self.play(cube.lightup(
            run_time=1.0,
        ))
        self.wait()

