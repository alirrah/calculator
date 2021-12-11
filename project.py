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
