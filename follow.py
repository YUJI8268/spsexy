from collections import defaultdict

# Function to compute FIRST sets
def compute_first(grammar):
    first = defaultdict(set)

    def first_of(symbol):
        if symbol not in grammar:
            return {symbol}  # Terminal
        if symbol in first and first[symbol]:
            return first[symbol]

        result = set()
        for production in grammar[symbol]:
            if production == ['ε']:
                result.add('ε')
                continue
            for sym in production:
                sym_first = first_of(sym)
                result.update(sym_first - {'ε'})
                if 'ε' not in sym_first:
                    break
            else:
                result.add('ε')
        first[symbol] = result
        return result

    for non_terminal in grammar:
        first_of(non_terminal)

    return first

# Function to compute FOLLOW sets
def compute_follow(grammar, start_symbol):
    follow = defaultdict(set)
    first = compute_first(grammar)

    follow[start_symbol].add('$')  # End marker

    while True:
        updated = False
        for lhs in grammar:
            for production in grammar[lhs]:
                for i, B in enumerate(production):
                    if B in grammar:  # B is non-terminal
                        follow_before = follow[B].copy()
                        # Check symbols after B
                        for symbol in production[i+1:]:
                            first_of_symbol = first[symbol]
                            follow[B].update(first_of_symbol - {'ε'})
                            if 'ε' in first_of_symbol:
                                continue
                            break
                        else:
                            follow[B].update(follow[lhs])
                        if follow_before != follow[B]:
                            updated = True
        if not updated:
            break
    return follow

# Example usage
grammar = {
    'S': [['A', 'B']],
    'A': [['a'], ['ε']],
    'B': [['b']]
}

start_symbol = 'S'
follow_sets = compute_follow(grammar, start_symbol)

print("FOLLOW sets:")
for non_terminal, follow in follow_sets.items():
    print(f"FOLLOW({non_terminal}) = {follow}")
