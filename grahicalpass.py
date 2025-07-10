import tkinter as tk
from PIL import Image, ImageDraw
import random

class GraphicalPasswordGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Graphical Password Generator")

        self.canvas_width = 400
        self.canvas_height = 400
        self.grid_size = 7
        self.square_size = self.canvas_width // self.grid_size

        self.selected_points = []

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.select_point)

        self.generate_button = tk.Button(self.master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

    def draw_grid(self):
        """Draw the grid of squares on the canvas."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = i * self.square_size
                y1 = j * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                self.canvas.create_text(x1 + self.square_size // 2, y1 + self.square_size // 2, text=f"({i},{j})")

    def select_point(self, event):
        """Record the point when clicked."""
        x, y = event.x, event.y
        row, col = x // self.square_size, y // self.square_size

        if (row, col) not in self.selected_points:
            self.selected_points.append((row, col))
            self.canvas.create_oval(
                row * self.square_size + 10,
                col * self.square_size + 10,
                row * self.square_size + self.square_size - 10,
                col * self.square_size + self.square_size - 10,
                outline="red", width=2
            )
        else:
            self.selected_points.remove((row, col))
            self.canvas.delete("all")
            self.draw_grid()

    def generate_password(self):
        """Generate the graphical password based on selected points."""
        if not self.selected_points:
            print("Please select at least one point.")
            return

        # Convert the selected points to a password (e.g., using coordinates)
        password = '-'.join([f"{x},{y}" for x, y in self.selected_points])
        print("Generated Password: ", password)

        # You can save it as an image as well
        self.save_password_image()

    def save_password_image(self):
        """Save the current grid with selected points as an image."""
        img = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        draw = ImageDraw.Draw(img)

        # Draw the grid and points
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = i * self.square_size
                y1 = j * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                draw.rectangle([x1, y1, x2, y2], outline="black")

        for point in self.selected_points:
            row, col = point
            draw.ellipse(
                (row * self.square_size + 10,
                 col * self.square_size + 10,
                 row * self.square_size + self.square_size - 10,
                 col * self.square_size + self.square_size - 10),
                outline="red", width=2
            )

        img.save("graphical_password.png")
        print("Password image saved as 'graphical_password.png'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicalPasswordGenerator(root)
    root.mainloop()
