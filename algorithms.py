# algorithms.py

def fcfs(arrival_time, burst_time):
    """ First Come First Serve Algorithm """
    processes_info = sorted([
        {'job': f'P{i+1}', 'at': at, 'bt': burst_time[i]}
        for i, at in enumerate(arrival_time)
    ], key=lambda x: x['at'])

    gantt_chart_info = []
    solved_processes_info = []
    current_time = 0

    for process in processes_info:
        start_time = max(current_time, process['at'])
        finish_time = start_time + process['bt']
        
        gantt_chart_info.append({
            'job': process['job'],
            'start': start_time,
            'stop': finish_time
        })

        turnaround_time = finish_time - process['at']
        waiting_time = turnaround_time - process['bt']
        response_time = start_time - process['at']
        
        solved_processes_info.append({
            **process,
            'ft': finish_time,
            'tat': turnaround_time,
            'wat': waiting_time,
            'rt': response_time
        })
        current_time = finish_time
        
    return solved_processes_info, gantt_chart_info

def sjf(arrival_time, burst_time):
    """ Shortest Job First (Non-Preemptive) Algorithm """
    n = len(arrival_time)
    processes_info = [
        {'job': f'P{i+1}', 'at': arrival_time[i], 'bt': burst_time[i]}
        for i in range(n)
    ]
    
    gantt_chart_info = []
    solved_processes_info = []
    current_time = 0
    completed = 0
    
    while completed < n:
        available_processes = [p for p in processes_info if p['at'] <= current_time and p.get('ft') is None]
        
        if not available_processes:
            current_time += 1
            continue
            
        # Select the process with the shortest burst time
        process_to_execute = min(available_processes, key=lambda p: p['bt'])
        
        start_time = current_time
        finish_time = start_time + process_to_execute['bt']
        
        gantt_chart_info.append({
            'job': process_to_execute['job'],
            'start': start_time,
            'stop': finish_time
        })
        
        turnaround_time = finish_time - process_to_execute['at']
        waiting_time = turnaround_time - process_to_execute['bt']
        response_time = start_time - process_to_execute['at']
        
        # Find the process in the original list to update it
        for p in processes_info:
            if p['job'] == process_to_execute['job']:
                p['ft'] = finish_time
                p['tat'] = turnaround_time
                p['wat'] = waiting_time
                p['rt'] = response_time
                solved_processes_info.append(p)
                break
                
        current_time = finish_time
        completed += 1
        
    solved_processes_info.sort(key=lambda p: p['job'])
    return solved_processes_info, gantt_chart_info

def srtf(arrival_time, burst_time):
    """ Shortest Remaining Time First (Preemptive) Algorithm """
    n = len(arrival_time)
    processes_info = [
        {'job': f'P{i+1}', 'at': arrival_time[i], 'bt': burst_time[i], 'rt': burst_time[i]}
        for i in range(n)
    ]
    
    gantt_chart_info = []
    solved_processes_info = []
    current_time = 0
    completed = 0
    
    while completed < n:
        available_processes = [p for p in processes_info if p['at'] <= current_time and p['rt'] > 0]
        
        if not available_processes:
            current_time += 1
            continue
            
        process_to_execute = min(available_processes, key=lambda p: p['rt'])
        
        # Record response time if it's the first execution
        if 'start_time' not in process_to_execute:
            process_to_execute['start_time'] = current_time

        # Add to Gantt chart
        if not gantt_chart_info or gantt_chart_info[-1]['job'] != process_to_execute['job']:
             gantt_chart_info.append({'job': process_to_execute['job'], 'start': current_time, 'stop': 0})

        process_to_execute['rt'] -= 1
        current_time += 1
        
        if gantt_chart_info[-1]['job'] == process_to_execute['job']:
            gantt_chart_info[-1]['stop'] = current_time
            
        if process_to_execute['rt'] == 0:
            completed += 1
            finish_time = current_time
            turnaround_time = finish_time - process_to_execute['at']
            waiting_time = turnaround_time - process_to_execute['bt']
            response_time = process_to_execute['start_time'] - process_to_execute['at']

            solved_processes_info.append({
                'job': process_to_execute['job'],
                'at': process_to_execute['at'],
                'bt': process_to_execute['bt'],
                'ft': finish_time,
                'tat': turnaround_time,
                'wat': waiting_time,
                'rt': response_time
            })
            
    solved_processes_info.sort(key=lambda p: p['job'])
    return solved_processes_info, gantt_chart_info

def npp(arrival_time, burst_time, priorities):
    """ Non-Preemptive Priority Algorithm """
    n = len(arrival_time)
    processes_info = [
        {'job': f'P{i+1}', 'at': arrival_time[i], 'bt': burst_time[i], 'priority': priorities[i]}
        for i in range(n)
    ]
    
    gantt_chart_info = []
    solved_processes_info = []
    current_time = 0
    completed = 0
    
    while completed < n:
        available_processes = [p for p in processes_info if p['at'] <= current_time and p.get('ft') is None]
        
        if not available_processes:
            current_time += 1
            continue
        
        process_to_execute = min(available_processes, key=lambda p: p['priority'])
        
        start_time = current_time
        finish_time = start_time + process_to_execute['bt']
        
        gantt_chart_info.append({
            'job': process_to_execute['job'],
            'start': start_time,
            'stop': finish_time
        })
        
        turnaround_time = finish_time - process_to_execute['at']
        waiting_time = turnaround_time - process_to_execute['bt']
        response_time = start_time - process_to_execute['at']
        
        for p in processes_info:
            if p['job'] == process_to_execute['job']:
                p['ft'] = finish_time
                p['tat'] = turnaround_time
                p['wat'] = waiting_time
                p['rt'] = response_time
                solved_processes_info.append(p)
                break
                
        current_time = finish_time
        completed += 1
        
    solved_processes_info.sort(key=lambda p: p['job'])
    return solved_processes_info, gantt_chart_info

def priority_preemptive(arrival_time, burst_time, priorities):
    """ Preemptive Priority Algorithm """
    n = len(arrival_time)
    processes_info = [
        {'job': f'P{i+1}', 'at': arrival_time[i], 'bt': burst_time[i], 'priority': priorities[i], 'rt': burst_time[i]}
        for i in range(n)
    ]
    
    gantt_chart_info = []
    solved_processes_info = []
    current_time = 0
    completed = 0
    
    while completed < n:
        available_processes = [p for p in processes_info if p['at'] <= current_time and p['rt'] > 0]
        
        if not available_processes:
            current_time += 1
            continue
            
        process_to_execute = min(available_processes, key=lambda p: p['priority'])
        
        if 'start_time' not in process_to_execute:
            process_to_execute['start_time'] = current_time

        if not gantt_chart_info or gantt_chart_info[-1]['job'] != process_to_execute['job']:
             gantt_chart_info.append({'job': process_to_execute['job'], 'start': current_time, 'stop': 0})

        process_to_execute['rt'] -= 1
        current_time += 1

        if gantt_chart_info[-1]['job'] == process_to_execute['job']:
            gantt_chart_info[-1]['stop'] = current_time
            
        if process_to_execute['rt'] == 0:
            completed += 1
            finish_time = current_time
            turnaround_time = finish_time - process_to_execute['at']
            waiting_time = turnaround_time - process_to_execute['bt']
            response_time = process_to_execute['start_time'] - process_to_execute['at']

            solved_processes_info.append({
                'job': process_to_execute['job'], 'at': process_to_execute['at'],
                'bt': process_to_execute['bt'], 'ft': finish_time,
                'tat': turnaround_time, 'wat': waiting_time, 'rt': response_time
            })
            
    solved_processes_info.sort(key=lambda p: p['job'])
    return solved_processes_info, gantt_chart_info


def rr(arrival_time, burst_time, time_quantum):
    """ Round Robin Algorithm """
    n = len(arrival_time)
    processes_info = [
        {'job': f'P{i+1}', 'at': arrival_time[i], 'bt': burst_time[i], 'rt': burst_time[i]}
        for i in range(n)
    ]
    
    gantt_chart_info = []
    solved_processes_info = []
    current_time = 0
    ready_queue = []
    
    processes_info.sort(key=lambda p: p['at'])
    process_idx = 0

    while any(p['rt'] > 0 for p in processes_info):
        # Add newly arrived processes to the ready queue
        while process_idx < n and processes_info[process_idx]['at'] <= current_time:
            ready_queue.append(processes_info[process_idx])
            process_idx += 1

        if not ready_queue:
            current_time += 1
            continue

        process_to_execute = ready_queue.pop(0)

        if 'start_time' not in process_to_execute:
            process_to_execute['start_time'] = current_time
        
        exec_time = min(time_quantum, process_to_execute['rt'])
        
        gantt_chart_info.append({
            'job': process_to_execute['job'],
            'start': current_time,
            'stop': current_time + exec_time
        })
        
        process_to_execute['rt'] -= exec_time
        current_time += exec_time

        # Add processes that arrived during execution
        while process_idx < n and processes_info[process_idx]['at'] <= current_time:
            ready_queue.append(processes_info[process_idx])
            process_idx += 1
            
        if process_to_execute['rt'] > 0:
            ready_queue.append(process_to_execute)
        else:
            finish_time = current_time
            turnaround_time = finish_time - process_to_execute['at']
            waiting_time = turnaround_time - process_to_execute['bt']
            response_time = process_to_execute['start_time'] - process_to_execute['at']
            solved_processes_info.append({
                'job': process_to_execute['job'], 'at': process_to_execute['at'],
                'bt': process_to_execute['bt'], 'ft': finish_time,
                'tat': turnaround_time, 'wat': waiting_time, 'rt': response_time
            })
            
    solved_processes_info.sort(key=lambda p: p['job'])
    return solved_processes_info, gantt_chart_info