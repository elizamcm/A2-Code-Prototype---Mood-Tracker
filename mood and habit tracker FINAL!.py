import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkcalendar import Calendar
from datetime import datetime
import os
import matplotlib.pyplot as plt
import mplcursors

# ---------------------- WINDOW SETUP ----------------------
root = tk.Tk()
root.title("🌈 Mood & Habit Tracker")
root.geometry("450x700")
root.config(bg="#F0F4FF")
root.resizable(False, False)

# ---------------------- FILE SETUP ----------------------
if not os.path.exists("mood_log.txt"):
    with open("mood_log.txt", "w") as file:
        file.write("")

# ---------------------- HABITS ----------------------
habits = ["Exercise", "Drink Water", "Meditate", "Read"]
habit_vars = {habit: tk.IntVar() for habit in habits}  # 0 = not done, 1 = done

# ---------------------- FUNCTIONS ----------------------
def save_mood():
    mood = mood_var.get()
    note = note_text.get("1.0", tk.END).strip()
    habits_done = [habit for habit, var in habit_vars.items() if var.get() == 1]

    if mood and mood != "Select Mood":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("mood_log.txt", "a") as file:
            file.write(f"{now},{mood},{note},{';'.join(habits_done)}\n")
        messagebox.showinfo("Saved", f"✅ Mood '{mood}' saved with habits!")
        note_text.delete("1.0", tk.END)
        for var in habit_vars.values():
            var.set(0)
    else:
        messagebox.showwarning("Empty Field", "Please select a mood first.")

def show_last_mood():
    try:
        with open("mood_log.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip().split(",", 3)
                date = last_line[0]
                mood = last_line[1]
                note = last_line[2] if len(last_line) > 2 else ""
                habits_done = last_line[3].split(";") if len(last_line) > 3 else []
                messagebox.showinfo("Last Entry", f"🕓 {date}\nMood: {mood}\n📝 Note: {note}\n✅ Habits: {', '.join(habits_done)}")
            else:
                messagebox.showinfo("No Data", "No entries logged yet.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not read the log.\n{e}")

def view_all_entries():
    entries_window = tk.Toplevel(root)
    entries_window.title("📔 All Entries")
    entries_window.geometry("500x600")
    entries_window.config(bg="#F0F4FF")

    text_area = scrolledtext.ScrolledText(entries_window, width=60, height=30, font=("Helvetica", 11))
    text_area.pack(padx=10, pady=10)

    try:
        with open("mood_log.txt", "r") as file:
            content = file.read().strip()
            text_area.insert(tk.END, content if content else "No entries yet.")
    except Exception as e:
        text_area.insert(tk.END, f"Error loading entries:\n{e}")
    text_area.config(state=tk.DISABLED)

def show_mood_chart():
    try:
        dates, moods, notes = [], [], []
        with open("mood_log.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",", 3)
                if len(parts) >= 2:
                    date_str, mood = parts[0], parts[1]
                    note = parts[2] if len(parts) > 2 else ""
                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        dates.append(date)
                        moods.append(mood)
                        notes.append(note)
                    except ValueError:
                        continue

        if not dates:
            messagebox.showinfo("No Data", "No moods to plot yet.")
            return

        mood_map = {
            "😊 Happy": 8, "😢 Sad": 2, "😡 Angry": 3, "😴 Tired": 4,
            "😌 Relaxed": 7, "🤔 Thoughtful": 6, "😎 Cool": 9, "😰 Stressed": 3
        }
        color_map = {
            "😊 Happy": "green", "😢 Sad": "blue", "😡 Angry": "red", "😴 Tired": "gray",
            "😌 Relaxed": "gold", "🤔 Thoughtful": "purple", "😎 Cool": "turquoise", "😰 Stressed": "orange"
        }

        mood_values = [mood_map.get(m, 5) for m in moods]
        colors = [color_map.get(m, "black") for m in moods]

        fig, ax = plt.subplots(figsize=(9,4))
        scatter = ax.scatter(dates, mood_values, color=colors, s=100)
        ax.plot(dates, mood_values, linestyle='--', color='gray', alpha=0.5)

        ax.set_title("Mood Trends Over Time", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood Level")
        yticks = list(mood_map.values())
        ylabels = list(mood_map.keys())
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels)
        ax.grid(True, linestyle='--', alpha=0.5)
        fig.autofmt_xdate(rotation=30)
        plt.tight_layout()

        cursor = mplcursors.cursor(scatter, hover=True)
        @cursor.connect("add")
        def on_add(sel):
            index = sel.index
            sel.annotation.set_text(f"{dates[index].strftime('%Y-%m-%d %H:%M')}\n{moods[index]}\nNote: {notes[index]}")
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate chart.\n{e}")

def open_calendar():
    cal_window = tk.Toplevel(root)
    cal_window.title("📅 Mood Calendar")
    cal_window.geometry("380x400")
    cal = Calendar(cal_window, selectmode="day",
                   year=datetime.now().year,
                   month=datetime.now().month,
                   day=datetime.now().day)
    cal.pack(pady=20)

    # Mood colors
    mood_colors = {
        "😊 Happy": "lightgreen", "😢 Sad": "lightblue", "😡 Angry": "tomato",
        "😴 Tired": "lightgray", "😌 Relaxed": "gold", "🤔 Thoughtful": "plum",
        "😎 Cool": "turquoise", "😰 Stressed": "orange"
    }
    for mood, color in mood_colors.items():
        cal.tag_config(mood, background=color, foreground="black")

    # Highlight dates
    try:
        with open("mood_log.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",", 3)
                if len(parts) >= 2:
                    date_str, mood = parts[0], parts[1]
                    try:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        if mood in mood_colors:
                            cal.calevent_create(date_obj, mood, mood)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass

    def show_mood_by_date():
        selected_date = cal.get_date()  # MM/DD/YYYY
        found = False
        try:
            with open("mood_log.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",", 3)
                    date_str, mood = parts[0], parts[1]
                    note = parts[2] if len(parts) > 2 else ""
                    habits_done = parts[3].split(";") if len(parts) > 3 else []
                    if datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date().strftime("%m/%d/%y") == selected_date:
                        messagebox.showinfo(f"Mood on {selected_date}", f"Mood: {mood}\nNote: {note}\nHabits: {', '.join(habits_done)}")
                        found = True
                        break
            if not found:
                messagebox.showinfo("No Entry", f"No mood logged on {selected_date}")
        except FileNotFoundError:
            messagebox.showerror("Error", "No mood log found.")

    btn = tk.Button(cal_window, text="Show Mood", command=show_mood_by_date)
    btn.pack(pady=10)

# ---------------------- STYLES ----------------------
title_font = ("Helvetica", 16, "bold")
button_font = ("Helvetica", 11, "bold")
button_style = {"width": 25, "height": 1, "font": button_font, "bd": 0, "relief": "solid", "highlightthickness": 0, "cursor": "hand2"}

# ---------------------- HEADER ----------------------
title_label = tk.Label(root, text="✨ How are you feeling today? ✨",
                       bg="#F0F4FF", font=title_font, fg="#444")
title_label.pack(pady=15)

# ---------------------- MOOD DROPDOWN ----------------------
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
note_text = tk.Text(root, width=45, height=4, font=("Helvetica", 11))
note_text.pack(pady=5)

# ---------------------- HABIT CHECKBOXES ----------------------
habit_frame = tk.LabelFrame(root, text="✅ Habits", bg="#F0F4FF", font=("Helvetica", 12, "bold"))
habit_frame.pack(pady=10)
for habit in habits:
    cb = tk.Checkbutton(habit_frame, text=habit, variable=habit_vars[habit], bg="#F0F4FF", font=("Helvetica", 11))
    cb.pack(anchor="w", padx=10)

# ---------------------- BUTTONS ----------------------
button_frame = tk.Frame(root, bg="#F0F4FF")
button_frame.pack(pady=15)

save_button = tk.Button(button_frame, text="💾 Save Mood", command=save_mood, bg="#A8E6CF", **button_style)
save_button.pack(pady=6)
show_button = tk.Button(button_frame, text="📖 Show Last Entry", command=show_last_mood, bg="#FFD3B6", **button_style)
show_button.pack(pady=6)
view_all_button = tk.Button(button_frame, text="🗂 View All Entries", command=view_all_entries, bg="#FFECB3", **button_style)
view_all_button.pack(pady=6)
chart_button = tk.Button(button_frame, text="📊 Show Mood Chart", command=show_mood_chart, bg="#B3E5FC", **button_style)
chart_button.pack(pady=6)
calendar_button = tk.Button(button_frame, text="📅 Open Calendar", command=open_calendar, bg="#FFDDC1", **button_style)
calendar_button.pack(pady=6)
exit_button = tk.Button(button_frame, text="🚪 Exit", command=root.quit, bg="#FFAAA5", **button_style)
exit_button.pack(pady=6)

# ---------------------- FOOTER ----------------------
footer = tk.Label(root, text="Made with 💛 in Python & Tkinter", bg="#F0F4FF", font=("Helvetica", 9), fg="#666")
footer.pack(side="bottom", pady=10)

# ---------------------- RUN ----------------------
root.mainloop()
