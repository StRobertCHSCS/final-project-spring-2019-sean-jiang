# Name: Sean Jiang
# File: Sean's Tetris 2019
# Version: 3

import arcade
import random
import os
import PIL
import random
import time
import multiprocessing

''' Objectives in this version
Step 1: Build a window that can select difficulty.
Step 2: Insert audio file. [Done]
Step 3: Change teal colour to darker colour. [Done]
Step 4: More colour options. [Done]
Step 5: Fixing the bugs in Version 1. [Done]

'''

# Set how many rows and columns we will have
ROW_COUNT = 23
COLUMN_COUNT = 10

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# Each cell's margin size.
MARGIN = 1
SELECTED_DIFFICULTY = 0

# Determine if the game can be started after selecting game difficulty.
START_GAME = False

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Sean's Tetris 2019"

colors = [(220, 220, 220), (255, 128, 170), (0, 150, 0), (220, 20, 60), (255, 69, 0),
          (231, 144, 143), (210, 105, 30), (255, 0, 255), (0, 230, 230),
          (255, 218, 185), (75, 0, 130), (219, 112, 147), (188, 143, 143)]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1], [0, 1, 0]],
    [[0, 2, 2], [2, 2, 0]],
    [[3, 3, 0], [0, 3, 3]],
    [[4, 0, 0], [4, 4, 4]],
    [[0, 0, 5], [5, 5, 5]],
    [[6, 6, 6, 6]],
    [[7, 7], [7, 7]]
]



def create_textures():
    """ Create a list of images for sprites based on the global colors. """
    texture_list = []

    for color in colors:
        image = PIL.Image.new('RGB', (WIDTH, HEIGHT), color)
        print(image)
        texture_list.append(arcade.Texture(str(color), image=image))

    return texture_list


def rotate_clockwise(shape):
    """ Rotates a matrix clockwise """
    return [[shape[y][x] for y in range(len(shape))] for x in
            range(len(shape[0]) - 1, -1, -1)]


def check_collision(board, shape, offset):
    """
    See if the matrix stored in the shape will intersect anything
    on the board based on the offset. Offset is an (x, y) coordinate.
    """
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            if cell and board[cy + off_y][cx + off_x]:
                return True
    return False


def remove_row(board, row):
    """ Removing a row from the game board. """
    del board[row]

    new_zero_list = []

    for i in range(0, COLUMN_COUNT):
        new_zero_list.append(0)

    return [new_zero_list] + board


def join_matrixes(matrix_1, matrix_2, matrix_2_offset):
    """ Copy matrix 2 onto matrix 1 based on the passed in x, y offset
    coordinate """
    offset_x, offset_y = matrix_2_offset
    for cy, row in enumerate(matrix_2):
        for cx, val in enumerate(row):
            matrix_1[cy + offset_y - 1][cx + offset_x] += val
    return matrix_1


def new_board():
    """ Creating the board. If the cell is 0, then it is unoccupied. If it is 1,
    then it is occupied. """

    game_board = []

    for i in range(0, ROW_COUNT):
        each_row = []
        for j in range(0, COLUMN_COUNT):
            each_row.append(0)

        game_board.append(each_row)

    last_row = []
    for i in range(0, COLUMN_COUNT):
        last_row.append(1)

    game_board.append(last_row)

    return game_board


class SeanTetris(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

        self.board = None
        self.frame_count = 0
        self.game_over = False
        self.paused = False
        self.board_sprite_list = None

    def new_stone(self):
        """
        Randomly grab a new stone and set the stone location to the top.
        If we immediately collide, then game-over.
        """
        self.stone = random.choice(tetris_shapes)
        self.stone_x = int(COLUMN_COUNT / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.game_over = True

    def setup(self):
        """ Set up the game. """

        # Create a board window that displays the game.
        self.board = new_board()
        self.board_sprite_list = arcade.SpriteList()

        # Fill up the board with cells.
        for row in range(0, len(self.board)):
            for column in range(0, len(self.board[0])):
                sprite = arcade.Sprite()

                # Add the texture of cell to sprite.
                for texture in texture_list:
                    sprite.append_texture(texture)

                sprite.set_texture(0)
                sprite.center_x = (MARGIN + WIDTH) * column + MARGIN + \
                                  WIDTH // 2
                sprite.center_y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * row + \
                                  MARGIN + HEIGHT // 2

                self.board_sprite_list.append(sprite)

        self.new_stone()
        self.update_board()

    def drop(self):
        """
        Drop the stone down one place.
        Check for collision.
        If collided, then
          join matrixes
          Check for rows we can remove
          Update sprite list with stones
          Create a new stone
        """
        if not self.game_over and not self.paused:
            self.stone_y += 1
            if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(self.board, i)
                            break
                    else:
                        break
                self.update_board()
                self.new_stone()

    def rotate_stone(self):
        """ Rotate the stone, check collision. """
        if not self.game_over and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def update(self, dt):
        """ Update, drop stone if warranted """
        self.frame_count = self.frame_count + 1

        if self.frame_count % 10 == 0:
            self.drop()

    def move(self, delta_x):
        """ Move the stone back and forth based on delta x. """
        if not self.game_over and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > COLUMN_COUNT - len(self.stone[0]):
                new_x = COLUMN_COUNT - len(self.stone[0])
            if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x

    def on_key_press(self, key, modifiers):
        """
        Handle user key presses
        User goes left, move -1
        User goes right, move 1
        Rotate stone,
        or drop down
        """
        if key == arcade.key.LEFT:
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.move(1)
        elif key == arcade.key.SPACE:
            self.rotate_stone()
        elif key == arcade.key.DOWN:
            self.drop()

        def on_key_press(self, key, modifiers):
            # If the user hits  the space bar, play the sound that we loaded
            music = 'uuu.wav'
            play = arcade.load_sound(music)

            if key > 0:
                arcade.play_sound(play)

    def draw_grid(self, grid, offset_x, offset_y):
        """
        Draw the grid. Used to draw the falling stones. The board is drawn
        by the sprite list.
        """
        # Draw the grid
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                # Figure out what color to draw the box
                if grid[row][column]:
                    color = colors[grid[row][column]]
                    # Do the math to figure out where the box is
                    x = (MARGIN + WIDTH) * (column + offset_x) + MARGIN + WIDTH // 2
                    y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * (row + offset_y) + \
                        MARGIN + HEIGHT // 2

                    # Draw the box
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def update_board(self):
        """
        Update the sprite list to reflect the contents of the 2d grid
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]
                i = row * COLUMN_COUNT + column
                self.board_sprite_list[i].set_texture(v)

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()
        self.board_sprite_list.draw()
        self.draw_grid(self.stone, self.stone_x, self.stone_y)



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

        arcade.set_background_color(arcade.color.AMAZON)

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

        my_game = SeanTetris(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        my_game.setup()

    def choose_difficulty_mediocre(self):
        global COLUMN_COUNT, SELECTED_DIFFICULTY
        COLUMN_COUNT = 10
        SELECTED_DIFFICULTY = 2

        my_game = SeanTetris(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        my_game.setup()

    def choose_difficulty_hard(self):
        global COLUMN_COUNT, SELECTED_DIFFICULTY
        COLUMN_COUNT = 5
        SELECTED_DIFFICULTY = 3

        my_game = SeanTetris(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        my_game.setup()

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



texture_list = create_textures()


def main():
    #my_difficulty_menu = DifficultyMenu(500, 400, "Select Difficulty")
    #my_difficulty_menu.setup()

    my_game = SeanTetris(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    my_game.setup()

    print("Playing music.")
    music = arcade.sound.load_sound("music.wav")
    arcade.sound.play_sound(music)

    arcade.run()


if __name__ == "__main__":
    main()

