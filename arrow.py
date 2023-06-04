from manim import *

from manim.mobject.geometry.tips import ArrowSquareTip


class ArrowExample(Scene):
    def construct(self):
        arrow_1 = Arrow(
            start=RIGHT, end=LEFT, color=BLUE
        )  # Specifies the starting point of the arrow as the right side.
        arrow_2 = Arrow(
            start=RIGHT, end=LEFT, color=BLUE, tip_shape=ArrowSquareTip
        ).shift(
            DOWN
        )  # Shifts the position of the arrow downward
        self.play(Create(arrow_1))
        self.play(Create(arrow_2))
