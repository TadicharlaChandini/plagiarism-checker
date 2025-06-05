package practice;

import java.util.Scanner;

public class Task1 {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		int num = sc.nextInt();
		if(num % 2 == 0) {
			System.out.println("Given number is Even");
		}
		else {
			System.out.println("Given number is Odd");
		}
		sc.close();
	}

}
