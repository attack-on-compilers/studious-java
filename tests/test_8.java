// Test 37: Multidimensional arrays work
public class test_8 {
    static int foo(int a)
    {
        return a*a;
    }
    public static void main(String args[])
    {
        int xdim = 7, ydim = 5+3, zdim = foo(3), wdim=11;   // The dimensions need not be constants
        int a[][][][] = new int[xdim][ydim][zdim][wdim];
        int i =0;
        while(i<xdim){
            int j=0;
            while(j<ydim){
                int k=0;
                while(k<zdim){
                    int l=0;
                    while(l<wdim){
                        a[i][j][k][l] = i+j+k+l;
                        int x= a[i][j][k][l];
                        System.out.print((a[i][j][k][l])+ " ");
                        l=l+1;
                    }
                    k=k+1;
                    System.out.println("");
                }
                j=j+1;
                System.out.println("");
            }
            i=i+1;
            System.out.println("");
        }
    }
}
