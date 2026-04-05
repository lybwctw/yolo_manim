from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything
from utils.image_pad import ImageRepad, ImageRaw

# def get_ints(n):
#     ds = VGroup(
#         *(Integer(np.random.randint(0, 256)) for _ in range(n*n)),
#     ).arrange_in_grid(n, n, buff=(0.6,0.9)).scale(0.3).set_opacity(0.8)
#     return ds

def get_ints(n):
    ds = VGroup(
        *(Integer(np.random.randint(0, 256), stroke_width=.8) for _ in range(n*n)),
    ).arrange_in_grid(n, n, buff=(0.7, 1.0)).scale(0.3)

    center = (n - 1) / 2

    # max possible (di + dj)
    max_dist = 2 * center

    for idx, mob in enumerate(ds):
        i = idx // n
        j = idx % n

        di = abs(i - center)
        dj = abs(j - center)

        dist = max(di, dj)

        t = dist / max_dist

        opacity = 1.0 * (1 - t) + -0.2 * t      # FIXME
        mob.set_opacity(opacity)

    return ds

class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=False,
        )
        # ************************************************************
        (
            image_raw, _,
            ac_a1, _,
            lf_image_raw, _, _,
        ) = load_everything(S007_EVERYTHING)

        self.add(image_raw, ac_a1, lf_image_raw)
        self.wait()

        # ************************************************************
        self.next_section(
            'resize image_raw',
            skip_animations=False,
        )
        # ************************************************************
        raw_copy = image_raw.copy()
        self.play(AnimationGroup(
            ac_a1.animate.set_opacity(0.0),     # TODO, notice
            raw_copy.animate.shift(RIGHT*5).scale(2/3),
        ))
        raw_copy._w = 640
        raw_copy._h = 360
        self.wait()

        self.play(AnimationGroup(
            image_raw.show_passing_flash(),
            raw_copy.show_passing_flash(),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'resize lf_image_raw',
            skip_animations=False,
        )
        # ***********************************************************
        lf_image_repad = lf_image_raw.copy()
        # FIXME, maybe, consider index_z issue
        self.play(
            lf_image_repad.animate.shift(RIGHT*5).scale(2/3),
        )
        lf_image_repad._w = 640
        lf_image_repad._h = 360
        self.wait()

        self.play(AnimationGroup(
            lf_image_raw.show_passing_flash(),
            lf_image_repad.show_passing_flash(),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'prepare for paddings',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            raw_copy.unwrite_shape_texts(),
            lf_image_repad.unwrite_shape_texts(),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'pad image_raw',
            skip_animations=False,
        )
        # ************************************************************
        image_repad = ImageRepad(raw_copy, False)
        self.play(image_repad.show_paddings())
        self.wait()
        self.play(image_repad.show_passing_flash())
        self.wait()

        # ************************************************************
        self.next_section(
            'pad lf_raw',
            skip_animations=False,
        )
        # ************************************************************
        self.play(lf_image_repad.stretch_to_square())
        self.wait()
        self.play(lf_image_repad.show_passing_flash())
        self.wait()

        # ************************************************************
        self.next_section(
            'clean shapes',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            image_raw.unwrite_shape_texts(),
            image_repad.unwrite_shape_texts(),
            lf_image_raw.unwrite_shape_texts(),
            lf_image_repad.unwrite_shape_texts(),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'make room for normed input',
            skip_animations=False,
        )
        # ************************************************************
        g1 = Group(image_raw, lf_image_raw)
        g2 = Group(image_repad, lf_image_repad)
        g3 = lf_image_repad.copy().set_opacity(0)       # for align purpose
        manager = Group(g1, g2, g3)
        self.play(manager.animate.arrange(buff=1.5))
        self.wait()

        # ************************************************************
        self.next_section(
            'generate lf_image_norm',
            skip_animations=False,
        )
        # ************************************************************
        # show fake internal ints of lf_image_repad
        lf_image_repad_ints = get_ints(4).move_to(lf_image_repad).shift(DL*0.1)
        self.play(Write(lf_image_repad_ints, lag_ratio=0))
        lf_image_repad.add(lf_image_repad_ints)
        lf_image_repad.fake_internal = lf_image_repad_ints  # for easier reference
        self.wait()

        # generate lf_image_norm as a copy lf_image_repad
        lf_image_norm = lf_image_repad.copy()
        self.play(lf_image_norm.animate.shift(RIGHT*3.5))       # FIXME, make shift constant
        self.wait()

        # introduce /255
        div_255 = []
        for orig in lf_image_norm.fake_internal:
            # FIXME: color and opacity issue
            d = MathTex('/255', stroke_width=0.8).scale(0.18).next_to(orig, RIGHT, buff=0)
            d.set_opacity(orig.fill_opacity)     # same opacity as target int
            # d.set_fill(color=WHITE)
            # d.set_stroke
            div_255.append(d)
            orig.add(d)
        div_255 = VGroup(*div_255).shift(DOWN*0.05)
        self.play(Write(div_255, lag_ratio=0))
        self.wait()

        # transform (0,255) -> (0,1)
        anims = []
        for orig in lf_image_norm.fake_internal:
            new_value = orig.number / 255
            dec = DecimalNumber(new_value, num_decimal_places=2, stroke_width=.8).scale(0.3)
            dec.set_opacity(orig.fill_opacity)
            dec.move_to(orig).shift(UL*0.03)     # adjust position due to added /255
            anims.append(Transform(orig, dec))

        self.play(AnimationGroup(*anims))
        self.wait()

        # ************************************************************
        self.next_section(
            'generate image_norm',
            skip_animations=False,
        )
        # ************************************************************
        image_norm = image_repad.copy()
        self.play(image_norm.animate.shift(RIGHT*3.5))
        self.wait()

        # ************************************************************
        self.next_section(
            'save for next scene',
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(
            image_raw, image_repad, image_norm,
            lf_image_raw, lf_image_repad, lf_image_norm,
        )
        save_everything(S009_EVERYTHING, everything)