// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class FactorOrd extends Factor {

    private FactorOrdFunc FactorOrdFunc;

    public FactorOrd (FactorOrdFunc FactorOrdFunc) {
        this.FactorOrdFunc=FactorOrdFunc;
        if(FactorOrdFunc!=null) FactorOrdFunc.setParent(this);
    }

    public FactorOrdFunc getFactorOrdFunc() {
        return FactorOrdFunc;
    }

    public void setFactorOrdFunc(FactorOrdFunc FactorOrdFunc) {
        this.FactorOrdFunc=FactorOrdFunc;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(FactorOrdFunc!=null) FactorOrdFunc.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(FactorOrdFunc!=null) FactorOrdFunc.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(FactorOrdFunc!=null) FactorOrdFunc.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("FactorOrd(\n");

        if(FactorOrdFunc!=null)
            buffer.append(FactorOrdFunc.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [FactorOrd]");
        return buffer.toString();
    }
}
