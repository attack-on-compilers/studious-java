// Default constructor, object creation, constructor calling by another class
class GoGo {
	int a,b;
    // Hii h;
	GoGo(int a, int id)
	{
        this.a = id;
        // h = new Hii();
        // h.a = 5;
        // int s = h
        int x = this.a;
        foo(1,2);
		System.out.println("Constructor called"+x);
	}

	public static void main(String[] args)
	{
        
		GoGo a = new GoGo(7,5);
        // a.b = 5;
        int x = a.a;

        a.foo(1,2);

        System.out.println(x);
	}

    public void foo(int a, int b)
       {
        int p = this.a + a + b;
            System.out.println("Hello" +p);
        int x = b;

        int arr[] = new int[5];
        // int x = arr[7];
    }
}

class Hii {
    int a;
}

class Temp {
    int foo() {
        Hii h = new Hii();
        h.a = 5;
        int s = h.a;
        return 1;
    }
}
