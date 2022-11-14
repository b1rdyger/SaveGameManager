import os
import subprocess
import threading
import tkinter as tk
from datetime import datetime
from tkinter import Menu, ttk, DISABLED, NORMAL
from tkinter import N, S, W, E
from tkinter.ttk import Scrollbar
from tkcalendar import Calendar

from PIL import ImageTk, Image

from app import Engine
from app.SGMEvents.MFSEvents import *
from app.SGMEvents.PCEvents import PCRunning
from app.widgets.ConsoleOutput import ConsoleOutput


class SaveGameWindow:
    frame_bg = '#ddd'
    game_running = False
    last_state = None
    window = None
    def ram_drive_mounted(self):
        self._memory_save_game.configure(bg='lime')

    def ram_drive_unmounted(self):
        self._memory_save_game.configure(bg='#c2d5e6')

    def process_checker(self, *state):
        self.game_running = state
        if self.last_state == state:
            return
        if state:
            self.frame_game.configure(background='lime')
            self.btn_start_game.configure(state=DISABLED)
        else:
            self.frame_game.configure(background='red')
            self.btn_start_game.configure(state=NORMAL)
        self.last_state = state

    def __init__(self, engine: Engine):
        # setup vars
        self.logoff_bool = False
        self.logoff_timer = None
        self.engine = engine
        self.config = self.engine.config
        self.event_bus = self.engine.event_bus
        self.root_dir = self.engine.root_dir
        self.asset_dir = f'{self.root_dir}assets{os.sep}'

        # start
        self.root = tk.Tk()
        self.root.geometry('732x382')
        self.root.title('Savegame Manager')
        self.root.iconphoto(False, tk.PhotoImage(file=f'{self.asset_dir}logo{os.sep}disk1-256.png'))
        self.width, self.height = self.root.winfo_width(), self.root.winfo_height()
        # setup layout
        self.generate_menu()
        self.configure_grid_weights()

        # events
        self.event_bus.add_listener(MFSSymlinkCreated, self.ram_drive_mounted)
        self.event_bus.add_listener(MFSSymlinkRemoved, self.ram_drive_unmounted)
        self.event_bus.add_listener(PCRunning, self.process_checker)
        self.root.protocol("WM_DELETE_WINDOW", lambda: threading.Thread(target=self.on_closing, daemon=True).start())

        # self.root.resizable(False, False)
        # self.root.protocol("WM_DELETE_WINDOW", self.root.iconify)
        # logo = ImageTk.PhotoImage(file=self.asset_dir + 'dsp_logo_rel32.png')
        self._generate_frame_game(None)
        self._generate_buttons()
        frame_disks_game = tk.Frame(self.root, bg=self.frame_bg, height=100, padx=3, pady=2)
        frame_disks_game.grid(row=1, column=0, sticky=N+S+E+W, padx=2, pady=2)
        frame_disks_game.columnconfigure(0, weight=0)
        frame_disks_game.columnconfigure(1, weight=1)

        label_arrow = tk.Canvas(frame_disks_game, bg=self.frame_bg, bd=0, highlightthickness=0, width=32, height=32)
        icon_game = ImageTk.PhotoImage(Image.open(f'{self.asset_dir}arrow_right.png'))
        label_arrow.create_image(0, 0, image=icon_game, anchor=N+W)
        label_arrow.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)

        default_save_game = tk.Label(frame_disks_game, text='default save-path', bg='#c2d5e6', borderwidth=2,
                                     relief='solid', padx=6, pady=4, anchor=W)
        default_save_game.grid(row=0, column=1, sticky=N+E+W, padx=4, pady=4)
        self._memory_save_game = tk.Label(frame_disks_game, text='RAM-disk', bg='#c2d5e6', borderwidth=2,
                                          relief='solid', padx=6, pady=4, anchor=W)
        self._memory_save_game.grid(row=1, column=1, sticky=N+E+W, padx=4, pady=4)

        frame_disks_others = tk.Frame(self.root, bg=self.frame_bg, padx=3, pady=2)
        frame_disks_others.grid(row=1, column=1, sticky=N+S+E+W, ipadx=2, ipady=1, padx=2, pady=2)

        _frame_log = tk.Frame(self.root, bg=self.frame_bg, padx=3, pady=2)
        _frame_log.grid(row=2, column=0, columnspan=2, sticky=N+S+E+W, ipadx=2, ipady=1, padx=2, pady=2)

        self.text_log = ConsoleOutput(self.root_dir, self.event_bus, _frame_log)
        self.text_log.pack(expand=True, fill='both')
        scroll = Scrollbar(_frame_log, command=self.text_log.yview)
        self.text_log.configure(yscrollcommand=scroll.set)
        self.root.bind("<Configure>", self.resize)

        # btn_start = tk.Button(self.root, text='Start Game', bd=2, command=self.root.destroy, bg='red')

        # running
        self.engine.set_write_callback(self.text_log)
        cu1 = threading.Thread(target=self.engine.main_runner, daemon=True)
        cu1.start()

        self.root.mainloop()
        self.event_bus.remove_all_listener()
        cu1.join()

    def on_closing(self):
        self.engine.stop()
        self.root.destroy()

    def start_dsp(self):
        subprocess.Popen(rf"{self.config.get('steam_path')} -applaunch 1366540")

    def _generate_frame_game(self, logo):
        self.frame_game = tk.Frame(self.root, bg=self.frame_bg, height=80, padx=3, pady=2)
        self.frame_game.grid(row=0, column=0, columnspan=2, sticky=N + S + E + W, padx=2, pady=2)
        self.frame_game.rowconfigure(0, weight=0, minsize=40)
        self.frame_game.rowconfigure(1, weight=0, minsize=40)
        self.frame_game.columnconfigure(0, weight=1)
        self.frame_game.columnconfigure(1, weight=0)


    def _generate_buttons(self):
        #Buttons
        self.btn_start_game = ttk.Button(self.frame_game, text='Start Game!', command=lambda: self.start_dsp())
        self.btn_logofftimer_pc = ttk.Button(self.frame_game, text='Logofftimer', command=self.logofftimer)
        self.btn_change_game = ttk.Button(self.frame_game, text='Exit!',
                                     command=lambda: threading.Thread(target=self.on_closing, daemon=True).start())

        #Grid them
        self.btn_start_game.grid(row=0, column=1, sticky=N + S + E + W, ipadx=3, ipady=3)
        self.btn_logofftimer_pc.grid(row=0, column=2, sticky=N + S + E + W, ipadx=3, ipady=3)
        self.btn_change_game.grid(row=0, column=3, sticky=N + S + E + W, ipadx=3, ipady=3)

# label_profile = tk.Label(frame_game, text='Dyson Sphere Program', compound='left', image=logo,
        #                          anchor=W, justify=LEFT)
        # label_profile.grid(row=0, column=0, sticky=W)

    def configure_grid_weights(self):
        self.root.columnconfigure(0, weight=1, uniform='fifthly')
        self.root.columnconfigure(1, weight=1, uniform='fifthly')
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=1)

    def resize(self, event):
        if (event.widget == self.root and
                (self.width != event.width or self.height != event.height)):
            self.text_log.update_screen()
            self.width, self.height = event.width, event.height

    def logofftimer(self):
        self.text_log.write('Logofftimer was clicked')
        self.create_logoff_window()

    def create_logoff_window(self):
        """
        @TODO Implent logoff function
        """
        self.window = tk.Toplevel(self.root)
        self.window.title('Logofftimer')
        self.window.geometry('350x275')
        self.window.resizable(False, False)
        def set_logoff():
            self.logoff_bool = True
            self.text_log.write(f'Timer auf "{self.logoff_timer}" gesetzt')
            self.window.forget(self.window)
        def create_logoff_window_my_upd(*args):
            dt=self.cal.get_date()    # collect the selected date as string
            if (len(dt)>5):
                dt = f"{dt}:{str(self.hr.get())},{str(self.mn.get())},00"
                self.logoff_timer=datetime.strptime(dt,'%m/%d/%y:%H,%M,%S')
                self.view_logofftime=self.logoff_timer.strftime("%d.%B %H:%M") # display format
                self.l1.config(text=self.view_logofftime)#Not used yet

        self.sel=tk.StringVar()
        self.cal=Calendar(self.window,selectmode='day')
        self.cal.grid(row=0, column=0, sticky=N + S + E + W, ipadx=3, ipady=3)
        l_hr= tk.Label(self.window,text='Hour')
        self.hr = tk.Scale(self.window, from_=0, to=23, orient='vertical',length=150,command=create_logoff_window_my_upd)
        self.hr.grid(row=0, column=1, sticky=N + S + E + W, ipadx=3, ipady=3)
        self.mn = tk.Scale(self.window, from_=0, to=59, orient='vertical',length=150,command=create_logoff_window_my_upd)
        self.mn.grid(row=0 ,column=2, sticky=N + S + E + W, ipadx=3, ipady=3)
        self.l1=tk.Label(self.window,font=('Times', 16,'normal'))# show date
        self.l1.grid(row=1, column=0, sticky=N + S + E  + W, ipadx=3, ipady=3, columnspan=1)
        l_hr.grid(row=1, column=1, sticky=N + S + E + W, ipadx=3, ipady=3)
        l_mn=tk.Label(self.window,text='Mintue')
        l_mn.grid(row=1, column=2, sticky=N + S + E + W, ipadx=3, ipady=3)

        self.sel.trace('w', create_logoff_window_my_upd) # on change of string variable
        create_logoff_window_my_upd() # Show the date and time while opening
        self.btn_set_timer = ttk.Button(self.window, text='set Timer', command=set_logoff)
        self.btn_set_timer.grid(row=2, column=0, sticky=N + S + E + W, ipadx=3, ipady=3, columnspan=4)



    def generate_menu(self):
            menubar = Menu(self.root)
            self.root.config(menu=menubar)
            file_menu = Menu(
                menubar,
                tearoff=0
            )
            file_menu.add_command(label='New')
            file_menu.add_command(label='Open...')
            file_menu.add_command(label='Close')
            file_menu.add_separator()
            file_menu.add_command(
                label='Exit',
                command=self.root.destroy
            )
            menubar.add_cascade(
                label="File",
                menu=file_menu
            )
            help_menu = Menu(
                menubar,
                tearoff=0
            )
            help_menu.add_command(label='Welcome')
            help_menu.add_command(label='About...')
            menubar.add_cascade(
                label="Help",
                menu=help_menu
            )
