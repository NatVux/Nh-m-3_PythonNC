import mysql.connector
from constants import DATABASE_CONFIG

class StudentModel:
    def __init__(self):
        self.connection = mysql.connector.connect(**DATABASE_CONFIG)
        self.cursor = self.connection.cursor()

    def get_account(self, tuple_us_pw):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Account WHERE account_username = %s AND account_password = %s;"
        cursor.execute(query, tuple_us_pw)
        account = cursor.fetchall()
        cursor.close()
        return account

    def get_account_name_by_account_us(self, tuple_account_name):
        cursor = self.connection.cursor()
        query = "SELECT account_name FROM Account WHERE account_username = %s;"
        cursor.execute(query, tuple_account_name)
        account_name = cursor.fetchall()
        cursor.close()
        return account_name

    def get_account_name_by_account_username(self, tuple_account_name):
        """Backward compatibility wrapper."""
        return self.get_account_name_by_account_us(tuple_account_name)

    def get_all_students(self):
      query = """Select Student.student_id, Student.student_name, 
          Student.student_gender,Student.student_birth, 
          Student.student_generation, Major.major_name, 
          Class.class_name,
          sum(
           Case
              When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 8.5 then 4
              When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 8 then 3.5
              When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 7 then 3
              When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 6.5 then 2.5
              When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 5.5 then 2
              When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 5 then 1.5
              When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 4 then 1
          else 0
          end * subject.subject_credit)/sum(subject.subject_credit) as gpa
          from Student
          Join Major on Student.major_id = Major.major_id
          Join Class on Student.class_id = Class.class_id
          LEFT JOIN SUBJECT_STUDENT ON SUBJECT_STUDENT.student_id = Student.student_id
          LEFT JOIN SUBJECT ON SUBJECT.subject_id = Subject_Student.Subject_id
          Group by Student.student_id
      """
      self.cursor.execute(query)
      students = self.cursor.fetchall()
      return students

    def get_all_fields_students(self, criteria, data):
        # Select lồng (từ 1 bảng nối)
        query = f"""SELECT student_data.* FROM
            (Select Student.student_id,Student.student_name, 
                Student.student_gender,Student.student_birth, 
                Student.student_generation, Major.major_name, 
                Class.class_name,
                sum(
                    Case
                      When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 8.5 then 4
                      When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 8 then 3.5
                      When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 7 then 3
                      When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 6.5 then 2.5
                      When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 5.5 then 2
                      When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 5 then 1.5
                      When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 4 then 1
                    else 0
                    end * subject.subject_credit)/sum(subject.subject_credit) as gpa
                from Student
                Join Major on Student.major_id = Major.major_id
                Join Class on Student.class_id = Class.class_id
                LEFT JOIN SUBJECT_STUDENT ON SUBJECT_STUDENT.student_id = Student.student_id
                LEFT JOIN SUBJECT ON SUBJECT.subject_id = Subject_Student.Subject_id
                Group by Student.student_id) as student_data
    		    Where student_data.{criteria} = %s
        """
        self.cursor.execute(query, (data,))
        students = self.cursor.fetchall()
        return students

    def get_student_by_id(self, student_id):
        query = """Select student_id, student_name, student_birth, student_address,
                    student_cccd,student_phone, student_email, student_gender,student_generation, 
                    student_image, Major.major_name, Class.class_name, Department.department_name 
                from Student 
                Join Major on Student.major_id = Major.major_id
                Join Class on Student.class_id = Class.class_id
                Join Department on Department.department_id = Class.department_id
                Where Student.student_id = %s"""
        self.cursor.execute(query, (student_id,))
        student = self.cursor.fetchone()
        return student

    def get_department_name(self):
        query = "Select department_name from Department"
        self.cursor.execute(query)
        department_name = self.cursor.fetchall()
        return department_name

    def get_class_name(self):
        query = "Select class_name from Class"
        self.cursor.execute(query)
        class_name = self.cursor.fetchall()
        return class_name

    def get_major_name(self):
        query = "Select major_name from Major"
        self.cursor.execute(query)
        major_name = self.cursor.fetchall()
        return major_name

    def get_student_name_by_id(self, tuple_student_id):
        cursor = self.connection.cursor()
        query = "SELECT student_name FROM Student WHERE student_id = %s"
        cursor.execute(query, tuple_student_id)
        student_name = cursor.fetchall()
        cursor.close()
        return student_name

    def get_student_by_cccd(self, tuple_student_cccd):
        cursor = self.connection.cursor()
        query = "SELECT student_name FROM Student WHERE student_cccd = %s"
        cursor.execute(query, tuple_student_cccd)
        student = cursor.fetchall()
        cursor.close()
        return student

    def get_student_by_email(self, tuple_student_email):
        cursor = self.connection.cursor()
        query = "SELECT student_name FROM Student WHERE student_email = %s"
        cursor.execute(query, tuple_student_email)
        student = cursor.fetchall()
        cursor.close()
        return student

    def get_subject_name_credit_by_id(self, tuple_subject_id):
        cursor = self.connection.cursor()
        query = "SELECT subject_name, subject_credit FROM Subject WHERE subject_id = %s"
        cursor.execute(query, tuple_subject_id)
        subject_name_credit = cursor.fetchall()
        cursor.close()
        return subject_name_credit

    def get_gpa(self):
        query = """ SELECT sum(
                    Case
                       When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 8.5 then 4
                       When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 8 then 3.5
                       When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 7 then 3
                       When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 6.5 then 2.5
                       When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 5.5 then 2
                       When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 5 then 1.5
                       When subject_student.score_regular*0.2 + subject_student.score_midterm *0.3+subject_student.score_final*0.5 >= 4 then 1
                    else 0 end *subject.subject_credit)/sum(subject.subject_credit) as gpa
                    from Student
                    LEFT JOIN subject_student on subject_student.student_id = student.student_id
                    LEFT JOIN subject on subject.subject_id = subject_student.subject_id
                    GROUP BY student.student_id
                """
        self.cursor.execute(query)
        gpa_each_student = self.cursor.fetchall()
        return gpa_each_student

    def get_id_by_name(self, table_name, name):
        cursor = self.connection.cursor()
        query = f"""Select {table_name}.{table_name}_id From {table_name} Where {table_name}_name = %s"""
        cursor.execute(query, (name,))
        table_id = cursor.fetchone()
        cursor.close()
        return table_id

    def get_subject_by_id_semester(self, tuple_id_semester):
        cursor = self.connection.cursor()
        query = """SELECT main.subject_id, main.subject_name, 
                        main.ss_semester,main.subject_credit,
                        main.score_regular, main.score_midterm, main.score_final,main.dtb,
                        Case
                           When main.dtb >= 8.5 then 'A'
                           When main.dtb >= 8.0 then 'B+'
                           When main.dtb >= 7.0 then 'B'
                           When main.dtb >= 6.5 then 'C+'
                           When main.dtb >= 5.5 then 'C'
                           When main.dtb >= 5 then 'D+'
                           When main.dtb >= 4 then 'D'
                        else 'F'
                        end as Xeploai
                    FROM (select student.student_id,subject.subject_id, subject.subject_name, 
                        subject.subject_credit,subject_student.ss_semester, subject_student.score_regular, 
                        subject_student.score_midterm, subject_student.score_final,
                        (subject_student.score_regular*0.2+ subject_student.score_midterm*0.3+ subject_student.score_final*0.5) as dtb
                            FROM Student
                            JOIN Subject_Student on Subject_Student.student_id = student.student_id
                            JOIN Subject on Subject.Subject_id = Subject_student.subject_id) as main
                    WHERE main.student_id = %s
            """
        if tuple_id_semester[1] == 'Tất cả':
            cursor.execute(query, (tuple_id_semester[0],))
        else:
            query += """ and main.ss_semester = %s; """
            cursor.execute(query, tuple_id_semester)
        subject = cursor.fetchall()
        cursor.close()
        return subject

    def add_student(self, tuple_student):
        cursor = self.connection.cursor()
        query = """INSERT INTO Student (student_id, student_name, student_birth, student_address,
                                        student_cccd, student_phone, student_email, student_gender,
                                        student_generation, student_image, class_id, major_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, tuple_student)
        self.connection.commit()
        cursor.close()

    def update_student(self, tuple_student):
        cursor = self.connection.cursor()
        query = """UPDATE Student SET student_name = %s, student_birth = %s, student_address = %s,
                           student_cccd = %s, student_phone = %s, student_email = %s, 
                           student_gender = %s, student_generation = %s, student_image = %s,
                           class_id = %s, major_id = %s
                WHERE student_id = %s"""
        cursor.execute(query, tuple_student)
        self.connection.commit()
        cursor.close()

    def delete_student(self, student_id):
        cursor = self.connection.cursor()
        query = """DELETE FROM Student WHERE student_id = %s"""
        cursor.execute(query, student_id)
        self.connection.commit()
        cursor.close()

    def get_id_subject(self):
        cursor = self.connection.cursor()
        query = """SELECT subject_id FROM Subject"""
        cursor.execute(query)
        subjects_id = cursor.fetchall()
        cursor.close()
        return subjects_id

    def add_subject_student(self, tuple_new_subject_student):
        cursor = self.connection.cursor()
        query = """INSERT INTO Subject_Student (subject_id, student_id, ss_semester,
                                               score_regular, score_midterm, score_final)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, tuple_new_subject_student)
        self.connection.commit()
        cursor.close()

    def get_subject_student(self, tuple_subject_student_semester):
        cursor = self.connection.cursor()
        query = """Select * from Subject_student
                   WHERE subject_id = %s
                   and student_id = %s
                   and ss_semester = %s;"""
        cursor.execute(query, tuple_subject_student_semester)
        result = cursor.fetchall()
        cursor.close()
        return result

    def update_subject_student(self, tuple_subject_student):
        cursor = self.connection.cursor()
        query = """UPDATE Subject_Student SET score_regular = %s, score_midterm = %s, score_final = %s
                   WHERE Subject_id = %s AND student_id = %s AND ss_semester = %s;
                """
        cursor.execute(query, tuple_subject_student)
        self.connection.commit()
        cursor.close()

    def delete_subject_student(self, tuple_subject_student):
        cursor = self.connection.cursor()
        query = """DELETE FROM Subject_Student WHERE subject_id = %s and student_id = %s and ss_semester = %s;"""
        cursor.execute(query, tuple_subject_student)
        self.connection.commit()
        cursor.close()

    def close(self):
        self.cursor.close()
        self.connection.close()