import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ============================================================
# 扭蛋式宣導互動系統
# VS Code + Python 3
#
# 安裝 Pillow：
#     python -m pip install pillow
#
# 將宣導圖片放入：
#     宣導用/
#
# 支援：PNG / JPG / JPEG / GIF
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTER_DIR = os.path.join(BASE_DIR, "宣導用")

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif")

BG = "#F7F1E8"
DARK = "#4B3B32"
ACCENT = "#F2A65A"
ACCENT_DARK = "#D9822B"
WHITE = "#FFFFFF"
GREEN = "#7FAF8A"


class GachaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("扭蛋式宣導互動系統")
        self.root.configure(bg=BG)

        # 可依現場螢幕調整
        self.root.geometry("1100x800")
        self.root.minsize(800, 600)

        self.last_poster = None
        self.current_poster = None
        self.poster_photo = None
        self.gacha_photo = None
        self.animating = False

        self.load_posters()
        self.build_ui()
        self.show_home()

    # -----------------------------
    # 圖片讀取
    # -----------------------------
    def load_posters(self):
        self.posters = []

        if not os.path.isdir(POSTER_DIR):
            return

        for filename in sorted(os.listdir(POSTER_DIR)):
            path = os.path.join(POSTER_DIR, filename)
            if os.path.isfile(path) and filename.lower().endswith(IMAGE_EXTENSIONS):
                self.posters.append(path)

    # -----------------------------
    # UI
    # -----------------------------
    def build_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.content = tk.Frame(self.main_frame, bg=BG)
        self.content.grid(row=0, column=0, sticky="nsew")
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            self.content,
            text="扭蛋式宣導活動",
            font=("Microsoft JhengHei", 30, "bold"),
            fg=DARK,
            bg=BG
        )
        self.title_label.grid(row=0, column=0, pady=(28, 8))

        self.canvas = tk.Canvas(
            self.content,
            bg=BG,
            highlightthickness=0
        )
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=20)

        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.hint_label = tk.Label(
            self.content,
            text="",
            font=("Microsoft JhengHei", 19, "bold"),
            fg=DARK,
            bg=BG
        )
        self.hint_label.grid(row=2, column=0, pady=(4, 8))

        self.button_frame = tk.Frame(self.content, bg=BG)
        self.button_frame.grid(row=3, column=0, pady=(0, 18))

        self.action_button = tk.Button(
            self.button_frame,
            text="開始抽扭蛋",
            command=self.start_gacha,
            font=("Microsoft JhengHei", 19, "bold"),
            bg=ACCENT,
            fg=WHITE,
            activebackground=ACCENT_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            padx=38,
            pady=14,
            cursor="hand2"
        )
        self.action_button.pack()

        self.footer = tk.Label(
            self.root,
            text="臺北市中山區公所政風室製作",
            font=("Microsoft JhengHei", 13),
            fg=DARK,
            bg=BG
        )
        self.footer.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    # -----------------------------
    # 畫面狀態
    # -----------------------------
    def clear_canvas(self):
        self.canvas.delete("all")

    def show_home(self):
        self.animating = False
        self.clear_canvas()

        self.title_label.config(text="扭蛋式宣導活動")
        self.hint_label.config(text="")

        self.action_button.config(
            text="開始抽扭蛋",
            command=self.start_gacha,
            state="normal"
        )

        self.draw_gacha_machine()

    def draw_gacha_machine(self):
        self.clear_canvas()

        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 500)

        cx = w / 2
        cy = h / 2

        # 地面陰影
        self.canvas.create_oval(
            cx - 180, cy + 185,
            cx + 180, cy + 220,
            fill="#D8C9BA",
            outline=""
        )

        # 扭蛋機底座
        # 底座
        self.canvas.create_rectangle(
            cx - 125, cy + 75,
            cx + 125, cy + 190,
            fill="#E5B77A",
            outline="#B77B43",
            width=4
        )
        self.canvas.create_rectangle(
            cx - 105, cy + 100,
            cx + 105, cy + 175,
            fill="#FFF8EF",
            outline="#C89058",
            width=3
        )

        # 機身
        self.canvas.create_rectangle(
            cx - 150, cy - 110,
            cx + 150, cy + 90,
            fill="#F5CBA7",
            outline="#B77B43",
            width=5
        )

        # 透明球體
        self.canvas.create_oval(
            cx - 145, cy - 235,
            cx + 145, cy + 35,
            fill="#FCEFE2",
            outline="#B77B43",
            width=5
        )

        # 球內扭蛋
        balls = [
            (cx - 65, cy - 130, "#F29E9E"),
            (cx + 10, cy - 165, "#8EC5A0"),
            (cx + 65, cy - 105, "#91B9E8"),
            (cx - 5, cy - 85, "#F3D36B"),
            (cx - 75, cy - 55, "#C5A7DD")
        ]
        for x, y, color in balls:
            self.canvas.create_oval(
                x - 25, y - 25, x + 25, y + 25,
                fill=color,
                outline="#8A6C5A",
                width=2
            )

        # 出球口
        self.canvas.create_rectangle(
            cx - 52, cy + 55,
            cx + 52, cy + 93,
            fill="#6B5549",
            outline="#4B3B32",
            width=3
        )

        # 旋鈕
        self.canvas.create_oval(
            cx - 28, cy + 112,
            cx + 28, cy + 168,
            fill=GREEN,
            outline="#56795E",
            width=3
        )
        self.canvas.create_line(
            cx, cy + 140,
            cx + 18, cy + 126,
            fill=WHITE,
            width=5
        )

        # 標語
        self.canvas.create_text(
            cx, cy + 10,
            text="LUCKY\nGACHA",
            font=("Arial", 18, "bold"),
            fill=DARK,
            justify="center"
        )

    # -----------------------------
    # 開始抽扭蛋
    # -----------------------------
    def start_gacha(self):
        self.load_posters()

        if not os.path.isdir(POSTER_DIR):
            messagebox.showwarning(
                "找不到資料夾",
                "找不到「宣導用」資料夾，請確認資料夾是否存在。"
            )
            return

        if not self.posters:
            messagebox.showinfo(
                "目前沒有圖片",
                "目前沒有可抽取的宣導圖片。"
            )
            return

        if self.animating:
            return

        self.animating = True
        self.action_button.config(state="disabled")
        self.hint_label.config(text="扭蛋機正在準備中……")
        self.title_label.config(text="準備抽出你的宣導扭蛋！")

        self.machine_animation(0)

    def machine_animation(self, step):
        if step >= 8:
            self.drop_ball_animation(0)
            return

        # 簡單縮放／閃動效果
        self.clear_canvas()

        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 500)
        cx = w / 2
        cy = h / 2

        offset = 8 if step % 2 == 0 else -8
        self.draw_gacha_machine_shift(offset)

        self.root.after(80, lambda: self.machine_animation(step + 1))

    def draw_gacha_machine_shift(self, offset):
        # 重新繪製時將畫布整體用局部座標模擬晃動
        self.clear_canvas()

        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 500)
        cx = w / 2 + offset
        cy = h / 2

        self.canvas.create_oval(
            cx - 180, cy + 185,
            cx + 180, cy + 220,
            fill="#D8C9BA", outline=""
        )

        self.canvas.create_rectangle(
            cx - 125, cy + 75,
            cx + 125, cy + 190,
            fill="#E5B77A", outline="#B77B43", width=4
        )
        self.canvas.create_rectangle(
            cx - 105, cy + 100,
            cx + 105, cy + 175,
            fill="#FFF8EF", outline="#C89058", width=3
        )
        self.canvas.create_rectangle(
            cx - 150, cy - 110,
            cx + 150, cy + 90,
            fill="#F5CBA7", outline="#B77B43", width=5
        )
        self.canvas.create_oval(
            cx - 145, cy - 235,
            cx + 145, cy + 35,
            fill="#FCEFE2", outline="#B77B43", width=5
        )

        balls = [
            (cx - 65, cy - 130, "#F29E9E"),
            (cx + 10, cy - 165, "#8EC5A0"),
            (cx + 65, cy - 105, "#91B9E8"),
            (cx - 5, cy - 85, "#F3D36B"),
            (cx - 75, cy - 55, "#C5A7DD")
        ]
        for x, y, color in balls:
            self.canvas.create_oval(
                x - 25, y - 25, x + 25, y + 25,
                fill=color, outline="#8A6C5A", width=2
            )

        self.canvas.create_rectangle(
            cx - 52, cy + 55, cx + 52, cy + 93,
            fill="#6B5549", outline="#4B3B32", width=3
        )

        self.canvas.create_oval(
            cx - 28, cy + 112, cx + 28, cy + 168,
            fill=GREEN, outline="#56795E", width=3
        )
        self.canvas.create_line(
            cx, cy + 140, cx + 18, cy + 126,
            fill=WHITE, width=5
        )

        self.canvas.create_text(
            cx, cy + 10,
            text="LUCKY\nGACHA",
            font=("Arial", 18, "bold"),
            fill=DARK, justify="center"
        )

    # -----------------------------
    # 扭蛋掉落
    # -----------------------------
    def drop_ball_animation(self, step):
        self.clear_canvas()

        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 500)
        cx = w / 2
        machine_y = h / 2

        # 先畫扭蛋機
        self.draw_gacha_machine()

        # 掉落路徑
        start_y = machine_y + 70
        end_y = machine_y + 180
        progress = min(step / 10, 1)
        y = start_y + (end_y - start_y) * progress

        self.draw_ball(cx, y, 48)

        if step < 10:
            self.root.after(60, lambda: self.drop_ball_animation(step + 1))
        else:
            self.ball_x = cx
            self.ball_y = end_y
            self.bounce_ball(0)

    def draw_ball(self, x, y, r):
        self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill="#F29E9E",
            outline="#8A6C5A",
            width=4,
            tags="gacha_ball"
        )
        self.canvas.create_arc(
            x - r + 3, y - r + 3,
            x + r - 3, y + r - 3,
            start=180,
            extent=180,
            outline="#FFFFFF",
            width=3,
            tags="gacha_ball"
        )
        self.canvas.create_oval(
            x - 20, y - 24,
            x - 7, y - 11,
            fill="#FFFFFF",
            outline="",
            tags="gacha_ball"
        )

    def bounce_ball(self, step):
        self.clear_canvas()
        self.draw_gacha_machine()

        bounce = [0, -10, -17, -12, -5, 0][min(step, 5)]
        self.draw_ball(self.ball_x, self.ball_y + bounce, 48)

        if step < 5:
            self.root.after(80, lambda: self.bounce_ball(step + 1))
        else:
            self.animating = False
            self.hint_label.config(text="點擊扭蛋看看有什麼！")
            self.action_button.config(state="disabled")
            self.canvas.config(cursor="hand2")

    # -----------------------------
    # 點擊扭蛋
    # -----------------------------
    def on_canvas_click(self, event):
        if self.animating:
            return

        # 只有扭蛋出現時才接受點擊
        if hasattr(self, "ball_x") and hasattr(self, "ball_y"):
            distance = ((event.x - self.ball_x) ** 2 +
                        (event.y - self.ball_y) ** 2) ** 0.5
            if distance <= 65:
                self.open_ball()

    def open_ball(self):
        self.animating = True
        self.hint_label.config(text="扭蛋開啟中……")
        self.open_animation(0)

    def open_animation(self, step):
        self.clear_canvas()

        # 背景星星
        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 500)
        cx = self.ball_x
        base_y = self.ball_y

        scale = 1 + step * 0.04
        radius = 48 * scale

        # 閃光
        if step >= 3:
            for dx, dy in [(-80, -50), (75, -55), (-85, 55), (85, 50)]:
                self.canvas.create_text(
                    cx + dx, base_y + dy,
                    text="✦",
                    font=("Arial", 26, "bold"),
                    fill="#E9B949"
                )

        # 扭蛋
        self.canvas.create_oval(
            cx - radius, base_y - radius,
            cx + radius, base_y + radius,
            fill="#F29E9E",
            outline="#8A6C5A",
            width=4
        )

        # 中間裂縫
        self.canvas.create_line(
            cx - radius * 0.9, base_y,
            cx + radius * 0.9, base_y,
            fill="#FFFFFF",
            width=max(2, int(3 + step / 2))
        )

        if step < 8:
            self.root.after(70, lambda: self.open_animation(step + 1))
        else:
            self.show_random_poster()

    # -----------------------------
    # 隨機宣導圖片
    # -----------------------------
    def choose_poster(self):
        self.load_posters()

        if len(self.posters) == 1:
            return self.posters[0]

        choices = [p for p in self.posters if p != self.last_poster]

        if not choices:
            choices = self.posters

        return random.choice(choices)

    def show_random_poster(self):
        self.current_poster = self.choose_poster()
        self.last_poster = self.current_poster

        self.title_label.config(text="今日宣導扭蛋")
        self.hint_label.config(text="看看這次抽到什麼宣導內容！")
        self.action_button.config(
            text="再抽一次",
            command=self.back_to_gacha
        )

        self.show_poster_animation(0)

    # -----------------------------
    # 海報彈出
    # -----------------------------
    def show_poster_animation(self, step):
        self.clear_canvas()

        if not self.current_poster:
            self.back_to_gacha()
            return

        try:
            image = Image.open(self.current_poster).convert("RGBA")
        except Exception:
            messagebox.showerror(
                "圖片錯誤",
                "宣導圖片無法讀取，請確認圖片檔案是否正常。"
            )
            self.back_to_gacha()
            return

        # 保持原始比例
        canvas_w = max(self.canvas.winfo_width() - 70, 500)
        canvas_h = max(self.canvas.winfo_height() - 40, 400)

        ratio = min(canvas_w / image.width, canvas_h / image.height)
        ratio = min(ratio, 1.0)

        # 動畫由小放大到完整大小
        animation_ratio = 0.45 + 0.55 * min(step / 8, 1)
        target_w = max(1, int(image.width * ratio * animation_ratio))
        target_h = max(1, int(image.height * ratio * animation_ratio))

        resized = image.resize((target_w, target_h), Image.LANCZOS)
        self.poster_photo = ImageTk.PhotoImage(resized)

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        self.canvas.create_rectangle(
            15, 15, w - 15, h - 15,
            fill=WHITE,
            outline="#E2D3C4",
            width=3
        )

        self.canvas.create_image(
            w / 2, h / 2,
            image=self.poster_photo,
            anchor="center"
        )

        if step < 8:
            self.root.after(55, lambda: self.show_poster_animation(step + 1))
        else:
            self.animating = False
            self.action_button.config(state="normal")
            self.canvas.config(cursor="")

    # -----------------------------
    # 再抽一次
    # -----------------------------
    def back_to_gacha(self):
        if self.animating:
            return

        self.current_poster = None
        self.ball_x = None
        self.ball_y = None
        self.canvas.config(cursor="")
        self.show_home()

    def on_canvas_resize(self, event):
        # 只在非動畫狀態下重新繪製首頁扭蛋機
        if not self.animating and self.current_poster is None:
            if not hasattr(self, "ball_x") or self.ball_x is None:
                self.draw_gacha_machine()


def main():
    root = tk.Tk()

    # Windows 高 DPI
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = GachaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
