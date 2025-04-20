from manim import *
import numpy as np
import random

cyan = ManimColor("#00e3bb")
lime = ManimColor("#bfff00")
yellow = ManimColor("#ffe000")
gray = ManimColor("#211f24")
light_gray = ManimColor("#7a7a7a")
whitish = ManimColor("#e9f4f1")
config.background_color = gray
Text.set_default(font="JetBrainsMono Nerd Font Mono", font_size=24)
ege_files = Text("@ege_files", font_size=16).to_corner(DR).set_color(light_gray)

class LinearSearch(Scene):
    def shuffle_until_target_position(self, numbers, target):
       while True:
           random.shuffle(numbers)
           if target not in numbers[:5]:
               break
       return numbers

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
            label = Text(str(num)).next_to(rect, DOWN)
            labels.add(label)

        elements = VGroup(*[VGroup(rect, label) for rect, label in zip(rectangles, labels)])
        elements.center()
        return elements

    def create_target(self, target, scale=0.1, opacity=0.7):
        dimensions = np.sqrt(target * scale)
        target_rect = Rectangle(width=dimensions, height=dimensions)
        target_rect.set_stroke(yellow, width=3)
        target_rect.set_fill(yellow, opacity=opacity)
        target_label = Text(str(target)).next_to(target_rect, DOWN).set_color(yellow)
        return VGroup(target_rect, target_label)

    def linear_search_animation(self, numbers, elements, target_group, target):
        self.play(target_group.animate.next_to(elements[0], DOWN))

        for i, element in enumerate(elements):
            rect = element[0] 
            label = element[1]

            self.play(rect.animate.set_color(yellow), label.animate.set_color(yellow), run_time=0.5)
            self.wait(0.5)

            if numbers[i] == target:
                self.play(rect.animate.set_color(lime), target_group.animate.set_color(lime), label.animate.set_color(lime), run_time=0.2)
                self.wait(2)
                break
            else:
                if i < len(elements) - 1:
                    self.play(rect.animate.set_color(cyan), 
                            label.animate.set_color(whitish),
                            element.animate.set_opacity(0.3),
                            target_group.animate.next_to(elements[i + 1], DOWN),
                            run_time=0.5)
                self.wait(0.5)

    def construct(self):
        header = Text("Линейный поиск", font_size=48).set_color(whitish).to_edge(UP, buff=1.5)
        self.add(VGroup(header, ege_files))
        
        scale = 0.1
        opacity = 0.7
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(numbers)
        target = 2

        numbers = self.shuffle_until_target_position(numbers, target)

        elements = self.create_elements(numbers, scale, opacity)
        target_group = self.create_target(target, scale, opacity)
        target_group.next_to(elements, DOWN, buff=0.9)

        self.add(elements, target_group)
        self.wait(1)

        self.linear_search_animation(numbers, elements, target_group, target)
        self.wait(2)
