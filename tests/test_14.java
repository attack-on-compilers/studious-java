public class test_14 {
    public int main(String[] args) {
        testprint(1, 2, 3);
        testprint2(1, 2);
        return 1;
    }

    public int testprint(int x, int y, int z) {
        System.out.println(x);
        System.out.println(y);
        System.out.println(z);
        return x+y+z;
    }

    public int testprint2(int x, int y) {
        System.out.println(x);
        System.out.println(y);
        return x*y;
    }
}
