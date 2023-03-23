// Default constructor, object creation, constructor calling by another class
class GoGo {
	String a = "A", b=a + 5.5;
	String name;
    
	GoGo(String name, int id)
	{ 
        float x = (float) id;
		this.name =name;
		System.out.println("Constructor called");
        GoGo go1 = new GoGo("Yo", 3);
	}

	public static void main(String[] args)
	{
        int a=968;
        System.out.println(a);
		Hii go1 = new Hii();
        GoGo go2 = new GoGo("Yo", 3);
        go2.a = "Yo"; // Need to fix this
        go1.a=5;
	}
}

class Hii {
    int a;
    public static void main(String[] args)
    {
        Hii h = new Hii(); //Default constructor

        GoGo go1;
        go1 = new GoGo("",5);
        go1.a = "555";

        System.out.println(go1.a);
        System.out.println(go1.ab); //Why this works?


    }
}
