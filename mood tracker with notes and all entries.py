import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import os

# ---------------------- WINDOW SETUP ----------------------
root = tk.Tk()
root.title("🌈 Mood Tracker + Notes + Journal View")
root.geometry("420x550")
root.config(bg="#F0F4FF")
root.resizable(False, False)

# ---------------------- FILE SETUP ----------------------
if not os.path.exists("mood_log.txt"):
    with open("mood_log.txt", "w") as file:
        file.write("")

# ---------------------- FUNCTIONS ----------------------
def save_mood():
    mood = mood_var.get()
    note = note_text.get("1.0", tk.END).strip()
    if mood and mood != "Select Mood":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("mood_log.txt", "a") as file:
            file.write(f"{now}: {mood} | Note: {note}\n")
        messagebox.showinfo("Mood Saved", f"✅ Mood '{mood}' saved successfully!")
        note_text.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Empty Field", "Please select a mood first.")

def show_last_mood():
    try:
        with open("mood_log.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                if " | Note: " in last_line:
                    mood_part, note_part = last_line.split(" | Note: ", 1)
                    date, mood = mood_part.split(": ", 1)
                    messagebox.showinfo("Last Mood", f"🕓 Last mood: '{mood}'\n📅 Logged on: {date}\n📝 Note: {note_part}")
                else:
                    messagebox.showinfo("Last Mood", f"{last_line}")
            else:
                messagebox.showinfo("No Data", "No moods have been logged yet.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not read the mood log.\n{e}")

def view_all_entries():
    # Create new window
    entries_window = tk.Toplevel(root)
    entries_window.title("📔 All Mood Entries")
    entries_window.geometry("420x500")
    entries_window.config(bg="#F0F4FF")

    # Title
    title_label = tk.Label(entries_window, text="📖 Your Mood Journal",
                           bg="#F0F4FF", font=("Helvetica", 15, "bold"), fg="#333")
    title_label.pack(pady=10)

    # Scrollable text area
    text_area = scrolledtext.ScrolledText(entries_window, width=50, height=20, font=("Helvetica", 11))
    text_area.pack(padx=10, pady=10)

    # Load all entries
    try:
        with open("mood_log.txt", "r") as file:
            content = file.read().strip()
            if content:
                text_area.insert(tk.END, content)
            else:
                text_area.insert(tk.END, "No mood entries found yet.")
    except Exception as e:
        text_area.insert(tk.END, f"Error loading entries:\n{e}")

    # Make text read-only
    text_area.config(state=tk.DISABLED)

# ---------------------- STYLES ----------------------
title_font = ("Helvetica", 16, "bold")
button_font = ("Helvetica", 11, "bold")
button_style = {
    "width": 20,
    "height": 1,
    "font": button_font,
    "bd": 0,
    "relief": "solid",
    "highlightthickness": 0,
    "cursor": "hand2"
}

# ---------------------- HEADER ----------------------
title_label = tk.Label(root, text="✨ How are you feeling today? ✨",
                       bg="#F0F4FF", font=title_font, fg="#444")
title_label.pack(pady=15)

# ---------------------- DROPDOWN LIST ----------------------
mood_options = ["😊 Happy", "😢 Sad", "😡 Angry", "😴 Tired", "😌 Relaxed", "🤔 Thoughtful", "😎 Cool", "😰 Stressed"]
mood_var = tk.StringVar(value="Select Mood")

dropdown_frame = tk.Frame(root, bg="#F0F4FF")
dropdown_frame.pack(pady=10)

mood_menu = tk.OptionMenu(dropdown_frame, mood_var, *mood_options)
mood_menu.config(width=20, font=("Helvetica", 12))
mood_menu.pack()

# ---------------------- NOTE SECTION ----------------------
note_label = tk.Label(root, text="📝 Add a short note about your day:", bg="#F0F4FF", font=("Helvetica", 12))
note_label.pack(pady=5)

note_text = tk.Text(root, width=40, height=5, font=("Helvetica", 11))
note_text.pack(pady=5)

# ---------------------- BUTTONS ----------------------
button_frame = tk.Frame(root, bg="#F0F4FF")
button_frame.pack(pady=15)

save_button = tk.Button(button_frame, text="💾 Save Mood", command=save_mood, bg="#A8E6CF", **button_style)
save_button.pack(pady=6)

show_button = tk.Button(button_frame, text="📖 Show Last Mood", command=show_last_mood, bg="#FFD3B6", **button_style)
show_button.pack(pady=6)

view_all_button = tk.Button(button_frame, text="🗂 View All Entries", command=view_all_entries, bg="#FFECB3", **button_style)
view_all_button.pack(pady=6)

exit_button = tk.Button(button_frame, text="🚪 Exit", command=root.quit, bg="#FFAAA5", **button_style)
exit_button.pack(pady=6)

# ---------------------- FOOTER ----------------------
footer = tk.Label(root, text="Made with 💛 in Python & Tkinter",
                  bg="#F0F4FF", font=("Helvetica", 9), fg="#666")
footer.pack(side="bottom", pady=10)

# ---------------------- RUN ----------------------
root.mainloop()
