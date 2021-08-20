import time
from random import randint, choice
import os
from psychopy import core, visual
from task_template import TaskTemplate


class GoNoGo(TaskTemplate):
    yes_key_name = "espace"
    yes_key_code = "space"
    quit_code = "q"
    keys = ["space", yes_key_name, quit_code]
    launch_example = True
    next = f"Pour passer à l'instruction suivante, appuyez sur la touche {yes_key_name}"
    instructions = [f"Dans ce mini-jeu, appuyez sur la touche {yes_key_name} si la flèche centralee.",
                    "S'il-vous-plaît, n'appuyez que lorsqu'on vous le demande ou lors du mini-jeu",
                    f"Placez votre index sur la touche espace s'il-vous-plaît",
                    ]
    csv_headers = ['no_trial', 'id_candidate', 'condition', 'ans_candidate', 'good_ans', 'correct',
                   'practice', 'reaction_time', 'time_stamp']

    def task(self, no_trial, exp_start_timestamp, trial_start_timestamp, practice=False):
        keyboard_pressed = False
        seed = choice([0, 1, 2, 4, 6, 8])

        if seed % 2 == 0:
            condition = "Go"
            color = "green"
            good_ans = "space"
        else:
            condition = "NoGo"
            color = "red"
            good_ans = ""

        self.create_visual_text("+").draw()
        self.win.flip()
        core.wait(.5)
        self.create_visual_rect(color=color).draw()
        self.create_visual_text(condition, color="black").draw()
        self.win.flip()
        try:
            resp, rt = self.get_response_with_time(timeout=1)
        except (TypeError, AttributeError):
            if condition == "NoGo":
                resp = ""
                rt = 1
            else:
                resp = ""
                rt = 1
        print(resp)

        if resp == good_ans:
            good_answer = True
        else:
            good_answer = False

        self.update_csv(no_trial, self.participant, condition, resp, good_ans, good_answer,
                        practice, round(rt, 2), round(time.time() - exp_start_timestamp, 2))
        self.create_visual_text("", color=color).draw()
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
