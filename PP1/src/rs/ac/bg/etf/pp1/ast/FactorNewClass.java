// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class FactorNewClass extends FactorExprActParts {

    private Type Type;
    private ActPartsOpt ActPartsOpt;

    public FactorNewClass (Type Type, ActPartsOpt ActPartsOpt) {
        this.Type=Type;
        if(Type!=null) Type.setParent(this);
        this.ActPartsOpt=ActPartsOpt;
        if(ActPartsOpt!=null) ActPartsOpt.setParent(this);
    }

    public Type getType() {
        return Type;
    }

    public void setType(Type Type) {
        this.Type=Type;
    }

    public ActPartsOpt getActPartsOpt() {
        return ActPartsOpt;
    }

    public void setActPartsOpt(ActPartsOpt ActPartsOpt) {
        this.ActPartsOpt=ActPartsOpt;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(Type!=null) Type.accept(visitor);
        if(ActPartsOpt!=null) ActPartsOpt.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(Type!=null) Type.traverseTopDown(visitor);
        if(ActPartsOpt!=null) ActPartsOpt.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(Type!=null) Type.traverseBottomUp(visitor);
        if(ActPartsOpt!=null) ActPartsOpt.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("FactorNewClass(\n");

        if(Type!=null)
            buffer.append(Type.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(ActPartsOpt!=null)
            buffer.append(ActPartsOpt.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [FactorNewClass]");
        return buffer.toString();
    }
}
