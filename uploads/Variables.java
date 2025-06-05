package practice;

public class Variables {
	//instance variable
	int id = 101;
	static long phno = 9391967337L;
	public static void main(String[] args) {
		Variables var = new Variables();
		System.out.println(var.id);
		System.out.println("Student contact no:"+phno);//to print static variable we don't need to make instance
	}

}
