from collections import defaultdict

# Function to parse input grammar
def parse_grammar():
    grammar = defaultdict(list)
    print("Enter grammar productions (e.g., A -> aB | ε). Type 'END' to finish:\n")

    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        if '->' not in line:
            print("Invalid format. Use A -> aB | ε")
            continue
        head, body = line.split('->')
        head = head.strip()
        productions = body.strip().split('|')
        for prod in productions:
            grammar[head].append(prod.strip())

    return grammar

# Recursive function to compute FIRST set
def compute_first(symbol, grammar, FIRST, terminals):
    # If symbol is a terminal, its FIRST is itself
    if symbol in terminals:
        return {symbol}

    # If FIRST already computed, return it
    if FIRST[symbol]:
        return FIRST[symbol]

    for production in grammar[symbol]:
        if production == 'ε':
            FIRST[symbol].add('ε')
        else:
            for i in range(len(production)):
                sym = production[i]
                temp_first = compute_first(sym, grammar, FIRST, terminals)
                FIRST[symbol].update(temp_first - {'ε'})
                if 'ε' not in temp_first:
                    break
                if i == len(production) - 1:
                    FIRST[symbol].add('ε')

    return FIRST[symbol]

def main():
    grammar = parse_grammar()

    non_terminals = list(grammar.keys())
    terminals = set()

    # Identify terminals
    for prods in grammar.values():
        for prod in prods:
            for ch in prod:
                if not ch.isupper() and ch != 'ε':
                    terminals.add(ch)

    FIRST = defaultdict(set)

    # Compute FIRST for each non-terminal
    for nt in non_terminals:
        compute_first(nt, grammar, FIRST, terminals)

    # Display results
    print("\nFIRST Sets:")
    for nt in non_terminals:
        print(f"FIRST({nt}) = {{ {', '.join(FIRST[nt])} }}")

if __name__ == "__main__":
    main()
