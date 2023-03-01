public interface Calculator {
    int subtract(int x, int y);
    int multiply(int x, int y);
    int divide(int x, int y) throws ArithmeticException;
    int modulo(int x, int y);
    int bitwiseAnd(int x, int y);
    int bitwiseOr(int x, int y);
    int bitwiseXor(int x, int y);
    int leftShift(int x, int y);
    int rightShift(int x, int y);
    int unsignedRightShift(int x, int y);
}
