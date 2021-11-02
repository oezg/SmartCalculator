from collections import deque, defaultdict


variables = {}
operators = set("^*/+-()")
priority = defaultdict(int)
priority.update({"+": 1, "-": 1, "*": 2, "/": 2, "^": 3})


def to_infix(assign: str) -> deque:
    infix = deque()
    assign = assign.replace(" ", "")
    assign = "(" + assign + ")"
    assign = deque(assign)
    operand = ""
    while assign:
        symbol = assign.popleft()
        if symbol in operators:
            if operand:
                infix.append(operand)
                operand = ""
            infix.append(symbol)
        else:
            operand += symbol
    return infix


def valid(assign: deque) -> bool:
    if assign.count("(") == assign.count(")"):
        last_term = ""
        for term in assign:
            if term in operators:
                if term in {"+", "-", "*", "/", "^"} and last_term == term:
                    return False
                last_term = term
                continue
            elif term.isalpha():
                last_term = term
                continue
            elif term.isdigit():
                last_term = term
                continue
            else:
                return False
        return True
    return False


def to_postfix(infix: deque) -> deque:
    stack = deque()
    postfix = deque()
    while infix:
        token = infix.popleft()
        if token == "(":
            stack.append(token)
        elif token == ")":
            while stack:
                top_of_stack = stack.pop()
                if top_of_stack == "(":
                    break
                postfix.append(top_of_stack)
            else:
                print("Opening parenthesis not found!")
                break
        elif token in priority:
            while priority[stack[-1]] >= priority[token]:
                postfix.append(stack.pop())
            stack.append(token)
        elif token.isalnum():
            postfix.append(token)
        else:
            print("Invalid expression")
            break
    else:
        return postfix


def ints_vars(raw_data: deque) -> deque:
    interpretation = deque()
    for token in raw_data:
        if token in operators:
            interpretation.append(token)
        elif token.isdecimal():
            interpretation.append(int(token))
        elif token.isalpha():
            if token in variables:
                interpretation.append(variables[token])
            else:
                print("Unknown variable")
                break
        else:
            print("Invalid expression")
            break
    else:
        return interpretation


def evaluate(postfix: deque) -> int:
    stack = deque()
    while postfix:
        token = postfix.popleft()
        if isinstance(token, int):
            stack.append(token)
        elif token in operators:
            assert len(stack) >= 2
            left_operand = stack.pop()
            right_operand = stack.pop()
            if token == "^":
                result_of_operation = right_operand ** left_operand
            elif token == "*":
                result_of_operation = right_operand * left_operand
            elif token == "/":
                result_of_operation = right_operand // left_operand
            elif token == "+":
                result_of_operation = right_operand + left_operand
            elif token == "-":
                result_of_operation = right_operand - left_operand
            stack.append(result_of_operation)
        else:
            print("Invalid expression")
            break
    else:
        return stack[-1]


def do_math(assign):
    infix = to_infix(assign)
    if valid(infix):
        postfix = to_postfix(infix)
        if postfix:
            postfix = ints_vars(postfix)
            if postfix:
                result = evaluate(postfix)
                print(result)
    else:
        print("Invalid expression")


def assignment(assign):
    index = assign.find('=')
    identifier = assign[:index].strip()
    if identifier.isalpha():
        value = assign[index + 1:].strip()
        if value.isdecimal():
            variables[identifier] = int(value)
        elif value.isalpha():
            if value in variables:
                variables[identifier] = variables[value]
            else:
                print("Unknown variable")
        else:
            print("Invalid assignment")
    else:
        print("Invalid identifier")


def main():
    while True:
        entry = input()
        if not entry:
            continue
        elif entry.startswith("/"):
            if entry[1:] == "exit":
                print("Bye!")
                break
            elif entry[1:] == "help":
                print("The program calculates any expression with four operations,"
                      "including the use of parentheses and variable assignments.")
            else:
                print("Unknown command")
        elif entry.find('=') > 0:
            assignment(entry)
        elif entry in variables:
            print(variables[entry])
        else:
            try:
                value = int(entry)
            except ValueError:
                do_math(entry)
            else:
                print(value)


if __name__ == "__main__":
    main()
