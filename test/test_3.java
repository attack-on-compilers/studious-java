import java.io.*;
import java.util.*;
public class Main
{
	int find(char[] s, int from, int step, char x)
	{
		for (int i = from; i >= 0 && i < s.length; i += step)
		{
			if (s[i] == x)
			{
				return i;
			}
		}
		return -1;
	}
    boolean fast(String ss)
    {
		char[] s = ss.toCharArray();
		int x = find(s, s.length - 1, -1, 'W');
		int y = find(s, 0, 1, 'B');
		if (x == -1)
		{
			return false;
		}
		if (y == -1)
		{
			return true;
		}
		if (y - x == 1)
		{
			char[] tmp = s.clone();
			tmp[x] = '.';
			if (fast(new String(tmp)))
			{
				return true;
			}
			tmp[x + 1] = 'W';
			if (!fast(reverse(tmp)))
			{
				return true;
			}
			return false;
		}
		int delta = (y - x) / 2 - 1;
		boolean flip;
		if ((y - x) % 2 == 0)
		{
			s[x] = '.';
			s[x + delta] = 'W';
			s[y] = '.';
			s[y - delta] = 'B';
			flip = false;
		}
		else
		{
			s[x] = '.';
			s[x + delta + 1] = 'W';
			s[y] = '.';
			s[y - delta] = 'B';
			flip = true;
			s = reverse(s).toCharArray();
		}
		x = find(s, s.length - 1, -1, 'W');
		y = find(s, 0, 1, 'B');
		long valX = 0;
		long valY = 0;
		for (int i = 0; i < s.length; i++)
		{
			if (s[i] == 'W')
			{
				valX += x - i;
				x--;
			}
			if (s[i] == 'B')
			{
				valY += i - y;
				y++;
			}
		}
		return flip ^ (valX > valY);
	}
	HashMap<String, Boolean> map = new HashMap<>();
	boolean firstWin(String s)
	{
		if (s.indexOf('W') == -1)
		{
			return false;
		}
		if (s.indexOf('B') == -1)
		{
			return true;
		}
		if (map.containsKey(s))
		{
			return map.get(s);
		}
		char[] tmp = s.toCharArray();
		for (int i = 0; i < tmp.length - 1; i++)
		{
			if (tmp[i] == 'W' && tmp[i + 1] != 'W')
			{
				char old = tmp[i + 1];
				tmp[i] = '.';
				tmp[i + 1] = 'W';
				String into = reverse(tmp);
				if (!firstWin(into))
				{
					map.put(s, true);
					return true;
				}
				tmp[i] = 'W';
				tmp[i + 1] = old;
			}
		}
		map.put(s, false);
		return false;
	}
	String reverse(char[] arr)
	{
		int start = arr.length - 1;
		while (arr[start] == '.')
		{
			start--;
		}
		int end = 0;
		while (arr[end] == '.')
		{
			end++;
		}
		char[] buf = new char[start - end + 1];
		for (int i = start; i >= end; i--)
		{
			buf[start - i] = flip(arr[i]);
		}
		return new String(buf);
	}
	char flip(char c)
	{
		if (c == '.')
		{
			return '.';
		}
		return (char) ('B' ^ 'W' ^ c);
	}
	void submit() throws IOException
	{
		int t = Integer.parseInt(in.readLine().trim());
		while (t-- > 0)
		{
			out.println(fast(nextToken()) ? "W" : "B");
		}
	}
	Main() throws IOException
	{
       boolean file = false;
       String filename = "ejemplo005";
		if (file)
		{
            in = new BufferedReader(new FileReader(filename + ".txt"));
            out = new PrintWriter(filename + ".output.txt");
        }
        else
        {
            in = new BufferedReader(new InputStreamReader(System.in));    
            out = new PrintWriter(System.out);
        }
		submit();
		out.close();
	}
	static final Random rng = new Random();
	static final int C = 10;
	public static void main(String[] args) throws IOException
	{
		new Main();
	}
	private BufferedReader in;
        PrintWriter out;
	private byte[] buf = new byte[1 << 14];
	private int bufSz = 0, bufPtr = 0;
	private boolean isTrash(int c)
	{
		return c < 33 || c > 126;
	}
	String nextToken()
	{
            try
            {
                return in.readLine();
            }
            catch (IOException ex)
            {
                System.out.println("Exception happened " + ex);
            }
            return "";
	}
}