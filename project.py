import math


class nodeStack:

    def __init__(self, value, next):
        self.value = value
        self.next = next


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


def evalPostfix(pharse):
    try:
        stack = Stack()
        l = pharse.split(' ')
        i = 0
        while i < len(l):
            item = l[i]
            if item == '+':
                stack.push(stack.pop() + stack.pop())
            elif item == '-':
                stack.push(-1 * (stack.pop() - stack.pop()))
            elif item == '*':
                stack.push(stack.pop() * stack.pop())
            elif item == '/':
                x, y = stack.pop(), stack.pop()
                stack.push(y / x)
            elif item == '^':
                x, y = stack.pop(), stack.pop()
                stack.push(math.pow(y, x))
            else:
                counter = 0
                for char in item:
                    if char == '.':
                        counter += 1
                if counter > 1:
                    raise Exception('The number is wrong.')
                stack.push(float(item))
            i += 1
        return stack.top()
    except:
        return 'error'
