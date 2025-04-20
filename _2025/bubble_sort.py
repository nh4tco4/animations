from manim import *
import random
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
header = Text("Пузырьковая сортировка", font_size = 48).set_color(whitish).to_edge(UP, buff = 1.5)

class BubbleSort(Scene):
    def create_elements(self, numbers, scale=0.1):
        rectangles = VGroup()
        labels = VGroup()
        
        for _, num in enumerate(numbers):
            dimensions = np.sqrt(num * scale)
            rect = Rectangle(width=dimensions, height=dimensions)
            rect.set_stroke(color=cyan, width=3)
            rect.set_fill(color=cyan, opacity=0.8)
            rectangles.add(rect)
            
            label = Text(str(num), font_size=20).next_to(rect, DOWN)
            labels.add(label)
        
        rectangles.arrange(RIGHT, buff=0.7)
        
        for label, rect in zip(labels, rectangles):
            label.next_to(rect, DOWN)
        
        return VGroup(*[VGroup(rect, label) for rect, label in zip(rectangles, labels)])

    def highlight_elements(self, elements, indices, color, run_time=0.3):
        animations = []
        for i in indices:
            colored_rect = elements[i][0].copy().set_fill(color, opacity=0.8).set_stroke(color)
            animations.append(Transform(elements[i][0], colored_rect))
        self.play(*animations, run_time=run_time)

    def bubble_sort(self, numbers, elements):
        n = len(numbers)
        
        for i in range(n):
            swapped = False
            for j in range(n - i - 1):
                self.highlight_elements(elements, [j, j+1], lime, run_time=0.3)
                self.highlight_elements(elements, [j, j+1], cyan, run_time=0.3)
                
                if numbers[j] > numbers[j + 1]:
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                    
                    pos_j = elements[j].get_center()
                    pos_j_plus_1 = elements[j + 1].get_center()
                    
                    self.play(
                        elements[j].animate.move_to(pos_j_plus_1),
                        elements[j + 1].animate.move_to(pos_j),
                        run_time=0.5
                    )
                    
                    elements[j], elements[j + 1] = elements[j + 1], elements[j]
                    swapped = True
                    
            if not swapped:
                for k in range(n-i):
                    self.highlight_elements(elements, [k], yellow, run_time=0.1)
                break
            else:
                self.highlight_elements(elements, [n-i-1], yellow, run_time=0.3)

    def construct(self):
        self.add(VGroup(header, ege_files))
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(numbers)

        elements = self.create_elements(numbers)
        self.add(elements)
        self.wait(0.5)

        self.bubble_sort(numbers, elements)
        
        self.play(
            *[element[0].animate.set_color(yellow) for element in elements],
            run_time=0.5
        )
        
        self.wait(1)
