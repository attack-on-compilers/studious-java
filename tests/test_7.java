// Default constructor, object creation, constructor calling by another class
class GoGo {
	// String b;
	// int a;
	int appp[][]=new int[55][66],bgr=5;
	String a = "A", b=a + 5.5;
	String name;
    Hii h = new Hii();
    
	GoGo(String name, int id)
	{ 
        float x = (float) id;
		this.name =name;
		System.out.println("Constructor called");
        GoGo go1 = new GoGo("Yo", 3);
	}

	public static void main(String[] args)
	{
		int n=10,m=5;
		GoGo a = new GoGo();
        int app[][][][] = new int[m][6][n][8], c[][], d, e[][][][]=new int[5][n][][], f[]=new int[5];
		f[1]= 5;
        app[1][n][m][4]=5;
		a.b = "Yo";
		System.out.println(a);
		Hii ho1 = new Hii();
        GoGo go2 = new GoGo("Yo", 3);
        go2.a = "Yo"; // Need to fix this
        ho1.a=5;
	}
}

class Hii {
    int a;
    GoGo g = new GoGo("Yo", 3);
	int foo(int a, double b, int[][][] arr[][])
	{
		return 1;
	}
    public static void main(String[] args)
    {
        Hii h = new Hii(); //Default constructor

        GoGo go1;
        go1 = new GoGo("",5);
        go1.b = "555";

        System.out.println(go1.a);
        System.out.println(go1.a); //Why this works?
    }
    double b;
}

class Temp {
    int foo() {
        Hii h = new Hii();
        h.a = 5;
        return 1;
    }
}
