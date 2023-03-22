// import java.io.*;

class GoGo {
	String a;
	String name;
    
	GoGo(String name, int id)
	{ 
		this.name =name;
		System.out.println("Constructor called");
	}
}

class Hii {
	public static void main(String[] args)
	{
		// this would invoke default constructor.
		GoGo go1;
        go1 = new GoGo("Yo");

        // GoGo go2 = new GoGo();

	}
}