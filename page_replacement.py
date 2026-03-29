import sys
import os

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_textbook_table(ref_string, snapshots, num_frames):
    print(f"\n{Colors.BOLD}{Colors.BLUE}--- Textbook Manual Calculation Grid ---{Colors.ENDC}\n")
    
    # Process reference row
    ref_row = f"{Colors.WARNING}Ref String: {Colors.ENDC}"
    for req in ref_string:
        ref_row += f"{req:3} "
    print(ref_row)
    print("─" * (12 + 4 * len(ref_string)))
    
    # Process each frame row (physical slots in memory)
    for f in range(num_frames):
        row_str = f"{Colors.BOLD}Frame {f+1}:{Colors.ENDC}    "
        for i in range(len(ref_string)):
            state = snapshots[i]['state']
            page = state[f]
            if page is not None:
                row_str += f"{page:3} "
            else:
                row_str += "    "
        print(row_str)
        
    print("─" * (12 + 4 * len(ref_string)))
    
    # Process faults row
    fault_row = f"{Colors.FAIL}Faults:{Colors.ENDC}     "
    for i in range(len(ref_string)):
        if snapshots[i]['status'] == "Fault":
            fault_row += f"{Colors.FAIL}  *{Colors.ENDC} "
        else:
            fault_row += "    "
    print(fault_row)
    print()

def print_result(algo_name, ref_string, frames_snapshots, faults, total_requests, num_frames):
    hits = total_requests - faults
    print(f"\n{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}║                 {algo_name:^38} ║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}╚════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
    
    print(f" {Colors.BOLD}Total Requests:{Colors.ENDC} {total_requests}")
    print(f" {Colors.BOLD}Page Faults:{Colors.ENDC}    {Colors.FAIL}{faults}{Colors.ENDC}")
    print(f" {Colors.BOLD}Page Hits:{Colors.ENDC}      {Colors.GREEN}{hits}{Colors.ENDC}")
    print(f" {Colors.BOLD}Failure Rate:{Colors.ENDC}   {Colors.WARNING}{(faults / total_requests * 100):.2f}%{Colors.ENDC}")
    print(f" {Colors.BOLD}Success Rate:{Colors.ENDC}   {Colors.GREEN}{(hits / total_requests * 100):.2f}%{Colors.ENDC}\n")
    
    # Dynamically calculate the maximum width for the "Memory Frames (State)" column
    max_state_len = 21 # Length of the header "Memory Frames (State)"
    for snapshot in frames_snapshots:
        state_str = "[" + ", ".join(str(x) if x is not None else " " for x in snapshot['state']) + "]"
        if len(state_str) > max_state_len:
            max_state_len = len(state_str)
            
    header_padding = " " * (max_state_len - 21)
    line_padding = "─" * max_state_len
    
    # Table Header
    print(f"{Colors.BOLD}┌──────┬─────────┬─{line_padding}─┬────────┐{Colors.ENDC}")
    print(f"{Colors.BOLD}│ Step │ Request │ Memory Frames (State){header_padding} │ Status │{Colors.ENDC}")
    print(f"{Colors.BOLD}├──────┼─────────┼─{line_padding}─┼────────┤{Colors.ENDC}")
    
    for i in range(total_requests):
        req = ref_string[i]
        state = frames_snapshots[i]['state']
        status = frames_snapshots[i]['status']
        
        status_color = Colors.FAIL if status == "Fault" else Colors.GREEN
        status_str = f"{status_color}{status:5}{Colors.ENDC}"
        
        state_str = "[" + ", ".join(str(x) if x is not None else " " for x in state) + "]"
        print(f"│ {i+1:4} │ {req:7} │ {state_str:<{max_state_len}} │ {status_str}  │")
        
    print(f"{Colors.BOLD}└──────┴─────────┴─{line_padding}─┴────────┘{Colors.ENDC}\n")
    
    choice = input(f"{Colors.WARNING}Would you like to view the textbook manual calculation grid? (y/n): {Colors.ENDC}")
    if choice.lower() == 'y':
        print_textbook_table(ref_string, frames_snapshots, num_frames)
        
    input(f"{Colors.WARNING}Press [Enter] to return to the menu...{Colors.ENDC}")

def simulate_fifo(ref_string, num_frames):
    memory = [None] * num_frames
    pointer = 0
    faults = 0
    snapshots = []
    
    for req in ref_string:
        status = ""
        if req in memory:
            status = "Hit"
        else:
            status = "Fault"
            faults += 1
            memory[pointer] = req
            pointer = (pointer + 1) % num_frames
        
        snapshots.append({'state': list(memory), 'status': status})
        
    return faults, snapshots

def simulate_lru(ref_string, num_frames):
    memory = [None] * num_frames
    last_used = [0] * num_frames
    time = 0
    faults = 0
    snapshots = []
    
    for req in ref_string:
        time += 1
        status = ""
        if req in memory:
            status = "Hit"
            idx = memory.index(req)
            last_used[idx] = time
        else:
            status = "Fault"
            faults += 1
            if None in memory:
                idx = memory.index(None)
            else:
                idx = last_used.index(min(last_used))
            memory[idx] = req
            last_used[idx] = time
            
        snapshots.append({'state': list(memory), 'status': status})
        
    return faults, snapshots

def simulate_mru(ref_string, num_frames):
    memory = [None] * num_frames
    last_used = [0] * num_frames
    time = 0
    faults = 0
    snapshots = []
    
    for req in ref_string:
        time += 1
        status = ""
        if req in memory:
            status = "Hit"
            idx = memory.index(req)
            last_used[idx] = time
        else:
            status = "Fault"
            faults += 1
            if None in memory:
                idx = memory.index(None)
            else:
                idx = last_used.index(max(last_used))
            memory[idx] = req
            last_used[idx] = time
            
        snapshots.append({'state': list(memory), 'status': status})
        
    return faults, snapshots

def simulate_optimal(ref_string, num_frames):
    memory = [None] * num_frames
    faults = 0
    snapshots = []
    
    for idx, req in enumerate(ref_string):
        status = ""
        if req in memory:
            status = "Hit"
        else:
            status = "Fault"
            faults += 1
            if None in memory:
                mem_idx = memory.index(None)
            else:
                farthest_time = -1
                mem_idx = -1
                for m_i, frame in enumerate(memory):
                    try:
                        next_use = ref_string[idx+1:].index(frame) + idx + 1
                    except ValueError:
                        next_use = float('inf')
                    
                    if next_use > farthest_time:
                        farthest_time = next_use
                        mem_idx = m_i
                
            memory[mem_idx] = req
                
        snapshots.append({'state': list(memory), 'status': status})
        
    return faults, snapshots

def simulate_second_chance(ref_string, num_frames):
    memory = [None] * num_frames
    ref_bits = [0] * num_frames
    pointer = 0
    faults = 0
    snapshots = []
    
    for req in ref_string:
        status = ""
        if req in memory:
            status = "Hit"
            idx = memory.index(req)
            ref_bits[idx] = 1
        else:
            status = "Fault"
            faults += 1
            if None in memory:
                idx = memory.index(None)
                memory[idx] = req
                ref_bits[idx] = 0
            else:
                while True:
                    if ref_bits[pointer] == 1:
                        ref_bits[pointer] = 0
                        pointer = (pointer + 1) % num_frames
                    else:
                        memory[pointer] = req
                        ref_bits[pointer] = 0
                        pointer = (pointer + 1) % num_frames
                        break
                        
        snapshots.append({'state': list(memory), 'status': status})
        
    return faults, snapshots

def parse_reference_string(raw_str):
    raw_str = raw_str.replace(",", " ")
    parts = raw_str.split()
    try:
        return [int(p) for p in parts]
    except ValueError:
        return []

def run_simulation(name, func, ref_string, num_frames):
    clear_screen()
    faults, snapshots = func(ref_string, num_frames)
    print_result(name, ref_string, snapshots, faults, len(ref_string), num_frames)

def main():
    if os.name == 'nt':
        os.system('color') # Enable ANSI escape characters in Windows CMD
        
    num_frames = 0
    ref_string = []
    
    while True:
        clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║          PAGED REPLACEMENT ALGORITHM SIMULATOR           ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
        
        # Setup inputs if needed
        if num_frames == 0 or len(ref_string) == 0:
            print(f"{Colors.BLUE}{Colors.BOLD}--- Initial Setup ---{Colors.ENDC}")
            while True:
                try:
                    num_frames = int(input("Enter the number of memory frames: "))
                    if num_frames <= 0:
                        print(f"{Colors.FAIL}Frames must be > 0.{Colors.ENDC}")
                        continue
                    break
                except ValueError:
                    print(f"{Colors.FAIL}Invalid input. Please enter a number.{Colors.ENDC}")
                    
            while True:
                raw_str = input("Enter reference string (e.g., '7,0,1,2,0' or '7 0 1'): ")
                ref_string = parse_reference_string(raw_str)
                if len(ref_string) > 0:
                    break
                print(f"{Colors.FAIL}Invalid string. Must contain integers.{Colors.ENDC}")
            continue

        # Display current parameters
        print(f" {Colors.BOLD}Current Settings:{Colors.ENDC}")
        print(f" • Frames: {Colors.GREEN}{num_frames}{Colors.ENDC}")
        print(f" • String: {Colors.WARNING}{', '.join(map(str, ref_string))}{Colors.ENDC}")
        print(f" • Length: {len(ref_string)} Requests\n")

        # Main Menu
        print(f"{Colors.BOLD}Select an Algorithm to Simulate:{Colors.ENDC}")
        print(f"  {Colors.BLUE}1.{Colors.ENDC} FIFO (First In First Out)")
        print(f"  {Colors.BLUE}2.{Colors.ENDC} LRU (Least Recently Used)")
        print(f"  {Colors.BLUE}3.{Colors.ENDC} MRU (Most Recently Used)")
        print(f"  {Colors.BLUE}4.{Colors.ENDC} OPTIMAL")
        print(f"  {Colors.BLUE}5.{Colors.ENDC} SECOND CHANCE (Clock)")
        print("  ─" * 20)
        print(f"  {Colors.WARNING}6.{Colors.ENDC} Run ALL Algorithms (Summary)")
        print(f"  {Colors.WARNING}7.{Colors.ENDC} Change Reference String or Frames")
        print(f"  {Colors.FAIL}8.{Colors.ENDC} Exit\n")
        
        choice = input(f"Enter choice {Colors.BLUE}[1-8]{Colors.ENDC}: ")
        
        if choice == '1':
            run_simulation("FIFO", simulate_fifo, ref_string, num_frames)
        elif choice == '2':
            run_simulation("LRU", simulate_lru, ref_string, num_frames)
        elif choice == '3':
            run_simulation("MRU", simulate_mru, ref_string, num_frames)
        elif choice == '4':
            run_simulation("OPTIMAL", simulate_optimal, ref_string, num_frames)
        elif choice == '5':
            run_simulation("SECOND CHANCE", simulate_second_chance, ref_string, num_frames)
        elif choice == '6':
            clear_screen()
            print(f"\n{Colors.BOLD}{Colors.WARNING}╔════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.WARNING}║                 ALL ALGORITHMS SUMMARY                 ║{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.WARNING}╚════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
            
            algos = [
                ("FIFO", simulate_fifo),
                ("LRU", simulate_lru),
                ("MRU", simulate_mru),
                ("OPTIMAL", simulate_optimal),
                ("SECOND CHANCE", simulate_second_chance)
            ]
            
            print(f"{Colors.BOLD}┌──────────────────┬──────────────┬─────────────┬────────┐{Colors.ENDC}")
            print(f"{Colors.BOLD}│ Algorithm        │ Faults (Bad) │ Hits (Good) │ Rate   │{Colors.ENDC}")
            print(f"{Colors.BOLD}├──────────────────┼──────────────┼─────────────┼────────┤{Colors.ENDC}")
            
            for alg_name, alg_func in algos:
                faults, _ = alg_func(ref_string, num_frames)
                hits = len(ref_string) - faults
                rate = f"{(hits / len(ref_string) * 100):.1f}%"
                print(f"│ {alg_name:<16} │ {Colors.FAIL}{faults:<12}{Colors.ENDC} │ {Colors.GREEN}{hits:<11}{Colors.ENDC} │ {Colors.BLUE}{rate:<6}{Colors.ENDC} │")
            
            print(f"{Colors.BOLD}└──────────────────┴──────────────┴─────────────┴────────┘{Colors.ENDC}\n")
            input(f"{Colors.WARNING}Press [Enter] to return to the menu...{Colors.ENDC}")
            
        elif choice == '7':
            num_frames = 0
            ref_string = []
        elif choice == '8':
            clear_screen()
            print(f"{Colors.GREEN}Exiting simulator. Goodbye!{Colors.ENDC}")
            sys.exit(0)

if __name__ == "__main__":
    main()
