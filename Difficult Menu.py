# Name: Sean Jiang
# File: Difficulty Menu
# Version: 4

import arcade
import os
import sys

ROW_COUNT = 16
COLUMN_COUNT = 5

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Difficulty Menu"


class TextButton:
    """ Text-based button """
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(x, y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class Difficulty_Easy(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Easy", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class Difficulty_Mediocre(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Mediocre", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class Difficulty_Hard(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Hard", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class DifficultyMenu(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.YELLOW_ORANGE)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.pause = False
        self.button_list = []

    def pause_program(self):
        self.pause = True

    def resume_program(self):
        self.pause = False

    def choose_difficulty_easy(self):
        global COLUMN_COUNT, SELECTED_DIFFICULTY
        COLUMN_COUNT = 10
        SELECTED_DIFFICULTY = 1
        os.system("python3 sean_tetrix_easy.py")

    def choose_difficulty_mediocre(self):
        global COLUMN_COUNT, SELECTED_DIFFICULTY
        COLUMN_COUNT = 10
        SELECTED_DIFFICULTY = 2
        os.system("python3 sean_tetrix_mediocre.py")

    def choose_difficulty_hard(self):
        global COLUMN_COUNT, SELECTED_DIFFICULTY
        COLUMN_COUNT = 5
        SELECTED_DIFFICULTY = 3
        os.system("python3 sean_tetrix_hard.py")


    def setup(self):
        # Create your sprites and sprite lists here

        button_difficulty_easy = Difficulty_Easy(100, 200, self.choose_difficulty_easy)
        self.button_list.append(button_difficulty_easy)

        button_difficulty_mediocre = Difficulty_Mediocre(220, 200, self.choose_difficulty_mediocre)
        self.button_list.append(button_difficulty_mediocre)

        button_difficulty_hard = Difficulty_Hard(340, 200, self.choose_difficulty_hard)
        self.button_list.append(button_difficulty_hard)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        for button in self.button_list:
            button.draw()

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        check_mouse_release_for_buttons(x, y, self.button_list)

def main():
    """ Main method """
    menu = DifficultyMenu(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu.setup()
    arcade.run()

if __name__ == "__main__":
    main()
