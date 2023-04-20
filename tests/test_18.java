public class test_18 {
    public static void main(String args[])
    {
        // int a[] = new int[100];
        // a[7] = 5;
        // a[3] = a[7];
        // int b=a[7];
        // System.out.println(b);
        // int c = a[3];
        // int d = a[1];
        // System.out.println(b+"    "+a+"    "+c+"    "+d);
        int xdim = 5, ydim = 3, zdim = 7;
        int a[][][] = new int[xdim][ydim][zdim];
        int i =0;
        while(i<xdim){
            int j=0;
            while(j<ydim){
                int k=0;
                while(k<zdim){
                    a[i][j][k] = i+j+k;
                    int x= a[i][j][k];
                    System.out.print((a[i][j][k])+ " ");
                    k=k+1;
                }
                j=j+1;
                System.out.println("");
            }
            i=i+1;
            System.out.println("\n");
        }
        // int c = 55;
        // int b = c;
        // System.out.println(a + "     " + b);
        // int xxxxx=7777;
        // int e = a[0];
        // System.out.println(a +"   " +e);
        // int yyyyyy=8888;
        // a[7] = 5;
        // a[5] = a[9];
    }
}
