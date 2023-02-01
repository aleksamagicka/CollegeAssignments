// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class SingleOptDesigInList extends OptDesigList {

    private OptDesig OptDesig;

    public SingleOptDesigInList (OptDesig OptDesig) {
        this.OptDesig=OptDesig;
        if(OptDesig!=null) OptDesig.setParent(this);
    }

    public OptDesig getOptDesig() {
        return OptDesig;
    }

    public void setOptDesig(OptDesig OptDesig) {
        this.OptDesig=OptDesig;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(OptDesig!=null) OptDesig.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(OptDesig!=null) OptDesig.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(OptDesig!=null) OptDesig.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("SingleOptDesigInList(\n");

        if(OptDesig!=null)
            buffer.append(OptDesig.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [SingleOptDesigInList]");
        return buffer.toString();
    }
}
