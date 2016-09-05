package tests;

import org.junit.Test;

@SuppressWarnings("javadoc")
public class ParseTests extends AbstractTestSuite {
	public ParseTests() {
		super("testfiles");// where test input files are
	}

    @Test
    public void validAllConstructs() {
        testValidSyntax("allConstructs.minis");
    }

	@Test
	public void validShortest() {
		testValidSyntax("shortest.minis");
	}

	@Test
	public void errorParsing() {
		testSyntaxError("parsingError.minis");
	}

    @Test
    public void errorScanning() {
        testSyntaxError("scanningError.minis");
    }
}
