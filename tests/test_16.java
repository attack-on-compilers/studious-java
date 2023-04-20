public class fileIOWrite {
    int fopen(String filename, String mode){;}
    void fprintf(int f, String message){;}
    void fclose(int f){;}

    public void main(String[] args) {
        int file = fopen("newfile", "w");
        fprintf(file, "This is a statement");
        fclose(file);
    }
}
