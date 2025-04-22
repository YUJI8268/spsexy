def macro_processor(source_code):
    macro_definitions = {}
    expanded_code = []
    inside_macro = False
    macro_name = ""
    macro_body = []
    macro_expansion_count = 0
    macro_defined = 0

    # First pass: Define macros
    processed_code = []
    for line in source_code:
        stripped = line.strip()

        if stripped == "MACRO":
            inside_macro = True
            macro_body = []
            continue

        if inside_macro:
            if stripped == "MEND":
                macro_definitions[macro_name] = macro_body.copy()
                macro_defined += 1
                inside_macro = False
                macro_name = ""
            elif not macro_name:
                macro_name = stripped
            else:
                macro_body.append(stripped)
        else:
            processed_code.append(stripped)

    # Second pass: Expand macros
    for line in processed_code:
        if line in macro_definitions:
            expanded_code.extend(macro_definitions[line])
            macro_expansion_count += 1
        else:
            expanded_code.append(line)

    stats = {
        "total_input_lines": len(source_code),
        "total_output_lines": len(expanded_code),
        "macros_defined": macro_defined,
        "macro_expansions": macro_expansion_count
    }

    return source_code, expanded_code, stats
source_code = [
    "MACRO",
    "HELLO",
    "LOAD A, MSG",
    "PRINT A",
    "MEND",
    "START",
    "HELLO",
    "MOV B, C",
    "HELLO",
    "END"
]

# Run the macro processor
input_code, output_code, stats = macro_processor(source_code)

# Display Input Source Code
print("Input Source Code:")
for line in input_code:
    print(line)

# Display Output Source Code
print("\nOutput Source Code (After Macro Expansion):")
for line in output_code:
    print(line)

# Display Statistical Output
print("\nStatistical Output:")
for key, value in stats.items():
    print(f"{key.replace('_', ' ').title()}: {value}")
