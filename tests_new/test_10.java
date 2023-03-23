// If else statements
private class TestIfElse {
    public void calculateGrade(int score) {
        int x=10;
        // z =x; Need to sort
        {
            {
                {
                    int y=10;
                }
                int z=10;
            }
        }
        if (score >= 90)
        {
            int j=100;
        }
        char grade;
        if ('b' >= 'a' ) {
            grade = 'A';
        } else if (score >= 80) {
            grade = 'B';
        } else if (score >= 70) {
            grade = 'C';
        } else if (score >= 60) {
            grade = 'D';
        } else if (score >= 50) {
            if (score < 55) {
                grade = 'E';
            } else {
                grade = 'F';
            }
        } else {
            if (score < 45) {
                grade = 'G';
            } else {
                if (score < 48) {
                    grade = 'H';
                } else {
                    grade = 'I';
                }
            }
        }
        System.out.println("Score: " + score + ", Grade: " + grade);
    }

}