// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class StatementGoto extends Matched {

    private Label Label;

    public StatementGoto (Label Label) {
        this.Label=Label;
        if(Label!=null) Label.setParent(this);
    }

    public Label getLabel() {
        return Label;
    }

    public void setLabel(Label Label) {
        this.Label=Label;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(Label!=null) Label.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(Label!=null) Label.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(Label!=null) Label.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("StatementGoto(\n");

        if(Label!=null)
            buffer.append(Label.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [StatementGoto]");
        return buffer.toString();
    }
}
