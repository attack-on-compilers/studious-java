// FUnction calls, type check on return type, field variables, recursive calls
public class test_3 {
    static int a = 1;
    static int b = 2;
    static int c = a + b;
    static double d = 1.0;
    static double e = 2;            // Field variables work
    public static int foo(int x, double y) {
        int a = 1;
        int b = 2;
        int c = a + b;
        double d = 1.0;
        double e = 2;
        System.out.println(c+d*e);
        foo(a,d);                   // Recursive call works
        // return 5.5;              // Is an error because of implicit conversion from double to int in return type
        // return "Test";           // Is an error because of implicit conversion from String to int in return type
        return 5;
    }
    public static void main(String[] args) {
        // test_3 t = new test_3();
        int z = foo(5,6.5);     // Return type of foo matches the type of z
        foo(5,4);               // Implicit conversion from int to double
        // foo(4.0,45);             // Error because of implicit conversion from double to int
        double h = foo(foo(4,5),5.5);
        h*=z;
        System.out.println(h);
        System.out.println(a);      //Can access static field variables
        // return 5;                // Error because of implicit conversion from int to void in return type
        return;
    }
}
