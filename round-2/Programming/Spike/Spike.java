import java.util.*;

class Spike {
    public static void main(String args[]) {
        Spike ptask = new Spike();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter password: ");
        String userInput = scanner.next();
	    String input = userInput.substring("HZ{".length(),userInput.length()-1);
	    
    	if (ptask.check(input)) {
    	    System.out.println("Goodjob. This is correct. You found a flag.");
    	} else {
    	    System.out.println("Please try again!");
        }
    }

    public boolean check(String pass) {
        if (pass.length() != 32) {
            return false;
        }
        char[] buffer = new char[32];
        
        int i;
        
        for (i=0; i<8; i++) {
            buffer[i] = pass.charAt(i);
        }
        for (; i<16; i++) {
            buffer[i] = pass.charAt(23-i);
        }
        for (; i<32; i+=2) {
            buffer[i] = pass.charAt(46-i);
        }
        for (i=31; i>=17; i-=2) {
            buffer[i] = pass.charAt(i);
        }
        String s = new String(buffer);
        return s.equals("y0u_unl03hT_d3kcBSj!d30g_0k_p0_!");
    }
}