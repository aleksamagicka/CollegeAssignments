// generated with ast extension for cup
// version 0.8
// 17/0/2023 19:48:25


package rs.ac.bg.etf.pp1.ast;

public class Program implements SyntaxNode {

    private SyntaxNode parent;
    private int line;
    public rs.etf.pp1.symboltable.concepts.Obj obj = null;

    private ProgName ProgName;
    private PreBodyList PreBodyList;
    private ProgramBodyStart ProgramBodyStart;
    private MethodDeclList MethodDeclList;

    public Program (ProgName ProgName, PreBodyList PreBodyList, ProgramBodyStart ProgramBodyStart, MethodDeclList MethodDeclList) {
        this.ProgName=ProgName;
        if(ProgName!=null) ProgName.setParent(this);
        this.PreBodyList=PreBodyList;
        if(PreBodyList!=null) PreBodyList.setParent(this);
        this.ProgramBodyStart=ProgramBodyStart;
        if(ProgramBodyStart!=null) ProgramBodyStart.setParent(this);
        this.MethodDeclList=MethodDeclList;
        if(MethodDeclList!=null) MethodDeclList.setParent(this);
    }

    public ProgName getProgName() {
        return ProgName;
    }

    public void setProgName(ProgName ProgName) {
        this.ProgName=ProgName;
    }

    public PreBodyList getPreBodyList() {
        return PreBodyList;
    }

    public void setPreBodyList(PreBodyList PreBodyList) {
        this.PreBodyList=PreBodyList;
    }

    public ProgramBodyStart getProgramBodyStart() {
        return ProgramBodyStart;
    }

    public void setProgramBodyStart(ProgramBodyStart ProgramBodyStart) {
        this.ProgramBodyStart=ProgramBodyStart;
    }

    public MethodDeclList getMethodDeclList() {
        return MethodDeclList;
    }

    public void setMethodDeclList(MethodDeclList MethodDeclList) {
        this.MethodDeclList=MethodDeclList;
    }

    public SyntaxNode getParent() {
        return parent;
    }

    public void setParent(SyntaxNode parent) {
        this.parent=parent;
    }

    public int getLine() {
        return line;
    }

    public void setLine(int line) {
        this.line=line;
    }

    public void accept(Visitor visitor) {
        visitor.visit(this);
    }

    public void childrenAccept(Visitor visitor) {
        if(ProgName!=null) ProgName.accept(visitor);
        if(PreBodyList!=null) PreBodyList.accept(visitor);
        if(ProgramBodyStart!=null) ProgramBodyStart.accept(visitor);
        if(MethodDeclList!=null) MethodDeclList.accept(visitor);
    }

    public void traverseTopDown(Visitor visitor) {
        accept(visitor);
        if(ProgName!=null) ProgName.traverseTopDown(visitor);
        if(PreBodyList!=null) PreBodyList.traverseTopDown(visitor);
        if(ProgramBodyStart!=null) ProgramBodyStart.traverseTopDown(visitor);
        if(MethodDeclList!=null) MethodDeclList.traverseTopDown(visitor);
    }

    public void traverseBottomUp(Visitor visitor) {
        if(ProgName!=null) ProgName.traverseBottomUp(visitor);
        if(PreBodyList!=null) PreBodyList.traverseBottomUp(visitor);
        if(ProgramBodyStart!=null) ProgramBodyStart.traverseBottomUp(visitor);
        if(MethodDeclList!=null) MethodDeclList.traverseBottomUp(visitor);
        accept(visitor);
    }

    public String toString(String tab) {
        StringBuffer buffer=new StringBuffer();
        buffer.append(tab);
        buffer.append("Program(\n");

        if(ProgName!=null)
            buffer.append(ProgName.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(PreBodyList!=null)
            buffer.append(PreBodyList.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(ProgramBodyStart!=null)
            buffer.append(ProgramBodyStart.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        if(MethodDeclList!=null)
            buffer.append(MethodDeclList.toString("  "+tab));
        else
            buffer.append(tab+"  null");
        buffer.append("\n");

        buffer.append(tab);
        buffer.append(") [Program]");
        return buffer.toString();
    }
}
