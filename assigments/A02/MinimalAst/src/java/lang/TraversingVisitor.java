package lang;
import lang.ast.*;

public abstract class TraversingVisitor implements lang.ast.Visitor {

    protected Object visitChildren(ASTNode node, Object data) {
        for (int i = 0; i < node.getNumChild(); ++i) {
            node.getChild(i).accept(this, data);
        }
        return data;
    }

    public Object visit(ASTNode node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Add node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Assign node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(BinaryLogicalExpression node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Div node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(ELSE node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(EQ node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(FunctionDeclaration node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(FunctionUse node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(GT node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(GTEQ node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(IF node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(IdDeclare node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(IdUse node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(LT node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(LTEQ node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(List node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Minus node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Mul node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(NOEQ node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Numeral node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Opt node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Program node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Remainder node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(Return node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(VarDeclare node, Object data) {
        return visitChildren(node, data);
    }

    public Object visit(WHILE node, Object data) {
        return visitChildren(node, data);
    }

}
