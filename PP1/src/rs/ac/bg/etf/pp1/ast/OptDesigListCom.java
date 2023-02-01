// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class OptDesigListCom extends OptDesigListComma {

    private OptDesigList OptDesigList;

    public OptDesigListCom (OptDesigList OptDesigList) {
        this.OptDesigList=OptDesigList;
        if(OptDesigList!=null) OptDesigList.setParent(this);
    }

    public OptDesigList getOptDesigList() {
        return OptDesigList;
    }

    public void setOptDesigList(OptDesigList OptDesigList) {
        this.OptDesigList=OptDesigList;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(OptDesigList!=null) OptDesigList.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(OptDesigList!=null) OptDesigList.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(OptDesigList!=null) OptDesigList.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("OptDesigListCom(\n");

        if(OptDesigList!=null)
            buffer.append(OptDesigList.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [OptDesigListCom]");
        return buffer.toString();
    }
}
