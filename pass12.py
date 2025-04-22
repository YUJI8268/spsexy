import re

# Helper function to extract components from a line (label, opcode, operand)
def parse_line(line):
    # Remove comments and strip extra spaces
    line = line.split(';')[0].strip()
    if not line:
        return None, None, None

    # Pattern to identify labels and opcodes
    label_pattern = r"^[A-Za-z][A-Za-z0-9_]*:"
    label_match = re.match(label_pattern, line)
    label = label_match.group(0)[:-1] if label_match else None

    if label:
        line = line[len(label) + 1:].strip()

    # Extract the opcode and operand (if any)
    parts = line.split()
    opcode = parts[0] if parts else None
    operand = parts[1] if len(parts) > 1 else None

    return label, opcode, operand

def pass_1(assembly_code):
    symbol_table = {}         # To store labels and their addresses
    location_counter = 0      # Start location counter at 0
    address_table = []        # Stores the final address of each instruction
    instructions = []         # Store the instructions without label

    for line in assembly_code:
        label, opcode, operand = parse_line(line)
        
        if label:
            if label in symbol_table:
                print(f"Error: Label '{label}' already defined.")
                return None, None, None  # Return None if there's an error
            symbol_table[label] = location_counter

        if opcode:
            instructions.append((opcode, operand))
            address_table.append(location_counter)
            location_counter += 1  # Increment LC for each instruction

    return symbol_table, address_table, instructions

# Sample assembly input
assembly_code = [
    "START: LOAD 100",
    "MOV R1, R2",
    "ADD R1, 50",
    "HALT",
    "; This is a comment",
    "LOOP: JMP START"
]

# Run Pass 1
symbol_table, address_table, instructions = pass_1(assembly_code)

# Output
print("Symbol Table:")
print(symbol_table)

print("\nAddress Table:")
print(address_table)

print("\nInstructions (without labels):")
print(instructions)
# Pass 1 is a preparatory phase where:
#
#    # The symbol table is built, containing labels and their corresponding memory addresses.
#
#    # The address allocation for instructions is completed, providing placeholders for machine code translation.
#
#    # Pass 1 does not generate executable machine code, but it lays the groundwork for Pass 2, where the actual translation of symbolic instructions into machine code occurs.
#
#    # Without Pass 1, we wouldn’t have the necessary information to handle labels and addresses during the actual code generation in Pass 2, making it a crucial first step in the two-pass assembly process.
