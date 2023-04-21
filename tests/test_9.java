// Test 38: Object creation, constructor calls, this keyword
class test_9
{
    int a,b;
    public static void main(String args[])
    {
        test_9 obj1 = new test_9(4,5);     //Object creation, constructor called
        System.out.println("obj1.a = " + (obj1.a)+ " obj1.b = " + (obj1.b) );
        obj1.a = 10;
        obj1.b = 20;
        System.out.println("obj1.a = " + (obj1.a)+ " obj1.b = " + (obj1.b));    //Values updated
        System.out.print("obj1.a * obj1.b = ");
        System.out.println((obj1.muliply()));                 //Function call on object
    }
    
    test_9(int a, int b)
    {
        System.out.println("Constructor called");
        this.a = square(a);         // this works in constructor
        this.b = b;
        int x = muliply();          // The object pointer is passed to the function on call
        System.out.println("Result of multiplication, x = " + x);   // Correct value of x
    }
    int muliply()
    {
        return this.a*this.b;       // this works with function calls
    }
    int square(int a)
    {
        return a*a;
    }
}