# CPU Scheduling Algorithm Visualizer

This is an **academic project** developed for an Operating Systems course. It's a desktop application built with Python and Tkinter that simulates and visualizes several common CPU scheduling algorithms. The tool provides a clear Gantt chart representation and calculates key performance metrics, making it easier to understand how each algorithm manages processes.

##  Features

* **Multiple Algorithms**: Simulates a variety of scheduling algorithms:
  * First-Come, First-Served (FCFS)
  * Shortest Job First (SJF) (Non-Preemptive)
  * Shortest Remaining Time First (SRTF) (Preemptive)
  * Priority Scheduling (Non-Preemptive & Preemptive)
  * Round Robin (RR)
* **Dynamic Visualization**: Generates a color-coded **Gantt chart** to visualize the process execution timeline.
* **Performance Metrics**: Calculates and displays a detailed table with metrics for each process, including:
  * Finish Time (FT)
  * Turnaround Time (TAT)
  * Waiting Time (WT)
  * Response Time (RT)
* **Interactive GUI**: A simple and intuitive graphical user interface for easy input and clear results.

##  Tech Stack

* **Language**: Python
* **GUI Framework**: Tkinter (standard Python library)

##  File Structure

The project is organized into a modular structure for better readability and maintenance:

* `main.py`: The main entry point to launch the application.
* `gui.py`: Manages the entire Tkinter-based graphical user interface and event handling.
* `algorithms.py`: Contains the core logic and implementation of all the CPU scheduling algorithms.

##  How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Elysian0987/CPU-Scheduling-Visualizer.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd CPU-Scheduling-Visualizer
   ```
3. **Run the application:**
   (Ensure you have Python 3 installed)
   ```bash
   python main.py
   ```

##  How to Use

1. Launch the application by running `main.py`.
2. Select a scheduling algorithm from the dropdown menu.
3. Enter the total number of processes.
4. Provide the **Arrival Times** and **Burst Times** for all processes, separated by spaces.
5. If using a **Priority** or **Round Robin** algorithm, the relevant input fields will appear. Fill them in.
6. Click the **"Calculate"** button.
7. The results table and the Gantt chart will be displayed below.
