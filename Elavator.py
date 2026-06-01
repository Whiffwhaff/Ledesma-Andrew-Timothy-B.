import tkinter as tk
import time
import threading

# ==========================================
# WINDOW
# ==========================================
root = tk.Tk()
root.title("Elevator Simulator By Ledesma,Andrew Timothy B.")

root.geometry("1280x720")
root.state("zoomed")
root.configure(bg="#d9d9d9")

# ==========================================
# VARIABLES
# ==========================================
current_floor = 1
door_open = True
moving = False
direction = "IDLE"

# Emergency state
emergency_stop = False

# Request queue
requests = []

# Floor positions
floor_positions = {
    1: 560,
    2: 420,
    3: 280,
    4: 140
}

# ==========================================
# LEFT SIDE CANVAS
# ==========================================
canvas = tk.Canvas(
    root,
    width=950,
    height=720,
    bg="#d6d6d6",
    highlightthickness=0
)

canvas.pack(side="left", fill="both", expand=True)

# ==========================================
# DRAW FLOORS
# ==========================================
for floor in range(1, 5):

    y = floor_positions[floor]

    canvas.create_rectangle(
        0,
        y - 80,
        950,
        y + 80,
        fill="#efefef",
        outline="#8c8c8c",
        width=3
    )

    canvas.create_text(
        80,
        y,
        text=f"FLOOR\n{floor}",
        font=("Arial", 24, "bold")
    )

# ==========================================
# ELEVATOR SHAFT
# ==========================================
canvas.create_rectangle(
    350,
    40,
    560,
    660,
    fill="#2b2b2b",
    outline="black",
    width=4
)

# Elevator body
elevator_body = canvas.create_rectangle(
    395,
    floor_positions[1] - 60,
    515,
    floor_positions[1] + 60,
    fill="#9e9e9e",
    outline="black",
    width=3
)

# Doors
door_left = canvas.create_rectangle(
    400,
    floor_positions[1] - 55,
    455,
    floor_positions[1] + 55,
    fill="#5f5f5f"
)

door_right = canvas.create_rectangle(
    455,
    floor_positions[1] - 55,
    510,
    floor_positions[1] + 55,
    fill="#737373"
)

# Floor display
floor_display = canvas.create_text(
    455,
    floor_positions[1] - 78,
    text="1",
    fill="#00ff00",
    font=("Arial", 18, "bold")
)

# ==========================================
# RIGHT CONTROL PANEL
# ==========================================
panel = tk.Frame(
    root,
    bg="#0b2a52",
    width=280
)

panel.pack(side="right", fill="y")

# ==========================================
# STATUS DISPLAY
# ==========================================
status_frame = tk.Frame(
    panel,
    bg="#07192f",
    bd=5,
    relief="ridge"
)

status_frame.pack(pady=15)

tk.Label(
    status_frame,
    text="ELEVATOR STATUS",
    bg="#07192f",
    fg="white",
    font=("Arial", 14, "bold")
).pack(pady=8)

floor_status = tk.Label(
    status_frame,
    text="CURRENT FLOOR\n1",
    bg="black",
    fg="#00ff00",
    width=16,
    height=2,
    font=("Courier", 18, "bold")
)

floor_status.pack(pady=5)

direction_status = tk.Label(
    status_frame,
    text="DIRECTION: IDLE",
    bg="black",
    fg="#00ff00",
    font=("Courier", 12)
)

direction_status.pack(fill="x", pady=3)

door_status = tk.Label(
    status_frame,
    text="DOOR STATUS: OPEN",
    bg="black",
    fg="#00ff00",
    font=("Courier", 12)
)

door_status.pack(fill="x", pady=3)

queue_status = tk.Label(
    status_frame,
    text="QUEUE: []",
    bg="black",
    fg="cyan",
    font=("Courier", 11)
)

queue_status.pack(fill="x", pady=3)

emergency_status = tk.Label(
    status_frame,
    text="EMERGENCY: OFF",
    bg="black",
    fg="red",
    font=("Courier", 12, "bold")
)

emergency_status.pack(fill="x", pady=3)

# ==========================================
# UPDATE STATUS
# ==========================================
def update_status():

    floor_status.config(
        text=f"CURRENT FLOOR\n{current_floor}"
    )

    direction_status.config(
        text=f"DIRECTION: {direction}"
    )

    door_status.config(
        text=f"DOOR STATUS: {'OPEN' if door_open else 'CLOSED'}"
    )

    queue_status.config(
        text=f"QUEUE: {requests}"
    )

    emergency_status.config(
        text=f"EMERGENCY: {'ON' if emergency_stop else 'OFF'}"
    )

# ==========================================
# DOOR FUNCTIONS
# ==========================================
def open_doors():

    global door_open

    if door_open:
        return

    for _ in range(25):

        canvas.move(door_left, -1, 0)
        canvas.move(door_right, 1, 0)

        canvas.update()
        time.sleep(0.01)

    door_open = True
    update_status()

def close_doors():

    global door_open

    if not door_open:
        return

    for _ in range(25):

        canvas.move(door_left, 1, 0)
        canvas.move(door_right, -1, 0)

        canvas.update()
        time.sleep(0.01)

    door_open = False
    update_status()

# ==========================================
# ADD REQUEST
# ==========================================
def add_request(floor):

    global requests

    if floor != current_floor:

        if floor not in requests:

            requests.append(floor)

            if direction == "UP":
                requests.sort()

            elif direction == "DOWN":
                requests.sort(reverse=True)

            update_status()

            if not moving:

                threading.Thread(
                    target=process_requests,
                    daemon=True
                ).start()

# ==========================================
# EMERGENCY STOP
# ==========================================
def toggle_emergency():

    global emergency_stop
    global direction

    emergency_stop = not emergency_stop

    if emergency_stop:

        direction = "STOPPED"

    else:

        direction = "IDLE"

    update_status()

# ==========================================
# PROCESS REQUESTS
# ==========================================
def process_requests():

    global moving
    global current_floor
    global direction

    if moving:
        return

    moving = True

    while requests:

        target_floor = requests[0]

        # Determine direction
        if target_floor > current_floor:
            direction = "UP"
        elif target_floor < current_floor:
            direction = "DOWN"
        else:
            direction = "IDLE"

        update_status()

        close_doors()

        while current_floor != target_floor:

            # ==================================
            # EMERGENCY PAUSE
            # ==================================
            while emergency_stop:

                direction = "STOPPED"
                update_status()

                time.sleep(0.1)

            # ==================================
            # NEXT FLOOR
            # ==================================
            next_floor = (
                current_floor + 1
                if target_floor > current_floor
                else current_floor - 1
            )

            current_y = floor_positions[current_floor]
            next_y = floor_positions[next_floor]

            step = -2 if next_y < current_y else 2

            distance = abs(next_y - current_y)

            # ==================================
            # MOVE ELEVATOR
            # ==================================
            for _ in range(distance // 2):

                # Emergency pause while moving
                while emergency_stop:

                    direction = "STOPPED"
                    update_status()

                    time.sleep(0.1)

                canvas.move(elevator_body, 0, step)
                canvas.move(door_left, 0, step)
                canvas.move(door_right, 0, step)
                canvas.move(floor_display, 0, step)

                canvas.update()

                time.sleep(0.01)

            # Arrived at next floor
            current_floor = next_floor

            canvas.itemconfig(
                floor_display,
                text=str(current_floor)
            )

            update_status()

            # ==================================
            # STOP IF FLOOR REQUESTED
            # ==================================
            if current_floor in requests:

                requests.remove(current_floor)

                update_status()

                open_doors()

                time.sleep(1.2)

                close_doors()

        # Remove completed target
        if target_floor in requests:
            requests.remove(target_floor)

        update_status()

        open_doors()

        time.sleep(1.2)

    direction = "IDLE"
    moving = False

    update_status()


# ==========================================
# FLOOR CALL BUTTONS
# ==========================================
for floor in range(1, 5):

    y = floor_positions[floor]

    # UP button
    if floor < 4:

        up_btn = tk.Button(
            root,
            text="▲",
            width=3,
            height=1,
            font=("Arial", 9, "bold"),
            command=lambda f=floor: add_request(f)
        )

        canvas.create_window(
            650,
            y - 20,
            window=up_btn
        )

    # DOWN button
    if floor > 1:

        down_btn = tk.Button(
            root,
            text="▼",
            width=3,
            height=1,
            font=("Arial", 9, "bold"),
            command=lambda f=floor: add_request(f)
        )

        canvas.create_window(
            650,
            y + 20,
            window=down_btn
        )

# ==========================================
# FLOOR BUTTONS PANEL
# ==========================================
floor_frame = tk.Frame(
    panel,
    bg="#0b2a52"
)

floor_frame.pack(pady=10)

tk.Label(
    floor_frame,
    text="FLOOR SELECTION",
    bg="#0b2a52",
    fg="white",
    font=("Arial", 13, "bold")
).grid(row=0, column=0, columnspan=2, pady=8)

button_style = {
    "width": 5,
    "height": 2,
    "font": ("Arial", 12, "bold")
}

# Row 1
tk.Button(
    floor_frame,
    text="4",
    command=lambda: add_request(4),
    **button_style
).grid(row=1, column=0, padx=4, pady=4)

tk.Button(
    floor_frame,
    text="3",
    command=lambda: add_request(3),
    **button_style
).grid(row=1, column=1, padx=4, pady=4)

# Row 2
tk.Button(
    floor_frame,
    text="2",
    command=lambda: add_request(2),
    **button_style
).grid(row=2, column=0, padx=4, pady=4)

tk.Button(
    floor_frame,
    text="1",
    command=lambda: add_request(1),
    **button_style
).grid(row=2, column=1, padx=4, pady=4)

# ==========================================
# DOOR CONTROLS
# ==========================================
door_frame = tk.Frame(
    panel,
    bg="#0b2a52"
)

door_frame.pack(pady=15)

tk.Label(
    door_frame,
    text="DOOR CONTROLS",
    bg="#0b2a52",
    fg="white",
    font=("Arial", 13, "bold")
).grid(row=0, column=0, columnspan=2, pady=8)

tk.Button(
    door_frame,
    text="OPEN",
    width=8,
    height=2,
    bg="green",
    fg="white",
    font=("Arial", 10, "bold"),
    command=lambda: threading.Thread(
        target=open_doors,
        daemon=True
    ).start()
).grid(row=1, column=0, padx=4, pady=4)

tk.Button(
    door_frame,
    text="CLOSE",
    width=8,
    height=2,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    command=lambda: threading.Thread(
        target=close_doors,
        daemon=True
    ).start()
).grid(row=1, column=1, padx=4, pady=4)

# ==========================================
# EMERGENCY BUTTON
# ==========================================
emergency_frame = tk.Frame(
    panel,
    bg="#0b2a52"
)

emergency_frame.pack(pady=20)

tk.Button(
    emergency_frame,
    text="EMERGENCY STOP",
    width=20,
    height=3,
    bg="darkred",
    fg="white",
    font=("Arial", 12, "bold"),
    command=toggle_emergency
).pack()

# ==========================================
# START
# ==========================================
update_status()

root.mainloop()