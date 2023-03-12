public class operators {
    int add(int x, int y) {
        return x + y;
    }
    int subtract(int x, int y) {
        return x - y;
    }
    int multiply(int x, int y) {
        return x * y;
    }
    int divide(int x, int y) throws ArithmeticException {
        return x / y;
    }
    int modulo(int x, int y) {
        return x % y;
    }
    int bitwiseAnd(int x, int y) {
        return x & y;
    }
    int bitwiseOr(int x, int y) {
        return x | y;
    }
    int bitwiseXor(int x, int y) {
        return x ^ y;
    }
    int leftShift(int x, int y) {
        return x << y;
    }
    int rightShift(int x, int y) {
        return x >> y;
    }
    int unsignedRightShift(int x, int y) {
        return x >>> y;
    }
    int increment(int x) {
        return ++x;
    }
    int decrement(int x) {
        return --x;
    }
    int negate(int x) {
        return -x;
    }
    int complement(int x) {
        return ~x;
    }
    boolean equal(int x, int y) {
        return x == y;
    }
    boolean notEqual(int x, int y) {
        return x != y;
    }
    boolean lessThan(int x, int y) {
        return x < y;
    }
    boolean lessThanOrEqual(int x, int y) {
        return x <= y;
    }
    boolean greaterThan(int x, int y) {
        return x > y;
    }
    boolean greaterThanOrEqual(int x, int y) {
        return x >= y;
    }
    boolean logicalAnd(int x, int y) {
        return x != 0 && y != 0;
    }
    boolean logicalOr(int x, int y) {
        return x != 0 || y != 0;
    }
    boolean logicalNot(int x) {
        return ! (x != 0);
    }
    boolean bitwiseAnd(int x, int y) {
        return (x & y) != 0;
    }
    boolean bitwiseOr(int x, int y) {
        return (x | y) != 0;
    }
    boolean bitwiseXor(int x, int y) {
        return (x ^ y) != 0;
    }
    boolean bitwiseNot(int x) {
        return ~x != 0;
    }
    boolean leftShift(int x, int y) {
        return (x << y) != 0;
    }
    boolean rightShift(int x, int y) {
        return (x >> y) != 0;
    }
    boolean unsignedRightShift(int x, int y) {
        return (x >>> y) != 0;
    }
    boolean add(int x, int y) {
        return x + y != 0;
    }
    void bye() {
        System.out.println("Bye!");
    }
}