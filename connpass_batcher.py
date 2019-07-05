from tkinter import *
import insert_event

window = Tk()


def add_calendar():
    input_texts = input_text.get()
    valid_tests = input_texts.replace(' ', '').split(',')
    add_event_num = insert_event.insert_event(int(valid_tests[0]), str(valid_tests[1:]))
    if event_values:
        event_values.delete(1.0,END)
    event_values.insert(END, add_event_num) # ENDで一番最後に配置と定義している

window.title("好きなイベント一括で登録してくれるツール")

descreption = Label(text='日付と検索文字入力')
descreption.grid(row=0, column=0)

input_text = StringVar()
input_text = Entry(window, textvariable=input_text)
input_text.grid(row=0, column=1)

b1 = Button(window, text="カレンダーに登録", command=add_calendar)
b1.grid(row=0, column=2)

descreption = Label(text='カレンダー登録数')
descreption.grid(row=1, column=0)

event_values = Text(window,  height=1, width=20)
event_values.grid(row=1, column=1)


window.mainloop()
