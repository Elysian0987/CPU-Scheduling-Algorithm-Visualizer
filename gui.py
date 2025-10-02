# gui.py

import tkinter as tk
from tkinter import messagebox
import random

# Import the scheduling algorithms
from algorithms import fcfs, sjf, srtf, npp, priority_preemptive, rr

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Algorithms")
        self.create_widgets()

    def create_widgets(self):
        # --- Algorithm Selection ---
        tk.Label(self.root, text="Choose Scheduling Algorithm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.selected_algo = tk.StringVar(value="Select Algorithm")
        algorithms = ["First Come First Serve", "Shortest Job First", "Shortest Remaining Time First", 
                      "Priority Non Pre-emptive", "Priority Pre-emptive", "Round Robin"]
        algo_menu = tk.OptionMenu(self.root, self.selected_algo, *algorithms, command=self.toggle_inputs)
        algo_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Process Inputs ---
        tk.Label(self.root, text="Number of Processes:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.n_processes = tk.StringVar()
        tk.Entry(self.root, textvariable=self.n_processes).grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.root, text="Arrival Times (space-separated):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.arrival_times = tk.StringVar()
        tk.Entry(self.root, textvariable=self.arrival_times).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.root, text="Burst Times (space-separated):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.burst_times = tk.StringVar()
        tk.Entry(self.root, textvariable=self.burst_times).grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # --- Conditional Inputs ---
        self.priority_label = tk.Label(self.root, text="Priorities (space-separated):")
        self.priority = tk.StringVar()
        self.priority_entry = tk.Entry(self.root, textvariable=self.priority)

        self.time_quantum_label = tk.Label(self.root, text="Time Quantum:")
        self.time_quantum = tk.StringVar()
        self.time_quantum_entry = tk.Entry(self.root, textvariable=self.time_quantum)

        # --- Submit Button ---
        submit_button = tk.Button(self.root, text="Calculate", command=self.on_submit)
        submit_button.grid(row=6, column=0, columnspan=2, pady=10)

        # --- Results Display ---
        self.result_text = tk.Text(self.root, height=10, width=60)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # --- Gantt Chart Canvas ---
        self.gantt_canvas = tk.Canvas(self.root, height=100, width=700, bg="white")
        self.gantt_canvas.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
    
    def toggle_inputs(self, _=None):
        algo = self.selected_algo.get()
        # Hide all conditional inputs first
        self.priority_label.grid_forget()
        self.priority_entry.grid_forget()
        self.time_quantum_label.grid_forget()
        self.time_quantum_entry.grid_forget()

        if "Priority" in algo:
            self.priority_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
            self.priority_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        elif "Round Robin" in algo:
            self.time_quantum_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
            self.time_quantum_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    def on_submit(self):
        try:
            num_processes = int(self.n_processes.get())
            at = list(map(int, self.arrival_times.get().split()))
            bt = list(map(int, self.burst_times.get().split()))
            algo = self.selected_algo.get()

            if len(at) != num_processes or len(bt) != num_processes:
                raise ValueError("Number of arrival/burst times must match the number of processes.")

            ans1, ans2 = None, None
            if algo == "Round Robin":
                tq = int(self.time_quantum.get())
                ans1, ans2 = rr(at, bt, tq)
            elif algo == "Shortest Remaining Time First":
                ans1, ans2 = srtf(at, bt)
            elif algo == "Shortest Job First":
                ans1, ans2 = sjf(at, bt)
            elif algo == "Priority Pre-emptive":
                priorities = list(map(int, self.priority.get().split()))
                ans1, ans2 = priority_preemptive(at, bt, priorities)
            elif algo == "Priority Non Pre-emptive":
                priorities = list(map(int, self.priority.get().split()))
                ans1, ans2 = npp(at, bt, priorities)
            elif algo == "First Come First Serve":
                ans1, ans2 = fcfs(at, bt)
            else:
                raise ValueError("Please select a valid scheduling algorithm.")
            
            self.display_results(ans1)
            self.draw_gantt_chart(ans2)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def display_results(self, solved_info):
        self.result_text.delete(1.0, tk.END)
        headers = f"{'Job':<5} | {'AT':<5} | {'BT':<5} | {'FT':<5} | {'TAT':<5} | {'WT':<5} | {'RT':<5}\n"
        self.result_text.insert(tk.END, headers)
        self.result_text.insert(tk.END, "-"*60 + "\n")
        for p in solved_info:
            line = f"{p['job']:<5} | {p['at']:<5} | {p['bt']:<5} | {p['ft']:<5} | {p['tat']:<5} | {p['wat']:<5} | {p['rt']:<5}\n"
            self.result_text.insert(tk.END, line)

    def draw_gantt_chart(self, gantt_data):
        self.gantt_canvas.delete("all")
        if not gantt_data: return

        # Generate unique colors for each job
        job_ids = sorted(list(set(job['job'] for job in gantt_data)))
        colors = {job_id: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for job_id in job_ids}

        # Calculate scaling factor
        max_time = max(job['stop'] for job in gantt_data)
        canvas_width = self.gantt_canvas.winfo_width()
        scale = (canvas_width - 40) / max_time if max_time > 0 else 1

        x_start, y_start, height = 20, 20, 40
        
        for job in gantt_data:
            start_pos = x_start + job['start'] * scale
            end_pos = x_start + job['stop'] * scale
            
            # Draw rectangle
            self.gantt_canvas.create_rectangle(start_pos, y_start, end_pos, y_start + height, 
                                             fill=colors[job['job']], outline="black")
            # Draw job label
            self.gantt_canvas.create_text((start_pos + end_pos) / 2, y_start + height / 2, text=job['job'])
            # Draw time marker
            self.gantt_canvas.create_text(start_pos, y_start + height + 10, text=str(job['start']), anchor="n")

        # Add the final time marker
        last_job = max(gantt_data, key=lambda x: x['stop'])
        self.gantt_canvas.create_text(x_start + last_job['stop'] * scale, y_start + height + 10, text=str(last_job['stop']), anchor="n")