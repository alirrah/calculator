import math
import os


class nodeStack:

    def __init__(self, value, next):
        self.value = value
        self.next = next


class nodeTree:
    def __init__(self, data, right, left):
        self.data = data
        self.right = right
        self.left = left


class Stack:

    def __init__(self):
        self.head = nodeStack("head", None)
        self.size = 0

    def Size(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def top(self):
        if self.isEmpty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value

    def push(self, value):
        node = nodeStack(value, self.head.next)
        self.head.next = node
        self.size += 1

    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value


def priority(char):
    if char == '^':
        return 3
    if char == '/' or char == '*' or char == 'a':
        return 2
    if char == '+' or char == '-':
        return 1
    return -1


def infixToPostfix(pharse):
    try:
        stack = Stack()
        result = ''
        for i in range(len(pharse)):
            c = pharse[i]
            if c == ' ':
                continue
            elif c.isnumeric() or c == '.':
                result += c
            else:
                if c == '(':
                    stack.push('(')
                elif c == '[':
                    stack.push('[')
                elif c == ')':
                    while stack.top() != '(':
                        if result != "" and result[-1] != ' ':
                            result += ' '
                        tmp = stack.pop()
                        if tmp == 'a':
                            result += '-1 *'
                        else:
                            result += tmp
                    stack.pop()
                elif c == ']':
                    while stack.top() != '[':
                        if result != "" and result[-1] != ' ':
                            result += ' '
                        tmp = stack.pop()
                        if tmp == 'a':
                            result += '-1 *'
                        else:
                            result += tmp
                    stack.pop()
                else:
                    if c == '-' and (i == 0 or pharse[i - 1] == '(' or pharse[i - 1] == '*' or pharse[i - 1] == '-'):
                        stack.push('a')
                    else:
                        if c == '^':
                            while not stack.isEmpty() and priority(c) < priority(stack.top()):
                                if result != "" and result[-1] != ' ':
                                    result += ' '
                                tmp = stack.pop()
                                if tmp == 'a':
                                    result += '-1 *'
                                else:
                                    result += tmp
                        else:
                            while not stack.isEmpty() and priority(c) <= priority(stack.top()):
                                if result != "" and result[-1] != ' ':
                                    result += ' '
                                tmp = stack.pop()
                                if tmp == 'a':
                                    result += '-1 *'
                                else:
                                    result += tmp
                        if result != '' and result[-1] != ' ':
                            result += ' '
                        stack.push(c)
        while not stack.isEmpty():
            if stack.top() == '(' or stack.top() == '[':
                raise Exception('The number of parentheses is incorrect.')
            if result != '' and result[-1] != ' ':
                result += ' '
            tmp = stack.pop()
            if tmp == 'a':
                result += '-1 *'
            else:
                result += tmp
        return result
    except:
        return 'error'


def postfixToInfix(list):
    changer = Stack()
    for k in list:
        if k in ['+', '-', '*', '/', '^']:
            b = changer.pop()
            a = changer.pop()
            add_str = '(' + a + k + b + ')'
            changer.push(add_str)
        else:
            changer.push(k)
    return changer.pop()


def evalPostfix(pharse):
    try:
        stack = Stack()
        l = pharse.split(' ')
        history = []
        history.append(postfixToInfix(l))
        i = 0
        while i < len(l):
            item = l[i]
            if item == '+':
                stack.push(stack.pop() + stack.pop())
                for __ in range(3):
                    l.pop(i)
                    i -= 1
                i += 1
                l = l[:i] + [str(stack.top())] + l[i:]
                history.append(postfixToInfix(l))
            elif item == '-':
                stack.push(-1 * (stack.pop() - stack.pop()))
                for __ in range(3):
                    l.pop(i)
                    i -= 1
                i += 1
                l = l[:i] + [str(stack.top())] + l[i:]
                history.append(postfixToInfix(l))
            elif item == '*':
                stack.push(stack.pop() * stack.pop())
                for __ in range(3):
                    l.pop(i)
                    i -= 1
                i += 1
                l = l[:i] + [str(stack.top())] + l[i:]
                history.append(postfixToInfix(l))
            elif item == '/':
                x, y = stack.pop(), stack.pop()
                stack.push(y / x)
                for __ in range(3):
                    l.pop(i)
                    i -= 1
                i += 1
                l = l[:i] + [str(stack.top())] + l[i:]
                history.append(postfixToInfix(l))
            elif item == '^':
                x, y = stack.pop(), stack.pop()
                stack.push(math.pow(y, x))
                for __ in range(3):
                    l.pop(i)
                    i -= 1
                i += 1
                l = l[:i] + [str(stack.top())] + l[i:]
                history.append(postfixToInfix(l))
            else:
                counter = 0
                for char in item:
                    if char == '.':
                        counter += 1
                if counter > 1:
                    raise Exception('The number is wrong.')
                stack.push(float(item))
            i += 1
        return history
    except:
        return 'error'


def makeTree(l):
    stack = Stack()
    tmp = l.split(' ')
    for i in range(len(tmp)):
        tmp[i] = nodeTree(tmp[i], None, None)
    for item in tmp:
        if item.data == '*' or item.data == '/' or item.data == '^' or item.data == '+' or item.data == '-':
            first = stack.pop()
            second = stack.pop()
            item.left = second
            item.right = first
            stack.push(item)
        else:
            stack.push(item)
    return stack.top()


def print_tree(root, data="data", left="left", right="right"):
    def display(root, data=data, left=left, right=right):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % getattr(root, data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))
            s = '%s' % getattr(root, data)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))
            s = '%s' % getattr(root, data)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = display(getattr(root, left))
        right, m, q, y = display(getattr(root, right))
        s = '%s' % getattr(root, data)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * \
            '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + \
            (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + \
            [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    lines, *_ = display(root, data, left, right)
    for line in lines:
        print(line)


while True:
    sentence = input('Enter the phrase (exit to end the program) : ')
    if sentence == 'exit':
        break
    sentence = infixToPostfix(sentence)
    tmp = sentence
    print()
    if sentence == 'error':
        print(sentence, end='\n\n')
    else:
        sentence = evalPostfix(sentence)
        if sentence == 'error':
            print(sentence, end='\n\n')
        else:
            tree = makeTree(tmp)
            print_tree(tree)
            print('\nHistory : ')
            for i in sentence:
                print(i)
            print('\nAnswer is : ' + sentence[-1], end='\n\n')
    os.system('pause')
    os.system('cls')
