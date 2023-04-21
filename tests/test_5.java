// Test 34: Function calls, nested function calls
public class test_5 {
    static int foo(int a, int b)
    {
        return 10*a*b;
    }
    public static void main(String args[])
    {
        int a=foo(1+2,2*2);
        int b=foo(foo(1,2),foo(3,4));                   //Nested function calls
        System.out.println("a="+a+" b="+b);
    }
}
