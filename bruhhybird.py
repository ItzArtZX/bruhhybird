import tkinter as tk
import random

class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bruhhybird by ArtZX")
        self.canvas = tk.Canvas(self.root, width=400, height=600, bg="sky blue")
        self.canvas.pack()

        self.bird = self.canvas.create_oval(50, 250, 90, 290, fill="yellow")

        self.pipes = []
        self.create_pipe()

        self.bird_y_velocity = 0
        self.gravity = 0.4

        self.tick_counter = 0
        self.lag_trigger = 50  

        self.is_game_over = False
        self.score = 0
        self.score_text = self.canvas.create_text(200, 50, text="Score: 0", font=('Arial', 24), fill='white')

        self.root.bind("<space>", self.flap)

        self.update()

    def create_pipe(self):
        gap_size = 200
        pipe_width = 60
        pipe_x = 400
        pipe_y_top = random.randint(100, 400)
        pipe_y_bottom = pipe_y_top + gap_size

        top_pipe = self.canvas.create_rectangle(pipe_x, 0, pipe_x + pipe_width, pipe_y_top, fill="green")
        bottom_pipe = self.canvas.create_rectangle(pipe_x, pipe_y_bottom, pipe_x + pipe_width, 600, fill="green")
        self.pipes.append((top_pipe, bottom_pipe))

    def flap(self, event):
        if not self.is_game_over:
            self.bird_y_velocity = -7

    def move_pipes(self):
        for top_pipe, bottom_pipe in self.pipes:
            self.canvas.move(top_pipe, -5, 0)
            self.canvas.move(bottom_pipe, -5, 0)

        if self.canvas.coords(self.pipes[0][0])[2] < 0:
            self.canvas.delete(self.pipes[0][0])
            self.canvas.delete(self.pipes[0][1])
            self.pipes.pop(0)
            self.create_pipe()
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def update(self):
        if not self.is_game_over:

            self.bird_y_velocity += self.gravity
            self.canvas.move(self.bird, 0, self.bird_y_velocity)

            self.tick_counter += 1
            if self.tick_counter % self.lag_trigger == 0:
                self.root.after(500)  

            self.move_pipes()

            self.check_collisions()

            self.root.after(20, self.update)

    def check_collisions(self):
        bird_coords = self.canvas.coords(self.bird)

        if bird_coords[1] <= 0 or bird_coords[3] >= 600:
            self.end_game()

        for top_pipe, bottom_pipe in self.pipes:
            top_coords = self.canvas.coords(top_pipe)
            bottom_coords = self.canvas.coords(bottom_pipe)

            if (bird_coords[2] > top_coords[0] and bird_coords[0] < top_coords[2] and
                (bird_coords[1] < top_coords[3] or bird_coords[3] > bottom_coords[1])):
                self.end_game()

    def end_game(self):
        self.is_game_over = True
        self.canvas.create_text(200, 300, text="Game Over", font=('Arial', 36), fill='red')

if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBirdGame(root)
    root.mainloop()