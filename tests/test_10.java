// If else statements
private class TestIfElse {
    public void main(int score) {
        int x=10;
        score = 44;
        // z =x; Need to sort
        if (score >= 91)
        {
            System.out.println("A");
            // int j=100;
        }
        char grade;
        if (score >= 90) {
            System.out.println("A*");
            grade = 'A';
        } else if (score >= 80) {
            System.out.println("B");
            grade = 'B';
        } else if (score >= 70) {
            System.out.println("C");
            grade = 'C';
        } else if (score >= 60) {
            System.out.println("D");
            grade = 'D';
        } else if (score >= 50) {
            if (score < 55) {
                System.out.println("E");
                grade = 'E';
            } else {
                System.out.println("F");
                grade = 'F';
            }
        } else {
            if (score < 45) {
                System.out.println("G");
                grade = 'G';
            } else {
                if (score < 48) {
                    System.out.println("H");
                    grade = 'H';
                } else {
                    System.out.println("I");
                    grade = 'I';
                }
            }
        }

        grade = grade - 'A';
        System.out.println("Score: " + score + ", Grade: " + grade);
    }

}