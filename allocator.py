class MemoryBlock:
    def __init__(self, start, size, process_name=None):
        self.start = start
        self.size = size
        self.process_name = process_name

    def __repr__(self):
        return f"[{self.start}-{self.start + self.size - 1}] {self.process_name or 'Free'}"

class Memory:
    def __init__(self, total_size):
        self.total_size = total_size
        self.blocks = [MemoryBlock(0, total_size)]

    def allocate(self, process_name, size):
        for i, block in enumerate(self.blocks):
            if block.process_name is None and block.size >= size:
                new_block = MemoryBlock(block.start, size, process_name)
                self.blocks[i] = new_block
                if block.size > size:
                    self.blocks.insert(i + 1, MemoryBlock(block.start + size, block.size - size))
                print(f"\n Allocated {process_name} ({size} units)")
                return True
        print(f"\n Failed to allocate {process_name} ({size} units) due to fragmentation")
        return False

    def deallocate(self, process_name):
        for block in self.blocks:
            if block.process_name == process_name:
                block.process_name = None
                print(f"\n Deallocated {process_name}")
                return
        print(f"\n Process {process_name} not found")

    def compact(self):
        new_blocks = []
        current_address = 0
        for block in self.blocks:
            if block.process_name is not None:
                new_blocks.append(MemoryBlock(current_address, block.size, block.process_name))
                current_address += block.size
        remaining_size = self.total_size - current_address
        if remaining_size > 0:
            new_blocks.append(MemoryBlock(current_address, remaining_size))
        self.blocks = new_blocks
        print("\n Memory Compacted")

    def print_memory(self):
        print("\n Current Memory Layout:")
        for block in self.blocks:
            print(block)
        print()

# --- Interactive Program ---
def main():
    memory = Memory(100)

    # Initial 4 processes
    processes = [("P1", 20), ("P2", 20), ("P3", 30), ("P4", 20)]
    print("\n Initializing Memory with 4 processes:")
    for name, size in processes:
        memory.allocate(name, size)
    memory.print_memory()

    while True:
        print(" Choose an option:")
        print("1.  Add Process")
        print("2.  Delete Process")
        print("3.  Compact Memory")
        print("4.  Show Memory")
        print("5.  Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            name = input("Enter process name: ")
            try:
                size = int(input("Enter process size: "))
                memory.allocate(name, size)
            except ValueError:
                print(" Invalid size.")
        elif choice == '2':
            name = input("Enter process name to delete: ")
            memory.deallocate(name)
        elif choice == '3':
            memory.compact()
        elif choice == '4':
            memory.print_memory()
        elif choice == '5':
            print(" Exiting...")
            break
        else:
            print(" Invalid choice.")
        
        memory.print_memory()

if __name__ == "__main__":
    main()
