package tests;

import static org.junit.Assert.*;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;

import lang.ast.ErrorMessage;
import lang.ast.Program;

import java.io.*;

/**
 * Tests name analysis
 */
@RunWith(Parameterized.class)
public class TestInterpreter extends AbstractParameterizedTest {
	/**
	 * Directory where test files live
	 */
	private static final String TEST_DIR = "testfiles/interpreter";

	/**
	 * Construct a new JastAdd test
	 * @param filename filename of test input file
	 */
	public TestInterpreter(String filename) {
		super(TEST_DIR, filename);
	}

	/**
	 * Run the JastAdd test
	 */
	@Test
	public void runTest() throws Exception {
        PrintStream out = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try {
            Program program = (Program) parse(inFile);
            if (!program.errors().isEmpty()) {
                StringBuilder sb = new StringBuilder();
                System.out.println("Errors in program, aborting.");
                for (ErrorMessage m: program.errors()) {
                    sb.append(m).append("\n");
                }
                System.out.println(sb.toString());
                throw new RuntimeException("Error in program.");
            }
            System.setOut(new PrintStream(baos));
            try {
                program.eval();
            } catch(RuntimeException e) {
                System.out.println("RuntimeException: "+e.getMessage());
            }
        } finally {
            compareOutput(baos.toString(), outFile, expectedFile);
            System.setOut(out);
        }
	}

	@SuppressWarnings("javadoc")
	@Parameters(name = "{0}")
	public static Iterable<Object[]> getTests() {
		return getTestParameters(TEST_DIR);
	}
}
