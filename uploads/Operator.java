package practice;

public class Operator {
	public static void main(String[] args) {
		int i = 10;
		int j = 20;
		//unary operator
		System.out.println(i);
		System.out.println(++i);
		System.out.println(i);
		System.out.println(i++);
		System.out.println(i);
		//relational operator(output will be in boolean values
		System.out.println(i == j);
		System.out.println(i != j);
		System.out.println(i > j);
		System.out.println(i < j);
		System.out.println(i >= j);
		System.out.println(i <= j);
		//assignment operators +=,-=,*=,/=,%=
		i += 5;
		System.out.println(i);
	}

}
