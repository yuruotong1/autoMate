import tkinter as tk
from tkinter import Button
import sys

class ScreenSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        # 创建全屏窗口
        self.window = tk.Toplevel(self.root)
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-alpha", 0.6)
        self.window.attributes("-topmost", True)
        
        # 初始化变量
        self.start_x = self.start_y = self.current_x = self.current_y = None
        self.selection_rect = self.confirm_button = None
        self.result = None
        
        # 创建画布
        self.canvas = tk.Canvas(self.window, bg="gray20", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.window.bind("<Escape>", self.cancel)
        
    def on_press(self, event):
        # 清除已有选择
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
        if self.confirm_button:
            self.confirm_button.destroy()
            self.confirm_button = None
            
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.selection_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=5
        )
        
    def on_drag(self, event):
        self.current_x = self.canvas.canvasx(event.x)
        self.current_y = self.canvas.canvasy(event.y)
        
        # 更新选择框
        self.canvas.coords(self.selection_rect, 
                           self.start_x, self.start_y,
                           self.current_x, self.current_y)
        
        # 更新透明区域
        self.update_region()
        
    def update_region(self):
        self.canvas.delete("transparent_region")
        
        # 计算坐标
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        
        # 绘制背景和透明区域
        self.canvas.create_rectangle(
            0, 0, self.window.winfo_width(), self.window.winfo_height(),
            fill="gray20", stipple="gray50", tags="transparent_region"
        )
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill="", outline="", tags="transparent_region"
        )
        
        # 确保选择框在最上层
        self.canvas.tag_raise(self.selection_rect)
    
    def on_release(self, event):
        self.current_x = self.canvas.canvasx(event.x)
        self.current_y = self.canvas.canvasy(event.y)
        
        # 有效选择判断
        if abs(self.current_x - self.start_x) > 5 and abs(self.current_y - self.start_y) > 5:
            self.show_button()
    
    def show_button(self):
        if self.confirm_button:
            self.confirm_button.destroy()
            
        # 计算坐标
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        
        # 计算距离四个角的距离
        distances = [
            ((self.current_x - x1)**2 + (self.current_y - y1)**2, (x1 - 90, y1 - 40)),  # 左上
            ((self.current_x - x2)**2 + (self.current_y - y1)**2, (x2 + 10, y1 - 40)),  # 右上
            ((self.current_x - x1)**2 + (self.current_y - y2)**2, (x1 - 90, y2 + 10)),  # 左下
            ((self.current_x - x2)**2 + (self.current_y - y2)**2, (x2 + 10, y2 + 10))   # 右下
        ]
        
        # 选择最近的角
        btn_x, btn_y = min(distances, key=lambda d: d[0])[1]
        
        # 边界检查
        width, height = self.window.winfo_width(), self.window.winfo_height()
        if btn_x + 80 > width: btn_x = x1 - 90
        if btn_x < 0: btn_x = x2 + 10
        if btn_y < 0: btn_y = y2 + 10
        if btn_y + 30 > height: btn_y = y1 - 40
        
        # 创建按钮
        self.confirm_button = Button(
            self.window, text="Confirm", command=self.confirm,
            bg="white", fg="black", font=("Arial", 12, "bold"),
            padx=10, pady=5
        )
        self.confirm_button.place(x=btn_x, y=btn_y)
    
    def confirm(self):
        # 获取选择区域坐标
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        
        self.result = (int(x1), int(y1), int(x2), int(y2))
        self.root.quit()
        self.window.destroy()
    
    def cancel(self, event=None):
        self.result = None
        self.root.quit()
        self.window.destroy()
        
    def get_selection(self):
        self.root.mainloop()
        if hasattr(self, 'root') and self.root:
            self.root.destroy()
        return self.result


if __name__ == "__main__":
    region = ScreenSelector().get_selection()
    print(f"Selected region: {region}")
    sys.exit(0)
