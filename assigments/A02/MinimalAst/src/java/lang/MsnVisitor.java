package lang;
import lang.ast.*;

public class MsnVisitor extends TraversingVisitor {

    public static int result(ASTNode root) {
        MsnVisitor visitor = new MsnVisitor();
        root.accept(visitor, 0);
        return visitor.maxDepth;
    }

    //state variables
    private int maxDepth = 0;

    public Object visit(Program node, Object data) {
        return visitChildren(node, 0);
    }

    public Object visit(FunctionDeclaration node, Object data) {
        int givenDepth = (int) data;
        int myDepth = givenDepth+1;
        if (myDepth > maxDepth) {
               maxDepth = myDepth;
        }
        return visitChildren(node, (Object)myDepth);
    }

    public Object visit(IF node, Object data) {
        int givenDepth = (int) data;
        int myDepth = givenDepth+1;
        if (myDepth > maxDepth) {
               maxDepth = myDepth;
        }
        return visitChildren(node, (Object)myDepth);
    }

    public Object visit(WHILE node, Object data) {
        int givenDepth = (int) data;
        int myDepth = givenDepth+1;
        if (myDepth > maxDepth) {
               maxDepth = myDepth;
        }
        return visitChildren(node, (Object)myDepth);
    }

}
