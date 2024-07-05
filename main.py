from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

compiler = Tk()
compiler.iconbitmap("icon.ico")
compiler.title("Python IDE")
file_path = ''

def set_file_path(path):
    global file_path
    file_path = path

def open_file():
    path = askopenfilename(filetypes=[('Python File', '*.py')])
    if path:
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            set_file_path(path)

def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python File', '*.py')])
    else:
        path = file_path
    if path:
        with open(path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            set_file_path(path)

def run():
    if file_path == '':
        save_prompt = Toplevel()
        save_prompt.title("Save Code")
        save_prompt.iconbitmap("error.ico")

        message_frame = Frame(save_prompt, padx=20, pady=20)
        message_frame.pack()

        icon_label = Label(message_frame, image=None)
        icon_label.grid(row=0, column=0, padx=10)

        text_label = Label(message_frame, text="Please save your code before running.")
        text_label.grid(row=0, column=1, padx=10)

        return

    command = f'python "{file_path}"'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.delete('1.0', END)  # Clear previous output
    code_output.insert('1.0', output.decode('utf-8'))
    code_output.insert('1.0', error.decode('utf-8'))

def clear_output():
    code_output.delete('1.0', END)

def update_line_numbers(event=None):
    lines = editor.get('1.0', 'end').count('\n')
    line_numbers.config(state=NORMAL)
    line_numbers.delete('1.0', END)
    line_numbers.insert('1.0', '\n'.join(str(i) for i in range(1, lines+2)))
    line_numbers.config(state=DISABLED)

menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

editor_frame = Frame(compiler)
editor_frame.pack(fill=BOTH, expand=True, side=LEFT)

line_numbers = Text(editor_frame, width=4, padx=5, pady=5, wrap=NONE)
line_numbers.pack(side=LEFT, fill=Y)

editor_scroll = Scrollbar(editor_frame)
editor_scroll.pack(side=RIGHT, fill=Y)

editor = Text(editor_frame, wrap=NONE, undo=True, yscrollcommand=editor_scroll.set)
editor.pack(fill=BOTH, expand=True)

editor_scroll.config(command=editor.yview)

line_numbers.config(state=DISABLED)

editor.bind('<KeyRelease>', update_line_numbers)

output_frame = Frame(compiler)
output_frame.pack(side=RIGHT, fill=Y)

output_label = Label(output_frame, text="Output")
output_label.grid(row=0, column=0, sticky=W)

clear_button = Button(output_frame, text="Clear Output", command=clear_output)
clear_button.grid(row=0, column=1, sticky=E)

code_output = Text(output_frame, height=30, width=50)
code_output.grid(row=1, column=0, columnspan=2)

compiler.mainloop()
