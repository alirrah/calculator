import math
import os


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
                l = l[:i] + [str(stack.top)] + l[i:]
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


while True:
    sentence = input('Enter the phrase (exit to end the program) : ')
    if sentence == 'exit':
        break
    sentence = infixToPostfix(sentence)
    if sentence == 'error':
        print(sentence)
    else:
        sentence = evalPostfix(sentence)
        if sentence == 'error':
            print(sentence)
        else:
            print('\nHistory : ')
            for i in sentence:
                print(i)
            print('\nAnswer is : ' + sentence[-1])
    os.system('pause')
    os.system('cls')
