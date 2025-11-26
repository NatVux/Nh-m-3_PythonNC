import tkinter as tk

from PIL.ImageOps import expand

from .base_view import BaseView
from constants import COLORS, FONTS


class LoginView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.setup_bindings()

    def create_widgets(self):
        # Main container
        container = tk.Frame(self, bg=COLORS['background'])
        container.grid(row=0, column=0, sticky='ns', pady=(220, 10))

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        titleFrame = tk.Frame(container, bg=COLORS['background'])
        titleFrame.grid(pady=(0, 30))

        titleLabel = tk.Label(
            titleFrame,
            text="ĐĂNG NHẬP HỆ THỐNG",
            font=FONTS['large'],
            fg=COLORS['primary'],
            bg=COLORS['background'],
            pady=10
        )
        titleLabel.pack()

        formFrame = tk.Frame(
            container,
            bg=COLORS['card_bg'],
            padx=30,
            pady=30,
            relief='raised',
            bd=1
        )
        formFrame.grid(row=1, column=0, sticky='nsew', padx=80)

        for i in range(4):
            formFrame.grid_rowconfigure(i, weight=1)
        formFrame.grid_columnconfigure(0, weight=1)
        formFrame.grid_columnconfigure(1, weight=2)

        # Username
        self.usernameLbl = tk.Label(
            formFrame,
            text="Tên tài khoản:",
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            font=FONTS['normal'],
            anchor='w'
        )
        self.usernameLbl.grid(row=0, column=0, padx=(0, 10), pady=15, sticky='ew')

        self.usernameEntry = tk.Entry(
            formFrame,
            font=FONTS['normal'],
            width=30,
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=COLORS['primary']
        )
        self.usernameEntry.grid(row=0, column=1, pady=15, sticky='ew')
        self.usernameEntry.focus_set()

        # Password
        self.passwordLbl = tk.Label(
            formFrame,
            text="Mật khẩu:",
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            font=FONTS['normal'],
            anchor='w'
        )
        self.passwordLbl.grid(row=1, column=0, padx=(0, 10), pady=15, sticky='ew')

        self.passwordEntry = tk.Entry(
            formFrame,
            font=FONTS['normal'],
            width=30,
            relief='solid',
            bd=1,
            show='*',
            highlightthickness=1,
            highlightcolor=COLORS['primary']
        )
        self.passwordEntry.grid(row=1, column=1, pady=15, sticky='ew')

        # Check show password
        self.showPassword = tk.IntVar(value=0)
        self.showPwBtn = tk.Checkbutton(
            formFrame,
            text="Hiển thị mật khẩu",
            variable=self.showPassword,
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            font=FONTS['small'],
            command=self.toggle_password_visibility
        )
        self.showPwBtn.grid(row=2, column=1, pady=10, sticky='w')

        # Button Login - cải thiện style
        self.loginBtn = tk.Button(
            formFrame,
            text="ĐĂNG NHẬP",
            width=20,
            height=2,
            bg=COLORS['primary'],
            fg="white",
            font=FONTS['heading'],
            relief='raised',
            bd=0,
            cursor="hand2",
            activebackground=COLORS['secondary']
        )
        self.loginBtn.grid(row=3, column=0, columnspan=2, pady=20)

    def setup_bindings(self):
        # Enter để đăng nhập
        self.usernameEntry.bind('<Return>', lambda e: self.passwordEntry.focus_set())
        self.passwordEntry.bind('<Return>', lambda e: self.loginBtn.invoke())

    def toggle_password_visibility(self):
        if self.showPassword.get():
            self.passwordEntry.config(show='')
        else:
            self.passwordEntry.config(show='*')

    def clear_form(self):
        self.usernameEntry.delete(0, tk.END)
        self.passwordEntry.delete(0, tk.END)
        self.showPassword.set(0)
        self.passwordEntry.config(show='*')
        self.usernameEntry.focus_set()

    def set_loading_state(self, loading=True):
        if loading:
            self.loginBtn.config(
                text="ĐANG XỬ LÝ...",
                state='disabled',
                bg=COLORS['text_light']
            )
        else:
            self.loginBtn.config(
                text="ĐĂNG NHẬP",
                state='normal',
                bg=COLORS['primary']
            )