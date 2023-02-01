// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class DesigMultiple extends DesignatorStatement {

    private OptDesigList OptDesigList;
    private AssignOp AssignOp;
    private Designator Designator;

    public DesigMultiple (OptDesigList OptDesigList, AssignOp AssignOp, Designator Designator) {
        this.OptDesigList=OptDesigList;
        if(OptDesigList!=null) OptDesigList.setParent(this);
        this.AssignOp=AssignOp;
        if(AssignOp!=null) AssignOp.setParent(this);
        this.Designator=Designator;
        if(Designator!=null) Designator.setParent(this);
    }

    public OptDesigList getOptDesigList() {
        return OptDesigList;
    }

    public void setOptDesigList(OptDesigList OptDesigList) {
        this.OptDesigList=OptDesigList;
    }

    public AssignOp getAssignOp() {
        return AssignOp;
    }

    public void setAssignOp(AssignOp AssignOp) {
        this.AssignOp=AssignOp;
    }

    public Designator getDesignator() {
        return Designator;
    }

    public void setDesignator(Designator Designator) {
        this.Designator=Designator;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(OptDesigList!=null) OptDesigList.accept(visitor);
        if(AssignOp!=null) AssignOp.accept(visitor);
        if(Designator!=null) Designator.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(OptDesigList!=null) OptDesigList.traverseTopDown(visitor);
        if(AssignOp!=null) AssignOp.traverseTopDown(visitor);
        if(Designator!=null) Designator.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(OptDesigList!=null) OptDesigList.traverseBottomUp(visitor);
        if(AssignOp!=null) AssignOp.traverseBottomUp(visitor);
        if(Designator!=null) Designator.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("DesigMultiple(\n");

        if(OptDesigList!=null)
            buffer.append(OptDesigList.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(AssignOp!=null)
            buffer.append(AssignOp.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(Designator!=null)
            buffer.append(Designator.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [DesigMultiple]");
        return buffer.toString();
    }
}
