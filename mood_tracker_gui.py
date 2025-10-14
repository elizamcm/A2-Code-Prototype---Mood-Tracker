import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

# ---------------------- WINDOW SETUP ----------------------
root = tk.Tk()
root.title("🌈 Mood Tracker")
root.geometry("400x350")
root.config(bg="#F0F4FF")
root.resizable(False, False)

# ---------------------- FILE SETUP ----------------------
if not os.path.exists("mood_log.txt"):
    with open("mood_log.txt", "w") as file:
        file.write("")

# ---------------------- FUNCTIONS ----------------------
def save_mood():
    mood = mood_var.get()
    if mood:
        now = datetime.now()
        with open("mood_log.txt", "a") as file:
            file.write(f"{now}: {mood}\n")
        messagebox.showinfo("Mood Saved", f"✅ Mood '{mood}' saved successfully!")
    else:
        messagebox.showwarning("Empty Field", "Please select a mood first.")

def show_last_mood():
    try:
        with open("mood_log.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip().split(": ")
                date = last_line[0]
                mood = last_line[-1]
                messagebox.showinfo("Last Mood", f"🕓 Last mood: '{mood}'\n📅 Logged on: {date}")
            else:
                messagebox.showinfo("No Data", "No moods have been logged yet.")
    except Exception:
        messagebox.showerror("Error", "Could not read the mood log.")

# ---------------------- STYLES ----------------------
title_font = ("Helvetica", 16, "bold")
button_font = ("Helvetica", 11, "bold")
button_style = {"width": 18, "height": 1, "font": button_font, "bd": 0, "relief": "solid", "highlightthickness": 0, "cursor": "hand2"}

# ---------------------- HEADER ----------------------
title_label = tk.Label(root, text="✨ How are you feeling today? ✨", 
                       bg="#F0F4FF", font=title_font, fg="#444")
title_label.pack(pady=20)

# ---------------------- DROPDOWN LIST ----------------------
mood_options = ["😊 Happy", "😢 Sad", "😡 Angry", "😴 Tired", "😌 Relaxed", "🤔 Thoughtful", "😎 Cool", "😰 Stressed"]
mood_var = tk.StringVar()
mood_var.set("Select Mood")

dropdown_frame = tk.Frame(root, bg="#F0F4FF")
dropdown_frame.pack(pady=10)

mood_menu = tk.OptionMenu(dropdown_frame, mood_var, *mood_options)
mood_menu.config(width=20, font=("Helvetica", 12))
mood_menu.pack()

# ---------------------- BUTTONS ----------------------
button_frame = tk.Frame(root, bg="#F0F4FF")
button_frame.pack(pady=20)

save_button = tk.Button(button_frame, text="💾 Save Mood", command=save_mood, bg="#A8E6CF", **button_style)
save_button.pack(pady=8)

show_button = tk.Button(button_frame, text="📖 Show Last Mood", command=show_last_mood, bg="#FFD3B6", **button_style)
show_button.pack(pady=8)

exit_button = tk.Button(button_frame, text="🚪 Exit", command=root.quit, bg="#FFAAA5", **button_style)
exit_button.pack(pady=8)

# ---------------------- FOOTER ----------------------
footer = tk.Label(root, text="Made with 💛 in Python & Tkinter", bg="#F0F4FF", font=("Helvetica", 9), fg="#666")
footer.pack(side="bottom", pady=10)

# ---------------------- RUN ----------------------
root.mainloop()



