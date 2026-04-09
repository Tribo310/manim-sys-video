from manimlib import *
import numpy as np

FONT = "Liberation Sans"


class NNTraining(Scene):
    def construct(self):
        np.random.seed(42)

        # ============ HELPERS ============
        def make_layer(n, r=0.22):
            layer = VGroup()
            for _ in range(n):
                c = Circle(radius=r)
                c.set_stroke(WHITE, 2)
                c.set_fill(BLACK, 1)
                layer.add(c)
            layer.arrange(DOWN, buff=0.35)
            return layer

        def make_edges(la, lb, sw=0.8, color=GREY, opacity=0.2):
            edges = VGroup()
            for a in la:
                for b in lb:
                    edges.add(Line(a.get_right(), b.get_left(),
                                   stroke_width=sw, stroke_color=color,
                                   stroke_opacity=opacity))
            return edges

        def part_title(text, sub=None):
            t = Text(text, font=FONT, font_size=42)
            t.move_to(ORIGIN)
            self.play(FadeIn(t, scale=0.8), run_time=1.0)
            if sub:
                s = Text(sub, font=FONT, font_size=22, color=GREY_B)
                s.next_to(t, DOWN, buff=0.4)
                self.play(FadeIn(s), run_time=0.5)
                self.wait(1.5)
                self.play(FadeOut(t), FadeOut(s), run_time=0.7)
            else:
                self.wait(1.5)
                self.play(FadeOut(t), run_time=0.7)

        def section(text):
            t = Text(text, font=FONT, font_size=34, color=BLUE)
            t.to_edge(UP, buff=0.5)
            self.play(Write(t), run_time=0.7)
            return t

        def clear_all():
            everything = Group(*self.mobjects)
            self.play(FadeOut(everything), run_time=0.6)

        # ================================================================
        #  НЭЭЛТ: Өмнөх бичлэгийн товч сэргээлт
        # ================================================================
        part_title("IV. Сүлжээг яаж сургадаг вэ?", "Training / Сургалт")

        # --- Товч сэргээлт ---
        s = section("Өмнөх бичлэгээс...")
        recap_items = VGroup(
            Text("Бид Neural Network-ийн бүтцийг мэдэж авсан:", font=FONT, font_size=20, color=GREY_A),
            Text("  Оролт → Нууц давхарга → Гаралт", font=FONT, font_size=18),
            Text("  z = Σ(w·x) + b,   a = σ(z)", font=FONT, font_size=18),
            Text("  Жин (w) ба Bias (b) нь сүлжээний \"тархи\"", font=FONT, font_size=18, color=YELLOW),
        )
        recap_items.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        recap_items.center().shift(UP * 0.3)
        for item in recap_items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.4)
            self.wait(0.5)

        question = Text(
            "Гэхдээ... жин, bias-ийн утгыг хэн тохируулдаг вэ?",
            font=FONT, font_size=22, color=RED,
        )
        question.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(question), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(question), run_time=0.3)

        answer = Text(
            "Сүлжээ өөрөө СУРЧ олдог!  →  Яаж?",
            font=FONT, font_size=22, color=GREEN,
        )
        answer.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(answer), run_time=0.6)
        self.wait(2.0)
        clear_all()

        # ================================================================
        #  1. LOSS ФУНКЦ (Алдааг хэмжих)
        # ================================================================
        part_title("1. Loss функц", "Таамаглал хэр алдаатай вэ?")

        # --- Жишээ: шалгалтын тохиолдол ---
        s = section("1. Loss функц гэж юу вэ?")

        # Бодит жишээ: өмнөх видеоны сүлжээ
        analogy = Text(
            "Шалгалтын жишээг санацгаая:",
            font=FONT, font_size=20, color=GREY_A,
        )
        analogy.next_to(s, DOWN, buff=0.6)
        self.play(FadeIn(analogy), run_time=0.4)

        # Prediction vs Reality
        pred_box = VGroup(
            Text("Сүлжээний таамаглал:", font=FONT, font_size=16, color=BLUE),
            Text("0.72", font=FONT, font_size=36, color=BLUE),
        ).arrange(DOWN, buff=0.15)
        real_box = VGroup(
            Text("Бодит хариулт:", font=FONT, font_size=16, color=GREEN),
            Text("1.00", font=FONT, font_size=36, color=GREEN),
            Text("(Тэнцсэн)", font=FONT, font_size=14, color=GREEN),
        ).arrange(DOWN, buff=0.15)
        vs = Text("vs", font=FONT, font_size=20, color=GREY)

        comp = VGroup(pred_box, vs, real_box).arrange(RIGHT, buff=1.0)
        comp.center().shift(DOWN * 0.3)

        self.play(FadeIn(pred_box), run_time=0.5)
        self.play(FadeIn(vs), run_time=0.3)
        self.play(FadeIn(real_box), run_time=0.5)
        self.wait(1.0)

        error_text = Text(
            "Алдаа = Бодит - Таамаглал = 1.00 - 0.72 = 0.28",
            font=FONT, font_size=18, color=RED,
        )
        error_text.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(error_text), run_time=0.5)
        self.wait(2.0)
        clear_all()

        # --- MSE томьёо ---
        s = section("2. MSE (Mean Squared Error)")

        mse_explain = Text(
            "Бүх жишээн дээрх алдааг нэг тоогоор илэрхийлдэг:",
            font=FONT, font_size=18, color=GREY_A,
        )
        mse_explain.next_to(s, DOWN, buff=0.6)
        self.play(FadeIn(mse_explain), run_time=0.4)

        mse_formula = Tex(
            r"L = \frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2",
            font_size=40,
        )
        mse_formula.center()
        mse_box = SurroundingRectangle(mse_formula, color=YELLOW, buff=0.15, stroke_width=2)
        self.play(Write(mse_formula), ShowCreation(mse_box), run_time=1.0)
        self.wait(0.5)

        # Тайлбар
        mse_parts = VGroup(
            Tex(r"\hat{y}", font_size=22, color=BLUE),
            Text(" = таамаглал,", font=FONT, font_size=16),
            Tex(r"y", font_size=22, color=GREEN),
            Text(" = бодит,", font=FONT, font_size=16),
            Tex(r"n", font_size=22, color=GREY_A),
            Text(" = жишээний тоо", font=FONT, font_size=16),
        ).arrange(RIGHT, buff=0.15)
        mse_parts.next_to(mse_box, DOWN, buff=0.4)
        self.play(FadeIn(mse_parts), run_time=0.5)
        self.wait(1.5)

        # Бодит тооцоолол
        self.play(FadeOut(mse_explain), FadeOut(mse_parts), run_time=0.3)

        calc_title = Text("Жишээ тооцоолол:", font=FONT, font_size=18, color=YELLOW)
        calc_title.next_to(mse_box, DOWN, buff=0.3)
        self.play(FadeIn(calc_title), run_time=0.3)

        # Хүснэгт: 3 жишээ
        calc_data = [
            ("Сурагч А", "0.72", "1", "(0.72-1)² = 0.08"),
            ("Сурагч Б", "0.41", "0", "(0.41-0)² = 0.17"),
            ("Сурагч В", "0.88", "1", "(0.88-1)² = 0.01"),
        ]
        calc_rows = VGroup()
        for name, pred, real, err in calc_data:
            row = VGroup(
                Text(name, font=FONT, font_size=14, color=GREY_A),
                Tex(r"\hat{y}=" + pred, font_size=18, color=BLUE),
                Tex(r"y=" + real, font_size=18, color=GREEN),
                Text(err, font=FONT, font_size=14, color=RED),
            ).arrange(RIGHT, buff=0.4)
            calc_rows.add(row)
        calc_rows.arrange(DOWN, buff=0.2)
        calc_rows.next_to(calc_title, DOWN, buff=0.25)

        for row in calc_rows:
            self.play(FadeIn(row), run_time=0.4)

        mse_result = Tex(
            r"L = \frac{0.08 + 0.17 + 0.01}{3} = 0.087",
            font_size=24, color=YELLOW,
        )
        mse_result.next_to(calc_rows, DOWN, buff=0.3)
        self.play(Write(mse_result), run_time=0.8)
        self.wait(1.0)

        loss_goal = Text(
            "Зорилго: L-ийг аль болох 0 руу ойртуулах!",
            font=FONT, font_size=20, color=GREEN,
        )
        loss_goal.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(loss_goal), run_time=0.5)
        self.wait(2.5)
        clear_all()

        # ================================================================
        #  2. GRADIENT DESCENT (Алдааг багасгах)
        # ================================================================
        part_title("2. Gradient Descent", "Алдааг багасгах арга")

        # --- Уулын зүйрлэл ---
        s = section("3. Gradient Descent гэж юу вэ?")

        analogy2 = Text(
            "Зүйрлэл: Манантай уулнаас нүдээ аниад бууж байгаа...",
            font=FONT, font_size=18, color=GREY_A,
        )
        analogy2.next_to(s, DOWN, buff=0.5)
        self.play(FadeIn(analogy2), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(analogy2), run_time=0.3)

        # Loss landscape график
        axes_gd = Axes(
            x_range=[-3, 3, 1], y_range=[0, 5, 1],
            width=8, height=4,
            axis_config={"stroke_width": 2, "include_tip": True},
        )
        axes_gd.center().shift(DOWN * 0.3)
        xl_gd = Text("жин (w)", font=FONT, font_size=14)
        xl_gd.next_to(axes_gd.x_axis, RIGHT, buff=0.15)
        yl_gd = Text("Loss (L)", font=FONT, font_size=14)
        yl_gd.next_to(axes_gd.y_axis, UP, buff=0.15)

        # Гүдгэр муруй (Loss landscape)
        loss_curve = axes_gd.get_graph(
            lambda x: 0.5 * x ** 2 + 0.3,
            color=YELLOW, stroke_width=3,
        )
        self.play(ShowCreation(axes_gd), FadeIn(xl_gd), FadeIn(yl_gd), run_time=0.6)
        self.play(ShowCreation(loss_curve), run_time=1.0)

        # Minimum цэг
        min_dot = Dot(axes_gd.c2p(0, 0.3), color=GREEN, radius=0.08)
        min_label = Text("хамгийн бага Loss", font=FONT, font_size=14, color=GREEN)
        min_label.next_to(min_dot, DOWN, buff=0.2)
        self.play(FadeIn(min_dot), FadeIn(min_label), run_time=0.4)
        self.wait(0.5)

        # Бөмбөг (одоогийн байрлал)
        start_x = 2.2
        ball = Dot(axes_gd.c2p(start_x, 0.5 * start_x ** 2 + 0.3),
                   color=RED, radius=0.12)
        ball_label = Text("Одоогийн жин", font=FONT, font_size=14, color=RED)
        ball_label.next_to(ball, UP, buff=0.15)
        self.play(FadeIn(ball), FadeIn(ball_label), run_time=0.4)
        self.wait(0.5)

        # Gradient сум (налуу чиглэл)
        grad_arrow = Arrow(
            axes_gd.c2p(start_x, 0.5 * start_x ** 2 + 0.3),
            axes_gd.c2p(start_x - 0.8, 0.5 * (start_x - 0.8) ** 2 + 0.3),
            color=TEAL, stroke_width=3,
        )
        grad_label = Text("Gradient чиглэл", font=FONT, font_size=14, color=TEAL)
        grad_label.next_to(grad_arrow, UP, buff=0.1)
        self.play(ShowCreation(grad_arrow), FadeIn(grad_label), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(grad_arrow), FadeOut(grad_label), FadeOut(ball_label), run_time=0.3)

        # Бөмбөгийг алхам алхамаар гулсуулах
        step_text = Text(
            "Gradient-ийн эсрэг чиглэлд алхам хийнэ",
            font=FONT, font_size=17, color=TEAL,
        )
        step_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(step_text), run_time=0.4)

        positions = [2.2, 1.5, 0.9, 0.5, 0.2, 0.05]
        for x_pos in positions[1:]:
            new_point = axes_gd.c2p(x_pos, 0.5 * x_pos ** 2 + 0.3)
            self.play(ball.animate.move_to(new_point), run_time=0.5)
            self.wait(0.2)

        arrived = Text("Loss хамгийн бага цэгт хүрлээ!", font=FONT, font_size=18, color=GREEN)
        arrived.next_to(step_text, UP, buff=0.2)
        self.play(FadeIn(arrived), run_time=0.4)
        self.wait(2.0)
        clear_all()

        # --- Жингийн шинэчлэлтийн томьёо ---
        s = section("4. Жин шинэчлэх томьёо")

        update_formula = Tex(
            r"w_{\text{new}} = w_{\text{old}} - \alpha \cdot \frac{\partial L}{\partial w}",
            font_size=38,
        )
        update_formula.center().shift(UP * 0.5)
        update_box = SurroundingRectangle(update_formula, color=YELLOW, buff=0.15, stroke_width=2)
        self.play(Write(update_formula), ShowCreation(update_box), run_time=1.0)
        self.wait(0.5)

        parts_explain = VGroup(
            VGroup(
                Tex(r"\alpha", font_size=24, color=TEAL),
                Text(" = learning rate (сургалтын хурд)", font=FONT, font_size=16),
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Tex(r"\frac{\partial L}{\partial w}", font_size=24, color=RED),
                Text(" = gradient (налуугийн хэмжээ)", font=FONT, font_size=16),
            ).arrange(RIGHT, buff=0.15),
        )
        parts_explain.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        parts_explain.next_to(update_box, DOWN, buff=0.5)

        for p in parts_explain:
            self.play(FadeIn(p), run_time=0.5)
            self.wait(0.5)

        self.wait(1.0)

        # Learning rate-ийн нөлөө
        self.play(FadeOut(parts_explain), run_time=0.3)

        lr_title = Text("Learning rate хэтэрхий том/жижиг бол?", font=FONT, font_size=18, color=YELLOW)
        lr_title.next_to(update_box, DOWN, buff=0.4)
        self.play(FadeIn(lr_title), run_time=0.4)

        # Жижиг lr vs том lr
        lr_small = VGroup(
            Text("α бага:", font=FONT, font_size=16, color=TEAL),
            Text("Удаан суралцана", font=FONT, font_size=15),
            Text("Гэхдээ тогтвортой", font=FONT, font_size=15, color=GREEN),
        ).arrange(DOWN, buff=0.1)
        lr_small_box = SurroundingRectangle(lr_small, color=TEAL, buff=0.15, stroke_width=1.5)

        lr_big = VGroup(
            Text("α том:", font=FONT, font_size=16, color=RED),
            Text("Хурдан суралцана", font=FONT, font_size=15),
            Text("Гэхдээ алгасч болно!", font=FONT, font_size=15, color=RED),
        ).arrange(DOWN, buff=0.1)
        lr_big_box = SurroundingRectangle(lr_big, color=RED, buff=0.15, stroke_width=1.5)

        lr_comp = VGroup(
            VGroup(lr_small, lr_small_box),
            VGroup(lr_big, lr_big_box),
        ).arrange(RIGHT, buff=1.5)
        lr_comp.next_to(lr_title, DOWN, buff=0.3)

        self.play(FadeIn(lr_small), ShowCreation(lr_small_box), run_time=0.5)
        self.play(FadeIn(lr_big), ShowCreation(lr_big_box), run_time=0.5)
        self.wait(2.5)
        clear_all()

        # ================================================================
        #  3. BACKPROPAGATION (Gradient тооцоолох)
        # ================================================================
        part_title("3. Backpropagation", "Gradient-г буцааж тооцоолох")

        s = section("5. Backpropagation гэж юу вэ?")

        bp_explain = Text(
            "Сүлжээний алдааг давхарга бүрт хэрхэн хуваарилах вэ?",
            font=FONT, font_size=18, color=GREY_A,
        )
        bp_explain.next_to(s, DOWN, buff=0.5)
        self.play(FadeIn(bp_explain), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(bp_explain), run_time=0.3)

        # Сүлжээ зурах: 2 → 2 → 1
        def mk(r=0.4):
            c = Circle(radius=r)
            c.set_stroke(WHITE, 2)
            c.set_fill(BLACK, 1)
            return c

        i1 = mk(); i2 = mk()
        il = VGroup(i1, i2).arrange(DOWN, buff=1.8).shift(LEFT * 4.5)

        h1 = mk(); h2 = mk()
        hl = VGroup(h1, h2).arrange(DOWN, buff=1.8)

        o1 = mk()
        ol = VGroup(o1).shift(RIGHT * 4.5)

        VGroup(il, hl, ol).center().shift(DOWN * 0.3)

        # Labels
        i1_lbl = Text("x₁", font=FONT, font_size=16, color=BLUE)
        i1_lbl.next_to(i1, LEFT, buff=0.3)
        i2_lbl = Text("x₂", font=FONT, font_size=16, color=BLUE)
        i2_lbl.next_to(i2, LEFT, buff=0.3)
        h1_lbl = Text("h₁", font=FONT, font_size=16, color=YELLOW)
        h1_lbl.move_to(h1)
        h2_lbl = Text("h₂", font=FONT, font_size=16, color=YELLOW)
        h2_lbl.move_to(h2)
        o1_lbl = Text("ŷ", font=FONT, font_size=18, color=GREEN)
        o1_lbl.move_to(o1)
        loss_lbl = Text("Loss", font=FONT, font_size=18, color=RED)
        loss_lbl.next_to(o1, RIGHT, buff=0.8)

        # Холбоосууд
        edges_ih = VGroup()
        for inp in [i1, i2]:
            for hid in [h1, h2]:
                edges_ih.add(Line(inp.get_right(), hid.get_left(),
                                  stroke_width=2, stroke_color=GREY, stroke_opacity=0.5))
        edges_ho = VGroup()
        for hid in [h1, h2]:
            edges_ho.add(Line(hid.get_right(), o1.get_left(),
                              stroke_width=2, stroke_color=GREY, stroke_opacity=0.5))
        loss_arrow = Arrow(o1.get_right(), loss_lbl.get_left(), buff=0.15,
                           stroke_width=2, color=RED)

        # Бүгдийг харуулах
        self.play(
            FadeIn(il), FadeIn(hl), FadeIn(ol),
            FadeIn(i1_lbl), FadeIn(i2_lbl), FadeIn(h1_lbl), FadeIn(h2_lbl), FadeIn(o1_lbl),
            ShowCreation(edges_ih), ShowCreation(edges_ho),
            run_time=0.8,
        )
        self.play(ShowCreation(loss_arrow), FadeIn(loss_lbl), run_time=0.5)
        self.wait(0.5)

        # --- Forward pass (зүүнээс баруун) ---
        fwd_title = Text("1) Forward Pass →", font=FONT, font_size=18, color=GREEN)
        fwd_title.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(fwd_title), run_time=0.4)

        # Flash forward
        for layer_nodes in [il, hl, ol]:
            self.play(
                *[n.animate.set_fill(BLUE, 0.4) for n in layer_nodes],
                run_time=0.3,
            )
            self.wait(0.15)
            self.play(
                *[n.animate.set_fill(BLACK, 1) for n in layer_nodes],
                run_time=0.2,
            )
        self.wait(0.5)

        # --- Backward pass (баруунаас зүүн) ---
        bwd_title = Text("2) Backward Pass ← (Backpropagation)", font=FONT, font_size=18, color=RED)
        bwd_title.next_to(fwd_title, DOWN, buff=0.2)
        self.play(FadeIn(bwd_title), run_time=0.4)

        # Flash backward with RED — gradient буцааж дамжих
        self.play(loss_lbl.animate.set_color(RED).scale(1.2), run_time=0.3)
        self.play(loss_lbl.animate.scale(1/1.2), run_time=0.2)

        # Loss → Output
        self.play(o1.animate.set_fill(RED, 0.5), run_time=0.3)
        grad_o = Tex(r"\frac{\partial L}{\partial w_{ho}}", font_size=18, color=RED)
        grad_o.next_to(edges_ho[0], UP, buff=0.05)
        self.play(FadeIn(grad_o), run_time=0.3)

        # Output → Hidden
        self.play(
            h1.animate.set_fill(RED, 0.3),
            h2.animate.set_fill(RED, 0.3),
            run_time=0.3,
        )
        grad_h = Tex(r"\frac{\partial L}{\partial w_{ih}}", font_size=18, color=RED)
        grad_h.next_to(edges_ih[0], UP, buff=0.05)
        self.play(FadeIn(grad_h), run_time=0.3)

        # Hidden → Input
        self.play(
            i1.animate.set_fill(RED, 0.2),
            i2.animate.set_fill(RED, 0.2),
            run_time=0.3,
        )
        self.wait(1.0)

        bp_summary = Text(
            "Алдааг буцааж дамжуулж, давхарга бүрийн gradient-г олно",
            font=FONT, font_size=17, color=GREY_A,
        )
        bp_summary.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bp_summary), run_time=0.5)
        self.wait(2.0)
        clear_all()

        # --- Chain Rule тайлбар ---
        s = section("6. Chain Rule (Гинжин дүрэм)")

        chain_explain = Text(
            "Backprop нь Chain Rule дээр суурилдаг:",
            font=FONT, font_size=18, color=GREY_A,
        )
        chain_explain.next_to(s, DOWN, buff=0.5)
        self.play(FadeIn(chain_explain), run_time=0.4)

        chain_formula = Tex(
            r"\frac{\partial L}{\partial w} = "
            r"\frac{\partial L}{\partial \hat{y}} \cdot "
            r"\frac{\partial \hat{y}}{\partial z} \cdot "
            r"\frac{\partial z}{\partial w}",
            font_size=34,
        )
        chain_formula.center().shift(UP * 0.2)
        chain_box = SurroundingRectangle(chain_formula, color=YELLOW, buff=0.12, stroke_width=2)
        self.play(Write(chain_formula), ShowCreation(chain_box), run_time=1.0)
        self.wait(0.5)

        # Тайлбар
        chain_parts = VGroup(
            VGroup(
                Tex(r"\frac{\partial L}{\partial \hat{y}}", font_size=22, color=RED),
                Text("= Loss-ийн уламжлал", font=FONT, font_size=15),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Tex(r"\frac{\partial \hat{y}}{\partial z}", font_size=22, color=YELLOW),
                Text("= Sigmoid-ийн уламжлал", font=FONT, font_size=15),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Tex(r"\frac{\partial z}{\partial w}", font_size=22, color=BLUE),
                Text("= Оролтын утга (x)", font=FONT, font_size=15),
            ).arrange(RIGHT, buff=0.1),
        )
        chain_parts.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        chain_parts.next_to(chain_box, DOWN, buff=0.4)

        for p in chain_parts:
            self.play(FadeIn(p), run_time=0.4)
            self.wait(0.3)

        chain_summary = Text(
            "Давхарга бүрийн gradient-г гинжин дүрмээр тооцоолно",
            font=FONT, font_size=17, color=GREEN,
        )
        chain_summary.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(chain_summary), run_time=0.5)
        self.wait(2.5)
        clear_all()

        # ================================================================
        #  4. СУРГАЛТЫН ДАВТАЛТ (Epoch)
        # ================================================================
        part_title("4. Сургалтын давталт", "Epoch бүрт сайжирна")

        s = section("7. Нэг epoch = нэг бүтэн давталт")

        # Сургалтын алхам
        steps = VGroup(
            Text("① Forward Pass: таамаглал гаргана", font=FONT, font_size=18, color=BLUE),
            Text("② Loss тооцоолно: хэр алдаатай вэ?", font=FONT, font_size=18, color=RED),
            Text("③ Backpropagation: gradient олно", font=FONT, font_size=18, color=YELLOW),
            Text("④ Жин шинэчлэнэ: w = w - α·gradient", font=FONT, font_size=18, color=GREEN),
            Text("⑤ Дахин давтана!", font=FONT, font_size=18, color=TEAL),
        )
        steps.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        steps.center().shift(DOWN * 0.2)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.4)
            self.wait(0.5)

        # Тойрог сум (давталтыг илтгэнэ)
        loop_text = Text(
            "Энэ процесс олон мянган удаа давтагдана!",
            font=FONT, font_size=18, color=GREY_A,
        )
        loop_text.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(loop_text), run_time=0.5)
        self.wait(2.5)
        clear_all()

        # --- Loss буурч байгааг харуулах график ---
        s = section("8. Loss буурч байгаа нь")

        axes_loss = Axes(
            x_range=[0, 50, 10], y_range=[0, 1, 0.2],
            width=9, height=4.5,
            axis_config={"stroke_width": 2, "include_tip": True},
        )
        axes_loss.center().shift(DOWN * 0.2)
        xl_loss = Text("Epoch", font=FONT, font_size=16)
        xl_loss.next_to(axes_loss.x_axis, RIGHT, buff=0.15)
        yl_loss = Text("Loss", font=FONT, font_size=16)
        yl_loss.next_to(axes_loss.y_axis, UP, buff=0.15)

        self.play(ShowCreation(axes_loss), FadeIn(xl_loss), FadeIn(yl_loss), run_time=0.6)

        # Loss муруй: exponential decay
        loss_values = [0.85 * np.exp(-0.08 * x) + 0.02 for x in range(51)]
        loss_graph = axes_loss.get_graph(
            lambda x: 0.85 * np.exp(-0.08 * x) + 0.02,
            x_range=[0, 50],
            color=RED, stroke_width=3,
        )

        # Аажмаар зурах
        self.play(ShowCreation(loss_graph), run_time=3.0)
        self.wait(0.5)

        # Epoch тэмдэглэл
        epoch_marks = VGroup()
        for ep, col, txt in [(1, RED, "Epoch 1: Loss=0.80"), (10, YELLOW, "Epoch 10: Loss=0.39"),
                              (30, TEAL, "Epoch 30: Loss=0.10"), (50, GREEN, "Epoch 50: Loss=0.03")]:
            y_val = 0.85 * np.exp(-0.08 * ep) + 0.02
            dot = Dot(axes_loss.c2p(ep, y_val), color=col, radius=0.07)
            lbl = Text(txt, font=FONT, font_size=14, color=col)
            lbl.next_to(dot, UR, buff=0.1)
            epoch_marks.add(VGroup(dot, lbl))

        for mark in epoch_marks:
            self.play(FadeIn(mark), run_time=0.4)
            self.wait(0.3)

        loss_insight = Text(
            "Epoch давтах тусам Loss буурч, сүлжээ илүү нарийвчлалтай болно!",
            font=FONT, font_size=17, color=GREEN,
        )
        loss_insight.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(loss_insight), run_time=0.5)
        self.wait(3.0)
        clear_all()

        # --- Жин өөрчлөгдөж байгааг харуулах ---
        s = section("9. Жин өөрчлөгдөж байгаа нь")

        # Шалгалтын жишээ: epoch бүрт prediction сайжирч байгаа
        epoch_demo = VGroup(
            Text("Сурагч А (бодит: Тэнцсэн = 1.0)", font=FONT, font_size=18, color=GREY_A),
        )
        epoch_demo.next_to(s, DOWN, buff=0.5)
        self.play(FadeIn(epoch_demo), run_time=0.4)

        predictions = [
            (1, 0.52, GREY),
            (5, 0.64, YELLOW),
            (15, 0.78, YELLOW),
            (30, 0.91, GREEN),
            (50, 0.97, GREEN),
        ]

        bars_group = VGroup()
        pred_texts = VGroup()
        bar_width = 1.2
        for idx, (ep, pred, col) in enumerate(predictions):
            bar = Rectangle(
                width=bar_width, height=pred * 3,
                fill_color=col, fill_opacity=0.6,
                stroke_color=col, stroke_width=1.5,
            )
            bar.move_to(LEFT * 3.5 + RIGHT * idx * 1.8 + DOWN * 0.5)
            bar.align_to(DOWN * 2.0, DOWN)

            ep_lbl = Text(f"Ep.{ep}", font=FONT, font_size=14)
            ep_lbl.next_to(bar, DOWN, buff=0.15)
            val_lbl = Text(f"{pred:.2f}", font=FONT, font_size=16, color=col)
            val_lbl.next_to(bar, UP, buff=0.1)

            bars_group.add(VGroup(bar, ep_lbl))
            pred_texts.add(val_lbl)

        # Target line
        target_line = DashedLine(
            LEFT * 4.5 + UP * 1.0, RIGHT * 5.0 + UP * 1.0,
            stroke_width=2, color=GREEN,
        )
        target_lbl = Text("Зорилго: 1.0", font=FONT, font_size=14, color=GREEN)
        target_lbl.next_to(target_line, RIGHT, buff=0.15)

        self.play(ShowCreation(target_line), FadeIn(target_lbl), run_time=0.5)

        for bar_g, val_lbl in zip(bars_group, pred_texts):
            self.play(FadeIn(bar_g), FadeIn(val_lbl), run_time=0.4)
            self.wait(0.3)

        improve_text = Text(
            "Сургалт давтах тусам таамаглал бодит утга руу ойртоно!",
            font=FONT, font_size=17, color=GREEN,
        )
        improve_text.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(improve_text), run_time=0.5)
        self.wait(3.0)
        clear_all()

        # ================================================================
        #  ДҮГНЭЛТ
        # ================================================================
        s = section("Дүгнэлт")

        summary = VGroup(
            Text("1. Loss функц: таамаглалын алдааг тоогоор хэмждэг", font=FONT, font_size=17),
            Text("2. Gradient Descent: алдааг багасгах чиглэлд жинг шинэчилдэг", font=FONT, font_size=17),
            Text("3. Backpropagation: gradient-г буцааж давхарга бүрт тооцоолдог", font=FONT, font_size=17),
            Text("4. Learning Rate: хэт том=тогтворгүй, хэт жижиг=удаан", font=FONT, font_size=17),
            Text("5. Epoch: давталт бүрт Loss буурч, нарийвчлал нэмэгдэнэ", font=FONT, font_size=17),
            Text("6. Жин, bias-ийг сүлжээ өөрөө сурч олдог!", font=FONT, font_size=17, color=GREEN),
        )
        summary.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        summary.center().shift(DOWN * 0.2)

        for item in summary:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.35)
            self.wait(0.3)

        self.wait(3.0)

        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=1.5)
        self.wait(0.5)
