// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class FactorChr extends Factor {

    private FactorChrFunc FactorChrFunc;

    public FactorChr (FactorChrFunc FactorChrFunc) {
        this.FactorChrFunc=FactorChrFunc;
        if(FactorChrFunc!=null) FactorChrFunc.setParent(this);
    }

    public FactorChrFunc getFactorChrFunc() {
        return FactorChrFunc;
    }

    public void setFactorChrFunc(FactorChrFunc FactorChrFunc) {
        this.FactorChrFunc=FactorChrFunc;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(FactorChrFunc!=null) FactorChrFunc.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(FactorChrFunc!=null) FactorChrFunc.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(FactorChrFunc!=null) FactorChrFunc.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("FactorChr(\n");

        if(FactorChrFunc!=null)
            buffer.append(FactorChrFunc.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [FactorChr]");
        return buffer.toString();
    }
}
