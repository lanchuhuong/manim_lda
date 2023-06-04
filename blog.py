from manim import *

import scipy.stats
from scipy.stats import dirichlet, multinomial

class LDASimulation(Scene):
    alpha = 2
    beta = 5
    num_samples = 1

    def construct(self):
        bar_kwargs = {
            "x_length": config["frame_width"] / 2.5,
            "y_length": config["frame_height"] - 3.25,
            "bar_colors": [RED, GREEN, BLUE, YELLOW],
            "y_range" : [0, 0.8, 0.2]
        }

        # set title for scene
        title_pdf = (
            Tex("Dirichlet Distribution's PDF")
            .set_color_by_gradient(*bar_kwargs["bar_colors"])
            .set_fill(color=WHITE, opacity=0.3)
            .set_stroke(width=1.2)
            .set(width=7)
            .to_corner(UL)
        )
        self.add(title_pdf)

        # set up axes
        ax = Axes(
            x_range=[0, 1],
            y_range=[0, 3],
            tips=False,
            x_length=config["frame_width"] / 3,
            y_length=config["frame_height"] * 0.6,
        ).add_coordinates()

        x_label = ax.get_x_axis_label(
            Tex("probability").scale(0.7), edge=DOWN, direction=ORIGIN
        )

        y_label = ax.get_y_axis_label(
            Tex("probability density").scale(0.7).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.2,
        )
        ax.add(x_label, y_label)

        def pdf(x):
            return dist.pdf(x)

        dist = scipy.stats.beta(self.alpha, self.beta)
        pdf_curve = ax.plot(pdf, x_range=[0, 1], color=BLUE_C)

        # add the PDF curve to the ax object.
        ax.add(pdf_curve)

        ax.to_edge(DL)
        ax.remove(pdf_curve)
        
        # add annotation to ax
        a_tex = Tex(r"$\alpha = 2$", color=BLUE).scale(0.7)
        b_tex = Tex(r"$\beta = 5$", color=BLUE).scale(0.7)

        a_tex.next_to(ax, direction=UP + LEFT, aligned_edge=RIGHT)
        b_tex.next_to(a_tex, DOWN)

        self.play(Write(a_tex), Write(b_tex))
        self.play(Create(ax), run_time=2)
        self.play(Create(pdf_curve), run_time=2)
        self.play(Wait(1))
        
        # create topic distribution
        topic_distribution = BarChart([0,0], **bar_kwargs)
        topic_distribution.to_edge(DOWN + RIGHT)
        self.add(topic_distribution)

        # at bar labels
        tex_animals = Tex("animals")
        tex_animals.next_to(topic_distribution.bars[0], DOWN, buff=0.1)
        tex_food = Tex("food")
        tex_food.next_to(topic_distribution.bars[1], DOWN, buff=0.1)
        self.play(Create(topic_distribution))
        self.play(Write(tex_food), Write(tex_animals))

        # resample 10 times
        for i in range(10):
            beta_distribution = scipy.stats.beta(self.alpha, self.beta)
            probability = beta_distribution.rvs(self.num_samples)[0]
            new_data = [probability, 1-probability]

            if i == 0:
                dot = Dot(ax.coords_to_point(probability, 0))
                self.play(Create(dot), topic_distribution.animate.change_bar_values(new_data))

            else:
                self.play(
                    dot.animate.move_to(ax.coords_to_point(probability, 0)),
                    topic_distribution.animate.change_bar_values(new_data),
                )

            self.wait(1)
        self.wait(2)


labels = np.array(["food", "animals"])

words = [
    "banana",
    "kiwi",
    "lemon",
    "strawberry",
    "tomato",
    "chicken",
    "piggy",
    "sheep",
    "crocodile",
    "zebra",
]


def add_svg_xticks(bar_chart):
    """Adds svg symbols instead of standard x-ticks to a BarChart."""
    for i, word in enumerate(words):
        symbol = create_word_token(word)
        symbol.next_to(bar_chart.bars[i], DOWN, buff=0.3, aligned_edge=DOWN)
        bar_chart.add(symbol)


def fix_svg(svgmobject):
    """Fixes missing attributes when loading svg."""
    attrs = [
        "fill_rgbas",
        "stroke_rgbas",
        "background_stroke_rgbas",
        "stroke_width",
        "background_stroke_width",
        "sheen_direction",
        "sheen_factor",
    ]
    for attr in attrs:
        if getattr(svgmobject, attr) is None:
            setattr(svgmobject, attr, 0)


def create_word_token(word):
    """Creates a word token."""
    symbol = SVGMobject(f"icons/{word}.svg", height=0.4)
    fix_svg(symbol)
    return symbol


def create_topic_symbol(row, value):
    """Creates a topic symbol."""
    if value == 0:
        symbol = Square(side_length=0.5, color=BLUE)
    else:
        symbol = Square(side_length=0.5, color=ORANGE)
    symbol.next_to(row, RIGHT, buff=0.05)
    row.add(symbol)
    return symbol


class TopicGenerationSimulation(Scene):
    alphas_topics = [10, 20]
    alphas_words_topic1 = [5, 10, 8, 3, 10]
    alphas_words_topic2 = [10, 3, 8, 9, 5]

    def construct(self):
        # create empty histograms
        topic_distribution = BarChart([0, 0.0], bar_names = ["food", "animals"], y_range=[0, 0.8, 0.2])
        word_distribution = BarChart(
            10 * [0],
            bar_names=None,
            bar_colors=5 * ["#003f5c"] + 5 * ["#ffa600"],
            y_range=(0, 0.5, 0.1),
        )
        add_svg_xticks(word_distribution)

        # create arrows
        arrow_topic = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)
        arrow_word = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)

        # align objects
        topic_distribution.to_edge(DOWN + LEFT)
        word_distribution.to_edge(DOWN + RIGHT)
        word_distribution.move_to(topic_distribution, UP, UP)

        row = VGroup(Tex(r"doc 1:"))
        row.to_edge(UP + LEFT, buff=0.1)

        # initialize view
        self.add(topic_distribution, word_distribution, row)

        for doc_index in range(3):
            # draw probabilities
            topic_prob = dirichlet(self.alphas_topics).rvs(1)[0]
            word_prob = np.concatenate(
                [
                    dirichlet(self.alphas_words_topic1).rvs(1)[0],
                    dirichlet(self.alphas_words_topic2).rvs(1)[0],
                ],
            )
            if doc_index > 0:
                self.play(FadeOut(arrow_topic), FadeOut(arrow_word))

            # update bar charts
            self.play(topic_distribution.animate.change_bar_values(topic_prob))
            self.play(word_distribution.animate.change_bar_values(word_prob))
            self.play(Wait(1))

            for word_index in range(5):
                # draw topic and word
                topic = np.argmax(multinomial.rvs(1, topic_prob))
                word = (
                    np.argmax(
                        multinomial.rvs(1, word_prob[5 * topic : 5 * (topic + 1)])
                    )
                    + 5 * topic
                )
                topic_symbol = create_topic_symbol(row, topic)

                if doc_index != 0 and word_index == 0:
                    new_row = VGroup(Tex(f"doc {doc_index+1}: "))
                    new_row.next_to(row, DOWN, buff=0.1, aligned_edge=LEFT)
                    self.add(new_row)
                    row = new_row
                    topic_symbol = create_topic_symbol(row, topic)

                if word_index == 0:
                    arrow_topic.next_to(topic_distribution[0][topic], UP, buff=0.1)
                    arrow_word.next_to(
                        word_distribution[0][word],
                        UP,
                        buff=0.1,
                    )
                    self.play(
                        FadeIn(topic_symbol),
                        FadeIn(arrow_topic),
                    )
                    self.play(FadeIn(arrow_word))
                else:
                    self.play(
                        FadeIn(topic_symbol),
                        arrow_topic.animate.next_to(
                            topic_distribution[0][topic], UP, buff=0.1
                        ),
                    )
                    self.play(
                        arrow_word.animate.next_to(
                            word_distribution[0][word],
                            UP,
                            buff=0.1,
                        ),
                    )

                word_symbol = create_word_token(words[word])
                word_symbol.next_to(
                    word_distribution[0][word], DOWN, buff=0.3, aligned_edge=DOWN
                )

                self.play(word_symbol.animate.move_to(topic_symbol.get_center()))
                self.play(FadeOut(topic_symbol), run_time=0.5)
        self.play(Wait(2))
 