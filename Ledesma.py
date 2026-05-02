import tkinter as tk

# Create window
root = tk.Tk()
root.title("My Canvas Drawing")
root.geometry("600x500")
root.configure(bg="white")

# Create canvas
canvas = tk.Canvas(root, width=600, height=450, bg="white")
canvas.pack()

# --- HOUSE DRAWING ---
# Rectangle (house body)
canvas.create_rectangle(150, 200, 450, 400, fill="lightblue", outline="black")

# Triangle roof
canvas.create_polygon(150, 200, 300, 100, 450, 200, fill="brown", outline="black")

# Door
canvas.create_rectangle(270, 300, 330, 400, fill="brown")

# Window
canvas.create_oval(200, 250, 250, 300, fill="yellow")

# Ground line
canvas.create_line(50, 400, 550, 400, fill="green", width=3)

# --- NAME AT THE BOTTOM ---
canvas.create_text(300, 430, text="Ledesma, Andrew Timothy B.", font=("Arial", 14))

# Run the program
root.mainloop()