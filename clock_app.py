import tkinter as tk
import time
import math

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reloj de Escritorio")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")  # Dark elegant background

        # State to track current view: "analog" or "digital"
        self.view_mode = "analog"
        
        # State to track analog clock model
        self.analog_models = ["Rolex", "Minimalista", "Deportivo"]
        self.current_model_idx = 0

        # UI Setup
        self.setup_ui()

        # Start the update loop
        self.update_clock()

    def setup_ui(self):
        """Creates the visual components of the app."""
        
        # Title Label
        self.title_label = tk.Label(
            self.root, text="Taller de Python: Reloj", 
            fg="white", bg="#2c3e50", font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(pady=20)

        # Container for the clocks
        self.clock_frame = tk.Frame(self.root, bg="#2c3e50")
        self.clock_frame.pack(expand=True, fill="both")

        # --- Analog Clock Area ---
        self.analog_frame = tk.Frame(self.clock_frame, bg="#2c3e50")
        self.analog_frame.pack(pady=10)

        # Left Arrow
        self.left_btn = tk.Button(
            self.analog_frame, text="<", command=self.prev_model,
            bg="#34495e", fg="white", font=("Arial", 18, "bold"), borderwidth=0
        )
        self.left_btn.grid(row=0, column=0, padx=10)

        # Canvas
        self.canvas = tk.Canvas(
            self.analog_frame, width=300, height=300, 
            bg="#2c3e50", highlightthickness=0
        )
        self.canvas.grid(row=0, column=1)

        # Right Arrow
        self.right_btn = tk.Button(
            self.analog_frame, text=">", command=self.next_model,
            bg="#34495e", fg="white", font=("Arial", 18, "bold"), borderwidth=0
        )
        self.right_btn.grid(row=0, column=2, padx=10)

        # --- Digital Clock Container ---
        # We use a Canvas to simulate the "screen" of the clock in the image
        self.digital_canvas = tk.Canvas(
            self.clock_frame, width=350, height=150,
            bg="#2c3e50", highlightthickness=0
        )
        
        # Draw the "Screen" (rounded-like rectangle)
        self.digital_canvas.create_rectangle(
            10, 10, 340, 140, 
            fill="black", outline="#1abc9c", width=2
        )
        
        # Digital Time Text
        self.digital_text = self.digital_canvas.create_text(
            175, 75, text="00:00:00", 
            fill="#00e5ff", font=("Courier New", 45, "bold")
        )
        # We don't pack it yet, it starts hidden

        # Switch Button
        self.switch_button = tk.Button(
            self.root, text="Cambiar a Vista Digital", 
            command=self.toggle_view,
            bg="#34495e", fg="white", font=("Helvetica", 12),
            padx=10, pady=5, borderwidth=0
        )
        self.switch_button.pack(pady=30)

    def toggle_view(self):
        """Switches between analog and digital view."""
        if self.view_mode == "analog":
            self.view_mode = "digital"
            self.analog_frame.pack_forget()  # Hide analog area
            self.digital_canvas.pack(expand=True, pady=40)  # Show digital screen
            self.switch_button.config(text="Cambiar a Vista Analógica")
        else:
            self.view_mode = "analog"
            self.digital_canvas.pack_forget()  # Hide digital
            self.analog_frame.pack(pady=10)  # Show analog area
            self.switch_button.config(text="Cambiar a Vista Digital")

    def next_model(self):
        self.current_model_idx = (self.current_model_idx + 1) % len(self.analog_models)

    def prev_model(self):
        self.current_model_idx = (self.current_model_idx - 1) % len(self.analog_models)

    def draw_analog_clock(self, hours, minutes, seconds):
        """Draws the hands and face of the analog clock."""
        self.canvas.delete("all")  # Clear previous frame

        # Center and Radius
        cx, cy = 150, 150
        radius = 120

        # Draw Clock Face (Circle)
        self.canvas.create_oval(
            cx - radius, cy - radius, cx + radius, cy + radius, 
            outline="white", width=4
        )

        # Draw Hour Marks and Numbers
        for i in range(1, 13):
            angle = math.radians(i * 30)
            
            # Draw marks based on model
            mark_len = 10 if self.current_model_idx != 1 else 15
            x1 = cx + (radius - mark_len) * math.sin(angle)
            y1 = cy - (radius - mark_len) * math.cos(angle)
            x2 = cx + radius * math.sin(angle)
            y2 = cy - radius * math.cos(angle)
            
            mark_color = "white" if self.current_model_idx != 2 else "#e67e22"
            self.canvas.create_line(x1, y1, x2, y2, fill=mark_color, width=2)

            # Draw numbers (only for Rolex and Sport models)
            if self.current_model_idx != 1:
                num_x = cx + (radius - 30) * math.sin(angle)
                num_y = cy - (radius - 30) * math.cos(angle)
                font_size = 12 if self.current_model_idx == 0 else 16
                self.canvas.create_text(
                    num_x, num_y, text=str(i), 
                    fill="white", font=("Helvetica", font_size, "bold")
                )
            else:
                # Cartier Style: Roman Numerals
                roman_nums = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
                num_x = cx + (radius - 35) * math.sin(angle)
                num_y = cy - (radius - 35) * math.cos(angle)
                self.canvas.create_text(
                    num_x, num_y, text=roman_nums[i-1], 
                    fill="black", font=("Times New Roman", 14)
                )

        # Model-specific Branding
        if self.current_model_idx == 0:
            self.canvas.create_text(
                cx, cy - 60, text="ROLEX", 
                fill="gold", font=("Times New Roman", 14, "bold")
            )
        elif self.current_model_idx == 1:
            self.canvas.create_text(
                cx, cy - 60, text="CARTIER", 
                fill="black", font=("Palatino Linotype", 14, "italic")
            )
        else:
            self.canvas.create_text(
                cx, cy - 60, text="SPORT+", 
                fill="#e74c3c", font=("Impact", 18)
            )

        # Calculate hand angles
        sec_angle = math.radians(seconds * 6)
        min_angle = math.radians(minutes * 6 + seconds * 0.1)
        hour_angle = math.radians((hours % 12) * 30 + minutes * 0.5)

        # Draw Hands based on model
        if self.current_model_idx == 0: # Rolex
            self.draw_hand(cx, cy, sec_angle, radius * 0.85, "red", 2)
            self.draw_hand(cx, cy, min_angle, radius * 0.7, "white", 4)
            self.draw_hand(cx, cy, hour_angle, radius * 0.5, "white", 6)
        elif self.current_model_idx == 1: # Cartier
            self.draw_hand(cx, cy, sec_angle, radius * 0.9, "blue", 1)
            self.draw_hand(cx, cy, min_angle, radius * 0.8, "black", 2)
            self.draw_hand(cx, cy, hour_angle, radius * 0.6, "black", 3)
        else: # Sport
            self.draw_hand(cx, cy, sec_angle, radius * 0.85, "#f1c40f", 3)
            self.draw_hand(cx, cy, min_angle, radius * 0.75, "white", 5)
            self.draw_hand(cx, cy, hour_angle, radius * 0.55, "white", 8)

        # Center Dot
        dot_color = "white" if self.current_model_idx != 2 else "#f1c40f"
        self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill=dot_color)

    def draw_hand(self, cx, cy, angle, length, color, width):
        """Helper to draw a single clock hand."""
        x = cx + length * math.sin(angle)
        y = cy - length * math.cos(angle)
        self.canvas.create_line(cx, cy, x, y, fill=color, width=width, capstyle="round")

    def update_clock(self):
        """Gets current time and updates the UI."""
        # Get current time
        current_time = time.localtime()
        h, m, s = current_time.tm_hour, current_time.tm_min, current_time.tm_sec

        if self.view_mode == "analog":
            self.draw_analog_clock(h, m, s)
        else:
            # Formato: HH:MM:SS
            time_string = time.strftime("%H:%M:%S")
            self.digital_canvas.itemconfig(self.digital_text, text=time_string)

        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()
