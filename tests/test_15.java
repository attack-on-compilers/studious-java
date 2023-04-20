public class test_15 {

    static int fun(int x){
        if (x==1)
            fun(x+2);
        System.out.println("fun"+x);
        return (x+1);
    }
    public static void main(String[] args) {
        // long a =100;
        // int b = 5;
        // long c = a*b;
        // long d = a+c;
        // long e = a+b+c+d;
        // long f = a+b+c+d+e;
        // long g = a*b*c*d*e*f*a*b*c*d*e*f;
        int h = fun(fun(1));
        // System.out.println(h);
        // int i = 999;
        // System.out.println("a="+a+" b="+b+" c="+c+" d="+d+" e="+e +" f="+f+" g="+g+" h="+h);
        // System.out.println("apple "+5+"apple "+a);
        
        // return;
    }
}
