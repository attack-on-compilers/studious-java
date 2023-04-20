// for, while, do-while, switch, nested blocks, variable declaration
public class test_5 {

    static int x;

    public static void main(String args[]) {
        int i; // Not an error as j and i are declared in the for loop
        i = 0;
        int j = 0;
        while (i < 10) {
            System.out.println("From while " + i);
            while (j < 10) {
                // System.out.println("nested while " + j);
                j = j + 1;
                int k = i * j + i + j;
                System.out.println("Nested While: " + k);
            }
            j = 5;
            i = i + 1;
        }

        int k = 0;

        do {
            System.out.println(k);
            k = k + 1;
            continue;
            System.out.println("This will not be printed");
        } while (k < 10);

        {
            int s = 100;
            // int i; // An error as i is already declared in the main method
            {
                int r;
                {
                    int t; // Nested blocks work
                }
                int t; // Not an error as t is declared in the aboveblock
            }
        }
        int s; // Not an error as above s is declared in the block
        int x = 1; // Not an error as x is declared in the class
    }
}
