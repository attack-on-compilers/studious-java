// Test 32: While loop, do-while loop, break, continue
public class test_32 {
    public static void main(String args[])
    {
        int i=0;
        while(i<=10)
        {
            int j=i*i;
            System.out.println("Hello "+(i++)+" "+j);
        }
        // System.out.println("Hello "+j);                     // Error as j is not defined
        do
        {
            int j=i*i;                                      //Blocks work
            System.out.println("Do Hello "+(i++)+" "+j);
        }while(i<=15);

        do
        {
            int j=i*i;
            System.out.println("Final Do Hello "+(++i)+" "+j);
        }
        while(i<=1);
        
        while(i<=30)
        {
            int j=i*i;
            if(i>=20)
                break;                                          //Break works
            System.out.println("Break Hello "+(i++)+" "+j);
        }

        while (i<=30)
        {
            int j=i*i;
            if(i%2==0)
            {
                i++;
                continue;                                       //Continue works
            }
            System.out.println("Continue Hello "+(i++)+" "+j);
        }

        // while (i>0)
        //     System.out.println("Hello "+(i++));                 // Uncomment for Infinite loop
    }
}
