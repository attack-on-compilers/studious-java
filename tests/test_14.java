public class test_14 {
    public int main(String[] args) {
        int t = testprint(1, 2, 3);
        int t1 = testprint2(1, 2);
        System.out.print("ANSWER: " + t + "\tnexr\t" + t1 + "\t");
        System.out.println("totot");
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
