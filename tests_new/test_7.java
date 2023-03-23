// Default constructor, object creation, constructor calling by another class
class GoGo {
	String a;
	String name;
    
	GoGo(String name, int id)
	{ 
		// this.name =name;
		System.out.println("Constructor called");
        GoGo go1 = new GoGo("Yo", 3);
	}

	public static void main(String[] args)
	{
        int a=968;
        System.out.println(a);
		Hii go1 = new Hii();
        // go1.a=5;
	}
}

class Hii {
    int a;
    public static void main(String[] args)
    {
        Hii h = new Hii(); //Default constructor

        GoGo go1;
        go1 = new GoGo("",5);

        // System.out.println(go1.a);

    }
}
