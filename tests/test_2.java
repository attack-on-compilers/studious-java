// Simple expressiona and implicit conversion
public class test_2 {
    public static void main(String[] args) {
        int a = 1;
        // int a = 1; // Is an error because of redeclaration
        int b = 2;
        int c = a + b + 7;
        System.out.println(c);
        double d = 1.0;
        double e = 2;       // Implicit conversion from int to double
        double f = d + e;
        System.out.println(f);
        char g = 'a';
        char h = 'b';
        int i = (g * h);    // Implicit conversion from char to int
        System.out.println(i);
        double j = 'a' + 45 ;
        double k = 'a' + 45.0 ;
        // float l = 'a' + 45.0 ; // Is an error because of implicit conversion from double to float
        float m = 'a' + 45.0f ; // Is not an error
        // int n =5 + 78l; // Is an error, on hold for now
        int o =5 << 4;
        int p =5 << 4; // Is an error
        System.out.println(j+k+m+o+p);
    }
}
