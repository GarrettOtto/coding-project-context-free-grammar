# Name: Garrett Otto
# Student ID: W01389350
# Date: 10/28/2025
# --- Task 1: Regular Grammar Validator ---
def is_regular_grammar(productions):
    """
    Check if a grammar is regular.
    
    Args:
        productions (list): List of tuples (left_side, right_side_list)
            Example: [("S", ["a", "A"]), ("A", ["b", "∧"])]
    
    Returns:
        bool: True if grammar is regular, False otherwise
    """
    # --- Implementation Here ---
    # Iterate through each production rule in the provided list
    for production in productions:
        # Each production is a tuple: (LHS, RHS)
        # e.g., ("S", ["a", "A"])
        lhs = production[0]
        rhs = production[1]
        
        # Checking LHS and seeing if it is a single uppercase letter
        if not (len(lhs) == 1 and lhs.isupper()):
            return False
        
        # Checking RHS length 1
        rhsLen = len(rhs)
        if rhsLen == 1:
            # Checking empty string
            if rhs[0] == "∧":
                continue
                
            # Checking if there is a single terminal
            if rhs[0].islower():
                continue
                
            # Checking if there is a single non-terminal
            if rhs[0].isupper():
                return False

        # Checking RHS length 2
        elif rhsLen == 2:
            # If there is a length 2, we need a terminal and a non-terminal in that order
            # Checking if the 0 index is terminal
            is_terminal = rhs[0].islower()
            # Checking if the 1 index is non-terminal
            is_non_terminal = rhs[1].isupper()
            
            # If both are true, continue
            if is_terminal and is_non_terminal:
                # This rule is valid, continue
                continue
            else:
                return False

        # Anything else is invalid
        else:
            return False
            
    # If we get here the grammar is valid
    return True
    # --- Implementation Here ---
    pass
# --- Task 1: Regular Grammar Validator ---

# --- Task 2: Balanced Parentheses Recognition ---
def recursive_parser(s):
    """
    Recursive descent parser to check if string is balanced.
    
    Args:
        s (str): Input string
    
    Returns:
        bool: True if string is balanced, False otherwise
    """
    # --- Implementation Here ---
    # Using this helper function to check if subS matches the grammar for S
    def check(subS):
        # Case: Empty string
        if not subS:
            return True
        
        # Case: S -> (S)
        # We are slicing off the first and last characters and calling the check function recursively
        if (subS.startswith("(") and subS.endswith(")") and check(subS[1:-1])):
            return True
        
        # Case: S -> [S]
        # Same as above but with square brackets
        if (subS.startswith("[") and subS.endswith("]") and check(subS[1:-1])):
            return True
        
        # Case: S -> {S}
        # Same as above but with curly braces
        if (subS.startswith("{") and subS.endswith("}") and check(subS[1:-1])):
            return True

        # --- Check the "concatenation" rule (Backtracking) ---

        # Rule: S -> SS
        # We try every possible split of the string into two parts
        for i in range(1, len(subS)):
            # Split the string into two parts
            left = subS[:i]
            right = subS[i:]
            # Check if both parts are valid
            if check(left) and check(right):
                return True
        
        # If none of the rules matched, return False
        return False

    # Call the helper function with the full string
    return check(s)
    # --- Implementation Here ---
    pass
# --- Task 2: Balanced Parentheses Recognition ---

# --- Part B: Stack-Based Algorithm ---
def stack_checker(s):
    """
    Stack-based balanced parentheses checker.
    
    Args:
        s (str): Input string
    
    Returns:
        bool: True if string is balanced, False otherwise
    """
    # --- Implementation Here ---
    stack = []
    
    for char in s:
        # Push opening symbol onto stack
        if char in "([{":
            stack.append(char)

        # Closing symbol
        elif char in ")]}":
            # If stack is empty there is no opening symbol
            if not stack:
                return False
            
            # Getting the top of the stack
            top = stack.pop()

            # Case ")"
            if char == ")" and top != "(":
                return False
            # Case "]"
            elif char == "]" and top != "[":
                return False
            # Case "}"
            elif char == "}" and top != "{":
                return False

    # Done checking
    # If the stack is empty, return true
    if not stack:
        return True
    else:
        return False
    # --- Implementation Here ---
    pass
# --- Part B: Stack-Based Algorithm ---

# --- Part C: Experimental Comparison ---
def grammarTests():
    # Creating a list of tests that we can use later
    tests = [
        # S -> a, A | A -> b | A -> ∧ | VALID
        ([("S", ["a", "A"]), ("A", ["b"]), ("A", ["∧"])], True),
        # S -> a, S | S -> b | VALID
        ([("S", ["a", "S"]), ("S", ["b"])], True),
        # ∧ | VALID
        ([], True),
        # SA -> a | INVALID - Multiple non-terminals on LHS
        ([("SA", ["a"])], False),
        # S -> A, a | INVALID - RHS has a non-terminal first
        ([("S", ["A", "a"])], False),
        # S -> A, B | INVALID - RHS has two non-terminals
        ([("S", ["A", "B"])], False),
        # S -> A | INVALID - RHS has only a non-terminal
        ([("S", ["A"])], False),
        # S -> a, b, s | INVALID - RHS has more than 2 symbols
        ([("S", ["a", "b", "S"])], False),
    ]
    # Running tests
    testNum = 0
    for answer, expected in tests:
        testNum += 1
        result = is_regular_grammar(answer)
        # Checking if the test passed or failed:
        passOrFail = ""
        if result == expected:
            passOrFail = "PASS"
        else:
            passOrFail = "FAIL"
        # Printing results:
        print(f"--- Test #{testNum} ---\nGrammar: {answer}\nisValid={result}\nExpected={expected} -> {passOrFail}")
    pass

def test_balanced_parentheses():
    test_cases = [
        ("()", True), ("[]", True), ("{}", True),
        ("([{}])", True), ("((()))", True), ("()[]", True),
        ("(]", False), ("([)]", False), ("((())", False),
        ("", True)
    ]
    
    for s, expected in test_cases:
        # Printing whether or not the function passed:
        recursiveResult = recursive_parser(s)
        stackResult = stack_checker(s)
        passOrFail = ""
        if (recursiveResult == expected and stackResult == expected):
            passOrFail = "PASS"
        else:
            passOrFail = "FAIL"

        print(f"'{s}': RecursiveParser={recursive_parser(s)}, "
              f"StackChecker={stack_checker(s)}, Expected={expected} -> {passOrFail}")

if __name__ == "__main__":
    grammarTests()
    test_balanced_parentheses()
# --- Part C: Experimental Comparison ---