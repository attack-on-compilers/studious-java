// Basic test case- Hello World!
public class test_1
{
    static int foo(int x, int y)
    {
        int z = x+y;
        return z;
    }
    public static void main(String[] args)
    {
        {
            int x=100;
            {
                x = 555;
                {
                    {
                        {
                            x=55;
                        }
                    }
                }
                int y=6555;
            }
            // int x = 5;
        }

        int t = (int) 5.0;
        // int x = 5;
        System.out.println(5);
        foo(4,5);
        foo(1,2);
    }
}