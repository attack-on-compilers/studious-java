// for, while, do-while, switch, nested blocks, variable declaration
public class test_5 {

    static int x;
    public static void main(String args[])
    {
        for (int i = 0; i < 10; i++) {
            // int j = i + 1;
            System.out.println(i+55);
        }
        int i; //Not an error as j and i are declared in the for loop
        i = 0;
        int j = 0;
        while (i < 10) {
            System.out.println(j);
            i+=1;
        }
        double k = 0;
        do {
            System.out.println(j);
            k+=1;
            continue;
        } while (k < 10);
        {
            int s = 100;
            // int i; // An error as i is already declared in the main method
            {
                int r;
                {
                    int t; // Nested blocks work
                }
                int t; //Not an error as t is declared in the aboveblock
            }
        }
        int s; //Not an error as above s is declared in the block 
        int x =1; //Not an error as x is declared in the class

        // switch (x) {
        //     case 1:
        //         int y; //Not an error as y is declared in the switch
        //         break;
        //     case 2:
        //         int y2;
        //         // int y; //An error as y is already declared in the switch
        //         break;
        //     default:
        //         int y3;
        //         // int y2; //An error as y2 is already declared in the switch
        //         break;
        // }

        while (true) {
            while(true){
                int z;
            }
        }
        
    }
}
