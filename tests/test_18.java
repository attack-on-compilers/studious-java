public class test_18 {
    public static void main(String args[])
    {
        int a[] = new int[100];
        // int c = 55;
        // int b = c;
        // System.out.println(a + "     " + b);
        // int xxxxx=7777;
        // int e = a[0];
        // System.out.println(a +"   " +e);
        a[7] = 5;
        a[3] = a[7];
        // int yyyyyy=8888;
        int b=a[7];
        System.out.println(b);
        int c = a[3];
        int d = a[1];
        System.out.println(b+"    "+a+"    "+c+"    "+d);
        // a[7] = 5;
        // a[5] = a[9];
    }
}
