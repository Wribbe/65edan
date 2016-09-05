package lang;

import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.Reader;

import java.io.FileNotFoundException;

import lang.ast.LangParser;
import lang.ast.LangScanner;



import static lang.ast.LangParser.Terminals.*;

public class RecursiveDescentCompiler extends RDPTemplate {

    private static RecursiveDescentCompiler compiler;
    private static LangScanner scanner;

    public static void fail(String message) {
        System.err.println(message);
        System.exit(0);
    }

    public void parseProgram() {
//        compiler.accept();
//        System.out.println(compiler.peek());
//        System.out.println("MUPP");
    }

    public static final void main(String[] args) {

        FileInputStream stream = null;
        try {
            stream = new FileInputStream(args[0]);
        } catch (FileNotFoundException e) {
            fail("File: \"" + args[0] + "\" not found, aborting.");
        }

        Reader reader = new InputStreamReader(stream);

        scanner = new LangScanner(reader);
        compiler = new RecursiveDescentCompiler();
        compiler.parse(scanner);
        //try {
        //} catch () {


//        Reader r = new InputStreamReader();
//        LangScanner scanner = new LangScanner(r);
    }
}
