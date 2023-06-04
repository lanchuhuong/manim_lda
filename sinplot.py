from manim import *
class SinFunctionPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10, 1],  # x-axis range and step size
            y_range=[-1.5, 1.5, 0.5],  # y-axis range and step size
            x_length=10,
            axis_config={"color": BLUE},
            x_axis_config={
                "numbers_to_include": np.arange(-10, 10, 2),
                "numbers_with_elongated_ticks": np.arange(-10, 10, 2),
            },
        )
        axes_labels = axes.get_axis_labels(Tex("$x$"), Tex("$\sin(x)$"))

        axes.add(axes_labels)
        # create the sin curve function
        sin_curve = axes.plot(lambda x: np.sin(x), color=RED)

        # Incrementally show the plot
        self.play(Create(axes), run_time=2)
        self.play(Create(sin_curve), run_time=2)
        self.wait(2)
       