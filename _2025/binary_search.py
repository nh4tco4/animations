from manim import *
import numpy as np

cyan = ManimColor("#00e3bb")
lime = ManimColor("#bfff00")
yellow = ManimColor("#ffe000")
gray = ManimColor("#211f24")
light_gray = ManimColor("#7a7a7a")
whitish = ManimColor("#e9f4f1")
config.background_color = gray
Text.set_default(font="JetBrainsMono Nerd Font Mono", font_size=24)
ege_files = Text("@ege_files", font_size=16).to_corner(DR).set_color(light_gray)

class BinarySearch(Scene):
    def create_elements(self, numbers, scale=0.1, opacity=0.7):
        rectangles = VGroup()
        for num in numbers:
            dimensions = np.sqrt(num * scale)
            rect = Rectangle(width=dimensions, height=dimensions)
            rect.set_stroke(cyan, width=3)
            rect.set_fill(cyan, opacity=opacity)
            rectangles.add(rect)
        rectangles.arrange(RIGHT, buff=0.7)

        labels = VGroup()
        for num, rect in zip(numbers, rectangles):
            label = Text(str(num)).next_to(rect, DOWN).set_color(whitish)
            labels.add(label)

        elements = VGroup(*[VGroup(rect, label) for rect, label in zip(rectangles, labels)])
        elements.center()
        return elements

    def create_target(self, target, scale=0.1, opacity=0.7):
        target_rect = Rectangle(width=target * scale, height=target * scale)
        target_rect.set_stroke(yellow, width=3)
        target_rect.set_fill(yellow, opacity=opacity)
        target_label = Text(str(target)).next_to(target_rect, DOWN).set_color(yellow)
        return VGroup(target_rect, target_label)

    def binary_search_animation(self, numbers, elements, target_group, target):
        low = 0
        high = len(numbers) - 1

        while low <= high:
            mid = (low + high) // 2

            self.play(target_group.animate.next_to(elements[mid], DOWN))
            self.wait(0.5)

            self.play(elements[mid].animate.set_color(yellow))
            self.wait(0.5)

            if numbers[mid] == target:
                self.play(elements[mid].animate.set_color(lime), target_group.animate.set_color(lime))
                self.wait(1)
                break
            elif numbers[mid] < target:
                low = mid + 1
                excluded = VGroup(*elements.submobjects[:mid + 1])
                if numbers[mid] != target:
                    self.play(elements[mid].animate.set_color(cyan),
                    excluded.animate.set_opacity(0.3))
                else:
                    self.play(excluded.animate.set_opacity(0.3))
            else:
                high = mid - 1
                excluded = VGroup(*elements.submobjects[mid:])
                self.play(excluded.animate.set_opacity(0.3))

            self.wait(0.5)

        if low > high:
            not_found = Text("Element not found").move_to(DOWN * 2).set_color(lime)
            self.play(Write(not_found))
            self.wait(1)

    def construct(self):
        header = Text("Бинарный поиск", font_size=48).set_color(whitish).to_edge(UP, buff=1.5)
        self.add(VGroup(header, ege_files))
        
        scale = 0.1
        opacity = 0.7
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        target = 4

        elements = self.create_elements(numbers, scale, opacity)
        target_group = self.create_target(target, scale, opacity)
        target_group.next_to(elements, DOWN, buff=0.9)

        self.add(elements, target_group)
        self.wait(1)

        self.binary_search_animation(numbers, elements, target_group, target)
