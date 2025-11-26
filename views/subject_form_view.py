# views/subject_form_view.py

import tkinter as tk
from tkinter import ttk
from constants import COLORS, FONTS, SEMESTER_OPTIONS


class TopLevelSubjectView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Form Học Phần')
        self.configure(bg=COLORS['background'])
        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=80)
        self.grid_rowconfigure(2, weight=10)

        # Frame 1 - Title
        self.frame1 = tk.Frame(self, bg=COLORS['primary'], height=60)
        self.frame1.grid(row=0, column=0, sticky='ew')
        self.frame1.grid_propagate(False)
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)

        # Frame 2 - Form
        self.frame2 = tk.Frame(self, bg=COLORS['card_bg'], padx=20, pady=20)
        self.frame2.grid(row=1, column=0, sticky='nsew')

        for i in range(5):
            self.frame2.grid_rowconfigure(i, weight=20)
            if i < 4:
                self.frame2.grid_columnconfigure(i, weight=25)

        # Frame 3 - Buttons
        self.frame3 = tk.Frame(self, bg=COLORS['background'], pady=15)
        self.frame3.grid(row=2, column=0, sticky='ew')
        self.frame3.grid_columnconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(1, weight=1)
        self.frame3.grid_rowconfigure(0, weight=1)

        # Widgets in frame 1
        self.title1 = tk.Label(self.frame1, text='Thêm học phần',
                               font=FONTS['title'], bg=COLORS['primary'], fg='white')
        self.title1.grid(row=0, column=0, padx=20, pady=15, sticky='w')

        # Widgets in frame 2
        # Student_id
        self.studentIdLbl = tk.Label(
            self.frame2,
            text='Mã sinh viên:',
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            font=FONTS['normal'])
        self.studentIdLbl.grid(row=0, column=0, padx=5, pady=10, sticky='w')

        self.studentIdEnt = tk.Entry(
            self.frame2,
            width=20,
            font=FONTS['normal'],
            relief='solid', bd=1)
        self.studentIdEnt.grid(row=0, column=1, padx=5, pady=10, sticky='w')

        # Student_name
        self.studentNameLbl = tk.Label(
            self.frame2,
            text='Tên sinh viên:',
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            font=FONTS['normal'])
        self.studentNameLbl.grid(row=0, column=2, padx=5, pady=10, sticky='w')

        self.studentNameEnt = tk.Entry(
            self.frame2,
            width=25,
            font=FONTS['normal'],
            state='disabled',
            relief='solid',
            bd=1)
        self.studentNameEnt.grid(row=0, column=3, padx=5, pady=10, sticky='w')

        # Subject_id
        self.subjectIdLbl = tk.Label(
            self.frame2,
            text='Mã học phần:',
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            font=FONTS['normal'])
        self.subjectIdLbl.grid(row=1, column=0, padx=5, pady=10, sticky='w')

        self.subjectId = tk.StringVar()
        self.subjectIdCombo = ttk.Combobox(
            self.frame2, state='readonly',
            textvariable=self.subjectId,
            width=18,
            font=FONTS['normal'])
        self.subjectIdCombo.grid(row=1, column=1, padx=5, pady=10, sticky='w')

        # Subject_name
        self.subjectNameLbl = tk.Label(self.frame2, text='Tên học phần:',
                                         bg=COLORS['card_bg'], fg=COLORS['text_dark'],
                                         font=FONTS['normal'])
        self.subjectNameLbl.grid(row=1, column=2, padx=5, pady=10, sticky='w')

        self.subjectNameEnt = tk.Entry(self.frame2, state='readonly', width=25,
                                         font=FONTS['normal'], relief='solid', bd=1)
        self.subjectNameEnt.grid(row=1, column=3, padx=5, pady=10, sticky='w')

        # Semester
        self.semesterLbl = tk.Label(self.frame2, text='Học kì:',
                                     bg=COLORS['card_bg'], fg=COLORS['text_dark'],
                                     font=FONTS['normal'])
        self.semesterLbl.grid(row=2, column=0, padx=5, pady=10, sticky='w')

        self.semester = tk.StringVar()
        self.semesterCombo = ttk.Combobox(self.frame2, state='readonly',
                                           textvariable=self.semester,
                                           width=18, font=FONTS['normal'])
        self.semesterCombo['values'] = [opt for opt in SEMESTER_OPTIONS if opt != 'Tất cả']
        self.semesterCombo.grid(row=2, column=1, padx=5, pady=10, sticky='w')

        # Credit
        self.creditlbl = tk.Label(self.frame2, text='Số tín chỉ:',
                                   bg=COLORS['card_bg'], fg=COLORS['text_dark'],
                                   font=FONTS['normal'])
        self.creditlbl.grid(row=2, column=2, padx=5, pady=10, sticky='w')

        self.creditEnt = tk.Entry(self.frame2, state='readonly', width=25,
                                   font=FONTS['normal'], relief='solid', bd=1)
        self.creditEnt.grid(row=2, column=3, padx=5, pady=10, sticky='w')

        # Score_regular
        self.scoreRegularLbl = tk.Label(self.frame2, text='Điểm thường xuyên:',
                                          bg=COLORS['card_bg'], fg=COLORS['text_dark'],
                                          font=FONTS['normal'])
        self.scoreRegularLbl.grid(row=3, column=0, padx=5, pady=10, sticky='w')

        self.scoreRegularEnt = tk.Entry(self.frame2, width=20, font=FONTS['normal'],
                                          relief='solid', bd=1)
        self.scoreRegularEnt.grid(row=3, column=1, padx=5, pady=10, sticky='w')

        # Score_midterm
        self.scoreMidtermLbl = tk.Label(self.frame2, text='Điểm giữa kì:',
                                          bg=COLORS['card_bg'], fg=COLORS['text_dark'],
                                          font=FONTS['normal'])
        self.scoreMidtermLbl.grid(row=3, column=2, padx=5, pady=10, sticky='w')

        self.scoreMidtermEnt = tk.Entry(self.frame2, width=25, font=FONTS['normal'],
                                          relief='solid', bd=1)
        self.scoreMidtermEnt.grid(row=3, column=3, padx=5, pady=10, sticky='w')

        # Score_final
        self.scoreFinalLbl = tk.Label(self.frame2, text='Điểm cuối kì:',
                                        bg=COLORS['card_bg'], fg=COLORS['text_dark'],
                                        font=FONTS['normal'])
        self.scoreFinalLbl.grid(row=4, column=0, padx=5, pady=10, sticky='w')

        self.scoreFinalEnt = tk.Entry(self.frame2, width=20, font=FONTS['normal'],
                                        relief='solid', bd=1)
        self.scoreFinalEnt.grid(row=4, column=1, padx=5, pady=10, sticky='w')

        # Widgets in frame 3
        self.confirmAddBtn = tk.Button(self.frame3, text='Xác nhận', width=12,
                                         bg=COLORS['success'], fg='white',
                                         font=FONTS['normal'])
        self.confirmAddBtn.grid(row=0, column=0, padx=5, pady=5)

        self.cancelAddBtn = tk.Button(self.frame3, text='Hủy bỏ', width=12,
                                        bg=COLORS['danger'], fg='white',
                                        font=FONTS['normal'])
        self.cancelAddBtn.grid(row=0, column=1, padx=5, pady=5)