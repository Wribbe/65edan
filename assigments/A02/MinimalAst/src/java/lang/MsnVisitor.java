package lang;
import lang.ast.*;

public class MsnVisitor extends TraversingVisitor {

    //state variables
    private int maxDepth = 0;

    public Object visit(ASTNode node, Object data) {
        return maxDepth;
    }

}
