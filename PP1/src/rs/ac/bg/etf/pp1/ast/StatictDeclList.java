// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class StatictDeclList extends PreBodyList {

    private PreBodyList PreBodyList;
    private PreBodyDecl PreBodyDecl;

    public StatictDeclList (PreBodyList PreBodyList, PreBodyDecl PreBodyDecl) {
        this.PreBodyList=PreBodyList;
        if(PreBodyList!=null) PreBodyList.setParent(this);
        this.PreBodyDecl=PreBodyDecl;
        if(PreBodyDecl!=null) PreBodyDecl.setParent(this);
    }

    public PreBodyList getPreBodyList() {
        return PreBodyList;
    }

    public void setPreBodyList(PreBodyList PreBodyList) {
        this.PreBodyList=PreBodyList;
    }

    public PreBodyDecl getPreBodyDecl() {
        return PreBodyDecl;
    }

    public void setPreBodyDecl(PreBodyDecl PreBodyDecl) {
        this.PreBodyDecl=PreBodyDecl;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(PreBodyList!=null) PreBodyList.accept(visitor);
        if(PreBodyDecl!=null) PreBodyDecl.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(PreBodyList!=null) PreBodyList.traverseTopDown(visitor);
        if(PreBodyDecl!=null) PreBodyDecl.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(PreBodyList!=null) PreBodyList.traverseBottomUp(visitor);
        if(PreBodyDecl!=null) PreBodyDecl.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("StatictDeclList(\n");

        if(PreBodyList!=null)
            buffer.append(PreBodyList.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(PreBodyDecl!=null)
            buffer.append(PreBodyDecl.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [StatictDeclList]");
        return buffer.toString();
    }
}
