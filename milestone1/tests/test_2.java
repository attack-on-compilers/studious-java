package test;

import java.util.Scanner;

public class LinkedList {
    private Node head;

    public LinkedList() {
        head = null;
    }

    public void add(int value) {
        Node newNode = new Node(value);
        if (head == null) {
            head = newNode;
        } else {
            Node current = head;
            while (current.getNext() != null) {
                current = current.getNext();
            }
            current.setNext(newNode);
        }
    }

    public void remove(int value) {
        if (head == null) {
            return;
        }
        if (head.getValue() == value) {
            head = head.getNext();
        } else {
            Node current = head;
            while (current.getNext() != null && current.getNext().getValue() != value) {
                current = current.getNext();
            }
            if (current.getNext() != null) {
                current.setNext(current.getNext().getNext());
            }
        }
    }

    public boolean contains(int value) {
        Node current = head;
        while (current != null) {
            if (current.getValue() == value) {
                return true;
            }
            current = current.getNext();
        }
        return false;
    }
}

class Node {
    private int value;
    private Node neIxt;

    public Node(int value) {
        value = value;
        next = null;
    }

    public int getValue() {
        return value;
    }

    public void setNext(Node next) {
        next = next;
    }

    public Node getNext() {
        return next;
    }
}
