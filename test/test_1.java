import java.io.OutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.Arrays;
import java.io.BufferedWriter;
import java.util.InputMismatchException;
import java.io.IOException;
import java.util.TreeSet;
import java.util.ArrayList;
import java.io.Writer;
import java.io.OutputStreamWriter;
import java.util.Comparator;
import java.util.Collections;
import java.io.InputStream;
/**
 * Built using CHelper plug-in
 * Actual solution is at the top
 *
 * @author Alex
 */
public class Main {
    public static void main(String[] args) {
        InputStream inputStream = System.in;
        OutputStream outputStream = System.out;
        InputReader in = new InputReader(inputStream);
        OutputWriter out = new OutputWriter(outputStream);
        TheNewRestaurant solver = new TheNewRestaurant();
        solver.solve(1, in, out);
        out.close();
    }
    static class TheNewRestaurant {
        int R2 = 51;
        double[][][] MEM = new double[R2][2 * R2][2 * R2];
        boolean[][][] MEMMEM = new boolean[R2][2 * R2][2 * R2];
        int MAX = 50050 + 1;
        double section(double h, double r) {
            return (h < r) ? Math.sqrt(r * r - h * h) : 0;
        }
        double g(double x, double h, double r) {
            return .5 * (Math.sqrt(1 - x * x / (r * r)) * x * r + r * r * Math.asin(x / r) - 2 * h * x);
        }
        double area(double x0, double x1, double h, double r) {
            double s = section(h, r);
            return g(Math.max(-s, Math.min(s, x1)), h, r) - g(Math.max(-s, Math.min(s, x0)), h, r); // integrate the area
        }
        double area(double x0, double x1, double y0, double y1, double r) {
            if (y0 > y1) {
                double temp = y0;
                y0 = y1;
                y1 = temp;
            }
            if (y0 < 0) {
                if (y1 < 0) return area(x0, x1, -y0, -y1, r);
                return area(x0, x1, 0, -y0, r) + area(x0, x1, 0, y1, r);
            }
            return area(x0, x1, y0, r) - area(x0, x1, y1, r);
        }
        double area(int x0, int x1, int y0, int y1, int cx, int cy, int r) {
            if (y0 >= y1) return 0;
            if (x0 >= x1) return 0;
            x0 -= cx;
            x1 -= cx;
            y0 -= cy;
            y1 -= cy;
            if (-x0 == x1 && x1 == r) {
                if (MEMMEM[r][y0 + R2][y1 + R2])
                    return MEM[r][y0 + R2][y1 + R2];
            }
            double res = area(x0, x1, y0, y1, r);
            if (-x0 == x1 && x1 == r) {
                MEMMEM[r][y0 + R2][y1 + R2] = true;
                MEM[r][y0 + R2][y1 + R2] = res;
            }
            return res;
        }
        public void solve(int testNumber, InputReader in, OutputWriter out) {
            int n = in.readInt(), q = in.readInt();
            Circle[] circles = new Circle[n];
            for (int i = 0; i < circles.length; i++)
                circles[i] = new Circle(in.readInt(), in.readInt(), in.readInt(), i);
            Rectangle[] rectangles = new Rectangle[q];
            for (int i = 0; i < rectangles.length; i++)
                rectangles[i] = new Rectangle(in.readInt(), in.readInt(), in.readInt(), in.readInt());
            ArrayList<Point>[] pointsByX = new ArrayList[MAX];
            for (int i = 0; i < pointsByX.length; i++) pointsByX[i] = new ArrayList<>();
            for (Rectangle rectangle : rectangles) for (Point p : rectangle.points) pointsByX[p.x].add(p);
            for (ArrayList<Point> al : pointsByX)
                Collections.sort(al, new Comparator<Point>() {
                    public int compare(Point a, Point b) {
                        return Integer.compare(a.y, b.y);
                    }
                });
            Arrays.sort(circles, new Comparator<Circle>() {
                public int compare(Circle a, Circle b) {
                    return Integer.compare(a.lowX, b.lowX);
                }
            });
            int ciclesPtr = 0;
            TreeSet<Circle> intersectLine = new TreeSet<>(new Comparator<Circle>() {
                public int compare(Circle a, Circle b) {
                    if (a.lowY != b.lowY) return Integer.compare(a.lowY, b.lowY);
                    return Integer.compare(a.idx, b.idx);
                }
            });
            FT ft = new FT();
            for (int sweepLine = 0; sweepLine < MAX; sweepLine++) {
                TreeSet<Circle> newIntersectLine = new TreeSet<>(new Comparator<Circle>() {
                    public int compare(Circle a, Circle b) {
                        if (a.lowY != b.lowY) return Integer.compare(a.lowY, b.lowY);
                        return Integer.compare(a.idx, b.idx);
                    }
                });
                for (Circle c : intersectLine) {
                    if (c.highX <= sweepLine) {
                        for (int y = Math.max(0, c.lowY); y < MAX && y < c.highY; y++) {
                            ft.add(y, area(Math.max(0, c.lowX), sweepLine, y, y + 1, c.x, c.y, c.r));
                        }
                    } else newIntersectLine.add(c);
                }
                intersectLine = newIntersectLine;
                while (ciclesPtr < circles.length && circles[ciclesPtr].lowX < sweepLine)
                    intersectLine.add(circles[ciclesPtr++]);
                double soFar = 0;
                Circle curCircle = (intersectLine.isEmpty() ? null : intersectLine.first());
                int maxY = 0;
                for (Point p : pointsByX[sweepLine]) {
                    Circle incomplete = null;
                    while (curCircle != null) {
                        soFar += area(Math.max(0, curCircle.lowX), sweepLine, maxY, p.y, curCircle.x, curCircle.y, curCircle.r);
                        if (curCircle.highY > p.y && incomplete == null) incomplete = curCircle;
                        Circle higher = intersectLine.higher(curCircle);
                        if (higher == null || higher.lowY >= p.y) break;
                        curCircle = higher;
                    }
                    if (incomplete != null) curCircle = incomplete;
                    maxY = p.y;
                    p.res = ft.get(p.y - 1) + soFar;
                }
            }
            for (Rectangle rectangle : rectangles) {
                double ans = 0;
                for (Point p : rectangle.points) ans += p.sign * p.res;
                out.printLine(ans);
            }
        }
        public class FT {
            int SQRT = 225;
            double[] value = new double[SQRT * SQRT];
            double[] parent = new double[SQRT];
            double get(int to) {
                double res = 0;
                for (int i = 0; i < parent.length; i++) {
                    int start = i * SQRT;
                    int idx = (i + 1) * SQRT - 1;
                    if (idx > to) {
                        for (int j = start; j <= to; j++) res += value[j];
                        break;
                    }
                    res += parent[i];
                }
                return res;
            }
            public void add(int at, double change) {
                value[at] += change;
                int idx = at / SQRT;
                double tot = 0;
                for (int i = 0; i < SQRT; i++) tot += value[i + SQRT * idx];
                parent[idx] = tot;
            }
        }
        class Point {
            int x;
            int y;
            int sign;
            double res;
            public Point(int x, int y, int sign) {
                this.x = x;
                this.y = y;
                this.sign = sign;
            }
        }
        class Rectangle {
            int x1;
            int y1;
            int x2;
            int y2;
            ArrayList<Point> points = new ArrayList<>();
            public Rectangle(int x1, int y1, int x2, int y2) {
                this.x1 = x1;
                this.y1 = y1;
                this.x2 = x2;
                this.y2 = y2;
                points.add(new Point(x1, y1, 1));
                points.add(new Point(x2, y2, 1));
                points.add(new Point(x1, y2, -1));
                points.add(new Point(x2, y1, -1));
            }
        }
        class Circle {
            int idx;
            int x;
            int y;
            int r;
            int lowX;
            int highX;
            int lowY;
            int highY;
            public Circle(int x, int y, int r, int idx) {
                this.x = x;
                this.y = y;
                this.r = r;
                this.idx = idx;
                lowX = x - r;
                highX = x + r;
                lowY = y - r;
                highY = y + r;
            }
        }
    }
    static class OutputWriter {
        private final PrintWriter writer;
        public OutputWriter(OutputStream outputStream) {
            writer = new PrintWriter(new BufferedWriter(new OutputStreamWriter(outputStream)));
        }
        public OutputWriter(Writer writer) {
            this.writer = new PrintWriter(writer);
        }
        public void print(Object... objects) {
            for (int i = 0; i < objects.length; i++) {
                if (i != 0)
                    writer.print(' ');
                writer.print(objects[i]);
            }
        }
        public void printLine(Object... objects) {
            print(objects);
            writer.println();
        }
        public void close() {
            writer.close();
        }
    }
    static class InputReader {
        private InputStream stream;
        private byte[] buf = new byte[1024];
        private int curChar;
        private int numChars;
        private InputReader.SpaceCharFilter filter;
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
        public boolean isSpaceChar(int c) {
            if (filter != null)
                return filter.isSpaceChar(c);
            return isWhitespace(c);
        }
        public static boolean isWhitespace(int c) {
            return c == ' ' || c == '\n' || c == '\r' || c == '\t' || c == -1;
        }
        public interface SpaceCharFilter {
            public boolean isSpaceChar(int ch);
        }
    }
} 