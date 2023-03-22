// KnapSack Using Dynamic Programming
public class test_8
{  
    public static int maximum(int a1, int a2)  
    {  
        return (a1 > a2) ? a1 : a2;  
    }  
    public static int maxValueKnapsack(int C, int w[], int val[], int l)  
    {  
        int j, wt;  
        int dp[][] = new int[l + 1][C + 1];  
                for (j = 0; j <= l; j++)  
        {  
            for (wt = 0; wt <= C; wt++)  
            {  
                if (j == 0 || wt == 0)  
                {  
                dp[j][wt] = 0;  
                }  
                else if (w[j - 1] <= wt)  
                {  
                dp[j][wt] = maximum(val[j - 1] + dp[j - 1][wt - w[j - 1]], dp[j - 1][wt]);  
                }  
                else  
                {  
                dp[j][wt] = dp[j - 1][wt];  
                }  
            }  
        }  
        return dp[j - 1][C];  
    }  
    public static void main(String argvs[])  
    {  
        int values[] = { 100, 60, 120 };  
        int weight[] = { 20, 10, 30 };  
        int C = 50;  
        int l = 3;  
        int maxVal = maxValueKnapsack(C, weight, values, l);  
        System.out.println("The maximum value is: " + maxVal);  
    }  
}  