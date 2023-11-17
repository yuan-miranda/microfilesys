import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Move Image Example")
root.geometry()
# Create a canvas widget to display the image
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Load your image (replace '1.png' with the actual image file)
image = tk.PhotoImage(file='1.png')
image_id = canvas.create_image(50, 50, anchor=tk.NW, image=image)

# Function to move the image
def move_image(event):
    # Define the movement step (in pixels)
    step = 10

    if event.keysym == 'Up':
        canvas.move(image_id, 0, -step)  # Move up
    elif event.keysym == 'Down':
        canvas.move(image_id, 0, step)   # Move down
    elif event.keysym == 'Left':
        canvas.move(image_id, -step, 0)  # Move left
    elif event.keysym == 'Right':
        canvas.move(image_id, step, 0)   # Move right

# Bind arrow key events to move the image
root.bind("<Up>", move_image)
root.bind("<Down>", move_image)
root.bind("<Left>", move_image)
root.bind("<Right>", move_image)

# Run the main event loop
root.mainloop()
