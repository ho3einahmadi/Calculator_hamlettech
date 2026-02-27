import tkinter as tk
import os
import sys

# ۱. تابع پیدا کردن مسیر (باید بیرون کلاس باشد تا راحت‌تر استفاده شود)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Calculator(tk.Tk):
    def __init__(self):  # اصلاح شد: دو تا آندرلاین قبل و بعد
        super().__init__()

        # ۲. لود کردن آیکون با آدرس هوشمند
        try:
            icon_path = resource_path("logo.png")
            self.photo = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self.photo)
        except Exception as e:
            print(f"Icon Error: {e}")

        self.title("ماشین حساب پیشرفته حسین")
        self.geometry("580x580")
        self.config(bg="#2c3e50")

        self.bind("<Key>", self.handle_keyboard)

        self.result = tk.Entry(self, font=("Arial", 40),
                               bg="#ecf0f1", borderwidth=0)
        self.result.grid(row=0, column=0, columnspan=4,
                         padx=20, pady=40, sticky="we")

        button_frame = tk.Frame(self, bg="#2c3e50")
        button_frame.grid(row=1, column=0, columnspan=4)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('C', 3, 0), ('0', 3, 1), ('=', 3, 2), ('+', 3, 3),
        ]

        for (text, r, c) in buttons:
            color = "#34495e"
            if text == "=":
                color = "#27ae60"
            if text == "C":
                color = "#e67e22"
            self.create_button(text, button_frame, r, c, color)

    def create_button(self, text, frame, row, column, bg_color):
        if text == "=":
            cmd = self.calculate
        elif text == "C":
            cmd = self.clear
        else:
            def cmd(t=text): return self.add_to_screen(t)

        btn = tk.Button(frame, text=text, command=cmd, font=("Arial", 18, "bold"),
                        width=5, height=2, bg=bg_color, fg="white",
                        relief="flat", activebackground="#95a5a6",
                        takefocus=0)
        btn.grid(row=row, column=column, padx=5, pady=5)
        btn.bind("<Enter>", lambda e: btn.config(bg="#7f8c8d"))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

    def add_to_screen(self, value):
        self.result.insert(tk.END, value)

    def calculate(self):
        try:
            expression = self.result.get()
            answer = eval(expression)
            self.result.delete(0, tk.END)
            self.result.insert(0, str(answer))
        except:
            self.result.delete(0, tk.END)
            self.result.insert(0, "Error")

    def clear(self):
        self.result.delete(0, tk.END)

    def handle_keyboard(self, event):
        # فقط وقتی کلید واقعی از کیبورد زده می‌شه عمل کن
        # چک می‌کنیم که فوکوس روی فیلد ورودی نباشه یا رویداد تکراری نباشه
        key = event.keysym
        char = event.char

        if char in "0123456789+-*/.":
            self.add_to_screen(char)
        elif key == "Return":
            self.calculate()
        elif key == "BackSpace":
            current = self.result.get()
            self.result.delete(0, tk.END)
            self.result.insert(0, current[:-1])
        elif key == "Escape":
            self.clear()

        return "break"  # <--- این خط به پایتون میگه: "همین‌جا متوقف شو و دستور رو دوبار اجرا نکن"


if __name__ == "__main__":  # اصلاح شد
    app = Calculator()
    app.mainloop()
