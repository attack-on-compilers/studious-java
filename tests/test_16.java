public class fileIOWrite {
    int fopen(String filename, String mode){;}
    void fprintf(int f, String message){;}
    void fclose(int f){;}

    public void main(String[] args) {
        int file = fopen("newfile", "w");
        fprintf(file, "This is a statement");
        fprintf(file, "This is a statement\n\n\\asdsd\n");
        fprintf(file, "This is a statement\nahsdkhskd");
        fprintf(file, "This is a statement\nahsdkhskd");
        fclose(file);
    }
}
