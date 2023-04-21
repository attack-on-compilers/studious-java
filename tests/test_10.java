// Default constructor, object creation, constructor calling by another class, function call!
class GoGo {
	int a,b;
	GoGo(int a, int b)
	{
        this.a = a;
        this.b = b;
        System.out.println("Constructor called for GoGo, this.a = " + (this.a) + " this.b = " + (this.b));
	}

	public static void main(String[] args)
	{
        Hii h = new Hii();              // Default constructor called
        System.out.println("h.a = " + (h.a)+ " h.b = " + (h.b) );
		GoGo g = new GoGo(7,5);
        System.out.println("g.a = " + (g.a)+ " g.b = " + (g.b) );
        System.out.print("Function call on object g succeded and returned: ");
        System.out.println((g.foo(1,2)));                 // Funtion call on object g
	}

    public int foo(int a, int b)
       {
        System.out.println("Inside foo! a = " + a+ " b = " + b + " this.a = " + (this.a) + " this.b = " + (this.b));
        return a+b+this.a+this.b;
    }
}

class Hii {
    int a,b;                          // Default constructor called
}
