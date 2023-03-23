// Bubble Sort in Java using Arrays and Functions 
public class test_6 {
    public static void main(String[] args) {
        int[] arr = { 5, 2, 9, 1, 5, 6 };

        // Displaying the original array
        System.out.println("Original Array: ");
        display(arr);

        // Sorting array elements using bubble sort
        bubbleSort(arr);

        // Displaying sorted array
        System.out.println("\nSorted Array: ");
        display(arr);
    }

    public static void bubbleSort(int arr[]) {
        int n = 6;

        for (int i = 0; i < n - 1; i++) {
            return;
        }
    }

    public static void display(int arr[]) {
        for (int i = 0; i < 6; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }
}