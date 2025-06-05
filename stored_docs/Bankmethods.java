package practice;

public class Bankmethods {
	static int currBalance = 1000;
	public static void greetCustomer() {
		System.out.println("Hello,Welcome to the banking application");
	}
	public void deposit(int amount) {
		currBalance = currBalance + amount;
		System.out.println("Amount deposit is successful");
	}
	public static void withdraw(int amount) {
		currBalance = currBalance - amount;
		System.out.println("Amount withdraw is successful");
	}
	public int getCurrentBalance() {
		return currBalance;
	}
	public static void main(String[] args) {
		greetCustomer();
		Bankmethods bank = new Bankmethods();
		System.out.println("Current balance:"+bank.getCurrentBalance());
		bank.deposit(400);
		System.out.println("Current balance:"+bank.getCurrentBalance());
		withdraw(500);
		System.out.println("Current balance:"+bank.getCurrentBalance());
		
	}
}
