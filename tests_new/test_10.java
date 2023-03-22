// If else statements
private class TestIfElse {
    public void calculateGrade(int score) {
        char grade;
        if (score >= 90) {
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