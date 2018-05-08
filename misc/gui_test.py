from Tkinter import *

from PIL import Image, ImageTk

class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):

        self.master.title("GUI")
        self.pack(fill=BOTH, expand = 1)

        menu = Menu(self.master)
        self.master.config(menu = menu)

        file = Menu(menu)

        file.add_command(label = "Exit", command=self.client_exit)

        menu.add_cascade(label = "File", menu=file)

        edit = Menu(menu)

        menu.add_cascade(label="Edit", menu = edit)

        edit.add_command(label="Show Img", command=self.ShowImg)
        edit.add_command(label="Show Text", command=self.ShowText)

        edit.add_command(label = "Undo")

        
        quitButton = Button(self, text="Quit",command=self.client_exit)
        quitButton.place(x=0,y=0)

    def ShowImg(self):
        load = Image.open("py.png")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image = render)
        img.image = render
        img.place(x=20, y=20)

    def ShowText(self):
        text = Label(self, text="Hi Liam")
        text.pack()



    def client_exit(self):
        exit()
        


root = Tk()
root.geometry("400x300")

app = Window(root)

root.mainloop()
        
