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

int main()
{
    return 0;
}