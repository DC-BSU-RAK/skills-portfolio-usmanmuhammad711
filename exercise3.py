
import os
import csv
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog

# === Set your data file name here ===
DATA_PATH = os.path.join(os.path.dirname(__file__), 'student_data.txt')   # if file is in same folder as script 

# ---------- Data handling ----------

def ensure_data_file(path=DATA_PATH):
    """
    Ensure the file exists. If a directory is part of the path, create that directory.
    If path has no directory (file in same folder), do not attempt to create directories.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    if not os.path.exists(path):
        # create empty file with count 0
        with open(path, 'w', newline='') as f:
            f.write('0\n')


def load_students(path=DATA_PATH):
    """Return list of student dicts: [{'id':int,'name':str,'cw1':int,'cw2':int,'cw3':int,'exam':int}]"""
    ensure_data_file(path)
    students = []
    with open(path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]
    if not rows:
        return []
    # If first row is a single integer, skip it
    first = rows[0]
    start = 0
    if len(first) == 1 and first[0].strip().isdigit():
        # count present
        start = 1
    for row in rows[start:]:
        # handle rows with spaces
        row = [cell.strip() for cell in row]
        if len(row) < 6:
            continue
        try:
            sid = int(row[0])
            name = row[1]
            cw1 = int(row[2])
            cw2 = int(row[3])
            cw3 = int(row[4])
            exam = int(row[5])
            students.append({'id': sid, 'name': name, 'cw1': cw1, 'cw2': cw2, 'cw3': cw3, 'exam': exam})
        except ValueError:
            # skip malformed
            continue
    return students


def save_students(students, path=DATA_PATH):
    """
    Save students to file. If path contains directory, create it; if not, write to same folder.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        # write count first
        writer.writerow([len(students)])
        for s in students:
            writer.writerow([s['id'], s['name'], s['cw1'], s['cw2'], s['cw3'], s['exam']])


# ---------- Business logic ----------

POTENTIAL_TOTAL = 160.0  # 60 coursework (3x20) + 100 exam


def coursework_total(s):
    return s['cw1'] + s['cw2'] + s['cw3']


def overall_percentage(s):
    total = coursework_total(s) + s['exam']
    return (total / POTENTIAL_TOTAL) * 100.0


def grade_from_pct(pct):
    if pct >= 70:
        return 'A'
    if pct >= 60:
        return 'B'
    if pct >= 50:
        return 'C'
    if pct >= 40:
        return 'D'
    return 'F'


# ---------- GUI ----------

class StudentManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Student Manager')
        self.geometry('900x600')

        self.students = load_students()

        # Menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        student_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Students', menu=student_menu)
        student_menu.add_command(label='View all records', command=self.view_all)
        student_menu.add_command(label='View individual record', command=self.view_individual)
        student_menu.add_separator()
        student_menu.add_command(label='Show highest overall', command=self.show_highest)
        student_menu.add_command(label='Show lowest overall', command=self.show_lowest)
        student_menu.add_separator()
        student_menu.add_command(label='Sort records', command=self.sort_records)
        student_menu.add_command(label='Add a student', command=self.add_student)
        student_menu.add_command(label='Delete a student', command=self.delete_student)
        student_menu.add_command(label='Update a student', command=self.update_student)
        student_menu.add_separator()
        student_menu.add_command(label='Reload from file', command=self.reload_data)
        student_menu.add_command(label='Save to file', command=self.save_data)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open data file...', command=self.open_data_file)
        file_menu.add_command(label='Exit', command=self.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About', command=self.show_about)

        # Text display
        self.text = tk.Text(self, wrap='none')
        self.text.pack(fill='both', expand=True)

        # Add simple scrollbar pairs
        xscroll = ttk.Scrollbar(self, orient='horizontal', command=self.text.xview)
        xscroll.pack(side='bottom', fill='x')
        yscroll = ttk.Scrollbar(self, orient='vertical', command=self.text.yview)
        yscroll.pack(side='right', fill='y')
        self.text.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

        # Status bar
        self.status = tk.StringVar()
        self.status.set(f'{len(self.students)} student(s) loaded')
        statusbar = ttk.Label(self, textvariable=self.status, anchor='w')
        statusbar.pack(side='bottom', fill='x')

    # ---------- UI helpers ----------
    def clear_text(self):
        self.text.delete('1.0', tk.END)

    def append(self, s=''):
        self.text.insert(tk.END, s + '\n')

    def reload_data(self):
        self.students = load_students()
        self.status.set(f'{len(self.students)} student(s) loaded')
        messagebox.showinfo('Reload', 'Data reloaded from file.')

    def save_data(self):
        save_students(self.students)
        self.status.set(f'{len(self.students)} student(s) saved')
        messagebox.showinfo('Save', f'Data saved to {DATA_PATH}')

    def open_data_file(self):
        path = filedialog.askopenfilename(title='Open student data', filetypes=[('Text files', '*.txt'), ('CSV', '*.csv'), ('All files','*.*')])
        if path:
            global DATA_PATH
            DATA_PATH = path
            # ensure the selected file exists (and its parent folder if given)
            ensure_data_file(DATA_PATH)
            self.reload_data()

    def show_about(self):
        messagebox.showinfo('About', 'Student Manager\nTkinter example\nImplements required features and file persistence')

    # ---------- Formatting ----------
    def student_header(self, s):
        self.append('Student Name: ' + s['name'])
        self.append('Student Number: ' + str(s['id']))
        self.append('Total coursework mark: ' + str(coursework_total(s)) + ' / 60')
        self.append('Exam Mark: ' + str(s['exam']) + ' / 100')
        pct = overall_percentage(s)
        self.append('Overall percentage: ' + f'{pct:.2f}%')
        self.append('Grade: ' + grade_from_pct(pct))
        self.append('')

    # ---------- Menu operations ----------
    def view_all(self):
        self.clear_text()
        if not self.students:
            self.append('No student records available.')
            return
        total_pct = 0.0
        for s in self.students:
            self.student_header(s)
            total_pct += overall_percentage(s)
        avg = total_pct / len(self.students)
        self.append('--- Summary ---')
        self.append(f'Number of students: {len(self.students)}')
        self.append(f'Average percentage: {avg:.2f}%')
        self.status.set(f'Viewing all {len(self.students)} students')

    def find_student_by_id(self, sid):
        for s in self.students:
            if s['id'] == sid:
                return s
        return None

    def find_students_by_name(self, name):
        return [s for s in self.students if name.lower() in s['name'].lower()]

    def view_individual(self):
        if not self.students:
            messagebox.showwarning('No data', 'No students loaded')
            return
        mode = simpledialog.askstring('Select', 'Enter student number OR part of name:')
        if mode is None or mode.strip() == '':
            return
        mode = mode.strip()
        # try id
        try:
            sid = int(mode)
            s = self.find_student_by_id(sid)
            if not s:
                messagebox.showinfo('Not found', f'No student with number {sid}')
                return
            self.clear_text()
            self.student_header(s)
            self.status.set(f'Viewing student {s["id"]}')
            return
        except ValueError:
            # treat as name search
            matches = self.find_students_by_name(mode)
            if not matches:
                messagebox.showinfo('Not found', 'No students matching that name')
                return
            if len(matches) == 1:
                self.clear_text()
                self.student_header(matches[0])
                self.status.set(f'Viewing student {matches[0]["id"]}')
                return
            # multiple matches - show list and let user choose
            choice = self.choose_from_list([f"{m['id']} - {m['name']}" for m in matches], title='Choose student')
            if choice is None:
                return
            idx = choice
            s = matches[idx]
            self.clear_text()
            self.student_header(s)
            self.status.set(f'Viewing student {s["id"]}')

    def choose_from_list(self, items, title='Choose'):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.grab_set()
        tk.Label(dialog, text='Select:').pack(padx=10, pady=5)
        lb = tk.Listbox(dialog, width=60, height=10)
        lb.pack(padx=10, pady=5)
        for it in items:
            lb.insert(tk.END, it)
        result = {'idx': None}

        def on_ok():
            sel = lb.curselection()
            if not sel:
                messagebox.showwarning('Select', 'Please select an item')
                return
            result['idx'] = sel[0]
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        btns = tk.Frame(dialog)
        btns.pack(pady=5)
        ttk.Button(btns, text='OK', command=on_ok).pack(side='left', padx=5)
        ttk.Button(btns, text='Cancel', command=on_cancel).pack(side='left', padx=5)
        self.wait_window(dialog)
        return result['idx']

    def show_highest(self):
        if not self.students:
            messagebox.showwarning('No data', 'No students loaded')
            return
        best = max(self.students, key=lambda s: overall_percentage(s))
        self.clear_text()
        self.append('--- Highest overall mark ---')
        self.student_header(best)
        self.status.set(f'Highest: {best["id"]} - {best["name"]}')

    def show_lowest(self):
        if not self.students:
            messagebox.showwarning('No data', 'No students loaded')
            return
        worst = min(self.students, key=lambda s: overall_percentage(s))
        self.clear_text()
        self.append('--- Lowest overall mark ---')
        self.student_header(worst)
        self.status.set(f'Lowest: {worst["id"]} - {worst["name"]}')

    def sort_records(self):
        if not self.students:
            messagebox.showwarning('No data', 'No students loaded')
            return
        choice = simpledialog.askstring('Sort', 'Enter A for ascending or D for descending:')
        if choice is None:
            return
        choice = choice.strip().upper()
        if choice not in ('A', 'D'):
            messagebox.showerror('Bad input', 'Please enter A or D')
            return
        reverse = (choice == 'D')
        self.students.sort(key=lambda s: overall_percentage(s), reverse=reverse)
        self.view_all()
        self.status.set(f'Students sorted ({"descending" if reverse else "ascending"})')

    def add_student(self):
        dialog = StudentEditDialog(self, title='Add a student')
        self.wait_window(dialog)
        if dialog.result:
            s = dialog.result
            # check uniqueness of id
            if any(st['id'] == s['id'] for st in self.students):
                messagebox.showerror('Duplicate', 'A student with that ID already exists')
                return
            self.students.append(s)
            save_students(self.students)
            self.status.set(f'Student {s["id"]} added')
            messagebox.showinfo('Added', f'Student {s["id"]} added and saved')

    def delete_student(self):
        if not self.students:
            messagebox.showwarning('No data', 'No students loaded')
            return
        mode = simpledialog.askstring('Delete', 'Enter student number OR part of name to delete:')
        if mode is None or mode.strip() == '':
            return
        mode = mode.strip()
        # try id
        try:
            sid = int(mode)
            s = self.find_student_by_id(sid)
            if not s:
                messagebox.showinfo('Not found', f'No student with number {sid}')
                return
            if messagebox.askyesno('Confirm', f'Delete {s["id"]} - {s["name"]}?'):
                self.students = [st for st in self.students if st['id'] != sid]
                save_students(self.students)
                self.status.set(f'Student {sid} deleted')
                messagebox.showinfo('Deleted', 'Student deleted and file updated')
            return
        except ValueError:
            matches = self.find_students_by_name(mode)
            if not matches:
                messagebox.showinfo('Not found', 'No students matching that name')
                return
            if len(matches) == 1:
                s = matches[0]
                if messagebox.askyesno('Confirm', f'Delete {s["id"]} - {s["name"]}?'):
                    self.students = [st for st in self.students if st['id'] != s['id']]
                    save_students(self.students)
                    self.status.set(f'Student {s["id"]} deleted')
                    messagebox.showinfo('Deleted', 'Student deleted and file updated')
                return
            choice = self.choose_from_list([f"{m['id']} - {m['name']}" for m in matches], title='Choose student to delete')
            if choice is None:
                return
            s = matches[choice]
            if messagebox.askyesno('Confirm', f'Delete {s["id"]} - {s["name"]}?'):
                self.students = [st for st in self.students if st['id'] != s['id']]
                save_students(self.students)
                self.status.set(f'Student {s["id"]} deleted')
                messagebox.showinfo('Deleted', 'Student deleted and file updated')

    def update_student(self):
        if not self.students:
            messagebox.showwarning('No data', 'No students loaded')
            return
        mode = simpledialog.askstring('Update', 'Enter student number OR part of name to update:')
        if mode is None or mode.strip() == '':
            return
        mode = mode.strip()
        try:
            sid = int(mode)
            s = self.find_student_by_id(sid)
            if not s:
                messagebox.showinfo('Not found', f'No student with number {sid}')
                return
            dialog = StudentEditDialog(self, student=s, title='Update student')
            self.wait_window(dialog)
            if dialog.result:
                new = dialog.result
                # replace
                for i,st in enumerate(self.students):
                    if st['id'] == sid:
                        self.students[i] = new
                        break
                save_students(self.students)
                self.status.set(f'Student {new["id"]} updated')
                messagebox.showinfo('Updated', 'Student updated and file saved')
            return
        except ValueError:
            matches = self.find_students_by_name(mode)
            if not matches:
                messagebox.showinfo('Not found', 'No students matching that name')
                return
            if len(matches) == 1:
                s = matches[0]
                dialog = StudentEditDialog(self, student=s, title='Update student')
                self.wait_window(dialog)
                if dialog.result:
                    new = dialog.result
                    for i,st in enumerate(self.students):
                        if st['id'] == s['id']:
                            self.students[i] = new
                            break
                    save_students(self.students)
                    self.status.set(f'Student {new["id"]} updated')
                    messagebox.showinfo('Updated', 'Student updated and file saved')
                return
            choice = self.choose_from_list([f"{m['id']} - {m['name']}" for m in matches], title='Choose student to update')
            if choice is None:
                return
            s = matches[choice]
            dialog = StudentEditDialog(self, student=s, title='Update student')
            self.wait_window(dialog)
            if dialog.result:
                new = dialog.result
                for i,st in enumerate(self.students):
                    if st['id'] == s['id']:
                        self.students[i] = new
                        break
                save_students(self.students)
                self.status.set(f'Student {new["id"]} updated')
                messagebox.showinfo('Updated', 'Student updated and file saved')


class StudentEditDialog(tk.Toplevel):
    def __init__(self, parent, student=None, title='Edit'):
        super().__init__(parent)
        self.title(title)
        self.grab_set()
        self.result = None

        # fields
        tk.Label(self, text='Student ID (1000-9999):').grid(row=0, column=0, sticky='e', padx=4, pady=4)
        self.e_id = tk.Entry(self)
        self.e_id.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(self, text='Name:').grid(row=1, column=0, sticky='e', padx=4, pady=4)
        self.e_name = tk.Entry(self, width=40)
        self.e_name.grid(row=1, column=1, padx=4, pady=4)

        tk.Label(self, text='Coursework mark 1 (0-20):').grid(row=2, column=0, sticky='e', padx=4, pady=4)
        self.e_cw1 = tk.Entry(self)
        self.e_cw1.grid(row=2, column=1, padx=4, pady=4)

        tk.Label(self, text='Coursework mark 2 (0-20):').grid(row=3, column=0, sticky='e', padx=4, pady=4)
        self.e_cw2 = tk.Entry(self)
        self.e_cw2.grid(row=3, column=1, padx=4, pady=4)

        tk.Label(self, text='Coursework mark 3 (0-20):').grid(row=4, column=0, sticky='e', padx=4, pady=4)
        self.e_cw3 = tk.Entry(self)
        self.e_cw3.grid(row=4, column=1, padx=4, pady=4)

        tk.Label(self, text='Exam mark (0-100):').grid(row=5, column=0, sticky='e', padx=4, pady=4)
        self.e_exam = tk.Entry(self)
        self.e_exam.grid(row=5, column=1, padx=4, pady=4)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text='OK', command=self.on_ok).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Cancel', command=self.on_cancel).pack(side='left', padx=5)

        if student:
            self.e_id.insert(0, str(student['id']))
            self.e_name.insert(0, student['name'])
            self.e_cw1.insert(0, str(student['cw1']))
            self.e_cw2.insert(0, str(student['cw2']))
            self.e_cw3.insert(0, str(student['cw3']))
            self.e_exam.insert(0, str(student['exam']))

    def on_ok(self):
        try:
            sid = int(self.e_id.get())
            if not (1000 <= sid <= 9999):
                raise ValueError('ID out of range')
            name = self.e_name.get().strip()
            if not name:
                raise ValueError('Name required')
            cw1 = int(self.e_cw1.get())
            cw2 = int(self.e_cw2.get())
            cw3 = int(self.e_cw3.get())
            for cw in (cw1, cw2, cw3):
                if not (0 <= cw <= 20):
                    raise ValueError('Coursework out of range')
            exam = int(self.e_exam.get())
            if not (0 <= exam <= 100):
                raise ValueError('Exam out of range')
            self.result = {'id': sid, 'name': name, 'cw1': cw1, 'cw2': cw2, 'cw3': cw3, 'exam': exam}
            self.destroy()
        except ValueError as e:
            messagebox.showerror('Invalid', f'Invalid input: {e}')

    def on_cancel(self):
        self.destroy()


if __name__ == '__main__':
    app = StudentManagerApp()
    app.mainloop()
