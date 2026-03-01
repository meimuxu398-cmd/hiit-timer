```python
import tkinter as tk
from tkinter import ttk
import threading
import time
from playsound import playsound
import os

class HIITTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("HIIT Timer")
        self.root.geometry("400x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.work_time = tk.IntVar(value=30)
        self.rest_time = tk.IntVar(value=10)
        self.cycles = tk.IntVar(value=8)
        self.current_cycle = 0
        self.current_time = 0
        self.is_work_phase = True
        self.is_running = False
        self.timer_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="HIIT TIMER", 
                        font=("Arial", 24, "bold"), 
                        fg='white', bg='#2c3e50')
        title.pack(pady=20)
        
        # Settings Frame
        settings_frame = tk.Frame(self.root, bg='#2c3e50')
        settings_frame.pack(pady=20)
        
        # Work Time
        tk.Label(settings_frame, text="Work Time (sec)", 
                font=("Arial", 12), fg='white', bg='#2c3e50').grid(row=0, column=0, padx=10)
        work_spinbox = tk.Spinbox(settings_frame, from_=10, to=300, 
                                 textvariable=self.work_time, width=10, font=("Arial", 12))
        work_spinbox.grid(row=0, column=1, padx=10)
        
        # Rest Time
        tk.Label(settings_frame, text="Rest Time (sec)", 
                font=("Arial", 12), fg='white', bg='#2c3e50').grid(row=1, column=0, padx=10, pady=5)
        rest_spinbox = tk.Spinbox(settings_frame, from_=5, to=180, 
                                 textvariable=self.rest_time, width=10, font=("Arial", 12))
        rest_spinbox.grid(row=1, column=1, padx=10, pady=5)
        
        # Cycles
        tk.Label(settings_frame, text="Cycles", 
                font=("Arial", 12), fg='white', bg='#2c3e50').grid(row=2, column=0, padx=10)
        cycles_spinbox = tk.Spinbox(settings_frame, from_=1, to=20, 
                                   textvariable=self.cycles, width=10, font=("Arial", 12))
        cycles_spinbox.grid(row=2, column=1, padx=10)
        
        # Timer Display
        self.timer_display = tk.Label(self.root, text="00:30", 
                                     font=("Arial", 48, "bold"), 
                                     fg='#e74c3c', bg='#2c3e50')
        self.timer_display.pack(pady=30)
        
        # Phase Label
        self.phase_label = tk.Label(self.root, text="WORK", 
                                   font=("Arial", 20, "bold"), 
                                   fg='#e74c3c', bg='#2c3e50')
        self.phase_label.pack(pady=10)
        
        # Cycle Counter
        self.cycle_label = tk.Label(self.root, text="Cycle: 0/8", 
                                   font=("Arial", 16), 
                                   fg='white', bg='#2c3e50')
        self.cycle_label.pack(pady=10)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.pack(pady=20)
        
        # Control Buttons
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(button_frame, text="START", 
                                  command=self.start_timer, 
                                  font=("Arial", 14, "bold"), 
                                  bg='#27ae60', fg='white', 
                                  width=8, height=2)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(button_frame, text="PAUSE", 
                                  command=self.pause_timer, 
                                  font=("Arial", 14, "bold"), 
                                  bg='#f39c12', fg='white', 
                                  width=8, height=2)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(button_frame, text="RESET", 
                                  command=self.reset_timer, 
                                  font=("Arial", 14, "bold"), 
                                  bg='#e74c3c', fg='white', 
                                  width=8, height=2)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            if self.current_cycle == 0:
                self.current_cycle = 1
                self.current_time = self.work_time.get()
                self.is_work_phase =