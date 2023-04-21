// Test 36: println, print, print with escape sequences, println with empty string, println with concatenation, println with integer, println with variable, println with expression, println with function call
public class test_36 {
    static long foo(int a)
    {
        return a*a;
    }
    public static void main()
    {
        int x=100;
        System.out.println("Hello World!");
        System.out.print("Hello World!");
        System.out.print("\\Hello\t\\World!\n");
        System.out.println("");
        System.out.println("Hello"+"World!");
        System.out.println(5);
        System.out.println(x);
        System.out.println((x*5));  // To print expressions, wrap in parentheses
        System.out.println("This was x: "+(x++)+" and this is x now:"+x);
        System.out.println("Square of " +x+ " is: "+(foo(x)));  // Print return values directly by wrapping in parentheses
    }
}
