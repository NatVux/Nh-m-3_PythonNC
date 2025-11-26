# views/subject_view.py

import tkinter as tk
from tkinter import ttk
from .base_view import BaseView
from constants import COLORS, FONTS, SEMESTER_OPTIONS


class SubjectView(BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Title
        titleFrame = tk.Frame(self, bg=COLORS['primary'], height=60)
        titleFrame.grid(row=0, column=0, sticky='ew')
        titleFrame.grid_propagate(False)

        self.title = tk.Label(titleFrame, text='QUẢN LÝ HỌC PHẦN', font=FONTS['title'], bg=COLORS['primary'], fg='white')
        self.title.grid(row=0, column=0, padx=20, pady=15, sticky='w')

        # Search
        searchFrame = tk.Frame(self, bg=COLORS['card_bg'], padx=20, pady=15)
        searchFrame.grid(row=1, column=0, sticky='ew')

        # Student ID
        tk.Label(searchFrame, text='Mã sinh viên:', bg=COLORS['card_bg'],
                 font=FONTS['normal']).grid(row=0, column=0, sticky='w', padx=(0, 5))

        self.idEntry = tk.Entry(searchFrame, width=15, font=FONTS['normal'], relief='solid', bd=1)
        self.idEntry.grid(row=0, column=1, sticky='w', padx=(0, 20))

        # Student name
        tk.Label(searchFrame, text='Tên sinh viên:', bg=COLORS['card_bg'],
                 font=FONTS['normal']).grid(row=0, column=2, sticky='w', padx=(0, 5))

        self.studentNameEntry = tk.Entry(searchFrame, width=25, font=FONTS['normal'],
                                         state='disabled', relief='solid', bd=1)
        self.studentNameEntry.grid(row=0, column=3, sticky='w', padx=(0, 20))

        # Semester
        tk.Label(searchFrame, text='Học kì:', bg=COLORS['card_bg'],
                 font=FONTS['normal']).grid(row=0, column=4, sticky='w', padx=(0, 5))

        self.semester = tk.StringVar()
        self.semesterCombo = ttk.Combobox(searchFrame, textvariable=self.semester, state='readonly', width=10, font=FONTS['normal'])
        self.semesterCombo['values'] = SEMESTER_OPTIONS
        self.semesterCombo.current(0)
        self.semesterCombo.grid(row=0, column=5, sticky='w', padx=(0, 20))

        # Buttons
        self.findBtn = tk.Button(searchFrame, text='Tìm kiếm', width=12, bg=COLORS['primary'], fg='white', font=FONTS['normal'])
        self.findBtn.grid(row=0, column=6, padx=5)

        self.exportBtn = tk.Button(searchFrame, text='Xuất danh sách', width=12, bg=COLORS['success'], fg='white', font=FONTS['normal'])
        self.exportBtn.grid(row=0, column=7, padx=5)

        # Treeview section
        treeFrame = tk.Frame(self, bg=COLORS['card_bg'])
        treeFrame.grid(row=2, column=0, sticky='nsew', padx=20, pady=(0, 10))

        columns = ('stt', 'subject_id', 'subject_name', 'semester', 'subject_credit',
                   'score_regular', 'score_midterm', 'score_final', 'score_avarage', 'rating')
        self.tree = ttk.Treeview(treeFrame, columns=columns, show='headings', height=12)

        # Define headings and widths
        headings = {
            'stt': 'STT', 'subject_id': 'Mã HP', 'subject_name': 'Tên học phần',
            'semester': 'HK', 'subject_credit': 'TC', 'score_regular': 'Điểm TX',
            'score_midterm': 'Điểm GK', 'score_final': 'Điểm CK',
            'score_avarage': 'Điểm TB', 'rating': 'Xếp loại'
        }

        widths = {
            'stt': 50, 'subject_id': 80, 'subject_name': 200, 'semester': 50,
            'subject_credit': 50, 'score_regular': 70, 'score_midterm': 70,
            'score_final': 70, 'score_avarage': 70, 'rating': 80
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor='center')

        # Scrollbars
        v_scroll = ttk.Scrollbar(treeFrame, orient='vertical', command=self.tree.yview)
        h_scroll = ttk.Scrollbar(treeFrame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        # Action buttons
        actionFrame = tk.Frame(self, bg=COLORS['card_bg'], pady=15)
        actionFrame.grid(row=3, column=0, sticky='ew', padx=20)

        buttons = [
            ('Thêm học phần', 'subjectAddBtn', COLORS['success']),
            ('Sửa học phần', 'subjectUpdateBtn', COLORS['warning']),
            ('Xóa học phần', 'subjectDelBtn', COLORS['danger']),
            ('Quay lại', 'backBtn', COLORS['secondary'])
        ]

        for i, (text, attr, color) in enumerate(buttons):
            btn = tk.Button(actionFrame, text=text, width=15, font=FONTS['normal'],
                            bg=color, fg='white', relief='raised', bd=1)
            btn.grid(row=0, column=i, padx=10)
            setattr(self, attr, btn)

        # Configure grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        treeFrame.grid_rowconfigure(0, weight=1)
        treeFrame.grid_columnconfigure(0, weight=1)