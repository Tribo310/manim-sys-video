from manimlib import *
import numpy as np
import os

# Видео/зургийг энэ .py файлын хажуугийн "videos" folder-т хадгална
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")


class NNCombined(Scene):
    default_file_writer_config = {"output_directory": OUTPUT_DIR}

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
            t = Text(text, font="Liberation Sans", font_size=42)
            t.move_to(ORIGIN)
            self.play(FadeIn(t, scale=0.8), run_time=1.0)
            if sub:
                s = Text(sub, font="Liberation Sans", font_size=22, color=GREY_B)
                s.next_to(t, DOWN, buff=0.4)
                self.play(FadeIn(s), run_time=0.5)
                self.wait(1.5)
                self.play(FadeOut(t), FadeOut(s), run_time=0.7)
            else:
                self.wait(1.5)
                self.play(FadeOut(t), run_time=0.7)

        def section(text):
            t = Text(text, font="Liberation Sans", font_size=34, color=BLUE)
            t.to_edge(UP, buff=0.5)
            self.play(Write(t), run_time=0.7)
            return t

        def clear_all():
            everything = Group(*self.mobjects)
            self.play(FadeOut(everything), run_time=0.6)

        # ================================================================
        #                  I. NN ГЭЖ ЮУ ВЭ?
        # ================================================================
        part_title("I. Neural Network гэж юу вэ?", "Хиймэл оюун ухааны суурь")

        # --- 1. Оролт ---
        s = section("1. Оролт (Input)")
        pattern = np.array([
            [0.1,0.9,0.9,0.9,0.1],
            [0.1,0.1,0.1,0.8,0.1],
            [0.1,0.5,0.9,0.9,0.1],
            [0.1,0.1,0.1,0.8,0.1],
            [0.1,0.9,0.9,0.9,0.1],
        ])
        grid = VGroup()
        for r in range(5):
            for c in range(5):
                sq = Square(side_length=0.5)
                sq.set_fill(WHITE, opacity=pattern[r][c])
                sq.set_stroke(GREY, 1)
                grid.add(sq)
        grid.arrange_in_grid(5, 5, buff=0.05)
        grid.shift(LEFT * 4 + DOWN * 0.5)
        img_lbl = Text("Зураг (5x5)", font="Liberation Sans", font_size=18)
        img_lbl.next_to(grid, DOWN, buff=0.25)
        self.play(FadeIn(grid, lag_ratio=0.02), FadeIn(img_lbl), run_time=0.8)

        arr = Arrow(LEFT * 1.8 + DOWN * 0.5, RIGHT * 0.0 + DOWN * 0.5, color=YELLOW)
        arr_l = Text("пиксел → тоо", font="Liberation Sans", font_size=16, color=YELLOW)
        arr_l.next_to(arr, UP, buff=0.1)
        nums = VGroup(*[Text(t, font="Liberation Sans", font_size=18) for t in ["0.1","0.9","...","0.9"]])
        nums.arrange(DOWN, buff=0.25)
        nums.move_to(RIGHT * 1.5 + DOWN * 0.5)
        self.play(ShowCreation(arr), FadeIn(arr_l), run_time=0.6)
        self.play(FadeIn(nums), run_time=0.6)

        exp = Text("Компьютер зургийг тоон массив хэлбэрээр хүлээн авдаг.", font="Liberation Sans", font_size=17, color=GREY_A)
        exp.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(exp), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(exp), run_time=0.3)

        # Зураг л биш — аудио, текст ч мөн адил
        other_title = Text("Зураг л биш...", font="Liberation Sans", font_size=22, color=YELLOW)
        other_title.to_edge(DOWN, buff=1.6)
        self.play(FadeIn(other_title), run_time=0.4)
        self.wait(0.5)
        self.play(
            FadeOut(other_title),
            FadeOut(grid), FadeOut(img_lbl),
            FadeOut(arr), FadeOut(arr_l),
            FadeOut(nums),
            run_time=0.4,
        )

        other_items = VGroup(
            Text("Аудио (дуу хоолой)  →  долгионы далайц = тоон цуваа",
                 font="Liberation Sans", font_size=17, color=TEAL),
            Text("Текст (үг, өгүүлбэр)  →  үг бүрийг тоогоор кодлодог",
                 font="Liberation Sans", font_size=17, color=ORANGE),
            Text("Видео  →  фрейм бүр = зургийн тоон массив",
                 font="Liberation Sans", font_size=17, color=PURPLE_A),
        )
        other_items.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        other_items.center().shift(DOWN * 0.8)

        for item in other_items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.8)

        other_summary = Text(
            "Ямар ч мэдээлэл → тоо болгоно → Neural Network-д оруулна",
            font="Liberation Sans", font_size=19, color=GREY_A,
        )
        other_summary.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(other_summary), run_time=0.5)
        self.wait(2.5)
        clear_all()

        # --- 2. Ерөнхий бүтэц ---
        s = section("2. Сүлжээний бүтэц")
        ov_in = make_layer(4); ov_h1 = make_layer(5); ov_h2 = make_layer(5); ov_out = make_layer(3)
        ov_layers = VGroup(ov_in, ov_h1, ov_h2, ov_out)
        ov_layers.arrange(RIGHT, buff=1.8).center().shift(DOWN*0.2).set_height(4.5)
        ov_edges = make_edges(ov_in, ov_h1)
        ov_edges.add(*make_edges(ov_h1, ov_h2))
        ov_edges.add(*make_edges(ov_h2, ov_out))
        ov_names = ["Оролт", "Нууц 1", "Нууц 2", "Гаралт"]
        ov_lbls = VGroup()
        for i, ll in enumerate(ov_layers):
            l = Text(ov_names[i], font="Liberation Sans", font_size=14)
            l.next_to(ll, DOWN, buff=0.3)
            ov_lbls.add(l)
        for i, ll in enumerate(ov_layers):
            self.play(FadeIn(ll), FadeIn(ov_lbls[i]), run_time=0.4)
        self.play(ShowCreation(ov_edges, lag_ratio=0.003), run_time=0.8)
        self.wait(0.3)

        # Highlight each layer
        layer_info = [
            (ov_in, [0], BLUE, "Оролтын давхарга: мэдээллийг хүлээн авдаг"),
            ([*ov_h1, *ov_h2], [1,2], YELLOW, "Нууц давхарга: pattern, хэв маягийг таньдаг"),
            (ov_out, [3], GREEN, "Гаралтын давхарга: эцсийн хариулт"),
        ]
        for neurons, lbl_idxs, col, txt in layer_info:
            ns = neurons if isinstance(neurons, list) else list(neurons)
            self.play(
                *[n.animate.set_fill(col, 0.5) for n in ns],
                *[ov_lbls[i].animate.set_color(col) for i in lbl_idxs],
                run_time=0.4,
            )
            info = Text(txt, font="Liberation Sans", font_size=16, color=col)
            info.to_edge(DOWN, buff=0.4)
            self.play(FadeIn(info), run_time=0.4)
            self.wait(1.5)
            self.play(
                FadeOut(info),
                *[n.animate.set_fill(BLACK, 1) for n in ns],
                *[ov_lbls[i].animate.set_color(WHITE) for i in lbl_idxs],
                run_time=0.3,
            )

        # Forward pass arrow
        fwd = Arrow(LEFT*5, RIGHT*5, color=YELLOW, stroke_width=3)
        fwd.next_to(ov_layers, UP, buff=0.35)
        fwd_l = Text("Forward Pass: зүүнээс баруун тийш", font="Liberation Sans", font_size=15, color=YELLOW)
        fwd_l.next_to(fwd, UP, buff=0.1)
        self.play(ShowCreation(fwd), FadeIn(fwd_l), run_time=0.7)
        self.wait(1.5)
        clear_all()

        # ================================================================
        #              II. ЯАЖ АЖИЛЛАДАГ ВЭ?
        # ================================================================
        part_title("II. Яаж ажилладаг вэ?", "Нейроны дотоод ажиллагаа")

        # --- 3. Нэг нейрон ---
        s = section("3. Нэг нейрон")
        big = Circle(radius=0.6); big.set_stroke(WHITE,3); big.set_fill(BLACK,1)
        sigma = Tex(r"\Sigma", font_size=40); sigma.move_to(big)
        inputs = [
            {"lbl":"x_1=0.9","wlbl":"w_1=0.5","x":0.9,"w":0.5},
            {"lbl":"x_2=0.3","wlbl":"w_2=-0.2","x":0.3,"w":-0.2},
            {"lbl":"x_3=0.7","wlbl":"w_3=0.8","x":0.7,"w":0.8},
        ]
        in_cs = VGroup(); in_ls = VGroup(); in_as = VGroup(); w_ls = VGroup()
        for i, d in enumerate(inputs):
            ic = Circle(radius=0.25); ic.set_stroke(GREY_A,2); ic.set_fill(WHITE, d["x"])
            yp = (1-i)*1.5; ic.move_to(LEFT*4.5+UP*yp); in_cs.add(ic)
            il = Tex(d["lbl"], font_size=20); il.next_to(ic, LEFT, buff=0.2); in_ls.add(il)
            a = Arrow(ic.get_right(), big.get_left()+UP*yp*0.3, buff=0.1, stroke_width=2,
                      color=BLUE if d["w"]>0 else RED); in_as.add(a)
            wl = Tex(d["wlbl"], font_size=16, color=BLUE if d["w"]>0 else RED)
            wl.next_to(a, UP, buff=0.05); w_ls.add(wl)
        oa = Arrow(big.get_right(), RIGHT*3.5, buff=0.1, stroke_width=2, color=GREEN)
        ol = Text("гаралт", font="Liberation Sans", font_size=16, color=GREEN); ol.next_to(oa, UP, buff=0.1)

        self.play(FadeIn(big), Write(sigma), run_time=0.5)
        for ic, il, a, wl in zip(in_cs, in_ls, in_as, w_ls):
            self.play(FadeIn(ic), FadeIn(il), ShowCreation(a), FadeIn(wl), run_time=0.5)
        self.play(ShowCreation(oa), FadeIn(ol), run_time=0.4)

        exp = Text("Нейрон: оролт хүлээн авч → тооцоолол → гаралт", font="Liberation Sans", font_size=17, color=GREY_A)
        exp.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(exp), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(exp), run_time=0.3)

        # --- 4. Үндсэн томьёо ---
        self.play(FadeOut(s), run_time=0.3)
        s = section("4. Үндсэн томьёо")
        ng = VGroup(big, sigma, in_cs, in_ls, in_as, w_ls, oa, ol)
        self.play(ng.animate.scale(0.5).shift(LEFT*3.5+UP*0.3), run_time=0.6)

        ft1 = Text("Алхам 1: Жинлэсэн нийлбэр", font="Liberation Sans", font_size=16, color=YELLOW)
        f1 = Tex(r"z = \sum_{i=1}^{n} w_i \cdot x_i + b", font_size=30)
        fb1 = SurroundingRectangle(f1, color=YELLOW, buff=0.12, stroke_width=1.5)
        ft2 = Text("Алхам 2: Идэвхжүүлэх функц", font="Liberation Sans", font_size=16, color=GREEN)
        f2 = Tex(r"a = \sigma(z) = \frac{1}{1+e^{-z}}", font_size=30)
        fb2 = SurroundingRectangle(f2, color=GREEN, buff=0.12, stroke_width=1.5)
        fmls = VGroup(VGroup(ft1,VGroup(f1,fb1)), VGroup(ft2,VGroup(f2,fb2)))
        for fg in fmls: fg.arrange(DOWN, buff=0.15)
        fmls.arrange(DOWN, buff=0.5).move_to(RIGHT*2.0+DOWN*0.1)

        self.play(Write(ft1), run_time=0.4)
        self.play(Write(f1), ShowCreation(fb1), run_time=0.8)
        parts1 = VGroup(
            Text("w=жин  x=оролт  b=хазайлт", font="Liberation Sans", font_size=14, color=GREY_B),
        )
        parts1.next_to(fb1, RIGHT, buff=0.2)
        self.play(FadeIn(parts1), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(parts1), run_time=0.2)

        self.play(Write(ft2), run_time=0.4)
        self.play(Write(f2), ShowCreation(fb2), run_time=0.8)
        self.wait(1.5)

        flow_t = Text("x,w → z → σ → a (гаралт)", font="Liberation Sans", font_size=16, color=GREY_A)
        flow_t.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(flow_t), run_time=0.4)
        self.wait(2.0)
        self.play(FadeOut(fmls), FadeOut(flow_t), FadeOut(s), run_time=0.5)
        self.play(ng.animate.scale(1/0.5).shift(RIGHT*3.5+DOWN*0.3), run_time=0.5)

        # --- 5. Тооцоолол ---
        s = section("5. Тооцоолол")
        bias_n = Text("b = 0.1", font="Liberation Sans", font_size=14, color=GREY_B)
        bias_n.next_to(big, DOWN, buff=0.25)
        self.play(FadeIn(bias_n), run_time=0.3)

        l1 = Tex(r"z = (0.5)(0.9)+(-0.2)(0.3)+(0.8)(0.7)+0.1", font_size=24)
        l2 = Tex(r"z = 0.45-0.06+0.56+0.1 = 1.05", font_size=24, color=YELLOW)
        l3 = Tex(r"a = \sigma(1.05) = \frac{1}{1+e^{-1.05}} = 0.74", font_size=24, color=GREEN)
        calc = VGroup(l1,l2,l3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=0.4)

        for l in calc:
            self.play(Write(l), run_time=0.8)
            self.wait(0.4)
        self.wait(1.5)
        self.play(FadeOut(calc), FadeOut(bias_n), run_time=0.5)

        # --- 6. Sigmoid график ---
        self.play(FadeOut(s), run_time=0.3)
        s = section("6. Sigmoid функц")
        self.play(ng.animate.scale(0.5).shift(LEFT*3.5+UP*0.3), run_time=0.5)

        axes = Axes(x_range=[-6,6,2], y_range=[0,1,0.5], width=5, height=3,
                     axis_config={"stroke_width":2, "include_tip":True})
        axes.move_to(RIGHT*2+DOWN*0.3)
        xl = Tex("z", font_size=22); xl.next_to(axes.x_axis, RIGHT, buff=0.1)
        yl = Tex(r"\sigma(z)", font_size=22); yl.next_to(axes.y_axis, UP, buff=0.1)
        curve = axes.get_graph(lambda x: 1/(1+np.exp(-x)), color=YELLOW, stroke_width=3)
        self.play(ShowCreation(axes), FadeIn(xl), FadeIn(yl), run_time=0.6)
        self.play(ShowCreation(curve), run_time=1.2)

        zv=1.05; sv=1/(1+np.exp(-zv))
        dot = Dot(axes.c2p(zv,sv), color=GREEN, radius=0.07)
        hd = DashedLine(axes.c2p(zv,0), axes.c2p(zv,sv), stroke_width=2, color=GREEN)
        vd = DashedLine(axes.c2p(0,sv), axes.c2p(zv,sv), stroke_width=2, color=GREEN)
        zm = Tex("1.05", font_size=16, color=GREEN); zm.next_to(hd, DOWN, buff=0.1)
        vm = Tex("0.74", font_size=16, color=GREEN); vm.next_to(vd, LEFT, buff=0.1)
        self.play(ShowCreation(hd), ShowCreation(vd), FadeIn(dot), run_time=0.6)
        self.play(FadeIn(zm), FadeIn(vm), run_time=0.4)

        props = VGroup(
            Text("Сөрөг → 0", font="Liberation Sans", font_size=14, color=RED_B),
            Text("Эерэг → 1", font="Liberation Sans", font_size=14, color=GREEN_B),
            Text("0 → 0.5", font="Liberation Sans", font_size=14, color=GREY_A),
        )
        props.arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(axes, LEFT, buff=0.4).shift(DOWN*0.6)
        for p in props:
            self.play(FadeIn(p), run_time=0.3)
        self.wait(1.5)
        sig_all = VGroup(axes,xl,yl,curve,dot,hd,vd,zm,vm,props)
        self.play(FadeOut(sig_all), FadeOut(s), run_time=0.5)
        self.play(ng.animate.scale(1/0.5).shift(RIGHT*3.5+DOWN*0.3), run_time=0.5)

        # --- 7. Жин (Weight) гэж юу вэ? ---
        s = section("7. Жин (Weight) гэж юу вэ?")

        # Тайлбар текст
        w_def = Text(
            "Жин = оролт бүрийн чухлын зэргийг тодорхойлдог тоо",
            font_size=19, color=GREY_A,
        )
        w_def.to_edge(DOWN, buff=1.8)
        self.play(FadeIn(w_def), run_time=0.6)
        self.wait(1.5)

        # Эерэг жин - холбоосыг зузаалж харуулах
        self.play(in_as[0].animate.set_stroke(width=6), run_time=0.4)
        pe = Text("Эерэг жин (w > 0): оролтыг ДЭМЖИНЭ", font="Liberation Sans", font_size=17, color=BLUE)
        pe.to_edge(DOWN, buff=1.0)
        pe_ex = Text(
            "Жишээ: w₁=0.5 → x₁ их байх тусам гаралт ихэснэ", font="Liberation Sans",
            font_size=15, color=BLUE_B,
        )
        pe_ex.next_to(pe, DOWN, buff=0.15)
        self.play(FadeIn(pe), FadeIn(pe_ex), run_time=0.5)
        self.wait(1.5)

        # Сөрөг жин
        self.play(
            in_as[0].animate.set_stroke(width=2),
            in_as[1].animate.set_stroke(width=6),
            run_time=0.4,
        )
        ne = Text("Сөрөг жин (w < 0): оролтыг ДАРАНГУЙЛНА", font="Liberation Sans", font_size=17, color=RED)
        ne.next_to(pe_ex, DOWN, buff=0.25)
        ne_ex = Text(
            "Жишээ: w₂=-0.2 → x₂ их байх тусам гаралт БУУРНА", font="Liberation Sans",
            font_size=15, color=RED_B,
        )
        ne_ex.next_to(ne, DOWN, buff=0.15)
        self.play(FadeIn(ne), FadeIn(ne_ex), run_time=0.5)
        self.wait(1.5)
        self.play(in_as[1].animate.set_stroke(width=2), run_time=0.3)

        # Жингийн хэмжээ = нөлөөлөх хүч
        self.play(FadeOut(w_def), FadeOut(pe), FadeOut(pe_ex),
                  FadeOut(ne), FadeOut(ne_ex), run_time=0.4)

        # Жин харьцуулах визуал: нарийн vs зузаан шугам
        w_comp_title = Text("Жингийн хэмжээ = нөлөөлөх хүч", font="Liberation Sans", font_size=19, color=YELLOW)
        w_comp_title.to_edge(DOWN, buff=2.0)
        self.play(FadeIn(w_comp_title), run_time=0.4)

        # w=0.1 (бага нөлөө) vs w=0.9 (их нөлөө)
        thin_line = Line(LEFT*2+DOWN*1.2, RIGHT*0+DOWN*1.2,
                         stroke_width=1.5, stroke_color=GREY_A)
        thin_lbl = Text("w = 0.1 (бага нөлөө)", font="Liberation Sans", font_size=14, color=GREY_A)
        thin_lbl.next_to(thin_line, DOWN, buff=0.1)

        thick_line = Line(RIGHT*0.5+DOWN*1.2, RIGHT*2.5+DOWN*1.2,
                          stroke_width=6, stroke_color=YELLOW)
        thick_lbl = Text("w = 0.9 (их нөлөө)", font="Liberation Sans", font_size=14, color=YELLOW)
        thick_lbl.next_to(thick_line, DOWN, buff=0.1)

        self.play(ShowCreation(thin_line), FadeIn(thin_lbl), run_time=0.5)
        self.play(ShowCreation(thick_line), FadeIn(thick_lbl), run_time=0.5)
        self.wait(2.0)

        # Жинг хэн тохируулдаг вэ?
        w_learn = Text(
            "Жинг хүн тохируулдаггүй — сүлжээ өөрөө СУРЧ олдог!", font="Liberation Sans",
            font_size=18, color=GREEN,
        )
        w_learn.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(w_learn), run_time=0.5)
        self.wait(2.0)
        clear_all()

        # --- 8. Bias (Хазайлт) гэж юу вэ? ---
        s = section("8. Bias (Хазайлт) гэж юу вэ?")

        # Нейроныг дахин харуулах (жижиг хэлбэрээр)
        b_neuron = Circle(radius=0.5)
        b_neuron.set_stroke(WHITE, 3)
        b_neuron.set_fill(BLACK, 1)
        b_sigma = Tex(r"\Sigma", font_size=36)
        b_sigma.move_to(b_neuron)
        b_ng = VGroup(b_neuron, b_sigma).shift(LEFT * 3 + UP * 0.5)

        # Оролтууд
        b_x = Circle(radius=0.2)
        b_x.set_stroke(GREY_A, 2)
        b_x.set_fill(WHITE, 0.5)
        b_x.move_to(LEFT * 5.5 + UP * 0.5)
        b_x_lbl = Text("x", font="Liberation Sans", font_size=16)
        b_x_lbl.next_to(b_x, LEFT, buff=0.15)
        b_x_arr = Arrow(b_x.get_right(), b_neuron.get_left(), buff=0.1,
                         stroke_width=2, color=BLUE)
        b_w_lbl = Text("w", font="Liberation Sans", font_size=14, color=BLUE)
        b_w_lbl.next_to(b_x_arr, UP, buff=0.05)

        # Bias сум (доороос ирж байгаа)
        b_bias_dot = Dot(LEFT * 3 + DOWN * 1.5, color=YELLOW, radius=0.08)
        b_bias_lbl = Text("b (bias)", font="Liberation Sans", font_size=16, color=YELLOW)
        b_bias_lbl.next_to(b_bias_dot, DOWN, buff=0.15)
        b_bias_arr = Arrow(b_bias_dot.get_top(), b_neuron.get_bottom(), buff=0.1,
                            stroke_width=2, color=YELLOW)

        # Гаралт
        b_out_arr = Arrow(b_neuron.get_right(), LEFT * 1, buff=0.1,
                           stroke_width=2, color=GREEN)
        b_out_lbl = Text("гаралт", font="Liberation Sans", font_size=14, color=GREEN)
        b_out_lbl.next_to(b_out_arr, UP, buff=0.05)

        self.play(FadeIn(b_ng), run_time=0.4)
        self.play(FadeIn(b_x), FadeIn(b_x_lbl), ShowCreation(b_x_arr),
                  FadeIn(b_w_lbl), run_time=0.5)
        self.play(ShowCreation(b_out_arr), FadeIn(b_out_lbl), run_time=0.4)

        # Bias-г онцлон харуулах
        self.play(FadeIn(b_bias_dot), FadeIn(b_bias_lbl),
                  ShowCreation(b_bias_arr), run_time=0.6)

        # Тайлбар
        b_def = Text(
            "Bias = оролтоос үл хамаарах нэмэлт тоо",
            font_size=19, color=GREY_A,
        )
        b_def.move_to(RIGHT * 2.5 + UP * 2.0)
        self.play(FadeIn(b_def), run_time=0.5)
        self.wait(1.5)

        # Томьёо дахин харуулах, bias-г тод болгох
        b_formula = Tex(r"z = w \cdot x + ", font_size=28)
        b_formula_b = Tex(r"b", font_size=28, color=YELLOW)
        b_formula_grp = VGroup(b_formula, b_formula_b).arrange(RIGHT, buff=0.05)
        b_formula_grp.move_to(RIGHT * 2.5 + UP * 1.0)
        b_box = SurroundingRectangle(b_formula_b, color=YELLOW, buff=0.08, stroke_width=2)
        self.play(Write(b_formula_grp), ShowCreation(b_box), run_time=0.7)
        self.wait(1.0)

        # Зүйрлэл: bias = босго
        b_analogy = Text(
            "Зүйрлэл: bias нь нейроныг хэр амархан\n"
            "\"идэвхждэг\"-ийг тодорхойлно", font="Liberation Sans",
            font_size=17, color=YELLOW,
        )
        b_analogy.move_to(RIGHT * 2.5 + DOWN * 0.3)
        self.play(FadeIn(b_analogy), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(b_analogy), run_time=0.3)

        # Bias-тай vs bias-гүй харьцуулалт (sigmoid шилжилт)
        b_axes = Axes(
            x_range=[-6, 6, 2], y_range=[0, 1, 0.5],
            width=4.5, height=2.5,
            axis_config={"stroke_width": 2, "include_tip": True},
        )
        b_axes.move_to(RIGHT * 2.5 + DOWN * 0.8)
        b_axes_xl = Tex("z", font_size=18)
        b_axes_xl.next_to(b_axes.x_axis, RIGHT, buff=0.1)

        # b=0 (төвд)
        sig_no_b = b_axes.get_graph(lambda x: 1/(1+np.exp(-x)),
                                     color=GREY_A, stroke_width=2)
        sig_no_b_lbl = Text("b=0", font="Liberation Sans", font_size=14, color=GREY_A)
        sig_no_b_lbl.next_to(b_axes.c2p(3, 0.95), RIGHT, buff=0.1)

        # b=+2 (зүүн тийш шилжсэн → илүү амархан идэвхждэг)
        sig_pos_b = b_axes.get_graph(lambda x: 1/(1+np.exp(-(x+2))),
                                      color=GREEN, stroke_width=2.5)
        sig_pos_b_lbl = Text("b=+2", font="Liberation Sans", font_size=14, color=GREEN)
        sig_pos_b_lbl.next_to(b_axes.c2p(-1, 0.95), LEFT, buff=0.1)

        # b=-2 (баруун тийш шилжсэн → хүндрэлтэй идэвхждэг)
        sig_neg_b = b_axes.get_graph(lambda x: 1/(1+np.exp(-(x-2))),
                                      color=RED, stroke_width=2.5)
        sig_neg_b_lbl = Text("b=-2", font="Liberation Sans", font_size=14, color=RED)
        sig_neg_b_lbl.next_to(b_axes.c2p(5, 0.95), RIGHT, buff=0.1)

        self.play(FadeOut(b_def), FadeOut(b_formula_grp), FadeOut(b_box), run_time=0.3)
        self.play(ShowCreation(b_axes), FadeIn(b_axes_xl), run_time=0.5)
        self.play(ShowCreation(sig_no_b), FadeIn(sig_no_b_lbl), run_time=0.6)
        self.wait(0.5)
        self.play(ShowCreation(sig_pos_b), FadeIn(sig_pos_b_lbl), run_time=0.6)

        b_pos_exp = Text("b>0: амархан идэвхждэг (зүүн шилжилт)", font="Liberation Sans", font_size=14, color=GREEN)
        b_pos_exp.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(b_pos_exp), run_time=0.4)
        self.wait(1.2)

        self.play(ShowCreation(sig_neg_b), FadeIn(sig_neg_b_lbl), run_time=0.6)
        b_neg_exp = Text("b<0: хүндрэлтэй идэвхждэг (баруун шилжилт)", font="Liberation Sans", font_size=14, color=RED)
        b_neg_exp.next_to(b_pos_exp, DOWN, buff=0.15)
        self.play(FadeIn(b_neg_exp), run_time=0.4)
        self.wait(2.0)

        # Дүгнэлт текст
        b_summary = Text(
            "Жин = оролтын нөлөө,  Bias = нейроны босго",
            font="Liberation Sans", font_size=19, color=YELLOW,
        )
        b_summary.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(b_pos_exp), FadeOut(b_neg_exp), run_time=0.3)
        self.play(FadeIn(b_summary), run_time=0.5)
        self.wait(2.5)
        clear_all()

        # ================================================================
        #             III. БОДИТ ЖИШЭЭ
        # ================================================================
        part_title("III. Бодит жишээ", "Шалгалтанд тэнцэх үү?")

        # --- 9. Асуудал ---
        s = section("9. Бодлого")
        q = Text("Хичээл цаг + Унтсан цаг → Тэнцэх/Унах?", font="Liberation Sans", font_size=24, color=YELLOW)
        q.next_to(s, DOWN, buff=0.8)
        self.play(Write(q), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(q), FadeOut(s), run_time=0.5)

        # --- 10. Өгөгдөл ---
        s = section("10. Сургалтын өгөгдөл")
        header = VGroup(
            Text("Хичээл", font="Liberation Sans", font_size=15, color=BLUE),
            Text("Нойр", font="Liberation Sans", font_size=15, color=GREEN),
            Text("Үр дүн", font="Liberation Sans", font_size=15, color=RED_B),
        ).arrange(RIGHT, buff=1.2).shift(UP*1.5)
        hl = Line(LEFT*4, RIGHT*4, stroke_width=1, color=GREY)
        hl.next_to(header, DOWN, buff=0.12)
        data = [(8,7,"Тэнцсэн"),(6,8,"Тэнцсэн"),(2,5,"Унасан"),
                (1,3,"Унасан"),(7,6,"Тэнцсэн"),(3,4,"Унасан")]
        rows = VGroup()
        for st,sl,res in data:
            col = GREEN if res=="Тэнцсэн" else RED
            row = VGroup(Text(str(st), font="Liberation Sans", font_size=16),Text(str(sl), font="Liberation Sans", font_size=16),
                         Text(res, font="Liberation Sans", font_size=16, color=col)).arrange(RIGHT, buff=1.4)
            rows.add(row)
        rows.arrange(DOWN, buff=0.25).next_to(hl, DOWN, buff=0.2)
        tbl = VGroup(header, hl, rows).center().shift(DOWN*0.2)
        self.play(FadeIn(header), ShowCreation(hl), run_time=0.5)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT*0.2), run_time=0.25)
        self.wait(2.0)
        self.play(FadeOut(tbl), FadeOut(s), run_time=0.5)

        # --- 11. Normalize ---
        s = section("11. Өгөгдөл бэлтгэх")
        ne1 = VGroup(Text("Хичээл:", font="Liberation Sans", font_size=20, color=BLUE),
                      Tex(r"x/10 \quad 8 \to 0.8", font_size=24)).arrange(RIGHT, buff=0.3)
        ne2 = VGroup(Text("Нойр:", font="Liberation Sans", font_size=20, color=GREEN),
                      Tex(r"x/10 \quad 7 \to 0.7", font_size=24)).arrange(RIGHT, buff=0.3)
        ne3 = Text("Тэнцсэн→1, Унасан→0", font="Liberation Sans", font_size=20, color=GREY_A)
        norms = VGroup(ne1,ne2,ne3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).center()
        for n in norms:
            self.play(FadeIn(n), run_time=0.5)
            self.wait(0.3)
        self.wait(1.5)
        self.play(FadeOut(norms), FadeOut(s), run_time=0.5)

        # --- 12. Сүлжээ бүтээх + Тооцоолол ---
        s = section("12. Сүлжээгээр тооцоолох")
        def mk(r=0.35):
            c = Circle(radius=r); c.set_stroke(WHITE,2); c.set_fill(BLACK,1); return c
        i1=mk(); i2=mk()
        il = VGroup(i1,i2).arrange(DOWN, buff=1.5).shift(LEFT*4.5)
        h1=mk(); h2=mk()
        hl_nn = VGroup(h1,h2).arrange(DOWN, buff=1.5)
        o1=mk()
        ol_nn = VGroup(o1).shift(RIGHT*4.5)
        VGroup(il,hl_nn,ol_nn).center().shift(DOWN*0.5)

        i1l=Text("Хичээл", font="Liberation Sans",font_size=14,color=BLUE); i1l.next_to(i1,LEFT,buff=0.25)
        i2l=Text("Нойр", font="Liberation Sans",font_size=14,color=GREEN); i2l.next_to(i2,LEFT,buff=0.25)
        o1l=Text("Тэнцэх?", font="Liberation Sans",font_size=14,color=YELLOW); o1l.next_to(o1,RIGHT,buff=0.25)

        wih = {(0,0):0.8,(0,1):-0.5,(1,0):0.6,(1,1):0.9}
        who = {(0,0):0.7,(1,0):0.5}
        bh=[0.1,-0.2]; bo=-0.3
        ins=[i1,i2]; hs=[h1,h2]

        eih=VGroup(); wlih=VGroup()
        for (si,hi),w in wih.items():
            col=BLUE if w>0 else RED
            e=Line(ins[si].get_right(),hs[hi].get_left(),
                   stroke_width=abs(w)*3+1,stroke_color=col,stroke_opacity=0.6)
            eih.add(e)
            wl=Text(f"{w}", font="Liberation Sans",font_size=14,color=col)
            wl.move_to(e.point_from_proportion(0.45)).shift(UP*0.12)
            wlih.add(wl)
        eho=VGroup(); wlho=VGroup()
        for (hi,oi),w in who.items():
            col=BLUE if w>0 else RED
            e=Line(hs[hi].get_right(),o1.get_left(),
                   stroke_width=abs(w)*3+1,stroke_color=col,stroke_opacity=0.6)
            eho.add(e)
            wl=Text(f"{w}", font="Liberation Sans",font_size=14,color=col)
            wl.move_to(e.point_from_proportion(0.5)).shift(UP*0.12)
            wlho.add(wl)

        self.play(FadeIn(il),FadeIn(hl_nn),FadeIn(ol_nn),
                  FadeIn(i1l),FadeIn(i2l),FadeIn(o1l), run_time=0.6)
        self.play(ShowCreation(eih),FadeIn(wlih), run_time=0.7)
        self.play(ShowCreation(eho),FadeIn(wlho), run_time=0.5)
        self.wait(0.5)

        # --- Жишээ 1: 8 цаг, 7 цаг ---
        self.play(FadeOut(s), run_time=0.2)
        s = section("13. Сурагч А: 8 цаг хичээл, 7 цаг нойр")
        x1,x2 = 0.8, 0.7
        iv1=Text("0.8", font="Liberation Sans",font_size=16,color=BLUE); iv1.move_to(i1)
        iv2=Text("0.7", font="Liberation Sans",font_size=16,color=GREEN); iv2.move_to(i2)
        self.play(i1.animate.set_fill(BLUE,0.4), i2.animate.set_fill(GREEN,0.35),
                  FadeIn(iv1), FadeIn(iv2), run_time=0.6)

        zh1 = wih[(0,0)]*x1+wih[(1,0)]*x2+bh[0]; ah1=1/(1+np.exp(-zh1))
        zh2 = wih[(0,1)]*x1+wih[(1,1)]*x2+bh[1]; ah2=1/(1+np.exp(-zh2))
        zo = who[(0,0)]*ah1+who[(1,0)]*ah2+bo; ao=1/(1+np.exp(-zo))

        c1 = VGroup(
            Tex(f"h_1: \\sigma({zh1:.2f})={ah1:.2f}", font_size=18),
            Tex(f"h_2: \\sigma({zh2:.2f})={ah2:.2f}", font_size=18),
            Tex(f"out: \\sigma({zo:.2f})={ao:.2f}", font_size=18, color=GREEN),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_edge(DOWN, buff=0.7)

        hv1=Text(f"{ah1:.2f}", font="Liberation Sans",font_size=14,color=YELLOW); hv1.move_to(h1)
        self.play(Write(c1[0]), h1.animate.set_fill(YELLOW,ah1*0.7), FadeIn(hv1), run_time=0.7)
        hv2=Text(f"{ah2:.2f}", font="Liberation Sans",font_size=14,color=YELLOW); hv2.move_to(h2)
        self.play(Write(c1[1]), h2.animate.set_fill(YELLOW,ah2*0.7), FadeIn(hv2), run_time=0.7)
        ov1=Text(f"{ao:.2f}", font="Liberation Sans",font_size=16,color=GREEN); ov1.move_to(o1)
        self.play(Write(c1[2]), o1.animate.set_fill(GREEN,0.7), FadeIn(ov1), run_time=0.7)

        v1 = Text(f"Гаралт: {ao:.0%} → Тэнцэнэ!", font="Liberation Sans", font_size=22, color=GREEN)
        v1.next_to(c1, DOWN, buff=0.2)
        self.play(FadeIn(v1), run_time=0.5)
        self.wait(2.0)

        # Reset
        self.play(FadeOut(v1),FadeOut(c1),FadeOut(s),
                  FadeOut(iv1),FadeOut(iv2),FadeOut(hv1),FadeOut(hv2),FadeOut(ov1),
                  i1.animate.set_fill(BLACK,1), i2.animate.set_fill(BLACK,1),
                  h1.animate.set_fill(BLACK,1), h2.animate.set_fill(BLACK,1),
                  o1.animate.set_fill(BLACK,1), run_time=0.5)

        # --- Жишээ 2: 2 цаг, 3 цаг ---
        s = section("14. Сурагч Б: 2 цаг хичээл, 3 цаг нойр")
        x1b,x2b = 0.2, 0.3
        iv1b=Text("0.2", font="Liberation Sans",font_size=16,color=BLUE); iv1b.move_to(i1)
        iv2b=Text("0.3", font="Liberation Sans",font_size=16,color=GREEN); iv2b.move_to(i2)
        self.play(i1.animate.set_fill(BLUE,0.15), i2.animate.set_fill(GREEN,0.12),
                  FadeIn(iv1b), FadeIn(iv2b), run_time=0.6)

        zh1b=wih[(0,0)]*x1b+wih[(1,0)]*x2b+bh[0]; ah1b=1/(1+np.exp(-zh1b))
        zh2b=wih[(0,1)]*x1b+wih[(1,1)]*x2b+bh[1]; ah2b=1/(1+np.exp(-zh2b))
        zob=who[(0,0)]*ah1b+who[(1,0)]*ah2b+bo; aob=1/(1+np.exp(-zob))

        c2 = VGroup(
            Tex(f"h_1: \\sigma({zh1b:.2f})={ah1b:.2f}", font_size=18),
            Tex(f"h_2: \\sigma({zh2b:.2f})={ah2b:.2f}", font_size=18),
            Tex(f"out: \\sigma({zob:.2f})={aob:.2f}", font_size=18, color=RED),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_edge(DOWN, buff=0.7)

        hv1b=Text(f"{ah1b:.2f}", font="Liberation Sans",font_size=14,color=YELLOW); hv1b.move_to(h1)
        self.play(Write(c2[0]), h1.animate.set_fill(YELLOW,ah1b*0.7), FadeIn(hv1b), run_time=0.7)
        hv2b=Text(f"{ah2b:.2f}", font="Liberation Sans",font_size=14,color=YELLOW); hv2b.move_to(h2)
        self.play(Write(c2[1]), h2.animate.set_fill(YELLOW,ah2b*0.7), FadeIn(hv2b), run_time=0.7)
        ov1b=Text(f"{aob:.2f}", font="Liberation Sans",font_size=16,color=RED); ov1b.move_to(o1)
        self.play(Write(c2[2]), o1.animate.set_fill(RED,0.5), FadeIn(ov1b), run_time=0.7)

        v2 = Text(f"Гаралт: {aob:.0%} → Унана!", font="Liberation Sans", font_size=22, color=RED)
        v2.next_to(c2, DOWN, buff=0.2)
        self.play(FadeIn(v2), run_time=0.5)
        self.wait(2.0)
        clear_all()

        # --- Харьцуулалт ---
        s = section("15. Харьцуулалт")
        b1 = VGroup(
            Text("Сурагч А", font="Liberation Sans", font_size=20, color=GREEN),
            Text("8 цаг хичээл, 7 цаг нойр", font="Liberation Sans", font_size=16),
            Text(f"{ao:.0%} → ТЭНЦЭНЭ", font="Liberation Sans", font_size=18, color=GREEN),
        ).arrange(DOWN, buff=0.2)
        r1 = SurroundingRectangle(b1, color=GREEN, buff=0.25, stroke_width=2)

        b2 = VGroup(
            Text("Сурагч Б", font="Liberation Sans", font_size=20, color=RED),
            Text("2 цаг хичээл, 3 цаг нойр", font="Liberation Sans", font_size=16),
            Text(f"{aob:.0%} → УНАНА", font="Liberation Sans", font_size=18, color=RED),
        ).arrange(DOWN, buff=0.2)
        r2 = SurroundingRectangle(b2, color=RED, buff=0.25, stroke_width=2)

        comp = VGroup(VGroup(b1,r1), VGroup(b2,r2)).arrange(RIGHT, buff=1.5).center().shift(DOWN*0.3)
        self.play(FadeIn(b1), ShowCreation(r1), run_time=0.6)
        self.play(FadeIn(b2), ShowCreation(r2), run_time=0.6)
        self.wait(2.5)
        clear_all()

        # ================================================================
        #                     ДҮГНЭЛТ
        # ================================================================
        s = section("Дүгнэлт")
        summary = VGroup(
            Text("1. Оролт: мэдээллийг тоон хэлбэрт хөрвүүлнэ", font="Liberation Sans", font_size=17),
            Text("2. Бүтэц: оролт → нууц давхарга → гаралт", font="Liberation Sans", font_size=17),
            Text("3. Томьёо: z = Σ(w·x) + b,  a = σ(z)", font="Liberation Sans", font_size=17),
            Text("4. Sigmoid: утгыг 0-1 хооронд шахдаг", font="Liberation Sans", font_size=17),
            Text("5. Жин (Weight): оролтын нөлөөллийн хүчийг тодорхойлно", font="Liberation Sans", font_size=17),
            Text("6. Bias: нейроны идэвхжих босгыг тохируулна", font="Liberation Sans", font_size=17),
            Text("7. Forward Pass: давхаргаар дамжин хариулт гарна", font="Liberation Sans", font_size=17),
            Text("8. Гаралт: 0.5+ = тийм,  0.5- = үгүй", font="Liberation Sans", font_size=17),
        )
        summary.arrange(DOWN, buff=0.25, aligned_edge=LEFT).center().shift(DOWN*0.2)
        for item in summary:
            self.play(FadeIn(item, shift=RIGHT*0.3), run_time=0.35)
            self.wait(0.3)
        self.wait(3.0)

        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=1.5)
        self.wait(0.5)
