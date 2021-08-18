import time
from random import randint, choice
import os
from psychopy import core
from task_template import TaskTemplate


class GoNoGo(TaskTemplate):
    yes_key_name = "a"
    no_key_name = "p"
    yes_key_code = "a"
    no_key_code = "p"
    quit_code = "q"
    keys = ["r", "v", "b", "j", yes_key_name, quit_code]
    launch_example = True
    next = f"Pour passer à l'instruction suivante, appuyez sur la touche {yes_key_name}"
    instructions = [f"Dans ce mini-jeu, appuyez sur la touche {yes_key_name} si la flèche centrale est vers la gauche,"
                    f" et sur la touche {no_key_code} si elle est vers la droite.",
                    "S'il-vous-plaît, n'appuyez que lorsqu'on vous le demande ou lors du mini-jeu",
                    f"Placez vos doigts sur les touches {yes_key_name} et {no_key_name} s'il-vous-plaît",
                    ]
    csv_headers = ['no_trial', 'id_candidate', 'word', 'color', 'condition', 'ans_candidate', 'good_ans', 'correct',
                   'practice', 'reaction_time', 'time_stamp']

    def task(self, no_trial, exp_start_timestamp, trial_start_timestamp, practice=False):
        configs = {"Rouge": "red", "Vert": "green", "Bleu": "blue", "Jaune": "yellow"}
        word = choice(list(configs.keys()))
        color = choice(list(configs.values()))
        seed = randint(0, 1)

        if seed == 0:
            condition = "Go"
            color = "green"
        else:
            condition = "NoGo"
            color = "red"
        self.create_visual_rect(color=color)
        self.create_visual_text("+").draw()
        self.win.flip()
        core.wait(0.5)
        arrows = self.create_visual_text(text=word, color=color)
        arrows.draw()
        self.win.flip()
        resp, rt = self.get_response_with_time()
        if resp == good_ans:
            good_answer = True
        else:
            good_answer = False
        self.update_csv(no_trial, self.participant, word, color, condition, resp, good_ans, good_answer,
                        practice, round(rt, 2), round(time.time() - exp_start_timestamp, 2))
        self.create_visual_text("", color).draw()
        self.win.flip()
        rnd_time = randint(8, 14)
        core.wait(rnd_time * 10 ** -3)
        if practice:
            return good_answer

    def example(self, exp_start_timestamp):
        score = 0
        example = self.create_visual_text(text='Commençons par un exemple')
        tutoriel_end = self.create_visual_text(text="Le tutoriel est désormais terminé")
        example.draw()
        self.create_visual_text(self.next, pos=(0, -0.4), font_size=0.04).draw()
        self.win.flip()
        self.wait_yes()
        for i in range(3):
            if self.task(i, exp_start_timestamp, time.time(), True):
                score += 1
                self.create_visual_text(f"Bravo ! Vous avez {score}/{i + 1}").draw()
                self.win.flip()
                core.wait(2)
            else:
                self.create_visual_text(f"Dommage... Vous avez {score}/{i + 1}").draw()
                self.win.flip(2)
        self.create_visual_text("+").draw()
        self.win.flip()
        core.wait(1)
        results = self.create_visual_text(f"Vous avez obtenu {score}/3")
        results.draw()
        self.win.flip()
        core.wait(5)
        tutoriel_end.draw()
        self.win.flip()
        core.wait(5)

    def quit_experiment(self):
        exit()


if not os.path.isdir("csv"):
    os.mkdir("csv")
exp = GoNoGo("csv")
exp.start()
