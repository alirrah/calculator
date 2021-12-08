#include <iostream>
#include <string>
#include <cmath>
using namespace std;

template <typename T>
class List
{
private:
    template <typename E>
    class node
    {
    public:
        E data;
        node *next;
    };
    node<T> *head;
    int size;

public:
    List()
    {
        head = nullptr;
        size = 0;
    }
    int getSize() const
    {
        return size;
    }
    bool isEmpty() const
    {
        return size == 0;
    }
    T first() const
    {
        if (isEmpty())
            throw "The data structure is empty.";
        return head->data;
    }
    void addFirst(T data)
    {
        node<T> *tmp = new node<T>();
        tmp->data = data;
        tmp->next = head;
        head = tmp;
        size++;
    }
    T removeFirst()
    {
        if (isEmpty())
            throw "The data structure is empty.";
        T answer = head->data;
        node<T> *tmp = head;
        head = head->next;
        size--;
        delete tmp;
        return answer;
    }
};

template <typename T>
class Stack
{
private:
    List<T> list;

public:
    int size() const
    {
        return list.getSize();
    }
    bool isEmpty() const
    {
        return list.isEmpty();
    }
    void push(T data)
    {
        list.addFirst(data);
    }
    T top()
    {
        return list.first();
    }
    T pop()
    {
        return list.removeFirst();
    }
};

int value(char);
string infixToPostfix(string);
string evalPostfix(string);

int main()
{
    return 0;
}

int value(char c)
{
    if (c == '^')
        return 3;
    if (c == '/' || c == '*' || c == 'a')
        return 2;
    if (c == '+' || c == '-')
        return 1;
    return -1;
}

string infixToPostfix(string s)
{
    try
    {
        Stack<char> st;
        string result;
        for (int i = 0; i < s.length(); i++)
        {
            char c = s[i];
            if (c == ' ')
                continue;
            else if (isdigit(c) || c == '.')
                result += c;
            else
            {
                switch (c)
                {
                case '(':
                    st.push('(');
                    break;
                case '[':
                    st.push('[');
                    break;
                case ')':
                    while (st.top() != '(')
                    {
                        if (result != "" && result[result.size() - 1] != ' ')
                            result += ' ';
                        char tmp = st.pop();
                        if (tmp == 'a')
                            result += "-1 *";
                        else
                            result += tmp;
                    }
                    st.pop();
                    break;
                case ']':
                    while (st.top() != '[')
                    {
                        if (result != "" && result[result.size() - 1] != ' ')
                            result += ' ';
                        char tmp = st.pop();
                        if (tmp == 'a')
                            result += "-1 *";
                        else
                            result += tmp;
                    }
                    st.pop();
                    break;
                default:
                    if (c == '-' && (i == 0 || s[i - 1] == '(' || s[i - 1] == '*' || s[i - 1] == '-'))
                    {
                        st.push('a');
                    }
                    else
                    {
                        if (c == '^')
                        {
                            while (!st.isEmpty() && value(s[i]) < value(st.top()))
                            {
                                if (result != "" && result[result.size() - 1] != ' ')
                                    result += ' ';
                                char tmp = st.pop();
                                if (tmp == 'a')
                                    result += "-1 *";
                                else
                                    result += tmp;
                            }
                        }
                        else
                        {
                            while (!st.isEmpty() && value(s[i]) <= value(st.top()))
                            {
                                if (result != "" && result[result.size() - 1] != ' ')
                                    result += ' ';
                                char tmp = st.pop();
                                if (tmp == 'a')
                                    result += "-1 *";
                                else
                                    result += tmp;
                            }
                        }
                        if (result != "" && result[result.size() - 1] != ' ')
                            result += ' ';
                        st.push(c);
                    }
                }
            }
        }
        while (!st.isEmpty())
        {
            if (st.top() == '(' || st.top() == '[')
                throw "The number of parentheses is incorrect.";
            if (result != "" && result[result.size() - 1] != ' ')
                result += ' ';
            char tmp = st.pop();
            if (tmp == 'a')
                result += "-1 *";
            else
                result += tmp;
        }
        return result;
    }
    catch (...)
    {
        return "error";
    }
}

string evalPostfix(string exp)
{
    try
    {
        List<string> history;
        Stack<double> stack;
        int start, last;
        for (start = 0; start < exp.size(); start++)
        {
            for (last = start; exp[last] != ' ' && last < exp.size(); last++)
            {
            }
            string tmp = "";
            for (int i = start; i < last; i++)
            {
                tmp += exp[i];
            }
            if (tmp == "+")
            {
                stack.push(stack.pop() + stack.pop());
            }
            else if (tmp == "-")
            {
                stack.push(-1 * (stack.pop() - stack.pop()));
            }
            else if (tmp == "*")
            {
                stack.push(stack.pop() * stack.pop());
            }
            else if (tmp == "/")
            {
                double x = stack.pop(), y = stack.pop();
                if (!x)
                    throw "Dividing the number by zero is invalid.";
                stack.push(y / x);
            }
            else if (tmp == "^")
            {
                double answer, x = stack.pop(), y = stack.pop();
                answer = pow(y, x);
                if (isnan(answer))
                    throw "The answer is imaginary";
                stack.push(answer);
            }
            else
            {
                int counter = 0;
                for (char character : tmp)
                    if (character == '.')
                        counter++;
                if (counter > 1)
                    throw "The number is wrong.";
                stack.push(stod(tmp));
            }
            start = last;
            for (; exp[start + 1] == ' ' && start < exp.size(); start++)
            {
            }
        }
        return to_string(stack.top());
    }
    catch (...)
    {
        return "error";
    }
}