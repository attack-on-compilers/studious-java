// Bubble Sort in Java using Arrays and Functions 
public class test_6 {
    public static void main(String[] args) {
        int[] arr = new int[10];
        arr[0] = 1;
        arr[1] = 56;
        arr[2] = 23;
        arr[3] = 12;
        arr[4] = 19;
        arr[5] = -9;
        arr[6] = 2;
        arr[7] = 6;
        arr[8] = 34;
        arr[9] = 0;

        // Displaying the original array
        System.out.println("Original Array: ");
        display(arr);

        // Sorting array elements using bubble sort
        bubbleSort(arr);

        // Displaying sorted array
        System.out.println("Sorted Array: ");
        display(arr);
    }

    public static void bubbleSort(int arr[]) {
        int n = 6;
        int i=1;
        while(i<n-i){
            if(arr[i]>arr[i+1]){
                int temp=arr[i];
                arr[i]=arr[i+1];
                arr[i+1]=temp;
            }
        }
        return;
    }

    public static void display(int arr[]) {
        int i=1;
        while(i<6){
            System.out.print(arr[i] + " ");
            i=i+1;
        }
        System.out.println("");
    }
}