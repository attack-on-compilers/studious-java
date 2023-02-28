import java.math.*;
import java.io.*;
import java.util.*;

/**
 * created by vidyut on 2019-07-21
 **/
class GIIKLUB {
    public static void main(String[] args) throws Exception {
        InputReader in = new InputReader(System.in);
        BufferedWriter out = new BufferedWriter(new OutputStreamWriter(System.out));
        int tc = in.readInt();
        for (int t = 0; t < tc; t++) {
            int n = in.readInt();
            long x = in.readLong();
            long a[][] = new long[n][n];
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    a[i][j] = in.readLong();
                }
            }
            long ans = 0l;
            ArrayList<Long>[] dp = new ArrayList[n];
            for (int i = 0; i < dp.length; i++) {
                dp[i] = new ArrayList<>();
            }
            for (int mask = 0; mask < 1 << (n - 1); mask++) {
                boolean r[] = new boolean[n - 1];
                int row = 0;
                for (int i = 0; i < n - 1; i++) {
                    if ((mask & (1  << i)) != 0) {
                        r[i] = true;
                        row++;
                    }
                }
                int i = 0;
                int j = 0;
                long sum = a[0][0];
                for (int k = 0; k < r.length; k++) {
                    if (r[k]) {
                        i++;
                    } else {
                        j++;
                    }
                    sum += a[i][j];
                }
                dp[row].add(sum);
            }
            for (int i = 0; i < dp.length; i++) {
                Collections.sort(dp[i]);
            }
            for (int mask = 0; mask < (1 << (n - 1)); mask++) {
                boolean[] r = new boolean[n - 1];
                int row = 0;
                for (int i = 0; i < r.length; i++) {
                    if ((mask & (1  << i)) != 0) {
                        r[i] = true;
                        row++;
                    }
                }
                int i = 0;
                int j = 0;
                long sum = 0;
                for (int k = 0; k < r.length; k++) {
                    sum += a[n - 1 - i][n - 1 - j];
                    if (r[k]) {
                        i++;
                    } else {
                        j++;
                    }
                }
                ArrayList<Long> list = dp[n - 1 - row];
                int left = 0;
                int right = list.size() - 1;
                long lans = 0L;
                while (left <= right) {
                    int mid = (left + right) >> 1;
                    if (list.get(mid) + sum > x) {
                        right = mid - 1;
                    } else {
                        lans = Math.max(lans, mid + 1);
                        left = mid + 1;
                    }
                }
                ans += lans;
            }
            out.write(Long.toString(ans));
            out.newLine();
        }
        out.close();
    }
}
class InputReader {
    private boolean finished = false;

    private InputStream stream;
    private byte[] buf = new byte[1024];
    private int curChar;
    private int numChars;

    public InputReader(InputStream stream) {
        this.stream = stream;
    }

    public int read() {
        if (numChars == -1)
            throw new InputMismatchException();
        if (curChar >= numChars) {
            curChar = 0;
            try {
                numChars = stream.read(buf);
            } catch (IOException e) {
                throw new InputMismatchException();
            }
            if (numChars <= 0)
                return -1;
        }
        return buf[curChar++];
    }

    public int peek() {
        if (numChars == -1)
            return -1;
        if (curChar >= numChars) {
            curChar = 0;
            try {
                numChars = stream.read(buf);
            } catch (IOException e) {
                return -1;
            }
            if (numChars <= 0)
                return -1;
        }
        return buf[curChar];
    }

    public int readInt() {
        int c = read();
        while (isSpaceChar(c))
            c = read();
        int sgn = 1;
        if (c == '-') {
            sgn = -1;
            c = read();
        }
        int res = 0;
        do {
            if (c < '0' || c > '9')
                throw new InputMismatchException();
            res *= 10;
            res += c - '0';
            c = read();
        } while (!isSpaceChar(c));
        return res * sgn;
    }

    public long readLong() {
        int c = read();
        while (isSpaceChar(c))
            c = read();
        int sgn = 1;
        if (c == '-') {
            sgn = -1;
            c = read();
        }
        long res = 0;
        do {
            if (c < '0' || c > '9')
                throw new InputMismatchException();
            res *= 10;
            res += c - '0';
            c = read();
        } while (!isSpaceChar(c));
        return res * sgn;
    }

    public String readString() {
        int length = readInt();
        if (length < 0)
            return null;
        byte[] bytes = new byte[length];
        for (int i = 0; i < length; i++)
            bytes[i] = (byte) read();
        try {
            return new String(bytes, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            return new String(bytes);
        }
    }

    public static boolean isSpaceChar(int c) {
        return c == ' ' || c == '\n' || c == '\r' || c == '\t' || c == -1;
    }

    private String readLine0() {
        StringBuffer buf = new StringBuffer();
        int c = read();
        while (c != '\n' && c != -1) {
            if (c != '\r')
                buf.appendCodePoint(c);
            c = read();
        }
        return buf.toString();
    }

    public String readLine() {
        String s = readLine0();
        while (s.trim().length() == 0)
            s = readLine0();
        return s;
    }

    public String readLine(boolean ignoreEmptyLines) {
        if (ignoreEmptyLines)
            return readLine();
        else
            return readLine0();
    }

    public BigInteger readBigInteger() {
        try {
            return new BigInteger(readString());
        } catch (NumberFormatException e) {
            throw new InputMismatchException();
        }
    }

    public char readCharacter() {
        int c = read();
        while (isSpaceChar(c))
            c = read();
        return (char) c;
    }

    public double readDouble() {
        int c = read();
        while (isSpaceChar(c))
            c = read();
        int sgn = 1;
        if (c == '-') {
            sgn = -1;
            c = read();
        }
        double res = 0;
        while (!isSpaceChar(c) && c != '.') {
            if (c == 'e' || c == 'E')
                return res * Math.pow(10, readInt());
            if (c < '0' || c > '9')
                throw new InputMismatchException();
            res *= 10;
            res += c - '0';
            c = read();
        }
        if (c == '.') {
            c = read();
            double m = 1;
            while (!isSpaceChar(c)) {
                if (c == 'e' || c == 'E')
                    return res * Math.pow(10, readInt());
                if (c < '0' || c > '9')
                    throw new InputMismatchException();
                m /= 10;
                res += (c - '0') * m;
                c = read();
            }
        }
        return res * sgn;
    }

    public boolean isExhausted() {
        int value;
        while (isSpaceChar(value = peek()) && value != -1)
            read();
        return value == -1;
    }

    public String next() {
        return readString();
    }

    public boolean readBoolean() {
        return readInt() == 1;
    }
}
