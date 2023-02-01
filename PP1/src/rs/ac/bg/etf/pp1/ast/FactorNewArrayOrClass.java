// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class FactorNewArrayOrClass extends Factor {

    private FactorExprActParts FactorExprActParts;

    public FactorNewArrayOrClass (FactorExprActParts FactorExprActParts) {
        this.FactorExprActParts=FactorExprActParts;
        if(FactorExprActParts!=null) FactorExprActParts.setParent(this);
    }

    public FactorExprActParts getFactorExprActParts() {
        return FactorExprActParts;
    }

    public void setFactorExprActParts(FactorExprActParts FactorExprActParts) {
        this.FactorExprActParts=FactorExprActParts;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(FactorExprActParts!=null) FactorExprActParts.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(FactorExprActParts!=null) FactorExprActParts.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(FactorExprActParts!=null) FactorExprActParts.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("FactorNewArrayOrClass(\n");

        if(FactorExprActParts!=null)
            buffer.append(FactorExprActParts.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [FactorNewArrayOrClass]");
        return buffer.toString();
    }
}
