package tests;

import static org.junit.Assert.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;

import lang.MsnVisitor;
import lang.ast.Program;

/**
 * Tests the interactive expression checking visitor
 * @author Jesper Öqvist <jesper.oqvist@cs.lth.se>
 */
@RunWith(Parameterized.class)
public class TestMsn extends AbstractParameterizedTest {
	/**
	 * Directory where test files live
	 */
	private static final String TEST_DIR = "testfiles/msn_visitor";

	/**
	 * Construct a new JastAdd test
	 * @param filename filename of test input file
	 */
	public TestMsn (String filename) {
		super(TEST_DIR, filename);
	}

	/**
	 * Run the JastAdd test
	 */
	@Test
	public void runTest() throws Exception {
		try (ByteArrayOutputStream bytes = new ByteArrayOutputStream();
				PrintStream outStream = new PrintStream(bytes)) {
			Program program = (Program) parse(inFile);
			outStream.println("" + MsnVisitor.result(program));
			compareOutput(bytes.toString(), outFile, expectedFile);
		}
	}

	@SuppressWarnings("javadoc")
	@Parameters(name = "{0}")
	public static Iterable<Object[]> getTests() {
		return getTestParameters(TEST_DIR);
	}
}
