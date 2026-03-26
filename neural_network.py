from manimlib import *
import numpy as np


class NeuralNetworkScene(Scene):
    def construct(self):
        np.random.seed(42)

        # ============================================================
        # HELPER: build a layer of neuron circles
        # ============================================================
        def make_layer(n, radius=0.22):
            layer = VGroup()
            for _ in range(n):
                c = Circle(radius=radius)
                c.set_stroke(WHITE, 2)
                c.set_fill(BLACK, 1)
                layer.add(c)
            layer.arrange(DOWN, buff=0.28)
            return layer

        def make_edges(layer_l, layer_r, **kw):
            edges = VGroup()
            for n1 in layer_l:
                for n2 in layer_r:
                    edges.add(Line(
                        n1.get_right(), n2.get_left(),
                        stroke_width=kw.get("sw", 1),
                        stroke_color=kw.get("color", GREY),
                        stroke_opacity=kw.get("opacity", 0.25),
                    ))
            return edges

        # ============================================================
        # 1.  TITLE
        # ============================================================
        title = Text("Neural Network гэж юу вэ?", font_size=44)
        title.to_edge(UP, buff=1.0)
        subtitle = Text(
            "Хиймэл оюун ухааны суурь ойлголт",
            font_size=24, color=GREY_B,
        )
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # ============================================================
        # 2.  INPUT: зураг → тоонууд
        # ============================================================
        section1 = Text("1. Оролт (Input)", font_size=36, color=BLUE)
        section1.to_edge(UP, buff=0.5)
        self.play(Write(section1), run_time=0.8)

        # 5x5 pixel grid representing a tiny "image"
        grid_size = 5
        pixel_vals = np.random.random((grid_size, grid_size))
        # Make it look like a rough "3"
        pattern = np.array([
            [0.1, 0.9, 0.9, 0.9, 0.1],
            [0.1, 0.1, 0.1, 0.8, 0.1],
            [0.1, 0.5, 0.9, 0.9, 0.1],
            [0.1, 0.1, 0.1, 0.8, 0.1],
            [0.1, 0.9, 0.9, 0.9, 0.1],
        ])
        pixel_vals = pattern

        grid = VGroup()
        for r in range(grid_size):
            for c in range(grid_size):
                sq = Square(side_length=0.5)
                brightness = pixel_vals[r][c]
                sq.set_fill(WHITE, opacity=brightness)
                sq.set_stroke(GREY, 1)
                grid.add(sq)
        grid.arrange_in_grid(grid_size, grid_size, buff=0.05)
        grid.shift(LEFT * 4 + DOWN * 0.5)

        img_label = Text("Зураг (5x5 пиксел)", font_size=20)
        img_label.next_to(grid, DOWN, buff=0.3)

        self.play(FadeIn(grid, lag_ratio=0.03), run_time=1.0)
        self.play(FadeIn(img_label), run_time=0.5)
        self.wait(0.8)

        # Arrow from image to number column
        arrow1 = Arrow(LEFT * 1.8 + DOWN * 0.5, RIGHT * 0.0 + DOWN * 0.5, color=YELLOW)
        arrow_label = Text("пиксел бүрийг\nтоо болгоно", font_size=16, color=YELLOW)
        arrow_label.next_to(arrow1, UP, buff=0.15)

        # Column of numbers
        flat = pixel_vals.flatten()
        num_col = VGroup()
        display_nums = [flat[0], flat[1], flat[4], flat[12], flat[24]]
        num_texts = ["0.1", "0.9", "0.1", "0.9", "0.9"]
        for t in num_texts:
            txt = Text(t, font_size=18)
            num_col.add(txt)

        dots_mid = Tex(r"\vdots").scale(0.8)
        top_nums = VGroup(*num_col[:2])
        bot_nums = VGroup(*num_col[2:])
        top_nums.arrange(DOWN, buff=0.2)
        bot_nums.arrange(DOWN, buff=0.2)
        dots_mid.next_to(top_nums, DOWN, buff=0.2)
        bot_nums.next_to(dots_mid, DOWN, buff=0.2)
        number_group = VGroup(top_nums, dots_mid, bot_nums)
        number_group.move_to(RIGHT * 1.0 + DOWN * 0.5)

        num_label = Text("25 тоо", font_size=20, color=GREY_B)
        num_label.next_to(number_group, DOWN, buff=0.3)

        self.play(ShowCreation(arrow1), FadeIn(arrow_label), run_time=0.8)
        self.play(FadeIn(number_group), FadeIn(num_label), run_time=0.8)
        self.wait(1.5)

        # Explain
        explain1 = Text(
            "Компьютер зургийг тоон массив хэлбэрээр хүлээн авдаг.\n"
            "Пиксел бүр 0 (хар) - 1 (цагаан) гэсэн утгатай.",
            font_size=18, color=GREY_A,
        )
        explain1.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(explain1), run_time=0.8)
        self.wait(2.0)

        # Clean section 1
        self.play(
            *[FadeOut(m) for m in [
                section1, grid, img_label, arrow1, arrow_label,
                number_group, num_label, explain1,
            ]],
            run_time=0.8,
        )

        # ============================================================
        # 3.  NETWORK STRUCTURE: давхаргууд
        # ============================================================
        section2 = Text("2. Сүлжээний бүтэц", font_size=36, color=BLUE)
        section2.to_edge(UP, buff=0.5)
        self.play(Write(section2), run_time=0.8)

        # Build layers
        l_in = make_layer(6, radius=0.18)
        l_h1 = make_layer(8, radius=0.18)
        l_h2 = make_layer(8, radius=0.18)
        l_out = make_layer(4, radius=0.18)

        # Add vdots to input layer
        in_dots = Tex(r"\vdots").scale(0.7)
        in_circles = list(l_in)
        in_top = VGroup(*in_circles[:3]).arrange(DOWN, buff=0.28)
        in_bot = VGroup(*in_circles[3:]).arrange(DOWN, buff=0.28)
        in_dots.next_to(in_top, DOWN, buff=0.2)
        in_bot.next_to(in_dots, DOWN, buff=0.2)

        network_layers = VGroup(l_in, l_h1, l_h2, l_out)
        network_layers.arrange(RIGHT, buff=1.6)
        network_layers.center().shift(DOWN * 0.3)
        network_layers.set_height(5)

        # Recalculate dots position after arranging
        mid = len(list(l_in)) // 2
        circles_in = list(l_in)
        in_dots.move_to(
            (circles_in[mid - 1].get_center() + circles_in[mid].get_center()) / 2
        )

        # Edges
        e1 = make_edges(l_in, l_h1)
        e2 = make_edges(l_h1, l_h2)
        e3 = make_edges(l_h2, l_out)
        all_edges = VGroup(e1, e2, e3)

        # Labels
        layer_names = ["Оролт\n(Input)", "Нууц давхарга\n(Hidden)", "Нууц давхарга\n(Hidden)", "Гаралт\n(Output)"]
        layer_labels = VGroup()
        for i, ll in enumerate(network_layers):
            lbl = Text(layer_names[i], font_size=16)
            lbl.next_to(ll, DOWN, buff=0.35)
            layer_labels.add(lbl)

        # Animate: layers one by one
        for i, ll in enumerate(network_layers):
            self.play(FadeIn(ll), run_time=0.5)
            self.play(FadeIn(layer_labels[i]), run_time=0.3)

        self.play(FadeIn(in_dots), run_time=0.3)

        # Edges
        for eg in all_edges:
            self.play(ShowCreation(eg, lag_ratio=0.02), run_time=0.7)

        self.wait(0.5)

        # Explanation
        explain2 = Text(
            "Нейрон сүлжээ нь давхаргуудаас бүрддэг.\n"
            "Давхарга бүр олон нейроноос бүрдэнэ.\n"
            "Нейронууд хоорондоо холболтоор (weight) холбогддог.",
            font_size=18, color=GREY_A,
        )
        explain2.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(explain2), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(explain2), run_time=0.5)

        # ============================================================
        # 4.  НЭГ НЕЙРОН ЯАЖ АЖИЛЛАДАГ
        # ============================================================
        self.play(FadeOut(section2), run_time=0.4)
        section3 = Text("3. Нэг нейрон яаж ажилладаг вэ?", font_size=36, color=BLUE)
        section3.to_edge(UP, buff=0.5)
        self.play(Write(section3), run_time=0.8)

        # Highlight one neuron in h1
        target = list(l_h1)[3]  # middle neuron
        self.play(
            target.animate.set_stroke(YELLOW, 3),
            target.animate.set_fill(YELLOW, 0.3),
            run_time=0.6,
        )

        # Highlight its incoming edges
        input_neurons = list(l_in)
        highlight_edges = VGroup()
        for n_in in input_neurons:
            edge = Line(
                n_in.get_right(), target.get_left(),
                stroke_width=2, stroke_color=YELLOW, stroke_opacity=0.7,
            )
            highlight_edges.add(edge)

        self.play(ShowCreation(highlight_edges, lag_ratio=0.08), run_time=1.0)
        self.wait(0.5)

        # Show the concept: inputs × weights → sum → activation
        # Move network left, show formula right
        net_group = VGroup(network_layers, all_edges, layer_labels, in_dots, highlight_edges)

        self.play(net_group.animate.shift(LEFT * 1.5).scale(0.75), run_time=0.8)

        # Formula box on the right
        step1 = Tex(r"\text{1. }", r"w_1 x_1 + w_2 x_2 + \cdots + w_n x_n", font_size=28)
        step1_label = Text("Жинлэсэн нийлбэр", font_size=16, color=GREY_B)

        step2 = Tex(r"\text{2. }", r"+ \; b", font_size=28)
        step2_label = Text("Хазайлт (bias) нэмнэ", font_size=16, color=GREY_B)

        step3 = Tex(r"\text{3. }", r"\sigma(\cdot)", font_size=28)
        step3_label = Text("Идэвхжүүлэх функц", font_size=16, color=GREY_B)

        steps = VGroup(
            VGroup(step1, step1_label),
            VGroup(step2, step2_label),
            VGroup(step3, step3_label),
        )
        for s in steps:
            s[1].next_to(s[0], RIGHT, buff=0.3)

        steps.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        steps.move_to(RIGHT * 3.2 + DOWN * 0.3)

        for s in steps:
            self.play(Write(s[0]), FadeIn(s[1]), run_time=0.8)
            self.wait(0.6)

        # Result arrow
        result_arrow = Arrow(steps.get_bottom() + DOWN * 0.1, steps.get_bottom() + DOWN * 0.7, color=GREEN)
        result_text = Text("Нейроны гаралт (0-1 хоорондох тоо)", font_size=16, color=GREEN)
        result_text.next_to(result_arrow, DOWN, buff=0.15)

        self.play(ShowCreation(result_arrow), FadeIn(result_text), run_time=0.6)
        self.wait(2.0)

        # Explain
        explain3 = Text(
            "Нейрон бүр: оролтуудыг жингээр үржүүлж нийлбэрийг олоод,\n"
            "идэвхжүүлэх функцээр 0-1 хооронд шахна.",
            font_size=17, color=GREY_A,
        )
        explain3.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(explain3), run_time=0.6)
        self.wait(2.5)

        # Clean formula
        formula_stuff = VGroup(steps, result_arrow, result_text, explain3)
        self.play(FadeOut(formula_stuff), run_time=0.6)

        # Unhighlight
        self.play(
            target.animate.set_stroke(WHITE, 2),
            target.animate.set_fill(BLACK, 1),
            FadeOut(highlight_edges),
            run_time=0.5,
        )

        # Restore network position
        self.play(
            net_group.animate.shift(RIGHT * 1.5).scale(1 / 0.75),
            run_time=0.6,
        )

        # ============================================================
        # 5.  FORWARD PASS: дохио дамжих
        # ============================================================
        self.play(FadeOut(section3), run_time=0.4)
        section4 = Text("4. Мэдээлэл хэрхэн дамждаг вэ?", font_size=36, color=BLUE)
        section4.to_edge(UP, buff=0.5)
        self.play(Write(section4), run_time=0.8)
        self.wait(0.5)

        explain_fwd = Text(
            "Оролтын давхаргаас эхлээд, давхарга бүрээр\n"
            "дохио урагшаа дамжина. Үүнийг 'Forward Pass' гэнэ.",
            font_size=18, color=GREY_A,
        )
        explain_fwd.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(explain_fwd), run_time=0.6)

        # Activate input layer
        input_acts = np.random.random(len(list(l_in)))
        in_anims = []
        for neuron, a in zip(l_in, input_acts):
            in_anims.append(neuron.animate.set_fill(WHITE, opacity=a))
        self.play(*in_anims, run_time=0.8)
        self.wait(0.3)

        # Arrow label
        fwd_label = Text("Forward Pass", font_size=22, color=YELLOW)
        fwd_arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, color=YELLOW)
        fwd_group = VGroup(fwd_arrow, fwd_label)
        fwd_label.next_to(fwd_arrow, UP, buff=0.1)
        fwd_group.next_to(network_layers, UP, buff=0.3)
        self.play(FadeIn(fwd_group), run_time=0.5)

        # Propagate layer by layer
        edge_groups = [e1, e2, e3]
        prop_layers = [l_h1, l_h2, l_out]
        for idx, (eg, ll) in enumerate(zip(edge_groups, prop_layers)):
            # Light up edges
            self.play(eg.animate.set_stroke(opacity=0.5), run_time=0.3)

            # Light up neurons
            acts = np.random.random(len(list(ll)))
            n_anims = []
            for neuron, a in zip(ll, acts):
                col = interpolate_color(BLACK, GREEN_B, a)
                n_anims.append(neuron.animate.set_fill(col, opacity=max(a, 0.15)))
            self.play(*n_anims, run_time=0.6)

            # Dim edges
            self.play(eg.animate.set_stroke(opacity=0.25), run_time=0.2)

        self.wait(1.0)

        # Highlight winner output
        out_neurons = list(l_out)
        winner = 1  # second neuron
        self.play(
            out_neurons[winner].animate.set_fill(GREEN, 1.0),
            out_neurons[winner].animate.set_stroke(GREEN, 3),
            run_time=0.6,
        )

        winner_label = Text("Хамгийн өндөр\nидэвхжил = хариулт", font_size=16, color=GREEN)
        winner_label.next_to(out_neurons[winner], RIGHT, buff=0.3)
        self.play(FadeIn(winner_label), run_time=0.5)
        self.wait(2.0)

        # ============================================================
        # 6.  ДҮГНЭЛТ
        # ============================================================
        self.play(
            FadeOut(explain_fwd), FadeOut(fwd_group),
            FadeOut(winner_label), FadeOut(section4),
            run_time=0.6,
        )

        section5 = Text("Дүгнэлт", font_size=36, color=BLUE)
        section5.to_edge(UP, buff=0.5)
        self.play(Write(section5), run_time=0.6)

        summary_items = VGroup(
            Text("1. Оролт: мэдээллийг тоон хэлбэрт хөрвүүлнэ", font_size=18),
            Text("2. Нууц давхарга: нейрон бүр жинлэсэн нийлбэр тооцоолно", font_size=18),
            Text("3. Идэвхжүүлэх функц: утгыг 0-1 хооронд шахна", font_size=18),
            Text("4. Forward Pass: давхаргаар дамжин гаралтад хүрнэ", font_size=18),
            Text("5. Гаралт: хамгийн өндөр утгатай нейрон = хариулт", font_size=18),
        )
        summary_items.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary_items.to_edge(DOWN, buff=0.8)

        for item in summary_items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.4)

        self.wait(3.0)

        # Final fade
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=1.5)
        self.wait(0.5)
