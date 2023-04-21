// Test 33: if-else-if ladder, nested if-else-if ladder, block declarations
public class test_4 {
    public static void main(String args[])
    {
        int a = 100;
        if (a == 100)
            System.out.println("a == 100");
        if (a == 200)
            System.out.println("a == 200");
        else if(a<200)
        {
            int b = 5;
            System.out.println("a < 200");
            if(a>50)
            {
                System.out.println("a > 50");
                if (a+b==105)
                    System.out.println("a+b == 105");
                else
                    System.out.println("a+b != 105");
                b=10;
            }
            else
            {
                System.out.println("a < 50");
                if (a+b==105)
                    System.out.println("a+b == 105");
                else
                    System.out.println("a+b != 105");
                b=20;
            }
            if(b==10)
                System.out.println("b == 10");
            else if(b==20)
                System.out.println("b == 20");
        }
        else
            System.out.println("a > 200");
        int b=55;
        if (a+b==155)
            System.out.println("a+b == 155");
        else
            System.out.println("a+b != 155");

    }
}
