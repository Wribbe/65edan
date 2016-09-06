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
        switch(compiler.peek()) {
//            case FOR: forStatement(); break;
//            case IF: ifStatement(); break;
            case ID: assignment(); break;
            default: compiler.error("Expected statement, got " +
                                    compiler.peek());
        }
    }

    private static void forStatement() {
//        compiler.accept(FOR);
//        compiler.accept(ID);
//        compiler.accept(ASSIGN);
//        expression();
//        compiler.accept(DO);
//        statement();
//        compiler.accept(OD);
    }

    private static void expression() {
        switch(compiler.peek()) {
            case ID: compiler.accept(ID); break;
            case NUMERAL: compiler.accept(NUMERAL); break;
            case NOT: compiler.accept(NOT); expression(); break;
        }
    }

    private static void assignment() {
        compiler.accept(ID);
        compiler.accept(ASSIGN);
        expression();
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
        System.out.println("Valid syntax.");
    }
}
