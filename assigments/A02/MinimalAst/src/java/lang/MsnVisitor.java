package lang;
import lang.ast.*;

public class MsnVisitor extends TraversingVisitor {

    public static int result(ASTNode root) {
        MsnVisitor visitor = new MsnVisitor();
        root.accept(visitor, null);
        return visitor.maxDepth;
    }

    //state variables
    private int maxDepth = 0;

    public Object visit(ASTNode node, Object data) {
        return maxDepth;
    }

}
