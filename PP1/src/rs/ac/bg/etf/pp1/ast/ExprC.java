// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class ExprC extends Expr {

    private OptMinus OptMinus;
    private Term Term;
    private AddTerm AddTerm;

    public ExprC (OptMinus OptMinus, Term Term, AddTerm AddTerm) {
        this.OptMinus=OptMinus;
        if(OptMinus!=null) OptMinus.setParent(this);
        this.Term=Term;
        if(Term!=null) Term.setParent(this);
        this.AddTerm=AddTerm;
        if(AddTerm!=null) AddTerm.setParent(this);
    }

    public OptMinus getOptMinus() {
        return OptMinus;
    }

    public void setOptMinus(OptMinus OptMinus) {
        this.OptMinus=OptMinus;
    }

    public Term getTerm() {
        return Term;
    }

    public void setTerm(Term Term) {
        this.Term=Term;
    }

    public AddTerm getAddTerm() {
        return AddTerm;
    }

    public void setAddTerm(AddTerm AddTerm) {
        this.AddTerm=AddTerm;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(OptMinus!=null) OptMinus.accept(visitor);
        if(Term!=null) Term.accept(visitor);
        if(AddTerm!=null) AddTerm.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(OptMinus!=null) OptMinus.traverseTopDown(visitor);
        if(Term!=null) Term.traverseTopDown(visitor);
        if(AddTerm!=null) AddTerm.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(OptMinus!=null) OptMinus.traverseBottomUp(visitor);
        if(Term!=null) Term.traverseBottomUp(visitor);
        if(AddTerm!=null) AddTerm.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("ExprC(\n");

        if(OptMinus!=null)
            buffer.append(OptMinus.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(Term!=null)
            buffer.append(Term.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(AddTerm!=null)
            buffer.append(AddTerm.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [ExprC]");
        return buffer.toString();
    }
}
