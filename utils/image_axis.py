from manim import *

class LogScalingExample(Scene):
    def construct(self):
        image_path = r'D:\deeplearning\ultralytics-8.3.163\runs\detect\predict25\005_frames\005_1.jpg'

        image = ImageMobject(image_path)
        _img = image.get_pixel_array()
        _height, _width = _img.shape[0], _img.shape[1]
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        image.scale_to_fit_height(3)
        self.add(image)

        _sf = _width / image.width
        ax = Axes(
            x_range=[0, (image.width+1)*_sf/100, image.width*_sf/100],
            y_range=[0, (image.height+1)*_sf/100, image.height*_sf/100],
            x_length=image.width+1,
            y_length=image.height+1,
            tips=True,
            axis_config={
                "include_numbers": True,
                'scaling': LinearBase(100),
                'decimal_number_config': {'num_decimal_places': 0},
            },
            x_axis_config={
                'label_direction': UP,
                'numbers_to_include': [_width],
            },
            # y_axis_config={"scaling": LogBase(custom_labels=True)},
            top_left_origin=True,
        )
        ax_labels = ax.get_axis_labels()

        # x_min must be > 0 because log is undefined at 0.
        # graph = ax.plot(lambda x: x ** 2, x_range=[0.001, 10], use_smoothing=False)
        # self.add(ax, graph)


        # _origin = ax.x_axis.number_to_point(
        #     ax._origin_shift([ax.x_axis.x_min, ax.x_axis.x_max]),
        # )
        ax.shift(image.get_corner(UL) - ax.get_origin())

        self.play(AnimationGroup(
            Write(ax),
            # Write(ax_labels),
        ))
        self.wait()