from database import ExamController
import PySimpleGUI as Gui

layout = [
    [Gui.Text(" " * 20 + "Add Exam Controller", size=(70, 3))],
    [Gui.Text("Name      :"), Gui.InputText(size=(30, 0))],
    [Gui.Text("Password:"), Gui.InputText(size=(30, 0))],
    [Gui.Text("Confirm Password")],
    [Gui.Text("Password:"), Gui.InputText(size=(30, 0))],
    [Gui.Text("", size=(70, 4))],
    [Gui.Button("Cancel"), Gui.Text("", size=(20, 0)), Gui.Button("Add Exam Controller")]
]


def add_exam_controller():
    while True:
        win = Gui.Window("Add Exam Controller")
        win.Layout(layout)
        b, values = win.Read()
        if b == 'Cancel' or b is None:
            win.Disappear()
            break
        elif b == 'Add Exam Controller':
            name = values[0]
            pw = values[1]
            pw1 = values[2]
            if name == "":
                Gui.Popup("Name is empty!")
            elif pw == "":
                Gui.Popup("Password is empty!")
            elif pw != pw1:
                Gui.Popup("Password doesnt match!")
            else:
                e = ExamController()
                if e.signup(name, pw):
                    Gui.Popup("Exam Controller successfully added!")
                else:
                    Gui.Popup("Username already exists")


if __name__ == '__main__':
    add_exam_controller()
