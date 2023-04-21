// Test 31: Relational, Logical Operators with if statements
public class test_31 {
    public static void main(String args[])
    {
        int x=5;
        // Relational Operators
        if(x==5)
            System.out.println("x==5");
        else
            System.out.println("NOT x==5");
        if(x==7)
            System.out.println("x==7");
        else
            System.out.println("NOT x==7");
        if(x!=5)
            System.out.println("x!=5");
        else
            System.out.println("NOT x!=5");
        if(x!=7)
            System.out.println("x!=7");
        else
            System.out.println("NOT x!=7");
        if(x>5)
            System.out.println("x>5");
        else
            System.out.println("NOT x>5");
        if(x>7)
            System.out.println("x>7");
        else
            System.out.println("NOT x>7");
        if(x<5)
            System.out.println("x<5");
        else
            System.out.println("NOT x<5");
        if(x<7)
            System.out.println("x<7");
        else
            System.out.println("NOT x<7");
        if(x>=5)
            System.out.println("x>=5");
        else
            System.out.println("NOT x>=5");
        if(x>=7)
            System.out.println("x>=7");
        else
            System.out.println("NOT x>=7");
        if(x<=5)
            System.out.println("x<=5");
        else
            System.out.println("NOT x<=5");
        if(x<=7)
            System.out.println("x<=7");
        else
            System.out.println("NOT x<=7");

        // Logical Operators

        if(x==5 && x==7)
            System.out.println("x==5 && x==7");
        else
            System.out.println("NOT x==5 && x==7");
        if(x==7 && x==5)
            System.out.println("x==7 && x==5");
        else
            System.out.println("NOT x==7 && x==5");
        if(x==5 && x==5)
            System.out.println("x==5 && x==5");
        else
            System.out.println("NOT x==5 && x==5");
        if(x==7 && x==7)
            System.out.println("x==5 && x==5");
        else
            System.out.println("NOT x==5 && x==5");
        if(x==5 || x==7)
            System.out.println("x==5 || x==7");
        else
            System.out.println("NOT x==5 || x==7");
        if(x==7 || x==5)
            System.out.println("x==7 || x==5");
        else
            System.out.println("NOT x==7 || x==5");
        if(x==5 || x==5)
            System.out.println("x==5 || x==5");
        else
            System.out.println("NOT x==5 || x==5");
        if(x==7 || x==7)
            System.out.println("x==7 || x==7");
        else
            System.out.println("NOT x==7 || x==7");

        if(!(x==5))
            System.out.println("!(x==5)");
        else
            System.out.println("NOT !(x==5)");
        if(!(x==7))
            System.out.println("!(x==7)");
        else
            System.out.println("NOT !(x==7)");

        //Some limited boolean support as well
        if(true && false)
            System.out.println("true && false");
        else
            System.out.println("NOT true && false");
        if(false && true)
            System.out.println("false && true");
        else
            System.out.println("NOT false && true");
        if(true && true)
            System.out.println("true && true");
        else
            System.out.println("NOT true && true");
        if(false && false)
            System.out.println("false && false");
        else
            System.out.println("NOT false && false");
        if(true || false)
            System.out.println("true || false");
        else
            System.out.println("NOT true || false");
        if(false || true)
            System.out.println("false || true");
        else
            System.out.println("NOT false || true");
        if(true || true)
            System.out.println("true || true");
        else
            System.out.println("NOT true || true");
        if(false || false)
            System.out.println("false || false");
        else
            System.out.println("NOT false || false");

        // Slightly more complex boolean expressions
        if(!(x==5) || !(x==7))
            System.out.println("!(x==5) || !(x==7)");
        else
            System.out.println("NOT !(x==5) || !(x==7)");
        if(!(x==7) || !(x==5))
            System.out.println("!(x==7) || !(x==5)");
        else
            System.out.println("NOT !(x==7) || !(x==5)");
        if(!(x==5) || !(x==5))
            System.out.println("!(x==5) || !(x==5)");
        else
            System.out.println("NOT !(x==5) || !(x==5)");
        if(!(x==7) || !(x==7))
            System.out.println("!(x==7) || !(x==7)");
        else
            System.out.println("NOT !(x==7) || !(x==7)");
        if(x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5)
            System.out.println("x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5");
        else
            System.out.println("NOT x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5 && x==5");
    }
}
