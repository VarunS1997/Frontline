import tkinter as tk
import tkinter.filedialog as filedialog
from pathlib import Path

class GUI():

    def __init__(self):
        self.root = tk.Tk()
        self.root_directory = None
        self.file_object = None
        self.generate_elements()


    def generate_elements(self):

        self.root.rowconfigure(1, weight = 1)

        self.file_dropdown = tk.Menubutton(self.root, text = 'File')
        self.file_dropdown.grid(row = 0, column = 0, sticky = tk.W)

        self.file_dropdown.menu = tk.Menu(self.file_dropdown, tearoff = 0)
        self.file_dropdown['menu'] = self.file_dropdown.menu

        self.file_dropdown.menu.add_command(label = 'New      Ctrl + N', command = self.event_new_file)
        self.file_dropdown.menu.add_command(label = 'Open     Ctrl + O', command = self.event_open_file)
        self.file_dropdown.menu.add_command(label = 'Save     Ctrl + S', command = self.event_save_file)
        self.file_dropdown.menu.add_command(label = 'Save As', command = self.event_save_as_file)
        self.file_dropdown.menu.add_command(label = 'Exit       Escape', command = self.event_exit)

        self.program_dropdown = tk.Menubutton(self.root, text = 'Program')
        self.program_dropdown.grid(row = 0, column = 1, sticky = tk.W)

        self.program_dropdown.menu = tk.Menu(self.program_dropdown, tearoff = 0)
        self.program_dropdown['menu'] = self.program_dropdown.menu

        self.program_dropdown.menu.add_command(label = 'Execute    F5', command = self.event_execute)

        self.gridpane = tk.PanedWindow(self.root, showhandle = False, orient = tk.HORIZONTAL)
        self.gridpane.grid(row = 1, column = 0, columnspan = 10)

        self.file_explorer = tk.Canvas(self.gridpane, width = 150, height = 500, image = None)
        self.gridpane.add(self.file_explorer)

        self.text_editor = tk.Text(self.gridpane, font = "fixedsys 12")
        self.gridpane.add(self.text_editor)

        self.root.bind('<Escape>', self.event_exit)
        self.root.bind('<Control-n>', self.event_new_file)
        self.root.bind('<Control-N>', self.event_new_file)
        self.root.bind('<Control-o>', self.event_open_file)
        self.root.bind('<Control-O>', self.event_open_file)
        self.root.bind('<Control-s>', self.event_save_file)
        self.root.bind('<Control-S>', self.event_save_file)
        self.root.bind('<Control-b>', self.open_optimizer)
        self.root.bind('<Control-B>', self.open_optimizer)
        self.root.bind('<F5>', self.event_execute)

    def open_optimizer(self, event, nope = None):
        '''
        Opens another Tkinter text window with the optimizer enabled.
        '''
        print("Hi")
        self.opt_root = tk.Tk()
        self.opt_text_editor = tk.Text(self.opt_root)
        self.opt_text_editor.pack()

        self.opt_root.mainloop()


    def redraw_file_explorer(self):
        '''
        Redraws the file explorer canvas.
        '''
        self.file_explorer.delete(tk.ALL)


    # ----------   FILE I/O   -----------
    def event_exit(self, event = None):
        '''
        Closes the file object and the program.
        '''
        try:
            self.file_object.close()
        finally:
            exit()

    def event_execute(self, event = None):
        pass

    def event_new_file(self, event = None):
        self.text_editor.delete('1.0', tk.END)

    def event_open_file(self, event = None):
        self.text_editor.delete('1.0', tk.END)
        the_file = filedialog.askopenfile()
        if the_file == None:
            return
        self.text_editor.insert('1.0', the_file.read())

        the_file.close()

    def event_save_file(self, event = None):
        '''
        Attempts to save a file with the current filename.
        If file is not saved yet, prompt user for filename.
        '''
        if self.file_object == None:
            self.file_object = tk.filedialog.asksaveasfile()
            if self.file_object == None:
                return
            self.file_object.write(self.text_editor.get("1.0", "end-1c"))
            self.file_object.flush()
        else:
            self.file_object.flush()

    def event_save_as_file(self, event = None):
        '''
        Prompts the user for a save destination and file name
        and saves the file.
        '''
        self.file_object = tk.filedialog.asksaveasfile()
        if self.file_object == None:
            return
        self.file_object.write(self.text_editor.get("1.0", "end-1c"))
        self.file_object.flush()

    # -------- Mainloop ---------

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    new_gui = GUI()
    new_gui.mainloop()