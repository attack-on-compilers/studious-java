// Single and multi-dimensional arrays, both local and instance variables
public class test_4 {
    int a;
    int b,c,d;
    int e = 5;
    int i[][] = new int[5][5];
    int j[][] = new int[5][];
    int[][] k = new int[5][];
    float l[];
    char m[] = new char[5], n[] = new char[5], o=6;
    double[][] q = new double[5][10], r = new double[5][], t={{4}};
    public static void main(String[] args) {
        int a;
        int b,c,d;
        int e = 5;
        int i[][] = new int[5][5];
        int j[][] = new int[5][];
        int[][] k = new int[5][];
        float l[];
        char m[] = new char[5], n[] = new char[5], o=6;
        double[][] q = new double[5][10], r = new double[5][];
        q[4][5] = 5.0;      //Array access on LHS
        q[7][8] = q[4][5];  //Array access on RHS
    }
}
