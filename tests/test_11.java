// Test 40: File Output using fprintf, fopen, fclose
public class test_11 {
    // We need these empty function declarations to make the code compile
    int fopen(String filename, String mode){return 0;}
    void fprintf(int f, String message){;}
    void fclose(int f){;}

    public void main(String[] args) {
        int file = fopen("newfile", "w");
        fprintf(file, "This is a statement");
        fprintf(file, "This is a statement with newlines!\n\n\\n Changes the line!\n");
        fprintf(file, "This is a statement\nahsdkhskd");
        fprintf(file, "Escapes work!\t\\\\\\\\\\\\\\\\\\\\\\");
        fprintf(file, "This is a statement\nahsdkhskd\n\n\n");
        fclose(file);
        file = fopen("newfile", "a");       // Append to the file
        fprintf(file, "Appended this statement!\n");
        fclose(file);
    }
}
