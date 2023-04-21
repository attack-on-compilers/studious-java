// Test 35 : Recursion, Function calls with multiple arguments
public class test_6 {
    static int x;
    static long fib(int n)
    {
        if(n==0)
            return 0;
        if(n==1)
            return 1;
        // System.out.println("Fibonacci of "+n+" is "+(fib(n-1)+fib(n-2)));
        return fib(n-1)+fib(n-2);
    }

    static long fact(int n)
    {
        if(n==0)
            return 1;
        return n*fact(n-1);
    }
    static int printargs(int x1, int x2, int x3, int x4, int x5, int x6, int x7, int x8, int x9, int x10)
    {
        System.out.println("x1="+x1+" x2="+x2+" x3="+x3+" x4="+x4+" x5="+x5+" x6="+x6+" x7="+x7+" x8="+x8+" x9="+x9+" x10="+x10);
        return 0; 
    }
    public static void main(String args[])
    {
        short n=20;
        byte m=15;
        long a=fib(n);                  // Typecasting short to int
        long b=fib(10);
        long c=fact(m);                 // Typecasting byte to int
        System.out.println("\nFibonacci of "+n+" is "+a +" and of "+ b+" is " + b + " and factorial of "+15+" is "+c);
        printargs(1,2,3,4,5,6,7,8,9,10);
    }
}
