import tkinter as tk
import tkinter.filedialog as filedialog
from pathlib import Path
from TempFile import TempFile
import os

class GUI():

    def __init__(self):
        self.root = tk.Tk()
        self.root_directory = None
        self.file_object = None
        self.file_path = None
        self.canvas_active = False

        self.py_xbm = r"@icons\py.xbm"
        self.dir_xbm = r"@icons\dir.xbm"

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

       #self.gridpane = tk.PanedWindow(self.root, showhandle = False, orient = tk.HORIZONTAL)
       #self.gridpane.grid(row = 1, column = 0, columnspan = 5)

        self.file_explorer = tk.Canvas(self.root, width = 150, height = 500, bg = 'white')
        
        self.text_editor = tk.Text(self.root, font = "fixedsys 12")
        
        self.text_editor.grid(row = 1, column = 0, sticky = tk.N + tk.E + tk.S + tk.W)
        self.file_explorer.grid(row = 1, column = 1)

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

        self.file_explorer.bind('<Button-1>', self.event_canvas)

    def open_optimizer(self, event, nope = None):
        '''
        Opens another Tkinter text window with the optimizer enabled.
        '''
        self.opt_root = tk.Tk()
        self.opt_text_editor = tk.Text(self.opt_root)
        self.opt_text_editor.pack()

        self.opt_root.mainloop()

    def init_file_explorer(self):
        '''
        Initial drawing of the file explorer, used when opening new projects or
        creating new ones.
        '''

        self.canvas_active = True
        
        drawlist_dirs = []
        drawlist_files = []

        self.pathlist = self.recursive_iterdir(self.root_directory)
        print(self.pathlist)
        #for item in pathlist:
        #    if item.isdir():
        #        drawlist_dirs.append(item)
        #    else: 
        #        drawlist_files.append(item)
        #
        #drawlist_dirs.sort(key = lambda x: x.name)
        #drawlist_files.sort(key = lambda x: x.name)

        #drawlist = drawlist_dirs.append(drawlist_files)
        counter = 0
        for item in self.pathlist:
            self.draw_item(item.name, item.is_dir(), counter, (len(item.parts) - len(self.root_directory.parts)) - 1)
            counter += 1

    def draw_item(self, name: str, isdir: bool, _index: int, indent_mult: int):
        print(isdir)
        indent_const = 10
        if isdir:
            print(6, (((500 / 20) / 500) * (1 + _index)) * 500)
            self.file_explorer.create_bitmap(18 + (indent_const * indent_mult), ((((500 / 20) / 500) * (1 + _index)) * 500) - 10, bitmap = self.dir_xbm)
            self.file_explorer.create_text(40 + (indent_const * indent_mult), ((((500 / 20) / 500) * (1 + _index)) * 500) - 10, text = name, anchor = tk.W)
        else:
            self.file_explorer.create_bitmap(18 + (indent_const * indent_mult), ((((500 / 20) / 500) * (1 + _index)) * 500) - 10, bitmap = self.py_xbm)
            self.file_explorer.create_text(40 + (indent_const * indent_mult), ((((500 / 20) / 500) * (1 + _index)) * 500) - 10, text = name, anchor = tk.W)
        

    def redraw_file_explorer(self):
        '''
        Redraws the file explorer canvas.
        '''
        self.file_explorer.delete(tk.ALL)
        
        self.pathlist = self.recursive_iterdir(self.root_directory)
        
        counter = 0
        for item in self.pathlist:
            self.draw_item(item.name, item.is_dir(), counter, (len(item.parts) - len(self.root_directory.parts)) - 1)
            counter += 1
           
    def recursive_iterdir(self, path_obj: Path):

        pathlist = []

        for item in path_obj.iterdir():
            if item.is_dir():
                pathlist.append(item)
                pathlist.extend(self.recursive_iterdir(item))
            else:
                pathlist.append(item)

        return pathlist

    def create_directories(self):
        '''
        Creates the directiories for the pseudocode and legal code.
        '''

        print("Output is", str(self.root_directory) / Path("OFiles"))

        if not (str(self.root_directory) / Path("OFiles")).exists() or \
        not (str(self.root_directory) / Path("AutoPy")).exists():

            try:
                os.mkdir(str(str(self.root_directory) / Path("OFiles")))
                os.mkdir(str(str(self.root_directory) / Path("AutoPy")))
            except:
                print("Didn't Work!")
            
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
        new_temp = TempFile(self.file_path.open('r'))
        new_temp.run()
        new_temp.writeTo(self.root_directory / Path('AutoPy') / self.file_path.name)        

    def event_canvas(self, event):
        '''
        Gets the input from canvas, decides whether to open a file or
        to expand or collapse directories.
        '''
        if not self.canvas_active:
            return

        loc_x, loc_y = event.x, event.y

        list_pos = int((loc_y / 500) // ((500 / 20) / 500))
        try:
            temp_path = self.pathlist[list_pos]
            if not temp_path.is_dir():
                self.event_save_as_file()
                self.event_open_file(canvas_path = temp_path)
        except IndexError:
            pass


    def event_new_file(self, event = None):
        '''
        Clear the text in the window, and ask the user for the root directory to
        display in the file explorer.
        '''
        self.text_editor.delete('1.0', tk.END)
        self.root_directory = Path(filedialog.askdirectory())

        print(str(self.root_directory))
        self.create_directories()
        self.init_file_explorer()

        self.root.wm_title(str(self.root_directory) + ", No file open yet.")

    def event_open_file(self, event = None, canvas_path = None):
        if canvas_path == None:
            self.text_editor.delete('1.0', tk.END)
            self.file_object = filedialog.askopenfile(defaultextension = '.py', filetypes = [('Python files', '.py'), ('all files', '.*')])
            if self.file_object == None:
                return
            self.text_editor.insert(tk.END, self.file_object.read())
            self.file_path = Path(self.file_object.name)
            self.file_object.close()

            self.init_file_explorer()

        else:
            self.text_editor.delete('1.0', tk.END)
            self.file_path = canvas_path
            self.file_object =  canvas_path.open('r')
            self.text_editor.insert(tk.END, self.file_object.read())

            self.file_object.close()
            self.redraw_file_explorer()
            
        self.root.wm_title(str(self.root_directory) + ", " + str(self.file_path))

    def event_save_file(self, event = None):
        '''
        Attempts to save a file with the current filename.
        If file is not saved yet, prompt user for filename.
        '''
        if self.file_object == None:
            self.event_save_as_file()
        else:
            self.file_object = self.file_path.open('w')
            self.file_object.write(self.text_editor.get("1.0", tk.END))
            self.file_object.flush()
            self.file_object.close()

    def event_save_as_file(self, event = None):
        '''
        Prompts the user for a save destination and file name
        and saves the file.
        '''
        self.file_object = tk.filedialog.asksaveasfile(defaultextension = '.py', filetypes = [('Python files', '.py'), ('all files', '.*')])
        if self.file_object == None:
            print('Broke the loop...')
            return
        self.file_object.write(self.text_editor.get("1.0", tk.END))
        self.file_object.flush()
        self.file_object.close()

    # -------- Mainloop ---------

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    new_gui = GUI()
    new_gui.mainloop()