import java.util.Random;
import java.util.Scanner;
public class Main {
    public static void main(String[] args) throws InterruptedException{
        Scanner sc = new Scanner(System.in);
        Random rdm = new Random();

        int min = 1;
        int max = 101;

        int num = rdm.nextInt(min, max);

        int guess, i=0;


        System.out.println("Number Guess!");
        Thread.sleep(1500);
        System.out.println("Guess the number, win a prize!");

        do {
            System.out.print("Enter your number: ");
            guess = sc.nextInt();
            if(guess > num){
                System.out.println("Too High!");
            } else if (guess < num) {
                System.out.println("Too Low!");
            }
            i++;
        }while(guess != num);

        if (guess == num){
            System.out.println("Congrats! You guessed it under " + i + " attempts.");
        }
        else {
            Thread.sleep(1500);
            System.out.println("You guessed the number in " + i + " attempts. That's called dumb in my book...");
            }
        

        sc.close();
    }
}