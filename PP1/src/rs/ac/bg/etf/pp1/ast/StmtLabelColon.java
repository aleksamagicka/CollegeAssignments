// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class StmtLabelColon extends Statement {

    private LabelColon LabelColon;
    private Matched Matched;

    public StmtLabelColon (LabelColon LabelColon, Matched Matched) {
        this.LabelColon=LabelColon;
        if(LabelColon!=null) LabelColon.setParent(this);
        this.Matched=Matched;
        if(Matched!=null) Matched.setParent(this);
    }

    public LabelColon getLabelColon() {
        return LabelColon;
    }

    public void setLabelColon(LabelColon LabelColon) {
        this.LabelColon=LabelColon;
    }

    public Matched getMatched() {
        return Matched;
    }

    public void setMatched(Matched Matched) {
        this.Matched=Matched;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(LabelColon!=null) LabelColon.accept(visitor);
        if(Matched!=null) Matched.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(LabelColon!=null) LabelColon.traverseTopDown(visitor);
        if(Matched!=null) Matched.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(LabelColon!=null) LabelColon.traverseBottomUp(visitor);
        if(Matched!=null) Matched.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("StmtLabelColon(\n");

        if(LabelColon!=null)
            buffer.append(LabelColon.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(Matched!=null)
            buffer.append(Matched.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [StmtLabelColon]");
        return buffer.toString();
    }
}
