import cmd, sys
import tkinter as tk
from tkinter import filedialog

class CLI(cmd.Cmd ):

    
    intro = 'Welcome to  Beldens VNA interface. Type help of ? to list commands.'
    prompt = '(VNA)'

    def do_importSNP(self, arg):





if __name__ == '__main__':
    CLI().cmdloop()
