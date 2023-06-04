from manim import *
class BarChartExample(Scene):
    def construct(self):
        # Create the initial bar chart
        barchart1 = BarChart(
            values=[0, 0, 0],
            y_range=[0, 0.6, 0.2],
            bar_names=["food", "animals", "sport"],
            y_length=6,
            x_length=10,
            x_axis_config={"font_size": 36},
        )

        # Create the second bar chart
        barchart2 = BarChart(
            values=[0.4, 0.3, 0.3],
            bar_names=["food", "animals", "sport"],
            y_length=6,
            x_length=10,
            x_axis_config={"font_size": 36},
        )

        self.play(Create(barchart1))

        # Animate the first bar chart to become the second one
        self.play(barchart1.animate.become(barchart2), run_time=1.5)
        self.wait(2)
