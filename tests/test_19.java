// Default constructor, object creation, constructor calling by another class
class GoGo {
	int a,b;
    // Hii h;
	GoGo(int a, int id)
	{
		System.out.println("Constructor called");
	}

	public static void main(String[] args)
	{
        
		GoGo a = new GoGo(7,5);
        // int x = a.b;
	}

    public void foo()
    {
        int arr[] = new int[5];
        int x = arr[7];
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
