import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from .base_view import BaseView
from constants import *

class StudentView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.leftFrame = tk.Frame(self, bg=COLORS['light'], width=400)
        self.leftFrame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        self.leftFrame.grid_propagate(False)

        self.rightFrame = tk.Frame(self, bg=COLORS['card_bg'])
        self.rightFrame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=40)
        self.grid_columnconfigure(1, weight=60)

        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        personalFrame = tk.LabelFrame(self.leftFrame, text='Thông tin cá nhân', bg=COLORS['light'], fg=COLORS['primary'],
                                     font=FONTS['heading'], padx=10, pady=10)
        personalFrame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        imgFrame = tk.Frame(personalFrame, bg=COLORS['light'])
        imgFrame.grid(row=0, column=0, columnspan=2, pady=10)

        self.canvas = tk.Canvas(imgFrame, width=120, height=160, bg=COLORS['light'], highlightthickness=1, highlightbackground=COLORS['text_light'])
        self.canvas.grid(row=0, column=0, padx=5)

        self.selectImgBtn = tk.Button(imgFrame, text='Chọn ảnh', width=12, bg=COLORS['info'], fg='white', font=FONTS['small'])
        self.selectImgBtn.grid(row=1, column=0, pady=5)

        # Form fields
        fields = [
            ('Mã sinh viên', 'ent_id'), ('Họ và tên', 'ent_name'),
            ('Ngày sinh', 'date_birth'), ('Địa chỉ', 'ent_address'),
            ('CCCD', 'ent_cccd'), ('Số điện thoại', 'ent_phone'),
            ('Email', 'ent_email'), ('Giới tính', 'combo_gender')
        ]

        for i, (label, attr) in enumerate(fields):
            lbl = tk.Label(personalFrame, text=label, bg=COLORS['light'], fg=COLORS['text_dark'], font=FONTS['small'],)
            lbl.grid(row=i+1, column=0, padx=5, pady=5)

            if 'combo' in attr:
                var = tk.StringVar()
                combo = ttk.Combobox(personalFrame, textvariable=var, state='readonly', width=20, font=FONTS['small'])
                combo['values'] = GENDER_OPTIONS
                combo.current(0)
                setattr(self, attr, combo)
                setattr(self, 'gender', var)

            elif 'date' in attr:
                dateEntry = DateEntry(personalFrame, width=20, font=FONTS['small'], date_pattern="dd/mm/yyyy", background=COLORS['primary'])
                setattr(self, attr, dateEntry)
            else:
                entry = tk.Entry(personalFrame, width=23, font=FONTS['small'], relief='solid', bd=1)
                setattr(self, attr, entry)

            getattr(self, attr).grid(row=i+1, column=1, sticky='w', padx=5, pady=5)\

            #Academic
        academicFrame = tk.LabelFrame(self.leftFrame, text="Thông tin học tập", bg=COLORS['light'], fg=COLORS['primary'], font=FONTS['heading'], padx=10, pady=10)
        academicFrame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        academic_fields = [
            ('Khoa', 'combo_department'), ('Chuyên ngành', 'combo_major'),
            ('Lớp', 'combo_class'), ('Khóa', 'combo_gen')
        ]

        for i, (label, attr) in enumerate(academic_fields):
            lbl = tk.Label(academicFrame, text=label, bg=COLORS['light'], fg=COLORS['text_dark'], font=FONTS['small'])
            lbl.grid(row=i, column=0, sticky='w', padx=5, pady=3)

            var = tk.StringVar()
            combo = ttk.Combobox(academicFrame, textvariable=var, state='readonly', width=20, font=FONTS['small'])
            setattr(self, attr, combo)

            if 'gen' in attr:
                combo['values'] = GENERATION_OPTIONS
                combo.current(0)
                setattr(self, 'gen', var)
            elif 'department' in attr:
                setattr(self, 'department', var)
            elif 'major' in attr:
                setattr(self, 'major', var)
            elif 'class' in attr:
                setattr(self, 'class_name', var)

            combo.grid(row=i, column=1, sticky='w', padx=5, pady=3)

        actionFrame = tk.Frame(self.leftFrame, bg=COLORS['light'], pady=10)
        actionFrame.grid(row=2, column=0, padx=5, pady=5)

        buttons = [
            ('Thêm', 'studentBtnAdd', COLORS['success']),
            ('Sửa', 'studentBtnUpdate', COLORS['warning']),
            ('Xóa', 'studentBtnDel', COLORS['danger']),
            ('Làm mới', 'studentBtnRefresh', COLORS['info'])
        ]

        for i, (text, attr, color) in enumerate(buttons):
            btn = tk.Button(actionFrame, text=text, width=8, font=FONTS['small'], bg=color, fg='white', relief='raised', bd=1)
            btn.grid(row=0, column=i, padx=2)
            setattr(self, attr, btn)

        self.studentBtnBack = tk.Button(actionFrame, text='Quay lại', width=8, bg=COLORS['secondary'], fg='white', font=FONTS['small'])
        self.studentBtnBack.grid(row=1, column=0, columnspan=4, pady=(5, 0), sticky='ew')

        self.leftFrame.grid_rowconfigure(0, weight=60)
        self.leftFrame.grid_rowconfigure(1, weight=30)
        self.leftFrame.grid_rowconfigure(2, weight=10)
        self.leftFrame.grid_columnconfigure(0, weight=1)

    def create_right_frame(self):
        searchFrame = tk.Frame(self.rightFrame, bg=COLORS['card_bg'], pady=10)
        searchFrame.grid(row=0, column=0, sticky='ew', padx=10)

        tk.Label(searchFrame, text='Tìm kiếm theo:', bg=COLORS['card_bg'],
                 font=FONTS['small']).grid(row=0, column=0, padx=(0, 5))

        self.find = tk.StringVar()
        self.findCombo = ttk.Combobox(searchFrame, textvariable=self.find,
                                       state='readonly', width=15, font=FONTS['small'])
        self.findCombo['values'] = ['Mã sinh viên', 'Tên sinh viên', 'Chuyên ngành', 'Khóa', 'Lớp']
        self.findCombo.current(0)
        self.findCombo.grid(row=0, column=1, padx=5)

        self.findEntry = tk.Entry(searchFrame, width=35, font=FONTS['small'], relief='solid', bd=1)
        self.findEntry.grid(row=0, column=2, padx=5)

        self.findBtn = tk.Button(searchFrame, text='Tìm kiếm', width=10, bg=COLORS['primary'], fg='white', font=FONTS['small'])
        self.findBtn.grid(row=0, column=3, padx=5)

        self.showAllBtn = tk.Button(searchFrame, text='Xem tất cả', width=10, bg=COLORS['info'], fg='white', font=FONTS['small'])
        self.showAllBtn.grid(row=0, column=4, padx=5)

        self.exportBtn = tk.Button(searchFrame, text='Xuất danh sách', width=15, bg=COLORS['success'], fg='white', font=FONTS['small'])
        self.exportBtn.grid(row=0, column=5, padx=5, sticky="we")

        # Treeview section
        treeFrame = tk.Frame(self.rightFrame, bg=COLORS['card_bg'])
        treeFrame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))

        columns = ('stt', 'student_id', 'name', 'gender', 'birth', 'generation', 'major', 'class', 'gpa')
        self.tree = ttk.Treeview(treeFrame, columns=columns, show='headings', height=15)

        # Define headings
        headings = {
            'stt': 'STT', 'student_id': 'Mã SV', 'name': 'Họ và tên',
            'gender': 'Giới tính', 'birth': 'Ngày sinh', 'generation': 'Khóa',
            'major': 'Chuyên ngành', 'class': 'Lớp', 'gpa': 'GPA'
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=80, anchor='center')

        self.tree.column('name', width=150, anchor='w')
        self.tree.column('major', width=120, anchor='w')

        # Scrollbars
        v_scroll = ttk.Scrollbar(treeFrame, orient='vertical', command=self.tree.yview)
        h_scroll = ttk.Scrollbar(treeFrame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        # Configure right panel grid
        self.rightFrame.grid_rowconfigure(0, weight=0)
        self.rightFrame.grid_rowconfigure(1, weight=1)
        self.rightFrame.grid_columnconfigure(0, weight=1)
        treeFrame.grid_rowconfigure(0, weight=1)
        treeFrame.grid_columnconfigure(0, weight=1)