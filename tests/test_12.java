import java.io.*;

class GoGo {
	String a;
    
	GoGo() { System.out.println("Constructor called"); }
}

class Hii {
	public static void main(String[] args)
	{
		// this would invoke default constructor.
		GoGo go1;
        go1 = new GoGo();

        GoGo go2 = new GoGo();

	}
}