package com.beginnersbook.string;

public class LongToString {
    public static void main(String[] args) {
        
        /* Method 1: using valueOf() method
         * of String class.
         */
        long lvar = 123;
        String str = String.valueOf(lvar);
        System.out.println("String is: "+str);
        
        /* Method 2: using toString() method 
         * of Long class
         */
        long lvar2 = 200;
        String str2 = Long.toString(lvar2);
        System.out.println("String2 is: "+str2);
    }
}
