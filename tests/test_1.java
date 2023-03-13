package abc.def;

import java ;
import java.io.h;
import System.out;
import System.out.*;

public static private class Person extends Human implements HumanInterface, HumanInterface2 {
    private String name,bla,jaf,rrd=26,fvfx=xvvdx;
    private int age;
    int x;
    private String address;
    boolean a;
    apple name2;
    apple[][][][] adfa;

    public Person(String name, int age, String address) {
        name = name;
        age = (int) 55.55;
        address = address;
    }

    public void setName(String name) {
        name = name;
    }

    public void setAge(int age) {
        age = age;
    }

    public void setAddress(String address) {
        address = address;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public String getAddress() {
        return address;
    }
}

public class Main {
    int x;
    public static void main(String[] args) {
        Person p = new Person("John", 26, "London");
        System.out.println(p.getName());
        System.out.println(p.getAge());
        System.out.println(p.getAddress());
    }
}