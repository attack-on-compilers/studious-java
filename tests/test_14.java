// Single and multi-dimensional arrays, both local and instance variables
public class test_14 {
    public static void main(String[] args) {
        int a;
        int b,c,d;
        int e = 5;
        int i[][] = new int[5][5];
        int j[][] = new int[5][];
        int[][] k = new int[5][];
        int l[];
        int m[] = new int[5], n[] = new int[5], o=6;
        int [][] q = new int[5][10], r = new int[5][];
        q[4][5] = 5;      //Array access on LHS
        q[7][8] = q[4][5];  //Array access on RHS
        System.out.println((q[7][8]));
    }
}
