import arcade
import random

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TASKBAR_HEIGHT = 50
SNAKE_SIZE = 20
MOVE_SPEED = 20


class SnakeGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Game with Taskbar")
        arcade.set_background_color(arcade.color.BLACK)

        self.reset_game()

        # Timer for controlling snake speed
        self.move_timer = 0
        self.move_interval = 0.15  # Start speed

    def reset_game(self):
        self.snake = [(100, 100)]
        self.direction = "RIGHT"
        self.food = self.random_food()
        self.bonus_food = None
        self.score = 0
        self.game_over = False
        self.paused = False
        self.move_interval = 0.15

    def random_food(self):
        while True:
            x = random.randrange(0, SCREEN_WIDTH, SNAKE_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT - TASKBAR_HEIGHT, SNAKE_SIZE)
            if (x, y) not in self.snake:
                return (x, y)

    def on_draw(self):
        self.clear()

        # Taskbar background
        arcade.draw_lbwh_rectangle_filled(
            0, SCREEN_HEIGHT - TASKBAR_HEIGHT,
            SCREEN_WIDTH, TASKBAR_HEIGHT,
            arcade.color.DARK_SLATE_GRAY
        )

        # Taskbar info
        arcade.draw_text("Pause [SPACE]", 10, SCREEN_HEIGHT - 35, arcade.color.WHITE, 14)
        arcade.draw_text("Restart [R]", 150, SCREEN_HEIGHT - 35, arcade.color.WHITE, 14)
        arcade.draw_text(f"Score: {self.score}", 300, SCREEN_HEIGHT - 35, arcade.color.YELLOW, 14)

        # Draw snake
        for i, segment in enumerate(self.snake):
            color = arcade.color.LIME_GREEN if i > 0 else arcade.color.YELLOW_GREEN
            arcade.draw_lbwh_rectangle_filled(
                segment[0], segment[1],
                SNAKE_SIZE, SNAKE_SIZE,
                color
            )

        # Draw food
        arcade.draw_lbwh_rectangle_filled(
            self.food[0], self.food[1],
            SNAKE_SIZE, SNAKE_SIZE,
            arcade.color.RED
        )

        # Draw bonus food (if exists)
        if self.bonus_food:
            arcade.draw_lbwh_rectangle_filled(
                self.bonus_food[0], self.bonus_food[1],
                SNAKE_SIZE, SNAKE_SIZE,
                arcade.color.RED
            
            )
            self.bonus_food = None
        self.bonus_timer = 0
        self.bonus_duration = 10.0  # seconds

        # Game over screen
        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 20,
                arcade.color.WHITE,
                30,
                anchor_x="center"
            )
            arcade.draw_text(
                "Press R to Restart",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 20,
                arcade.color.GRAY,
                16,
                anchor_x="center"
            )

        # Pause screen
        elif self.paused:
            arcade.draw_text(
                "PAUSED",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.LIGHT_GRAY,
                25,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        if self.game_over or self.paused:
            return

        self.move_timer += delta_time
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0

        head_x, head_y = self.snake[0]
        if self.direction == "UP":
            head_y += MOVE_SPEED
        elif self.direction == "DOWN":
            head_y -= MOVE_SPEED
        elif self.direction == "LEFT":
            head_x -= MOVE_SPEED
        elif self.direction == "RIGHT":
            head_x += MOVE_SPEED

        new_head = (head_x, head_y)
        self.snake.insert(0, new_head)

        # Check for bonus food collision
        if self.bonus_food and new_head == self.bonus_food:
            self.score += 3
            self.bonus_food = None
            self.food = self.random_food()
            self.move_interval = max(0.05, self.move_interval - 0.005)

        # Check for normal food collision
        elif new_head == self.food:
            self.score += 1
            self.food = self.random_food()
            # Occasionally spawn bonus food
            if random.random() < 0.2:
                self.bonus_food = self.random_food()
            self.move_interval = max(0.05, self.move_interval - 0.005)
        else:
            self.snake.pop()

        # Check for collision with walls or self
        if (
            head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT - TASKBAR_HEIGHT or
            new_head in self.snake[1:]
        ):
            self.game_over = True

    def on_key_press(self, key, _):
        if key == arcade.key.UP and self.direction != "DOWN":
            self.direction = "UP"
        elif key == arcade.key.DOWN and self.direction != "UP":
            self.direction = "DOWN"
        elif key == arcade.key.LEFT and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif key == arcade.key.RIGHT and self.direction != "LEFT":
            self.direction = "RIGHT"
        elif key == arcade.key.R:
            self.reset_game()
        elif key == arcade.key.SPACE and not self.game_over:
            self.paused = not self.paused


if __name__ == "__main__":
    game = SnakeGame()
    arcade.run()
