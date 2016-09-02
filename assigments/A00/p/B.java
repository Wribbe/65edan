package p;

import p.A;

public class B {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Not enough arguments, aborting.");
            System.exit(1);
        }
        while (true) {
            System.out.println(args[0]);
        }
        //A a = new A("A object");
        //String output = String.format("Name of object: %s", a.toString());
        //System.out.println(output);
    }
}
