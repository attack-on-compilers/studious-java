public class test_15 {

    static int fun(int x){
        if (x<=0)
            return x;
        System.out.println("fun "+x);
        return fun(x-1);
    }
    public static void main(String[] args) {
        long a =100;
        long b = 5;
        System.out.println("a="+a+" b="+b);
        long c = a*b;
        long d = a+c;
        long e = a+b+c+d;
        long f = a+b+c+d+e;
        long g = a*b*c*d*e*f*a*b*c*d*e*f;
        long h =100;                         // Uncommenting will make it work
        long h =100;                         // Uncommenting will make it work
        // long x = fun(0);
        // long h = fun(1);
        int h1 =fun(fun(fun(1)));
        int h11 =fun(fun(1));
        int h2 =fun(55);
        // System.out.println(h);
        System.out.println(h1);
        System.out.println(h11);
        System.out.println(h2);
        // int i = 999;
        System.out.println("a="+a+" b="+b+" c="+c+" d="+d+" e="+e +" f="+f+" g="+g +" h1="+h1 + " h2="+h2);
        // System.out.println("apple "+5+"apple "+a);
        
        // return;
    }
}
