// Test 30: Arithmetic, Increment/Decrement, Bitwise, Assignment Operators
public class test_1 {
    public static void main(String args[])
    {
        // Arithmetic Operators
        int x=45;
        System.out.println("x = "+x);
        int a=7;
        int b=a+7;
        int c=b-a-5;
        int d=c*6+89*0;
        int e=d/5;
        int f=77/5;
        int g=77%5;
        System.out.println("a = "+a+" b = "+b+" c = "+c+" d = "+d+" e = "+e+" f = "+f+" g = "+g);
        // Increment and Decrement Operators, both pre and post
        int h=g++;
        int i=++h;
        int j=--i;
        int k=i--;
        System.out.println("a = "+(++a)+" b = "+b+" c = "+c+" d = "+d+" e = "+e+" f = "+f+" g = "+g+" h = "+h+" i = "+i+" j = "+j+" k = "+k);
        // Bitwise Operators
        int l=777;
        int m=555;
        int n=l&m;
        int o=l|m;
        int p=l^m;
        int q=~l;
        int r=l<<2;
        int s=l>>2;
        int t=l>>>2;
        System.out.println("l = "+l+" m = "+m+" n = "+n+" o = "+o+" p = "+p+" q = "+q+" r = "+r+" s = "+s+" t = "+t);
        // Assignment Operators
        a*=70;
        b/=70;
        c+=70;
        d-=70;
        e&=60;
        f|=30;
        g^=70;
        System.out.println("a = "+a+" b = "+b+" c = "+c+" d = "+d+" e = "+e+" f = "+f+" g = "+g);
    }
}
