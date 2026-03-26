from manimlib import *
import numpy as np


class HowNNWorks(Scene):
    def construct(self):
        np.random.seed(42)

        # ============================================================
        # 1.  TITLE
        # ============================================================
        title = Text("Neural Network яаж ажилладаг вэ?", font_size=42)
        title.to_edge(UP, buff=1.2)
        subtitle = Text("Нейроны дотоод ажиллагаа", font_size=24, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.7)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.7)

        # ============================================================
        # 2.  ЕРӨНХИЙ БҮТЭЦ
        # ============================================================
        sec_struct = Text("1. Ерөнхий бүтэц", font_size=36, color=BLUE)
        sec_struct.to_edge(UP, buff=0.5)
        self.play(Write(sec_struct), run_time=0.7)

        # Helper
        def make_layer_circle(n, radius=0.22):
            layer = VGroup()
            for _ in range(n):
                c = Circle(radius=radius)
                c.set_stroke(WHITE, 2)
                c.set_fill(BLACK, 1)
                layer.add(c)
            layer.arrange(DOWN, buff=0.35)
            return layer

        # Build overview network: 4 - 5 - 5 - 3
        ov_in = make_layer_circle(4)
        ov_h1 = make_layer_circle(5)
        ov_h2 = make_layer_circle(5)
        ov_out = make_layer_circle(3)

        ov_layers = VGroup(ov_in, ov_h1, ov_h2, ov_out)
        ov_layers.arrange(RIGHT, buff=1.8)
        ov_layers.center().shift(DOWN * 0.2)
        ov_layers.set_height(4.5)

        # Edges
        ov_edges = VGroup()
        for i in range(len(ov_layers) - 1):
            layer_l = ov_layers[i]
            layer_r = ov_layers[i + 1]
            for n1 in layer_l:
                for n2 in layer_r:
                    ov_edges.add(Line(
                        n1.get_right(), n2.get_left(),
                        stroke_width=0.8, stroke_color=GREY,
                        stroke_opacity=0.2,
                    ))

        # Layer labels
        ov_names = ["Оролт\n(Input)", "Нууц давхарга 1\n(Hidden)", "Нууц давхарга 2\n(Hidden)", "Гаралт\n(Output)"]
        ov_labels = VGroup()
        for i, ll in enumerate(ov_layers):
            lbl = Text(ov_names[i], font_size=14)
            lbl.next_to(ll, DOWN, buff=0.3)
            ov_labels.add(lbl)

        # Animate: fade in layers one by one
        for i, ll in enumerate(ov_layers):
            self.play(FadeIn(ll), FadeIn(ov_labels[i]), run_time=0.5)

        self.play(ShowCreation(ov_edges, lag_ratio=0.005), run_time=1.0)
        self.wait(0.5)

        # Explanation: what are layers?
        struct_exp1 = Text(
            "Neural Network давхаргуудаас бүрддэг.\n"
            "Давхарга бүр олон нейроноос бүрдэнэ.",
            font_size=18, color=GREY_A,
        )
        struct_exp1.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(struct_exp1), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(struct_exp1), run_time=0.4)

        # Highlight input layer
        self.play(
            *[n.animate.set_fill(BLUE, opacity=0.5) for n in ov_in],
            ov_labels[0].animate.set_color(BLUE),
            run_time=0.5,
        )
        struct_input = Text(
            "Оролтын давхарга: мэдээллийг хүлээн авдаг\n"
            "(жишээ нь: зургийн пиксел, тоон өгөгдөл)",
            font_size=17, color=BLUE_B,
        )
        struct_input.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(struct_input), run_time=0.5)
        self.wait(2.0)
        self.play(
            FadeOut(struct_input),
            *[n.animate.set_fill(BLACK, opacity=1) for n in ov_in],
            ov_labels[0].animate.set_color(WHITE),
            run_time=0.4,
        )

        # Highlight hidden layers
        self.play(
            *[n.animate.set_fill(YELLOW, opacity=0.4) for n in [*ov_h1, *ov_h2]],
            ov_labels[1].animate.set_color(YELLOW),
            ov_labels[2].animate.set_color(YELLOW),
            run_time=0.5,
        )
        struct_hidden = Text(
            "Нууц давхарга: мэдээллийг боловсруулдаг\n"
            "Энд pattern, хэв маягийг таньдаг",
            font_size=17, color=YELLOW_B,
        )
        struct_hidden.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(struct_hidden), run_time=0.5)
        self.wait(2.0)
        self.play(
            FadeOut(struct_hidden),
            *[n.animate.set_fill(BLACK, opacity=1) for n in [*ov_h1, *ov_h2]],
            ov_labels[1].animate.set_color(WHITE),
            ov_labels[2].animate.set_color(WHITE),
            run_time=0.4,
        )

        # Highlight output layer
        self.play(
            *[n.animate.set_fill(GREEN, opacity=0.5) for n in ov_out],
            ov_labels[3].animate.set_color(GREEN),
            run_time=0.5,
        )
        struct_output = Text(
            "Гаралтын давхарга: эцсийн хариултыг өгдөг\n"
            "(жишээ нь: ямар цифр вэ? тэнцэх үү?)",
            font_size=17, color=GREEN_B,
        )
        struct_output.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(struct_output), run_time=0.5)
        self.wait(2.0)
        self.play(
            FadeOut(struct_output),
            *[n.animate.set_fill(BLACK, opacity=1) for n in ov_out],
            ov_labels[3].animate.set_color(WHITE),
            run_time=0.4,
        )

        # Highlight edges - connections
        self.play(ov_edges.animate.set_stroke(opacity=0.5), run_time=0.5)
        struct_edges = Text(
            "Холболт (weight): нейронуудыг хооронд нь холбоно.\n"
            "Холболт бүр жинтэй - мэдээллийн чухлыг тодорхойлно.",
            font_size=17, color=GREY_A,
        )
        struct_edges.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(struct_edges), run_time=0.5)
        self.wait(2.0)
        self.play(
            FadeOut(struct_edges),
            ov_edges.animate.set_stroke(opacity=0.2),
            run_time=0.4,
        )

        # Information flow arrow
        flow_arrow = Arrow(LEFT * 5, RIGHT * 5, color=YELLOW, stroke_width=3)
        flow_arrow.next_to(ov_layers, UP, buff=0.4)
        flow_label = Text("Мэдээлэл зүүнээс баруун тийш урсдаг (Forward Pass)", font_size=16, color=YELLOW)
        flow_label.next_to(flow_arrow, UP, buff=0.1)

        self.play(ShowCreation(flow_arrow), FadeIn(flow_label), run_time=0.8)
        self.wait(2.0)

        # Clean overview
        ov_all = VGroup(ov_layers, ov_edges, ov_labels, flow_arrow, flow_label)
        self.play(FadeOut(ov_all), FadeOut(sec_struct), run_time=0.7)

        # ============================================================
        # 3.  НЭГ НЕЙРОН - дэлгэрэнгүй
        # ============================================================
        sec1 = Text("2. Нэг нейрон", font_size=36, color=BLUE)
        sec1.to_edge(UP, buff=0.5)
        self.play(Write(sec1), run_time=0.7)

        # Big neuron in center
        big_neuron = Circle(radius=0.6)
        big_neuron.set_stroke(WHITE, 3)
        big_neuron.set_fill(BLACK, 1)
        big_neuron.move_to(ORIGIN)

        sigma_inside = Tex(r"\Sigma", font_size=40)
        sigma_inside.move_to(big_neuron.get_center())

        # Input arrows with values
        inputs_data = [
            {"label": "x_1 = 0.9", "weight": "w_1 = 0.5", "x": 0.9, "w": 0.5},
            {"label": "x_2 = 0.3", "weight": "w_2 = -0.2", "x": 0.3, "w": -0.2},
            {"label": "x_3 = 0.7", "weight": "w_3 = 0.8", "x": 0.7, "w": 0.8},
        ]

        input_circles = VGroup()
        input_labels = VGroup()
        weight_labels = VGroup()
        input_arrows = VGroup()

        for i, d in enumerate(inputs_data):
            # Input node
            ic = Circle(radius=0.25)
            ic.set_stroke(GREY_A, 2)
            ic.set_fill(WHITE, opacity=d["x"])
            y_pos = (1 - i) * 1.5
            ic.move_to(LEFT * 4.5 + UP * y_pos)
            input_circles.add(ic)

            # Input value label
            il = Tex(d["label"], font_size=22)
            il.next_to(ic, LEFT, buff=0.2)
            input_labels.add(il)

            # Arrow
            arr = Arrow(
                ic.get_right(), big_neuron.get_left() + UP * y_pos * 0.3,
                buff=0.1, stroke_width=2,
                color=BLUE if d["w"] > 0 else RED,
            )
            input_arrows.add(arr)

            # Weight label on arrow
            wl = Tex(d["weight"], font_size=18, color=BLUE if d["w"] > 0 else RED)
            wl.next_to(arr, UP, buff=0.05)
            weight_labels.add(wl)

        # Output arrow
        out_arrow = Arrow(
            big_neuron.get_right(), RIGHT * 3.5,
            buff=0.1, stroke_width=2, color=GREEN,
        )
        out_label = Text("гаралт", font_size=18, color=GREEN)
        out_label.next_to(out_arrow, UP, buff=0.1)

        # Animate
        self.play(FadeIn(big_neuron), Write(sigma_inside), run_time=0.7)
        self.wait(0.3)

        for ic, il, arr, wl in zip(input_circles, input_labels, input_arrows, weight_labels):
            self.play(
                FadeIn(ic), FadeIn(il),
                ShowCreation(arr), FadeIn(wl),
                run_time=0.6,
            )

        self.play(ShowCreation(out_arrow), FadeIn(out_label), run_time=0.5)
        self.wait(1.0)

        # Explanation
        exp1 = Text(
            "Нейрон нь оролтуудыг хүлээн авч,\n"
            "тооцоолол хийгээд нэг гаралт өгдөг.",
            font_size=18, color=GREY_A,
        )
        exp1.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(exp1), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(exp1), run_time=0.4)

        # ============================================================
        # 3a. ҮНДСЭН ТОМЬЁО - эхлээд харуулах
        # ============================================================
        self.play(FadeOut(sec1), run_time=0.3)
        sec_formula = Text("3. Үндсэн томьёо", font_size=36, color=BLUE)
        sec_formula.to_edge(UP, buff=0.5)
        self.play(Write(sec_formula), run_time=0.7)

        # Move neuron to the left to make room
        neuron_group = VGroup(
            big_neuron, sigma_inside, input_circles, input_labels,
            input_arrows, weight_labels, out_arrow, out_label,
        )
        self.play(neuron_group.animate.scale(0.55).shift(LEFT * 3.5 + UP * 0.3), run_time=0.7)

        # Show all key formulas on the right
        f_title1 = Text("Алхам 1: Жинлэсэн нийлбэр", font_size=18, color=YELLOW)
        f1 = Tex(
            r"z = \sum_{i=1}^{n} w_i \cdot x_i + b",
            font_size=32, color=WHITE,
        )
        f1_box = SurroundingRectangle(f1, color=YELLOW, buff=0.15, stroke_width=1.5)

        f_title2 = Text("Алхам 2: Идэвхжүүлэх функц (Sigmoid)", font_size=18, color=GREEN)
        f2 = Tex(
            r"a = \sigma(z) = \frac{1}{1 + e^{-z}}",
            font_size=32, color=WHITE,
        )
        f2_box = SurroundingRectangle(f2, color=GREEN, buff=0.15, stroke_width=1.5)

        formulas = VGroup(
            VGroup(f_title1, VGroup(f1, f1_box)),
            VGroup(f_title2, VGroup(f2, f2_box)),
        )
        for fg in formulas:
            fg.arrange(DOWN, buff=0.2)
        formulas.arrange(DOWN, buff=0.6)
        formulas.move_to(RIGHT * 2.0 + DOWN * 0.1)

        # Animate formulas one by one
        self.play(Write(f_title1), run_time=0.5)
        self.play(Write(f1), ShowCreation(f1_box), run_time=1.0)
        self.wait(0.5)

        # Label parts
        f1_parts = VGroup(
            Text("w = жин (weight)", font_size=14, color=BLUE_B),
            Text("x = оролт (input)", font_size=14, color=GREY_A),
            Text("b = хазайлт (bias)", font_size=14, color=RED_B),
        )
        f1_parts.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        f1_parts.next_to(f1_box, RIGHT, buff=0.3)
        self.play(FadeIn(f1_parts), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(f1_parts), run_time=0.3)

        self.play(Write(f_title2), run_time=0.5)
        self.play(Write(f2), ShowCreation(f2_box), run_time=1.0)
        self.wait(0.5)

        f2_parts = VGroup(
            Text("z = жинлэсэн нийлбэр", font_size=14, color=YELLOW),
            Text("a = нейроны гаралт (0-1)", font_size=14, color=GREEN_B),
        )
        f2_parts.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        f2_parts.next_to(f2_box, RIGHT, buff=0.3)
        self.play(FadeIn(f2_parts), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(f2_parts), run_time=0.3)

        # Show the flow: x,w → z → σ → a
        flow_exp = Text(
            "Оролт, жин → нийлбэр (z) → sigmoid → гаралт (a)",
            font_size=17, color=GREY_A,
        )
        flow_exp.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(flow_exp), run_time=0.5)
        self.wait(2.5)

        # Clean formulas, keep them slightly visible or fade
        self.play(
            FadeOut(formulas), FadeOut(flow_exp), FadeOut(sec_formula),
            run_time=0.6,
        )

        # Restore neuron to center
        self.play(neuron_group.animate.scale(1 / 0.55).shift(RIGHT * 3.5 + DOWN * 0.3), run_time=0.6)

        # ============================================================
        # 3b. ТООЦООЛОЛ - томьёонд тоо орлуулах
        # ============================================================
        sec2 = Text("4. Тооцоолол", font_size=36, color=BLUE)
        sec2.to_edge(UP, buff=0.5)
        self.play(Write(sec2), run_time=0.7)

        # Show the general formula first, then substitute
        general_formula = Tex(
            r"z = \sum_{i} w_i \cdot x_i + b",
            font_size=28, color=GREY_B,
        )
        general_formula.to_edge(DOWN, buff=3.5)
        self.play(FadeIn(general_formula), run_time=0.5)
        self.wait(0.5)

        # Bias label
        bias_note = Text("b = 0.1 (хазайлт)", font_size=16, color=GREY_B)
        bias_note.next_to(big_neuron, DOWN, buff=0.3)
        self.play(FadeIn(bias_note), run_time=0.4)

        # Now substitute numbers
        line1 = Tex(
            r"z = w_1 \cdot x_1 + w_2 \cdot x_2 + w_3 \cdot x_3 + b",
            font_size=26,
        )

        line2 = Tex(
            r"z = (0.5)(0.9) + (-0.2)(0.3) + (0.8)(0.7) + 0.1",
            font_size=26,
        )

        line3 = Tex(
            r"z = 0.45 + (-0.06) + 0.56 + 0.1",
            font_size=26,
        )

        line4 = Tex(
            r"z = 1.05",
            font_size=30, color=YELLOW,
        )

        # Sigmoid step
        line5 = Tex(
            r"a = \sigma(1.05) = \frac{1}{1 + e^{-1.05}} = 0.74",
            font_size=28, color=GREEN,
        )

        calc_lines = VGroup(line1, line2, line3, line4, line5)
        calc_lines.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        calc_lines.to_edge(DOWN, buff=0.3)

        # Transform general formula into expanded form
        self.play(ReplacementTransform(general_formula, line1), run_time=0.8)
        self.wait(0.5)

        sub_label = Text("тоо орлуулъя", font_size=15, color=YELLOW)
        sub_label.next_to(line1, RIGHT, buff=0.3)
        self.play(FadeIn(sub_label), run_time=0.3)

        self.play(Write(line2), FadeOut(sub_label), run_time=1.0)
        self.wait(0.5)

        self.play(Write(line3), run_time=0.8)
        self.wait(0.5)

        self.play(Write(line4), run_time=0.6)
        self.wait(0.8)

        # Now apply sigmoid
        sig_label = Text("sigmoid хэрэглэнэ", font_size=15, color=GREEN)
        sig_label.next_to(line4, RIGHT, buff=0.3)
        self.play(FadeIn(sig_label), run_time=0.3)

        self.play(Write(line5), FadeOut(sig_label), run_time=1.0)
        self.wait(1.0)

        result_note = Text("Нейроны гаралт: 0.74", font_size=20, color=GREEN)
        result_note.next_to(line5, DOWN, buff=0.2)
        self.play(FadeIn(result_note), run_time=0.5)
        self.wait(2.0)

        # Clean calc
        self.play(
            FadeOut(calc_lines), FadeOut(result_note), FadeOut(bias_note),
            run_time=0.6,
        )

        # ============================================================
        # 4.  АЛХАМ 2: Идэвхжүүлэх функц (Sigmoid)
        # ============================================================
        self.play(FadeOut(sec2), run_time=0.3)
        sec3 = Text("5. Идэвхжүүлэх функц (Sigmoid)", font_size=36, color=BLUE)
        sec3.to_edge(UP, buff=0.5)
        self.play(Write(sec3), run_time=0.7)

        # Move neuron diagram to the left
        neuron_group = VGroup(
            big_neuron, sigma_inside, input_circles, input_labels,
            input_arrows, weight_labels, out_arrow, out_label,
        )
        self.play(neuron_group.animate.scale(0.6).shift(LEFT * 3 + UP * 0.5), run_time=0.7)

        # Draw sigmoid curve on the right
        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[0, 1, 0.5],
            width=5,
            height=3,
            axis_config={"stroke_width": 2, "include_tip": True},
        )
        axes.move_to(RIGHT * 2 + DOWN * 0.3)

        x_label = Tex("z", font_size=24)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.15)
        y_label = Tex(r"\sigma(z)", font_size=24)
        y_label.next_to(axes.y_axis, UP, buff=0.15)

        # Sigmoid function
        sigmoid_curve = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-x)),
            color=YELLOW,
            stroke_width=3,
        )

        # Formula
        sig_formula = Tex(
            r"\sigma(z) = \frac{1}{1 + e^{-z}}",
            font_size=28, color=YELLOW,
        )
        sig_formula.next_to(axes, UP, buff=0.4)

        self.play(ShowCreation(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        self.play(Write(sig_formula), run_time=0.8)
        self.play(ShowCreation(sigmoid_curve), run_time=1.5)
        self.wait(0.5)

        # Mark our z = 1.05 on the curve
        z_val = 1.05
        sig_val = 1 / (1 + np.exp(-z_val))  # ≈ 0.741

        dot_on_curve = Dot(
            axes.c2p(z_val, sig_val),
            color=GREEN, radius=0.08,
        )

        # Dashed lines to axes
        h_dash = DashedLine(
            axes.c2p(z_val, 0), axes.c2p(z_val, sig_val),
            stroke_width=2, color=GREEN,
        )
        v_dash = DashedLine(
            axes.c2p(0, sig_val), axes.c2p(z_val, sig_val),
            stroke_width=2, color=GREEN,
        )

        z_mark = Tex(r"z = 1.05", font_size=18, color=GREEN)
        z_mark.next_to(h_dash, DOWN, buff=0.15)

        out_val_label = Tex(r"\sigma = 0.74", font_size=18, color=GREEN)
        out_val_label.next_to(v_dash, LEFT, buff=0.15)

        self.play(
            ShowCreation(h_dash), ShowCreation(v_dash),
            FadeIn(dot_on_curve),
            run_time=0.8,
        )
        self.play(FadeIn(z_mark), FadeIn(out_val_label), run_time=0.5)
        self.wait(0.5)

        exp3 = Text(
            "Sigmoid функц нь ямар ч тоог 0-1 хооронд шахдаг.\n"
            "z = 1.05 → σ(1.05) = 0.74  Энэ бол нейроны гаралт!",
            font_size=17, color=GREY_A,
        )
        exp3.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(exp3), run_time=0.6)
        self.wait(2.5)

        # Show key properties
        prop1 = Text("Сөрөг тоо → 0-д ойр", font_size=16, color=RED_B)
        prop2 = Text("Эерэг тоо → 1-д ойр", font_size=16, color=GREEN_B)
        prop3 = Text("0 орчим → 0.5", font_size=16, color=GREY_A)
        props = VGroup(prop1, prop2, prop3)
        props.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        props.next_to(axes, LEFT, buff=0.5).shift(DOWN * 0.8)

        self.play(FadeOut(exp3), run_time=0.3)
        for p in props:
            self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.4)
            self.wait(0.3)

        self.wait(1.5)

        # Clean sigmoid section
        sigmoid_stuff = VGroup(
            axes, x_label, y_label, sigmoid_curve, sig_formula,
            dot_on_curve, h_dash, v_dash, z_mark, out_val_label, props,
        )
        self.play(FadeOut(sigmoid_stuff), FadeOut(sec3), run_time=0.6)

        # Restore neuron position
        self.play(neuron_group.animate.scale(1 / 0.6).shift(RIGHT * 3 + DOWN * 0.5), run_time=0.6)

        # ============================================================
        # 5.  ЖИНГИЙН НӨЛӨӨ - weight-ийн утга яагаад чухал вэ
        # ============================================================
        sec4 = Text("6. Жин (weight) яагаад чухал вэ?", font_size=36, color=BLUE)
        sec4.to_edge(UP, buff=0.5)
        self.play(Write(sec4), run_time=0.7)

        # Highlight positive weight arrow (thick blue)
        pos_arrow = input_arrows[0]  # w = 0.5
        neg_arrow = input_arrows[1]  # w = -0.2

        self.play(
            pos_arrow.animate.set_stroke(width=5),
            run_time=0.5,
        )
        pos_exp = Text("Эерэг жин → оролтыг \"дэмждэг\"", font_size=18, color=BLUE)
        pos_exp.to_edge(DOWN, buff=1.2)
        self.play(FadeIn(pos_exp), run_time=0.5)
        self.wait(1.5)

        self.play(
            pos_arrow.animate.set_stroke(width=2),
            neg_arrow.animate.set_stroke(width=5),
            run_time=0.5,
        )
        neg_exp = Text("Сөрөг жин → оролтыг \"дарангуйлдаг\"", font_size=18, color=RED)
        neg_exp.next_to(pos_exp, DOWN, buff=0.3)
        self.play(FadeIn(neg_exp), run_time=0.5)
        self.wait(1.5)

        self.play(neg_arrow.animate.set_stroke(width=2), run_time=0.3)

        big_w_exp = Text(
            "Жин том → оролтын нөлөө их\n"
            "Жин бага → оролтын нөлөө бага",
            font_size=18, color=GREY_A,
        )
        big_w_exp.next_to(neg_exp, DOWN, buff=0.3)
        self.play(FadeIn(big_w_exp), run_time=0.5)
        self.wait(2.0)

        self.play(FadeOut(pos_exp), FadeOut(neg_exp), FadeOut(big_w_exp), run_time=0.5)

        # ============================================================
        # 6.  БҮТЭН СҮЛЖЭЭГЭЭР ДАМЖИХ - жишээ тоонуудтай
        # ============================================================
        self.play(FadeOut(sec4), FadeOut(neuron_group), run_time=0.5)

        sec5 = Text("7. Бүтэн сүлжээгээр дамжих", font_size=36, color=BLUE)
        sec5.to_edge(UP, buff=0.5)
        self.play(Write(sec5), run_time=0.7)

        # Build a small 3-2-2 network with actual values
        def make_neuron(r=0.3):
            c = Circle(radius=r)
            c.set_stroke(WHITE, 2)
            c.set_fill(BLACK, 1)
            return c

        # Input layer
        in1 = make_neuron()
        in2 = make_neuron()
        in3 = make_neuron()
        in_layer = VGroup(in1, in2, in3).arrange(DOWN, buff=0.8)
        in_layer.shift(LEFT * 4.5)

        # Hidden layer
        h1 = make_neuron()
        h2 = make_neuron()
        h_layer = VGroup(h1, h2).arrange(DOWN, buff=1.2)

        # Output layer
        o1 = make_neuron()
        out_layer = VGroup(o1)
        out_layer.shift(RIGHT * 4.5)

        all_layers = VGroup(in_layer, h_layer, out_layer)
        all_layers.center().shift(DOWN * 0.3)

        # Input values
        in_vals = [0.8, 0.4, 0.6]
        in_val_labels = VGroup()
        for neuron, v in zip(in_layer, in_vals):
            lbl = Text(str(v), font_size=18)
            lbl.move_to(neuron.get_center())
            in_val_labels.add(lbl)

        # Layer labels
        in_lbl = Text("Оролт", font_size=18, color=GREY_B)
        in_lbl.next_to(in_layer, DOWN, buff=0.4)
        h_lbl = Text("Нууц", font_size=18, color=GREY_B)
        h_lbl.next_to(h_layer, DOWN, buff=0.4)
        o_lbl = Text("Гаралт", font_size=18, color=GREY_B)
        o_lbl.next_to(out_layer, DOWN, buff=0.4)

        self.play(
            FadeIn(in_layer), FadeIn(h_layer), FadeIn(out_layer),
            FadeIn(in_lbl), FadeIn(h_lbl), FadeIn(o_lbl),
            run_time=0.7,
        )

        # Show input values
        in_anims = []
        for neuron, v in zip(in_layer, in_vals):
            in_anims.append(neuron.animate.set_fill(WHITE, opacity=v))
        self.play(*in_anims, run_time=0.6)
        self.play(FadeIn(in_val_labels), run_time=0.4)
        self.wait(0.5)

        # Draw edges input → hidden with weight labels
        # h1 weights: [0.3, 0.5, -0.1], bias 0.2
        # h2 weights: [-0.4, 0.7, 0.2], bias -0.1
        w_h1 = [0.3, 0.5, -0.1]
        w_h2 = [-0.4, 0.7, 0.2]
        b_h = [0.2, -0.1]

        edges_ih = VGroup()
        edge_w_labels = VGroup()
        for target, weights in [(h1, w_h1), (h2, w_h2)]:
            for src, w in zip(in_layer, weights):
                col = BLUE if w > 0 else RED
                e = Line(
                    src.get_right(), target.get_left(),
                    stroke_width=abs(w) * 4 + 1,
                    stroke_color=col,
                    stroke_opacity=0.6,
                )
                edges_ih.add(e)

                wl = Tex(f"{w}", font_size=14, color=col)
                wl.move_to(e.point_from_proportion(0.5))
                wl.shift(UP * 0.12)
                edge_w_labels.add(wl)

        self.play(ShowCreation(edges_ih, lag_ratio=0.05), run_time=1.0)
        self.play(FadeIn(edge_w_labels), run_time=0.6)
        self.wait(0.5)

        # Calculate h1
        # z_h1 = 0.3*0.8 + 0.5*0.4 + (-0.1)*0.6 + 0.2 = 0.24 + 0.20 - 0.06 + 0.2 = 0.58
        z_h1 = sum(w * x for w, x in zip(w_h1, in_vals)) + b_h[0]
        a_h1 = 1 / (1 + np.exp(-z_h1))

        calc_h1 = VGroup(
            Tex(r"h_1: z = 0.3 \times 0.8 + 0.5 \times 0.4 + (-0.1) \times 0.6 + 0.2", font_size=20),
            Tex(f"z = {z_h1:.2f}", font_size=20),
            Tex(f"\\sigma({z_h1:.2f}) = {a_h1:.2f}", font_size=20, color=GREEN),
        )
        calc_h1.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        calc_h1.to_edge(DOWN, buff=0.6)

        for line in calc_h1:
            self.play(Write(line), run_time=0.7)
            self.wait(0.3)

        # Light up h1
        h1_val_label = Text(f"{a_h1:.2f}", font_size=18, color=GREEN)
        h1_val_label.move_to(h1.get_center())
        self.play(
            h1.animate.set_fill(GREEN, opacity=a_h1),
            FadeIn(h1_val_label),
            run_time=0.6,
        )
        self.wait(1.0)

        # Calculate h2
        z_h2 = sum(w * x for w, x in zip(w_h2, in_vals)) + b_h[1]
        a_h2 = 1 / (1 + np.exp(-z_h2))

        self.play(FadeOut(calc_h1), run_time=0.3)

        calc_h2 = VGroup(
            Tex(r"h_2: z = (-0.4) \times 0.8 + 0.7 \times 0.4 + 0.2 \times 0.6 + (-0.1)", font_size=20),
            Tex(f"z = {z_h2:.2f}", font_size=20),
            Tex(f"\\sigma({z_h2:.2f}) = {a_h2:.2f}", font_size=20, color=GREEN),
        )
        calc_h2.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        calc_h2.to_edge(DOWN, buff=0.6)

        for line in calc_h2:
            self.play(Write(line), run_time=0.7)
            self.wait(0.3)

        h2_val_label = Text(f"{a_h2:.2f}", font_size=18, color=GREEN)
        h2_val_label.move_to(h2.get_center())
        self.play(
            h2.animate.set_fill(GREEN, opacity=a_h2),
            FadeIn(h2_val_label),
            run_time=0.6,
        )
        self.wait(1.0)

        # Hidden → Output edges
        w_o = [0.6, -0.3]
        b_o = 0.15

        self.play(FadeOut(calc_h2), run_time=0.3)

        edges_ho = VGroup()
        edge_wo_labels = VGroup()
        for src, w in zip(h_layer, w_o):
            col = BLUE if w > 0 else RED
            e = Line(
                src.get_right(), o1.get_left(),
                stroke_width=abs(w) * 4 + 1,
                stroke_color=col,
                stroke_opacity=0.6,
            )
            edges_ho.add(e)
            wl = Tex(f"{w}", font_size=16, color=col)
            wl.move_to(e.point_from_proportion(0.5))
            wl.shift(UP * 0.12)
            edge_wo_labels.add(wl)

        self.play(ShowCreation(edges_ho), FadeIn(edge_wo_labels), run_time=0.7)

        # Calculate output
        z_o = w_o[0] * a_h1 + w_o[1] * a_h2 + b_o
        a_o = 1 / (1 + np.exp(-z_o))

        calc_o = VGroup(
            Tex(f"out: z = 0.6 \\times {a_h1:.2f} + (-0.3) \\times {a_h2:.2f} + 0.15", font_size=20),
            Tex(f"z = {z_o:.2f}", font_size=20),
            Tex(f"\\sigma({z_o:.2f}) = {a_o:.2f}", font_size=20, color=YELLOW),
        )
        calc_o.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        calc_o.to_edge(DOWN, buff=0.6)

        for line in calc_o:
            self.play(Write(line), run_time=0.7)
            self.wait(0.3)

        o_val_label = Text(f"{a_o:.2f}", font_size=18, color=YELLOW)
        o_val_label.move_to(o1.get_center())
        self.play(
            o1.animate.set_fill(YELLOW, opacity=a_o),
            FadeIn(o_val_label),
            run_time=0.6,
        )
        self.wait(1.0)

        # Final output explanation
        result_text = Text(
            f"Сүлжээний эцсийн гаралт: {a_o:.2f}",
            font_size=22, color=YELLOW,
        )
        result_text.next_to(calc_o, UP, buff=0.3)
        self.play(FadeIn(result_text), run_time=0.5)
        self.wait(2.0)

        # Clean
        self.play(FadeOut(calc_o), FadeOut(result_text), run_time=0.5)

        # ============================================================
        # 7.  ДҮГНЭЛТ
        # ============================================================
        self.play(FadeOut(sec5), run_time=0.3)
        sec6 = Text("Дүгнэлт", font_size=36, color=BLUE)
        sec6.to_edge(UP, buff=0.5)
        self.play(Write(sec6), run_time=0.6)

        summary = VGroup(
            Text("1. Нейрон бүр: оролт × жин → нийлбэр → sigmoid", font_size=18),
            Text("2. Жин эерэг = дэмжих, жин сөрөг = дарангуйлах", font_size=18),
            Text("3. Sigmoid: утгыг 0-1 хооронд шахдаг", font_size=18),
            Text("4. Давхарга бүрийн гаралт → дараагийн давхаргын оролт", font_size=18),
            Text("5. Эцсийн давхаргын утга = сүлжээний хариулт", font_size=18),
        )
        summary.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.to_edge(DOWN, buff=0.6)

        for item in summary:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.4)
            self.wait(0.4)

        self.wait(3.0)

        # Final fade
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=1.5)
        self.wait(0.5)
