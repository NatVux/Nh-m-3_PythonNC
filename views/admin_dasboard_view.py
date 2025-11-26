import tkinter as tk
from .base_view import BaseView
from constants import *

class AdminDashboardView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        headerFrame = tk.Frame(self, bg=COLORS['primary'], height=80)
        headerFrame.grid(row=0, column=0, sticky="we", columnspan=2)
        headerFrame.grid_propagate(False)

        self.welcomeLbl = tk.Label(headerFrame, bg=COLORS['primary'], fg='white', font=FONTS['title'])
        self.welcomeLbl.grid(row=0, column=0, sticky="w", padx=30, pady=20)

        #main content
        contentFrame = tk.Frame(self, bg=COLORS['background'], padx=50, pady=50)
        contentFrame.grid(row=1, column=0, sticky="nswe", columnspan=2)

        button_style = {
            'width': 18,
            'height': 6,
            'font': FONTS['heading'],
            'relief': 'raised',
            'bd': 2,
            'cursor': 'hand2'
        }

        # buttons
        self.studentsBtn = tk.Button(contentFrame, text="Quản lý Sinh Viên", bg='#E7CBCB', fg=COLORS['text_dark'], **button_style)
        self.studentsBtn.grid(row=0, column=0, sticky="nswe", padx=25, pady=25)


        self.resultsBtn = tk.Button(contentFrame, text="KẾT QUẢ HỌC TẬP", bg='#92DFC8', fg=COLORS['text_dark'], **button_style)
        self.resultsBtn.grid(row=0, column=1, sticky="nswe", padx=25, pady=25)

        self.logoutBtn = tk.Button(contentFrame, text="ĐĂNG XUẤT", bg=COLORS['accent'], fg='white', **button_style)
        self.logoutBtn.grid(row=1, column=1, padx=25, pady=25)

        # configure grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        contentFrame.grid_rowconfigure(0, weight=1)
        contentFrame.grid_rowconfigure(1, weight=1)
        contentFrame.grid_columnconfigure(0, weight=1)
        contentFrame.grid_columnconfigure(1, weight=1)