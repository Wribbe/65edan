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

    public static void errorParsing() {
        String name = LangParser.Terminals.NAMES[compiler.peek()];
        name = name.toLowerCase();
        fail("Parsing Error; Unexpected token: <" + name + ">.");
    }

    public void parseProgram() {
        try {
            statement();
        } catch (RuntimeException e) {
            String[] tokens = e.toString().split(":");
            fail("Scanning Error; " + tokens[tokens.length-1].trim() + ".");
        }
    }

    private static void expression() {
        switch(compiler.peek()) {
            case ID: compiler.accept(ID); break;
            case NUMERAL: compiler.accept(NUMERAL); break;
            case NOT: compiler.accept(NOT); expression(); break;
            default: errorParsing();
        }
    }

    private static void statement() {
        switch(compiler.peek()) {
            case FOR: forStatement(); break;
            case IF: ifStatement(); break;
            case ID: assignment(); break;
            default: errorParsing();
        }
    }

    private static void assignment() {
        compiler.accept(ID);
        compiler.accept(ASSIGN);
        expression();
    }

    private static void forStatement() {
        compiler.accept(FOR);
        compiler.accept(ID);
        compiler.accept(ASSIGN);
        expression();
        compiler.accept(UNTIL);
        expression();
        compiler.accept(DO);
        statement();
        compiler.accept(OD);
    }

    private static void ifStatement() {
        compiler.accept(IF);
        expression();
        compiler.accept(THEN);
        statement();
        compiler.accept(FI);
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
