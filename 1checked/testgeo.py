import tkinter as tk

def print_window_size():
    x = window.winfo_width()
    y = window.winfo_height()
    print(f"Window size: {x}x{y}")

window = tk.Tk()
window.title("Get Window Size")

# Bind the event to call print_window_size when the window resizes
window.bind("<Configure>", lambda event: print_window_size())

window.mainloop()
