package practice;

import java.util.Scanner;

public class Task2 {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter the Student Marks");
		int marks = sc.nextInt();
		if(marks < 35) {
			System.out.println("Fail");
		}
		else if(marks == 35) {
			System.out.println("Pass");
		}
		else if(marks > 35 && marks <=70) {
			System.out.println("Third Class");
		}
		else if(marks >70 && marks <=85) {
			System.out.println("SEcond Class");
		}
		else {
			System.out.println("First Class");
		}
		sc.close();
	}
}
