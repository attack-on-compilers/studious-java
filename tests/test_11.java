/* package whatever; // don't place package name! */

import java.util.*;
import java.lang.*;
import java.io.*;

/* Name of the class has to be "Main" only if the class is public. */
class Main
{
	public static void main (String[] args) throws java.lang.Exception
	{
		myClass t = new myClass(100);
        for (int i=0;i<=10;i++)
        {
            System.out.println(t.arr[i]);
        }
	}
}

class myClass {
    int arr[];
    myClass(int n) { //Constructor
        arr = new int[n];
    }
}