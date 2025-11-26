import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from fpdf import FPDF
import os
from PIL import Image, ImageTk

from views import LoginView, AdminDashboardView, StudentView, SubjectView, TopLevelSubjectView
from models.student_model import StudentModel
from constants import COLORS, FONTS


class AppController:
    def __init__(self, root):
        self.user_name = None
        self.root = root
        self.root.title('Student Management')
        self.root.geometry("1280x800")
        self.root.resizable(True, True)
        self.root.configure(bg=COLORS['background'])

        # Cấu hình khung chính
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Model
        self.student_model = StudentModel()
        self.show_login_view()

    def show_login_view(self, event=None):
        self.clear_frame()
        self.login_view = LoginView(self.root)
        self.login_view.grid(row=0, column=0, sticky='nsew')

        # Sự kiện khi bấm nút
        self.login_view.showPwBtn.bind('<Button-1>', self.show_password)
        self.login_view.loginBtn.bind('<Button-1>', self.valid_account)

    def valid_account(self, event):
        self.user_name = self.login_view.usernameEntry.get()
        password = self.login_view.passwordEntry.get()
        if self.user_name.strip() == '' or password.strip() == '':
            messagebox.showwarning('Lỗi', 'Dữ liệu không hợp lệ')
        else:
            account = self.student_model.get_account((self.user_name, password))
            if len(account) != 0:
                self.show_admin_dashboard_view()
            else:
                messagebox.showwarning('Lỗi', 'Tài khoản hoặc mật khẩu không chính xác')

    def show_admin_dashboard_view(self, event=None):
        self.clear_frame()
        self.admin_dashboard_view = AdminDashboardView(self.root)
        self.admin_dashboard_view.grid(row=0, column=0, sticky='nsew')
        self.set_welcome(self.user_name)

        # Event bindings
        self.admin_dashboard_view.studentsBtn.bind('<Button-1>', self.show_student_view)
        self.admin_dashboard_view.resultsBtn.bind('<Button-1>', self.show_subject_view)
        self.admin_dashboard_view.logoutBtn.bind('<Button-1>', self.dashboard_logout)

    def set_welcome(self, user_name):
        account_name = self.student_model.get_account_name_by_account_us((user_name,))[0][0]
        self.admin_dashboard_view.welcomeLbl.config(text=f'Welcome {account_name}')

    def show_student_view(self, event=None):
        self.clear_frame()
        self.student_view = StudentView(self.root)
        self.student_view.grid(row=0, column=0, sticky='nsew')

        # Event bindings
        self.student_view.tree.bind('<<TreeviewSelect>>', self.on_select_student_view)
        self.student_view.showAllBtn.bind('<Button-1>', self.get_all_students)
        self.student_view.selectImgBtn.bind('<Button-1>', self.on_select_image)
        self.student_view.studentBtnAdd.bind('<Button-1>', self.add_student)
        self.student_view.studentBtnUpdate.bind('<Button-1>', self.update_student)
        self.student_view.studentBtnDel.bind('<Button-1>', self.delete_student)
        self.student_view.exportBtn.bind('<Button-1>', self.export_file_student)
        self.student_view.studentBtnRefresh.bind('<Button-1>', self.refresh_infor)
        self.student_view.studentBtnBack.bind('<Button-1>', self.studentview_back_dashboard)
        self.student_view.findBtn.bind('<Button-1>', self.find_student)

        # Load initial data
        self.load_student_combobox_data()
        self.get_all_students()

    def show_subject_view(self, event=None):
        self.clear_frame()
        self.subjectView = SubjectView(self.root)
        self.subjectView.grid(row=0, column=0, sticky='nsew')

        # Event bindings
        self.subjectView.findBtn.bind('<Button-1>', self.get_subject_by_id_semester)
        self.subjectView.subjectAddBtn.bind('<Button-1>', self.show_form_subject_add)
        self.subjectView.subjectUpdateBtn.bind('<Button-1>', self.show_form_subject_update)
        self.subjectView.subjectDelBtn.bind('<Button-1>', self.delete_subject_student)
        self.subjectView.exportBtn.bind('<Button-1>', self.export_file_subject)
        self.subjectView.backBtn.bind('<Button-1>', self.subjectview_back_dashboard)
        self.subjectView.tree.bind('<<TreeviewSelect>>', self.on_selected_subject_student_view)

    def show_password(self, event):
        if self.login_view.showPassword.get():
            self.login_view.passwordEntry.config(show='')
        else:
            self.login_view.passwordEntry.config(show='*')

    def load_student_combobox_data(self):
        # Department data
        department_name = self.student_model.get_department_name()
        department_name = [i[0] for i in department_name]
        self.student_view.combo_department['values'] = department_name
        if department_name:
            self.student_view.combo_department.current(0)

        # Class data
        class_name = self.student_model.get_class_name()
        class_name = [i[0] for i in class_name]
        self.student_view.combo_class['values'] = class_name
        if class_name:
            self.student_view.combo_class.current(0)

        # Major data
        major_name = self.student_model.get_major_name()
        major_name = [i[0] for i in major_name]
        self.student_view.combo_major['values'] = major_name
        if major_name:
            self.student_view.combo_major.current(0)

    def find_student(self, event):
        find_criteria = self.student_view.find.get()
        find_data = self.student_view.findEntry.get()

        if not find_data:
            messagebox.showwarning('Lỗi', 'Vui lòng nhập thông tin tìm kiếm')
            return

        # Map criteria to database fields
        criteria_map = {
            'Mã sinh viên': 'student_id',
            'Tên sinh viên': 'student_name',
            'Chuyên ngành': 'major_name',
            'Khóa': 'student_generation',
            'Lớp': 'class_name'
        }

        db_criteria = criteria_map.get(find_criteria, 'student_id')
        students = self.student_model.get_all_fields_students(db_criteria, find_data)

        self.delete_all_items_tree(self.student_view.tree)

        # Format birth date
        for i in range(len(students)):
            students[i] = list(students[i])
            students[i][3] = self.format_birth(str(students[i][3]))

        # Add to treeview
        for i, student in enumerate(students):
            self.student_view.tree.insert('', tk.END, values=((i + 1,) + tuple(student)))

    def on_select_student_view(self, event):
        if self.student_view.tree.selection():
            selected_item = self.student_view.tree.selection()[0]
            values = self.student_view.tree.item(selected_item, 'values')
            student_id = values[1]

            student = self.student_model.get_student_by_id(student_id)
            if student:
                self.populate_student_form(student)
                self.student_view.studentBtnUpdate.config(state='normal')
                self.student_view.studentBtnDel.config(state='normal')
                self.student_view.studentBtnAdd.config(state='disabled')
        else:
            self.student_view.studentBtnUpdate.config(state='disabled')
            self.student_view.studentBtnDel.config(state='disabled')
            self.student_view.studentBtnAdd.config(state='normal')

    def populate_student_form(self, student):
        # Clear form first
        self.student_view.ent_id.config(state='normal')
        self.student_view.ent_id.delete(0, tk.END)
        self.student_view.ent_id.insert(0, student[0])
        self.student_view.ent_id.config(state='readonly')

        self.student_view.ent_name.delete(0, tk.END)
        self.student_view.ent_name.insert(0, student[1])

        self.student_view.date_birth.set_date(student[2])

        self.student_view.ent_address.delete(0, tk.END)
        self.student_view.ent_address.insert(0, student[3])

        self.student_view.ent_cccd.delete(0, tk.END)
        self.student_view.ent_cccd.insert(0, student[4])

        self.student_view.ent_phone.delete(0, tk.END)
        self.student_view.ent_phone.insert(0, student[5])

        self.student_view.ent_email.delete(0, tk.END)
        self.student_view.ent_email.insert(0, student[6])

        self.student_view.gender.set(student[7])

        self.student_view.gen.set(student[8])

        # Load image if exists
        self.image_path = student[9] if student[9] else ''
        if self.image_path and os.path.exists(self.image_path):
            self.load_student_image(self.image_path)

        # Set academic info
        self.student_view.department.set(student[12])
        self.student_view.major.set(student[10])
        self.student_view.class_name.set(student[11])

    def load_student_image(self, image_path):
        try:
            image = Image.open(image_path)
            resized_image = image.resize((120, 160))
            self.photo = ImageTk.PhotoImage(resized_image)
            self.student_view.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        except Exception as e:
            print(f"Error loading image: {e}")

    def on_select_image(self, event):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
        )
        if self.image_path:
            self.load_student_image(self.image_path)

    def get_all_students(self, event=None):
        self.delete_all_items_tree(self.student_view.tree)
        students = self.student_model.get_all_students()

        for i, student in enumerate(students):
            student = list(student)
            student[3] = self.format_birth(str(student[3]))
            self.student_view.tree.insert('', tk.END, values=((i + 1,) + tuple(student)))

    def format_birth(self, old_birth):
        try:
            old_birth = old_birth.replace('/', '-')
            birth = old_birth.split('-')
            birth.reverse()
            return '/'.join(birth)
        except:
            return old_birth

    def add_student(self, event):
        student_data = self.get_student_form_data()
        if not student_data:
            return

        if not all(student_data[:7]):
            messagebox.showwarning('Lỗi', 'Vui lòng điền đầy đủ thông tin bắt buộc')
            return

        if self.student_model.get_student_name_by_id((student_data[0],)):
            messagebox.showwarning('Lỗi', 'Mã sinh viên đã tồn tại')
            return

        try:
            self.student_model.add_student(tuple(student_data))
            messagebox.showinfo('Thành công', 'Thêm sinh viên thành công')
            self.get_all_students()
            self.refresh_infor()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi thêm sinh viên: {str(e)}')

    def get_student_form_data(self):
        try:
            student_id = self.student_view.ent_id.get().strip()
            student_name = self.student_view.ent_name.get().strip()
            student_birth = self.student_view.date_birth.get().strip()
            student_address = self.student_view.ent_address.get().strip()
            student_cccd = self.student_view.ent_cccd.get().strip()
            student_phone = self.student_view.ent_phone.get().strip()
            student_email = self.student_view.ent_email.get().strip()
            student_gender = self.student_view.gender.get().strip()
            student_gen = self.student_view.gen.get().strip()

            # Get IDs for foreign keys
            major_id = self.student_model.get_id_by_name('Major', self.student_view.major.get())
            class_id = self.student_model.get_id_by_name('Class', self.student_view.class_name.get())

            return [
                student_id, student_name, self.format_birth(student_birth),
                student_address, student_cccd, student_phone, student_email,
                student_gender, student_gen, self.image_path,
                class_id[0] if class_id else None,
                major_id[0] if major_id else None
            ]
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi lấy dữ liệu form: {str(e)}')
            return None

    def update_student(self, event):
        if not messagebox.askokcancel('Xác nhận', 'Bạn có chắc chắn muốn cập nhật thông tin sinh viên?'):
            return

        student_data = self.get_student_form_data()
        if not student_data:
            return

        try:
            # Reorder data for update
            update_data = student_data[1:] + [student_data[0]]
            self.student_model.update_student(tuple(update_data))
            messagebox.showinfo('Thành công', 'Cập nhật sinh viên thành công')
            self.get_all_students()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi cập nhật sinh viên: {str(e)}')

    def delete_student(self, event):
        student_id = self.student_view.ent_id.get()
        if not student_id:
            messagebox.showwarning('Lỗi', 'Vui lòng chọn sinh viên để xóa')
            return

        if not messagebox.askokcancel('Xác nhận', 'Bạn có chắc chắn muốn xóa sinh viên này?'):
            return

        try:
            self.student_model.delete_student((student_id,))
            messagebox.showinfo('Thành công', 'Xóa sinh viên thành công')
            self.get_all_students()
            self.refresh_infor()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi xóa sinh viên: {str(e)}')

    def refresh_infor(self, event=None):
        self.student_view.ent_id.config(state='normal')
        self.student_view.ent_id.delete(0, tk.END)
        self.student_view.ent_name.delete(0, tk.END)
        self.student_view.ent_address.delete(0, tk.END)
        self.student_view.ent_cccd.delete(0, tk.END)
        self.student_view.ent_phone.delete(0, tk.END)
        self.student_view.ent_email.delete(0, tk.END)
        self.student_view.canvas.delete("all")
        self.image_path = ''
        self.student_view.studentBtnAdd.config(state='normal')
        self.student_view.studentBtnUpdate.config(state='disabled')
        self.student_view.studentBtnDel.config(state='disabled')

    def show_form_subject_add(self, event):
        self.form_subject_view = TopLevelSubjectView(self.subjectView)
        self.form_subject_view.geometry('680x440')

        # Event bindings
        self.form_subject_view.subjectIdCombo.bind('<<ComboboxSelected>>', self.set_value_by_subject_id)
        self.form_subject_view.studentIdEnt.bind('<FocusOut>', self.set_value_by_student_id)
        self.form_subject_view.confirmAddBtn.bind('<Button-1>', self.add_subject_student)
        self.form_subject_view.cancelAddBtn.bind('<Button-1>', lambda e: self.form_subject_view.destroy())

        # Load subject IDs
        subjects_id = self.student_model.get_id_subject()
        subjects_id = [i[0] for i in subjects_id]
        self.form_subject_view.subjectIdCombo['values'] = subjects_id
        if subjects_id:
            self.form_subject_view.subjectIdCombo.current(0)

    def set_value_by_subject_id(self, event):
        subject_id = self.form_subject_view.subjectId.get()
        if subject_id:
            subject_info = self.student_model.get_subject_name_credit_by_id((subject_id,))
            if subject_info:
                self.form_subject_view.subjectNameEnt.config(state='normal')
                self.form_subject_view.subjectNameEnt.delete(0, tk.END)
                self.form_subject_view.subjectNameEnt.insert(0, subject_info[0][0])
                self.form_subject_view.subjectNameEnt.config(state='readonly')

                self.form_subject_view.creditEnt.config(state='normal')
                self.form_subject_view.creditEnt.delete(0, tk.END)
                self.form_subject_view.creditEnt.insert(0, subject_info[0][1])
                self.form_subject_view.creditEnt.config(state='readonly')

    def set_value_by_student_id(self, event):
        student_id = self.form_subject_view.studentIdEnt.get()
        if student_id:
            student_info = self.student_model.get_student_name_by_id((student_id,))
            if student_info:
                self.form_subject_view.studentNameEnt.config(state='normal')
                self.form_subject_view.studentNameEnt.delete(0, tk.END)
                self.form_subject_view.studentNameEnt.insert(0, student_info[0][0])
                self.form_subject_view.studentNameEnt.config(state='disabled')

    def add_subject_student(self, event):
        student_id = self.form_subject_view.studentIdEnt.get()
        subject_id = self.form_subject_view.subjectId.get()
        semester = self.form_subject_view.semester.get()
        score_regular = self.form_subject_view.scoreRegularEnt.get()
        score_midterm = self.form_subject_view.scoreMidtermEnt.get()
        score_final = self.form_subject_view.scoreFinalEnt.get()

        if not all([student_id, subject_id, semester]):
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin")
            return

        try:
            score_regular = int(score_regular) if score_regular else 0
            score_midterm = int(score_midterm) if score_midterm else 0
            score_final = int(score_final) if score_final else 0

            existing = self.student_model.get_subject_student((subject_id, student_id, semester))
            if existing:
                messagebox.showwarning("Lỗi", "Học pần này đã tồn tại cho sinh viên trong học kỳ này")
                return

            self.student_model.add_subject_student((subject_id, student_id, semester, score_regular, score_midterm, score_final))
            messagebox.showinfo("Thành công", "Thêm học phần thành công")
            self.form_subject_view.destroy()
            self.get_subject_by_id_semester()

        except ValueError:
            messagebox.showwarning("Lỗi", "Điểm nhập vào ở dạng số")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi thêm học phần: {str(e)}")

    def show_form_subject_update(self, event):
        selected_item = self.subjectView.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Hãy chọn học phần cần sửa")
            return

        self.form_subject_view = TopLevelSubjectView(self.subjectView)
        self.form_subject_view.geometry('680x440')
        self.form_subject_view.title("Sửa học phần")

        values = self.subjectView.tree.item(selected_item[0], 'values')
        student_id = self.subjectView.idEntry.get()
        subject_id = values[1]
        semester = values[3]

        self.form_subject_view.studentIdEnt.insert(0, student_id)
        self.form_subject_view.studentIdEnt.config(state='disabled')

        student_info = self.student_model.get_student_name_by_id((student_id,))
        if student_info:
            self.form_subject_view.studentNameEnt.config(state='normal')
            self.form_subject_view.studentNameEnt.insert(0, student_info[0][0])
            self.form_subject_view.studentNameEnt.config(state='disabled')

        subjects_id = self.student_model.get_id_subject()
        subjects_id = [i[0] for i in subjects_id]
        self.form_subject_view.subjectIdCombo['values'] = subjects_id
        self.form_subject_view.subjectId.set(subject_id)
        self.set_value_by_subject_id(None)

        self.form_subject_view.semester.set(semester)

        self.form_subject_view.scoreRegularEnt.insert(0, values[5])
        self.form_subject_view.scoreMidtermEnt.insert(0, values[6])
        self.form_subject_view.scoreFinalEnt.insert(0, values[7])

        self.form_subject_view.confirmAddBtn.config(text='Cập nhật', command=lambda: self.update_subject_student_data(subject_id, student_id, semester))
        self.form_subject_view.cancelAddBtn.bind('<Button-1>', lambda e: self.form_subject_view.destroy())

    def update_subject_student_data(self, old_subject_id, student_id, old_semester):
        new_subject_id = self.form_subject_view.subjectId.get()
        new_semester = self.form_subject_view.semester.get()
        score_regular = self.form_subject_view.scoreRegularEnt.get()
        score_midterm = self.form_subject_view.scoreMidtermEnt.get()
        score_final = self.form_subject_view.scoreFinalEnt.get()

        if not all([student_id, new_subject_id, new_semester]):
            messagebox.showwarning('Lỗi', 'Vui lòng điền đầy đủ thông tin bắt buộc')
            return

        try:
            score_regular = float(score_regular) if score_regular else 0
            score_midterm = float(score_midterm) if score_midterm else 0
            score_final = float(score_final) if score_final else 0

            if old_subject_id != new_subject_id or old_semester != new_semester:
                existing = self.student_model.get_subject_student((new_subject_id, student_id, new_semester))
                if existing:
                    messagebox.showwarning('Lỗi', 'Học phần đã tồn tại cho sinh viên này trong học kỳ này')
                    return

            self.student_model.update_subject_student((score_regular, score_midterm, score_final, new_subject_id, student_id, new_semester))
            messagebox.showinfo('Thành công', 'Cập nhật học phần thành công')
            self.form_subject_view.destroy()
            self.get_subject_by_id_semester()
        except ValueError:
            messagebox.showwarning('Lỗi', 'Điểm nhập vào phải là số')
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi cập nhật học phần: {str(e)}')

    def delete_subject_student(self, event):
        selected_item = self.subjectView.tree.selection()
        if not selected_item:
            messagebox.showwarning('Lỗi', 'Vui lòng chọn học phần cần xóa')
            return

        if not messagebox.askokcancel('Xác nhận', 'Bạn có chắc chắn muốn xóa học phần này?'):
            return

        values = self.subjectView.tree.item(selected_item[0], 'values')
        student_id = self.subjectView.idEntry.get()
        subject_id = values[1]
        semester = values[3]

        try:
            self.student_model.delete_subject_student((subject_id, student_id, semester))
            messagebox.showinfo('Thành công', 'Xóa học phần thành công')
            self.get_subject_by_id_semester()
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi xóa học phần: {str(e)}')

    def get_subject_by_id_semester(self, event=None):
        student_id = self.subjectView.idEntry.get()
        semester = self.subjectView.semester.get()

        if not student_id:
            messagebox.showwarning('Lỗi', 'Vui lòng nhập mã sinh viên')
            return

        # Set student name
        student_info = self.student_model.get_student_name_by_id((student_id,))
        if student_info:
            self.subjectView.studentNameEntry.config(state='normal')
            self.subjectView.studentNameEntry.delete(0, tk.END)
            self.subjectView.studentNameEntry.insert(0, student_info[0][0])
            self.subjectView.studentNameEntry.config(state='disabled')
        else:
            self.subjectView.studentNameEntry.config(state='normal')
            self.subjectView.studentNameEntry.delete(0, tk.END)
            self.subjectView.studentNameEntry.config(state='disabled')
            messagebox.showwarning('Lỗi', 'Không tìm thấy sinh viên với mã này')
            return

        subjects = self.student_model.get_subject_by_id_semester((student_id, semester))
        self.delete_all_items_tree(self.subjectView.tree)

        for i, subject in enumerate(subjects):
            self.subjectView.tree.insert('', tk.END, values=((i + 1,) + tuple(subject)))

    def on_selected_subject_student_view(self, event):
        if self.subjectView.tree.selection():
            self.subjectView.subjectUpdateBtn.config(state='normal')
            self.subjectView.subjectDelBtn.config(state='normal')
        else:
            self.subjectView.subjectUpdateBtn.config(state='disabled')
            self.subjectView.subjectDelBtn.config(state='disabled')

    def export_file_student(self, event):
        try:
            students = self.student_model.get_all_students()
            df = pd.DataFrame(students, columns=['Mã SV', 'Họ tên', 'Giới tính', 'Ngày sinh', 'Khóa', 'Chuyên ngành', 'Lớp',
                                       'GPA'])

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )

            if file_path:
                if file_path.endswith('.xlsx'):
                    df.to_excel(file_path, index=False)
                else:
                    df.to_csv(file_path, index=False)

                messagebox.showinfo('Thành công', f'Xuất danh sách thành công: {file_path}')
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi xuất file: {str(e)}')

    def export_file_subject(self, event):
        try:
            student_id = self.subjectView.idEntry.get()
            if not student_id:
                messagebox.showwarning('Lỗi', 'Vui lòng nhập mã sinh viên trước khi xuất danh sách')
                return

            semester = self.subjectView.semester.get()
            subjects = self.student_model.get_subject_by_id_semester((student_id, semester))

            df = pd.DataFrame(subjects,
                              columns=['Mã HP', 'Tên học phần', 'Học kỳ', 'Số TC', 'Điểm TX', 'Điểm GK', 'Điểm CK',
                                       'Điểm TB', 'Xếp loại'])

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )

            if file_path:
                if file_path.endswith('.xlsx'):
                    df.to_excel(file_path, index=False)
                else:
                    df.to_csv(file_path, index=False)

                messagebox.showinfo('Thành công', f'Xuất danh sách thành công: {file_path}')
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi khi xuất file: {str(e)}')

    def delete_all_items_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def studentview_back_dashboard(self, event=None):
        self.show_admin_dashboard_view()

    def subjectview_back_dashboard(self, event=None):
        self.show_admin_dashboard_view()

    def dashboard_logout(self, event=None):
        self.show_login_view()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()