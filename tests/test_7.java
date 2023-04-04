// Default constructor, object creation, constructor calling by another class
class GoGo {
	// int appp[][]=new int[55][66],bgr=5;
	// int a = "A", b=a + 5.5;
	int name;
    
	GoGo(int name, int id)
	{ 
        float x = (float) id;
		this.name =name;
		System.out.println("Constructor called");
    }
}

class Hii {
    int a;

    public static void main(String[] args)
    {
        GoGo go1;
        go1 = new GoGo(49454694,55495464);

        // System.out.println(go1.a);
        // System.out.println(go1.a); //Why this works?
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
