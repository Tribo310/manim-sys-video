from manimlib import *
import numpy as np


class SimpleNNExample(Scene):
    def construct(self):
        np.random.seed(42)

        # ============================================================
        # 1.  БОДЛОГО ТАВИХ
        # ============================================================
        title = Text("Neural Network - Бодит жишээ", font_size=40)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        question = Text(
            "Асуулт: Шалгалтанд тэнцэх үү?",
            font_size=32, color=YELLOW,
        )
        question.next_to(title, DOWN, buff=0.6)
        self.play(Write(question), run_time=1.0)
        self.wait(1.0)

        # Two factors
        factor1 = Text("Хичээл цаг", font_size=24, color=BLUE)
        factor2 = Text("Унтсан цаг", font_size=24, color=GREEN)
        factors = VGroup(factor1, factor2)
        factors.arrange(RIGHT, buff=2.0)
        factors.next_to(question, DOWN, buff=0.8)

        arrow_r = Arrow(factor1.get_bottom(), factor1.get_bottom() + DOWN * 0.8, color=BLUE)
        arrow_r2 = Arrow(factor2.get_bottom(), factor2.get_bottom() + DOWN * 0.8, color=GREEN)

        result = Text("Тэнцэх / Унах ?", font_size=24, color=RED_B)
        result.next_to(VGroup(arrow_r, arrow_r2), DOWN, buff=0.3)

        self.play(FadeIn(factor1, shift=UP * 0.3), FadeIn(factor2, shift=UP * 0.3), run_time=0.7)
        self.play(ShowCreation(arrow_r), ShowCreation(arrow_r2), run_time=0.5)
        self.play(FadeIn(result), run_time=0.5)
        self.wait(1.5)

        self.play(
            FadeOut(title), FadeOut(question), FadeOut(factors),
            FadeOut(arrow_r), FadeOut(arrow_r2), FadeOut(result),
            run_time=0.7,
        )

        # ============================================================
        # 2.  СУРГАЛТЫН ӨГӨГДӨЛ (Training Data)
        # ============================================================
        sec2 = Text("1. Сургалтын өгөгдөл", font_size=34, color=BLUE)
        sec2.to_edge(UP, buff=0.5)
        self.play(Write(sec2), run_time=0.7)

        # Data table
        header = VGroup(
            Text("Хичээл\n(цаг)", font_size=16, color=BLUE),
            Text("Нойр\n(цаг)", font_size=16, color=GREEN),
            Text("Үр дүн", font_size=16, color=RED_B),
        )
        header.arrange(RIGHT, buff=1.2)
        header.shift(UP * 1.5)

        # Underline
        h_line = Line(LEFT * 4, RIGHT * 4, stroke_width=1, color=GREY)
        h_line.next_to(header, DOWN, buff=0.15)

        data = [
            # study_hrs, sleep_hrs, result
            (8, 7, "Тэнцсэн"),
            (6, 8, "Тэнцсэн"),
            (2, 5, "Унасан"),
            (1, 3, "Унасан"),
            (7, 6, "Тэнцсэн"),
            (3, 4, "Унасан"),
        ]

        rows = VGroup()
        for study, sleep, res in data:
            color = GREEN if res == "Тэнцсэн" else RED
            row = VGroup(
                Text(str(study), font_size=18),
                Text(str(sleep), font_size=18),
                Text(res, font_size=18, color=color),
            )
            row.arrange(RIGHT, buff=1.5)
            rows.add(row)

        rows.arrange(DOWN, buff=0.3)
        rows.next_to(h_line, DOWN, buff=0.25)

        table_group = VGroup(header, h_line, rows)
        table_group.center().shift(DOWN * 0.2)

        self.play(FadeIn(header), ShowCreation(h_line), run_time=0.6)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.3)

        self.wait(1.0)

        explain_data = Text(
            "Их хичээллэж, сайн унтсан = тэнцдэг.\n"
            "Бага хичээллэж, муу унтсан = унадаг.",
            font_size=18, color=GREY_A,
        )
        explain_data.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(explain_data), run_time=0.6)
        self.wait(2.0)

        self.play(FadeOut(table_group), FadeOut(explain_data), FadeOut(sec2), run_time=0.6)

        # ============================================================
        # 3.  ӨГӨГДЛИЙГ ХЭВИЙН БОЛГОХ (Normalize)
        # ============================================================
        sec3 = Text("2. Өгөгдлийг бэлтгэх", font_size=34, color=BLUE)
        sec3.to_edge(UP, buff=0.5)
        self.play(Write(sec3), run_time=0.7)

        norm_explain = VGroup(
            Text("Neural Network 0-1 хоорондох тоотой ажилладаг.", font_size=20),
            Text("Тиймээс өгөгдлийг хэвийн болгоно (normalize):", font_size=20),
        )
        norm_explain.arrange(DOWN, buff=0.25)
        norm_explain.shift(UP * 1.5)
        self.play(FadeIn(norm_explain), run_time=0.6)

        # Show normalization
        ne1_label = Text("Хичээл:", font_size=22, color=BLUE)
        ne1_formula = Tex(r"x / 10 \quad 8 \to 0.8", font_size=26)
        ne1 = VGroup(ne1_label, ne1_formula).arrange(RIGHT, buff=0.3)

        ne2_label = Text("Нойр:", font_size=22, color=GREEN)
        ne2_formula = Tex(r"x / 10 \quad 7 \to 0.7", font_size=26)
        ne2 = VGroup(ne2_label, ne2_formula).arrange(RIGHT, buff=0.3)

        ne3_text = Text("Үр дүн:  Тэнцсэн → 1,   Унасан → 0", font_size=22)
        ne3_text.set_color(GREY_A)

        norm_examples = VGroup(ne1, ne2, ne3_text)
        norm_examples.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        norm_examples.center().shift(DOWN * 0.3)

        for ex in norm_examples:
            self.play(FadeIn(ex), run_time=0.8)
            self.wait(0.4)

        self.wait(1.5)
        self.play(FadeOut(norm_explain), FadeOut(norm_examples), FadeOut(sec3), run_time=0.6)

        # ============================================================
        # 4.  СҮЛЖЭЭ БҮТЭЭХ
        # ============================================================
        sec4 = Text("3. Neural Network бүтээх", font_size=34, color=BLUE)
        sec4.to_edge(UP, buff=0.5)
        self.play(Write(sec4), run_time=0.7)

        def make_neuron(r=0.35):
            c = Circle(radius=r)
            c.set_stroke(WHITE, 2)
            c.set_fill(BLACK, 1)
            return c

        # 2 inputs -> 2 hidden -> 1 output
        i1 = make_neuron()
        i2 = make_neuron()
        in_layer = VGroup(i1, i2).arrange(DOWN, buff=1.5)
        in_layer.shift(LEFT * 4.5)

        h1 = make_neuron()
        h2 = make_neuron()
        h_layer = VGroup(h1, h2).arrange(DOWN, buff=1.5)

        o1 = make_neuron()
        out_layer = VGroup(o1).shift(RIGHT * 4.5)

        all_layers = VGroup(in_layer, h_layer, out_layer)
        all_layers.center().shift(DOWN * 0.5)

        # Labels for input neurons
        i1_label = Text("Хичээл", font_size=16, color=BLUE)
        i1_label.next_to(i1, LEFT, buff=0.3)
        i2_label = Text("Нойр", font_size=16, color=GREEN)
        i2_label.next_to(i2, LEFT, buff=0.3)

        # Label for output
        o1_label = Text("Тэнцэх\nмагадлал", font_size=16, color=YELLOW)
        o1_label.next_to(o1, RIGHT, buff=0.3)

        # Layer titles
        lt_in = Text("Оролт", font_size=16, color=GREY_B)
        lt_in.next_to(in_layer, DOWN, buff=0.5)
        lt_h = Text("Нууц давхарга", font_size=16, color=GREY_B)
        lt_h.next_to(h_layer, DOWN, buff=0.5)
        lt_o = Text("Гаралт", font_size=16, color=GREY_B)
        lt_o.next_to(out_layer, DOWN, buff=0.5)

        self.play(
            FadeIn(in_layer), FadeIn(h_layer), FadeIn(out_layer),
            FadeIn(i1_label), FadeIn(i2_label), FadeIn(o1_label),
            FadeIn(lt_in), FadeIn(lt_h), FadeIn(lt_o),
            run_time=0.8,
        )
        self.wait(0.5)

        # Edges with weights
        # i->h weights
        weights_ih = {
            (0, 0): 0.8,   # i1 -> h1
            (0, 1): -0.5,  # i1 -> h2
            (1, 0): 0.6,   # i2 -> h1
            (1, 1): 0.9,   # i2 -> h2
        }
        # h->o weights
        weights_ho = {
            (0, 0): 0.7,   # h1 -> o1
            (1, 0): 0.5,   # h2 -> o1
        }
        biases_h = [0.1, -0.2]
        bias_o = -0.3

        edges_ih = VGroup()
        w_labels_ih = VGroup()
        in_neurons = [i1, i2]
        h_neurons = [h1, h2]

        for (si, hi), w in weights_ih.items():
            col = BLUE if w > 0 else RED
            e = Line(
                in_neurons[si].get_right(), h_neurons[hi].get_left(),
                stroke_width=abs(w) * 3 + 1,
                stroke_color=col,
                stroke_opacity=0.6,
            )
            edges_ih.add(e)
            wl = Text(f"{w}", font_size=13, color=col)
            wl.move_to(e.point_from_proportion(0.45))
            wl.shift(UP * 0.15 + LEFT * 0.1)
            w_labels_ih.add(wl)

        edges_ho = VGroup()
        w_labels_ho = VGroup()
        for (hi, oi), w in weights_ho.items():
            col = BLUE if w > 0 else RED
            e = Line(
                h_neurons[hi].get_right(), o1.get_left(),
                stroke_width=abs(w) * 3 + 1,
                stroke_color=col,
                stroke_opacity=0.6,
            )
            edges_ho.add(e)
            wl = Text(f"{w}", font_size=13, color=col)
            wl.move_to(e.point_from_proportion(0.5))
            wl.shift(UP * 0.15)
            w_labels_ho.add(wl)

        self.play(ShowCreation(edges_ih), run_time=0.8)
        self.play(FadeIn(w_labels_ih), run_time=0.5)
        self.play(ShowCreation(edges_ho), run_time=0.6)
        self.play(FadeIn(w_labels_ho), run_time=0.5)
        self.wait(0.5)

        net_explain = Text(
            "2 оролт (хичээл, нойр) → 2 нууц нейрон → 1 гаралт (магадлал)",
            font_size=17, color=GREY_A,
        )
        net_explain.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(net_explain), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(net_explain), FadeOut(sec4), run_time=0.5)

        # ============================================================
        # 5.  ЖИШЭЭ 1: Тэнцэх сурагч (8 цаг хичээл, 7 цаг нойр)
        # ============================================================
        sec5 = Text("4. Жишээ: 8 цаг хичээллэсэн, 7 цаг унтсан", font_size=30, color=BLUE)
        sec5.to_edge(UP, buff=0.5)
        self.play(Write(sec5), run_time=0.8)

        # Input values
        x1, x2 = 0.8, 0.7  # normalized

        i1_val = Text("0.8", font_size=18, color=BLUE)
        i1_val.move_to(i1.get_center())
        i2_val = Text("0.7", font_size=18, color=GREEN)
        i2_val.move_to(i2.get_center())

        self.play(
            i1.animate.set_fill(BLUE, opacity=0.4),
            i2.animate.set_fill(GREEN, opacity=0.35),
            FadeIn(i1_val), FadeIn(i2_val),
            run_time=0.7,
        )
        self.wait(0.5)

        # Calculate h1: 0.8*0.8 + 0.6*0.7 + 0.1 = 0.64 + 0.42 + 0.1 = 1.16
        z_h1 = weights_ih[(0,0)] * x1 + weights_ih[(1,0)] * x2 + biases_h[0]
        a_h1 = 1 / (1 + np.exp(-z_h1))

        # Calculate h2: (-0.5)*0.8 + 0.9*0.7 + (-0.2) = -0.40 + 0.63 - 0.2 = 0.03
        z_h2 = weights_ih[(0,1)] * x1 + weights_ih[(1,1)] * x2 + biases_h[1]
        a_h2 = 1 / (1 + np.exp(-z_h2))

        # Show h1 calculation
        calc_box = VGroup()

        h1_calc = VGroup(
            Tex(f"h_1: ({weights_ih[(0,0)]})\\times {x1} + ({weights_ih[(1,0)]})\\times {x2} + {biases_h[0]}", font_size=20),
            Tex(f"= {z_h1:.2f} \\quad \\sigma \\to {a_h1:.2f}", font_size=20, color=YELLOW),
        )
        h1_calc.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        h1_calc.to_edge(DOWN, buff=1.2)

        self.play(Write(h1_calc[0]), run_time=0.8)
        self.play(Write(h1_calc[1]), run_time=0.6)

        # Highlight edges to h1 and light up
        self.play(
            edges_ih[0].animate.set_stroke(opacity=1.0),  # i1->h1
            edges_ih[2].animate.set_stroke(opacity=1.0),  # i2->h1
            run_time=0.4,
        )

        h1_val = Text(f"{a_h1:.2f}", font_size=16, color=YELLOW)
        h1_val.move_to(h1.get_center())
        self.play(
            h1.animate.set_fill(YELLOW, opacity=a_h1 * 0.7),
            FadeIn(h1_val),
            run_time=0.5,
        )
        self.play(
            edges_ih[0].animate.set_stroke(opacity=0.6),
            edges_ih[2].animate.set_stroke(opacity=0.6),
            run_time=0.3,
        )
        self.wait(0.8)

        # Show h2 calculation
        h2_calc = VGroup(
            Tex(f"h_2: ({weights_ih[(0,1)]})\\times {x1} + ({weights_ih[(1,1)]})\\times {x2} + ({biases_h[1]})", font_size=20),
            Tex(f"= {z_h2:.2f} \\quad \\sigma \\to {a_h2:.2f}", font_size=20, color=YELLOW),
        )
        h2_calc.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        h2_calc.next_to(h1_calc, DOWN, buff=0.25)

        self.play(FadeOut(h1_calc), run_time=0.2)
        h1_calc.to_edge(DOWN, buff=2.0)
        # Actually let's just show h2 calc at bottom
        h2_calc.to_edge(DOWN, buff=1.0)

        self.play(Write(h2_calc[0]), run_time=0.8)
        self.play(Write(h2_calc[1]), run_time=0.6)

        self.play(
            edges_ih[1].animate.set_stroke(opacity=1.0),
            edges_ih[3].animate.set_stroke(opacity=1.0),
            run_time=0.4,
        )

        h2_val = Text(f"{a_h2:.2f}", font_size=16, color=YELLOW)
        h2_val.move_to(h2.get_center())
        self.play(
            h2.animate.set_fill(YELLOW, opacity=a_h2 * 0.7),
            FadeIn(h2_val),
            run_time=0.5,
        )
        self.play(
            edges_ih[1].animate.set_stroke(opacity=0.6),
            edges_ih[3].animate.set_stroke(opacity=0.6),
            run_time=0.3,
        )
        self.wait(0.8)

        # Output calculation
        z_o = weights_ho[(0,0)] * a_h1 + weights_ho[(1,0)] * a_h2 + bias_o
        a_o = 1 / (1 + np.exp(-z_o))

        self.play(FadeOut(h2_calc), run_time=0.2)

        o_calc = VGroup(
            Tex(f"out: ({weights_ho[(0,0)]})\\times {a_h1:.2f} + ({weights_ho[(1,0)]})\\times {a_h2:.2f} + ({bias_o})", font_size=20),
            Tex(f"= {z_o:.2f} \\quad \\sigma \\to {a_o:.2f}", font_size=20, color=GREEN),
        )
        o_calc.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        o_calc.to_edge(DOWN, buff=1.0)

        self.play(
            edges_ho[0].animate.set_stroke(opacity=1.0),
            edges_ho[1].animate.set_stroke(opacity=1.0),
            run_time=0.4,
        )
        self.play(Write(o_calc[0]), run_time=0.8)
        self.play(Write(o_calc[1]), run_time=0.6)

        o_val = Text(f"{a_o:.2f}", font_size=18, color=GREEN)
        o_val.move_to(o1.get_center())
        self.play(
            o1.animate.set_fill(GREEN, opacity=0.7),
            FadeIn(o_val),
            run_time=0.6,
        )
        self.play(
            edges_ho[0].animate.set_stroke(opacity=0.6),
            edges_ho[1].animate.set_stroke(opacity=0.6),
            run_time=0.3,
        )

        # Verdict
        verdict1 = Text(
            f"Гаралт: {a_o:.0%} → Тэнцэнэ!",
            font_size=24, color=GREEN,
        )
        verdict1.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(o_calc), run_time=0.2)
        self.play(FadeIn(verdict1), run_time=0.6)
        self.wait(2.0)

        # ============================================================
        # 6.  ЖИШЭЭ 2: Унах сурагч (2 цаг хичээл, 3 цаг нойр)
        # ============================================================
        # Reset neurons
        self.play(
            FadeOut(verdict1), FadeOut(sec5),
            FadeOut(i1_val), FadeOut(i2_val),
            FadeOut(h1_val), FadeOut(h2_val), FadeOut(o_val),
            i1.animate.set_fill(BLACK, 1),
            i2.animate.set_fill(BLACK, 1),
            h1.animate.set_fill(BLACK, 1),
            h2.animate.set_fill(BLACK, 1),
            o1.animate.set_fill(BLACK, 1),
            run_time=0.6,
        )

        sec6 = Text("5. Жишээ: 2 цаг хичээллэсэн, 3 цаг унтсан", font_size=30, color=RED_B)
        sec6.to_edge(UP, buff=0.5)
        self.play(Write(sec6), run_time=0.8)

        x1_b, x2_b = 0.2, 0.3

        i1_val2 = Text("0.2", font_size=18, color=BLUE)
        i1_val2.move_to(i1.get_center())
        i2_val2 = Text("0.3", font_size=18, color=GREEN)
        i2_val2.move_to(i2.get_center())

        self.play(
            i1.animate.set_fill(BLUE, opacity=0.15),
            i2.animate.set_fill(GREEN, opacity=0.12),
            FadeIn(i1_val2), FadeIn(i2_val2),
            run_time=0.7,
        )

        # h1
        z_h1b = weights_ih[(0,0)] * x1_b + weights_ih[(1,0)] * x2_b + biases_h[0]
        a_h1b = 1 / (1 + np.exp(-z_h1b))
        # h2
        z_h2b = weights_ih[(0,1)] * x1_b + weights_ih[(1,1)] * x2_b + biases_h[1]
        a_h2b = 1 / (1 + np.exp(-z_h2b))
        # out
        z_ob = weights_ho[(0,0)] * a_h1b + weights_ho[(1,0)] * a_h2b + bias_o
        a_ob = 1 / (1 + np.exp(-z_ob))

        # Animate faster this time
        calc_b = VGroup(
            Tex(f"h_1: z={z_h1b:.2f} \\to \\sigma={a_h1b:.2f}", font_size=20),
            Tex(f"h_2: z={z_h2b:.2f} \\to \\sigma={a_h2b:.2f}", font_size=20),
            Tex(f"out: z={z_ob:.2f} \\to \\sigma={a_ob:.2f}", font_size=20, color=RED),
        )
        calc_b.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        calc_b.to_edge(DOWN, buff=0.8)

        # h1
        h1_val2 = Text(f"{a_h1b:.2f}", font_size=16, color=YELLOW)
        h1_val2.move_to(h1.get_center())
        self.play(
            Write(calc_b[0]),
            h1.animate.set_fill(YELLOW, opacity=a_h1b * 0.7),
            FadeIn(h1_val2),
            run_time=0.8,
        )

        # h2
        h2_val2 = Text(f"{a_h2b:.2f}", font_size=16, color=YELLOW)
        h2_val2.move_to(h2.get_center())
        self.play(
            Write(calc_b[1]),
            h2.animate.set_fill(YELLOW, opacity=a_h2b * 0.7),
            FadeIn(h2_val2),
            run_time=0.8,
        )

        # out
        o_val2 = Text(f"{a_ob:.2f}", font_size=18, color=RED)
        o_val2.move_to(o1.get_center())
        self.play(
            Write(calc_b[2]),
            o1.animate.set_fill(RED, opacity=0.5),
            FadeIn(o_val2),
            run_time=0.8,
        )
        self.wait(0.5)

        verdict2 = Text(
            f"Гаралт: {a_ob:.0%} → Унана!",
            font_size=24, color=RED,
        )
        verdict2.next_to(calc_b, DOWN, buff=0.3)
        self.play(FadeIn(verdict2), run_time=0.5)
        self.wait(2.0)

        # ============================================================
        # 7.  ХАРЬЦУУЛАЛТ
        # ============================================================
        self.play(
            FadeOut(calc_b), FadeOut(verdict2), FadeOut(sec6),
            FadeOut(i1_val2), FadeOut(i2_val2),
            FadeOut(h1_val2), FadeOut(h2_val2), FadeOut(o_val2),
            run_time=0.5,
        )

        # Fade out network
        net_stuff = VGroup(
            in_layer, h_layer, out_layer,
            edges_ih, edges_ho, w_labels_ih, w_labels_ho,
            i1_label, i2_label, o1_label,
            lt_in, lt_h, lt_o,
        )
        self.play(FadeOut(net_stuff), run_time=0.6)

        sec7 = Text("6. Харьцуулалт", font_size=34, color=BLUE)
        sec7.to_edge(UP, buff=0.5)
        self.play(Write(sec7), run_time=0.6)

        # Comparison boxes
        box1 = VGroup(
            Text("Сурагч А", font_size=22, color=GREEN),
            Text("Хичээл: 8 цаг", font_size=18),
            Text("Нойр: 7 цаг", font_size=18),
            Text(f"Үр дүн: {a_o:.0%}", font_size=20, color=GREEN),
            Text("ТЭНЦЭНЭ", font_size=22, color=GREEN),
        )
        box1.arrange(DOWN, buff=0.25)

        rect1 = SurroundingRectangle(box1, color=GREEN, buff=0.3, stroke_width=2)

        box2 = VGroup(
            Text("Сурагч Б", font_size=22, color=RED),
            Text("Хичээл: 2 цаг", font_size=18),
            Text("Нойр: 3 цаг", font_size=18),
            Text(f"Үр дүн: {a_ob:.0%}", font_size=20, color=RED),
            Text("УНАНА", font_size=22, color=RED),
        )
        box2.arrange(DOWN, buff=0.25)

        rect2 = SurroundingRectangle(box2, color=RED, buff=0.3, stroke_width=2)

        comparison = VGroup(
            VGroup(box1, rect1),
            VGroup(box2, rect2),
        )
        comparison.arrange(RIGHT, buff=1.5)
        comparison.center().shift(DOWN * 0.3)

        self.play(FadeIn(box1), ShowCreation(rect1), run_time=0.7)
        self.play(FadeIn(box2), ShowCreation(rect2), run_time=0.7)
        self.wait(2.0)

        explain_final = Text(
            "Neural Network оролтын утгуудаас хамааран\n"
            "0-1 хоорондох магадлал гаргаж өгдөг.",
            font_size=18, color=GREY_A,
        )
        explain_final.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(explain_final), run_time=0.6)
        self.wait(2.5)

        self.play(FadeOut(comparison), FadeOut(explain_final), FadeOut(sec7), run_time=0.6)

        # ============================================================
        # 8.  ДҮГНЭЛТ
        # ============================================================
        sec8 = Text("Дүгнэлт", font_size=36, color=BLUE)
        sec8.to_edge(UP, buff=0.5)
        self.play(Write(sec8), run_time=0.5)

        summary = VGroup(
            Text("1. Бодит асуудлыг тоон хэлбэрт оруулна", font_size=18),
            Text("2. 0-1 хооронд normalize хийнэ", font_size=18),
            Text("3. Оролтуудыг weight-ээр үржүүлж, нийлбэрлэнэ", font_size=18),
            Text("4. Sigmoid-аар магадлал болгоно", font_size=18),
            Text("5. 0.5-аас дээш = тийм, доош = үгүй", font_size=18),
        )
        summary.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        summary.center().shift(DOWN * 0.3)

        for item in summary:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.4)
            self.wait(0.4)

        self.wait(3.0)

        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=1.5)
        self.wait(0.5)
