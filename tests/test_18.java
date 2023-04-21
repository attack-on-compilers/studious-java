
public class test_18 {

  public static void main(String args[]) {
    long nFactorial = factorialProgram(9);
    System.out.println(nFactorial);
  }

  /* Java factorial program with recursion. */
  public static long factorialProgram(long n) {
    if (n <= 1) {
      return 1;
    } else {
      return n * factorialProgram(n - 1);
    }
  }
}
