from manim import *

class PostProcessScene(Scene):
    def construct(self):
        # Create a simple title
        title = Text("Post-Processing Animation", font_size=48)
        title.to_edge(UP)

        # Create a circle
        circle = Circle(radius=1, color=BLUE)
        circle.move_to(LEFT * 2)

        # Create a square
        square = Square(side_length=2, color=RED)
        square.move_to(RIGHT * 2)

        # Add elements to the scene
        self.play(Write(title))
        self.play(Create(circle), Create(square))

        # Animate transformations
        self.play(
            circle.animate.scale(0.5).set_color(GREEN),
            square.animate.rotate(PI/4).set_color(YELLOW)
        )

        self.wait(2)

