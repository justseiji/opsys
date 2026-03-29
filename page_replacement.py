import sys

def print_result(ref_string, frames_snapshots, faults, total_requests):
    print(f"\nTotal Requests: {total_requests}")
    print(f"Page Faults (Interrupts): {faults}")
    print(f"Page Hits: {total_requests - faults}")
    print(f"Failure Rate: {(faults / total_requests * 100):.2f}%")
    print(f"Success Rate: {((total_requests - faults) / total_requests * 100):.2f}%\n")
    
    # Print tracing table
    print("Step | Request | Memory Frames (State) | Status")
    print("-" * 55)
    for i in range(total_requests):
        req = ref_string[i]
        state = frames_snapshots[i]['state']
        status = frames_snapshots[i]['status']
        # Format the state array to standard length for clean column view
        state_str = "[" + ", ".join(str(x) if x is not None else " " for x in state) + "]"
        print(f"{i+1:4} | {req:7} | {state_str:21} | {status}")
    print("-" * 55)

def simulate_fifo(ref_string, num_frames):
    frames = []
    faults = 0
    snapshots = []
    
    for req in ref_string:
        status = ""
        if req in frames:
            status = "Hit"
        else:
            status = "Fault"
            faults += 1
            if len(frames) < num_frames:
                frames.append(req)
            else:
                frames.pop(0)
                frames.append(req)
        
        # Capture state for table
        state = frames + [None] * (num_frames - len(frames))
        snapshots.append({'state': state, 'status': status})
        
    print_result(ref_string, snapshots, faults, len(ref_string))


def simulate_lru(ref_string, num_frames):
    frames = []
    faults = 0
    snapshots = []
    
    for req in ref_string:
        status = ""
        if req in frames:
            status = "Hit"
            frames.remove(req)
            frames.append(req)
        else:
            status = "Fault"
            faults += 1
            if len(frames) < num_frames:
                frames.append(req)
            else:
                frames.pop(0)
                frames.append(req)
                
        state = frames + [None] * (num_frames - len(frames))
        snapshots.append({'state': state, 'status': status})
        
    print_result(ref_string, snapshots, faults, len(ref_string))


def simulate_mru(ref_string, num_frames):
    frames = []
    faults = 0
    snapshots = []
    
    for req in ref_string:
        status = ""
        if req in frames:
            status = "Hit"
            frames.remove(req)
            frames.append(req)
        else:
            status = "Fault"
            faults += 1
            if len(frames) < num_frames:
                frames.append(req)
            else:
                frames.pop(-1)
                frames.append(req)
                
        state = frames + [None] * (num_frames - len(frames))
        snapshots.append({'state': state, 'status': status})
        
    print_result(ref_string, snapshots, faults, len(ref_string))


def simulate_optimal(ref_string, num_frames):
    frames = []
    faults = 0
    snapshots = []
    
    total_len = len(ref_string)
    
    for idx, req in enumerate(ref_string):
        status = ""
        if req in frames:
            status = "Hit"
        else:
            status = "Fault"
            faults += 1
            if len(frames) < num_frames:
                frames.append(req)
            else:
                # Find page to replace
                farthest_idx = -1
                replace_candidate = -1
                for frame in frames:
                    try:
                        # Find the first occurrence of `frame` from `idx+1` to end of string
                        next_use = ref_string[idx+1:].index(frame) + idx + 1
                    except ValueError:
                        # Never used again
                        next_use = float('inf')
                    
                    if next_use > farthest_idx:
                        farthest_idx = next_use
                        replace_candidate = frame
                
                frames[frames.index(replace_candidate)] = req
                
        state = frames + [None] * (num_frames - len(frames))
        snapshots.append({'state': state, 'status': status})
        
    print_result(ref_string, snapshots, faults, len(ref_string))


def simulate_second_chance(ref_string, num_frames):
    frames = []  # stores pages
    ref_bits = {} # maps page to ref bit
    pointer = 0
    faults = 0
    snapshots = []
    
    for req in ref_string:
        status = ""
        if req in frames:
            status = "Hit"
            ref_bits[req] = 1
        else:
            status = "Fault"
            faults += 1
            if len(frames) < num_frames:
                frames.append(req)
                ref_bits[req] = 0
            else:
                while True:
                    candidate = frames[pointer]
                    if ref_bits[candidate] == 1:
                        ref_bits[candidate] = 0
                        pointer = (pointer + 1) % num_frames
                    else:
                        # replace this candidate
                        frames[pointer] = req
                        ref_bits[req] = 0
                        pointer = (pointer + 1) % num_frames
                        break
                        
        state = frames + [None] * (num_frames - len(frames))
        snapshots.append({'state': state, 'status': status})
        
    print_result(ref_string, snapshots, faults, len(ref_string))


def parse_reference_string(raw_str):
    # Determine the separator (comma or space)
    raw_str = raw_str.replace(",", " ")
    parts = raw_str.split()
    try:
        return [int(p) for p in parts]
    except ValueError:
        print("Error: Reference string must contain only integers.")
        return []

def main():
    print("===========================================")
    print("   Paged Replacement Algorithm Simulator")
    print("===========================================")
    
    while True:
        try:
            num_frames = int(input("\nEnter the number of frames: "))
            if num_frames <= 0:
                print("Number of frames must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")
            
    while True:
        raw_str = input("Enter the page reference string (e.g., '7,0,1,2,0' or '7 0 1 2 0'): ")
        ref_string = parse_reference_string(raw_str)
        if len(ref_string) > 0:
            break
            
    while True:
        print("\nAlgorithms Menu:")
        print("1. FIFO (First In First Out)")
        print("2. LRU (Least Recently Used)")
        print("3. MRU (Most Recently Used)")
        print("4. OPTIMAL")
        print("5. SECOND CHANCE")
        print("6. Change Reference String or Frames")
        print("7. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            print("\n--- FIFO Simulation ---")
            simulate_fifo(ref_string, num_frames)
        elif choice == '2':
            print("\n--- LRU Simulation ---")
            simulate_lru(ref_string, num_frames)
        elif choice == '3':
            print("\n--- MRU Simulation ---")
            simulate_mru(ref_string, num_frames)
        elif choice == '4':
            print("\n--- OPTIMAL Simulation ---")
            simulate_optimal(ref_string, num_frames)
        elif choice == '5':
            print("\n--- SECOND CHANCE Simulation ---")
            simulate_second_chance(ref_string, num_frames)
        elif choice == '6':
            main() # restart
            return
        elif choice == '7':
            print("Exiting simulator. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, please select from 1-7.")

if __name__ == "__main__":
    main()
