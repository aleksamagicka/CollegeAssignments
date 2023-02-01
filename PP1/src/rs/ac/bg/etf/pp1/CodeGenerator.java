package rs.ac.bg.etf.pp1;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Stack;

import rs.ac.bg.etf.pp1.ast.*;
import rs.ac.bg.etf.pp1.ast.VisitorAdaptor;
import rs.etf.pp1.mj.runtime.Code;
import rs.etf.pp1.symboltable.Tab;
import rs.etf.pp1.symboltable.concepts.Obj;
import rs.etf.pp1.symboltable.concepts.Struct;

public class CodeGenerator extends VisitorAdaptor {

	private int mainPc;

	/* desig multiple */
	private ArrayList<Designator> currentLeftDesignators = new ArrayList<>();
	
	public int getMainPc() {
		return mainPc;
	}

	public void visit(VarDeclaration varDeclaration) {
		SyntaxNode sn = varDeclaration.getParent();
		while (sn instanceof VarList || sn instanceof VarListComma)
			sn = sn.getParent();
		// Ako je VarDecls static velicina cnt++
	}

	public void visit(MethodTypeName methodTypeName) {
		if ("main".equalsIgnoreCase(methodTypeName.getMethName())) {
			mainPc = Code.pc;
		}

		methodTypeName.obj.setAdr(Code.pc);

		int formalParamCnt = methodTypeName.obj.getLevel();
		int localCnt = methodTypeName.obj.getLocalSymbols().size();

		Code.put(Code.enter);
		Code.put(formalParamCnt);
		Code.put(localCnt);
	}

	public void visit(MethodDeclaration method) {
		Code.put(Code.exit);
		Code.put(Code.return_);
	}

	private int constValue(SyntaxNode type) {
		if (type instanceof NumConst)
			return ((NumConst) type).getN1();
		if (type instanceof CHARACTERConst)
			return ((CHARACTERConst) type).getC1();
		if (type instanceof BOOLEANConst)
		{
			BOOLEANConst boolVal = (BOOLEANConst) type;
			return boolVal.getB1() ? 1 : 0;
		}
			
		return -1;
	}

	public void visit(ConstDeclaration cnst) {
		cnst.obj.setAdr(constValue(cnst.getConstVal()));
		Code.load(cnst.obj);
	}

	// Obicne konstante
	public void visit(FactorConst cnst) {
		Obj con = Tab.insert(Obj.Con, "$", cnst.struct);
		con.setAdr(constValue(cnst.getConstVal()));

		Code.load(con);
	}

	public void visit(DesigAssign desigAssign) {
		Code.store(desigAssign.getDesignator().obj);
		if (desigAssign.getDesignator().obj.getType().getKind() == Struct.Array) {
			// Ispis
		}
	}

	public void visit(Designator designator) {
		if (designator.obj.getType().getKind() == Struct.Array) {
			System.out.println("Posetio array designatora: " + designator.getDesigName().getDesigName());
		}
	}

	public void visit(ProgramBodyStart gs) {
	}

	public void visit(DesigName desigName) {
		// Posledjni?
		if (((Designator) desigName.getParent()).getDesigAdditional() instanceof NoDesigAddit) {
			SyntaxNode parent = desigName.getParent().getParent();
			if (!(parent instanceof DesigAssign) // delovi -> dohvataj
					&& !(parent instanceof FactorDes && ((FactorDes) parent).getOptActPartsOpt() instanceof OActPO) // f-ja
					&& !(parent instanceof StatementRead) && !(parent instanceof DesigMultiple)
					&& !(parent instanceof SingleOptDesignator)
				&& !(parent instanceof DesigINC))
			{
				System.out.println("desigName: loadujem");
				Code.load(desigName.obj);
			}
				
		} else
			Code.load(desigName.obj);
	}

	public void visit(DesigId desigId) {
		// Posledjni?
		if (desigId.getParent().getParent() instanceof Designator) {
			SyntaxNode desig = desigId.getParent().getParent();
			SyntaxNode parent = desig.getParent();
			if (!(parent instanceof DesigAssign) // delovi -> dohvataj
					&& !(parent instanceof FactorDes && ((FactorDes) parent).getOptActPartsOpt() instanceof OActPO)
					&& !(parent instanceof StatementRead)
				&& !(parent instanceof DesigINC))
			{
				System.out.println("desigid: loadujem");
				Code.load(desigId.obj);
			}
				
		} else
			Code.load(desigId.obj);
	}

	/* desig multiple */
	public void visit(SingleOptDesignator designator) {
		currentLeftDesignators.add(designator.getDesignator());
	}

	public void visit(NoOptDesig noOptDesig) {
		currentLeftDesignators.add(null);
	}

	public void visit(DesigMultiple desigMultiple) {
		Designator rightDesignator = desigMultiple.getDesignator();
		//System.out.println("codegen desigmultiple: rightadr: " + rightDesignator.obj.getType().getKind()); // Struct, ne
																											// Obj!!

		Code.loadConst(currentLeftDesignators.size());
		Code.load(rightDesignator.obj);
		Code.put(Code.arraylength);

		int jmpPc = Code.pc;
		Code.putFalseJump(Code.gt, 0); // gt daje le?
		// Code.fixup(jmpPc+1);

		Code.put(Code.trap);
		Code.loadConst(0);

		Boolean setJmp = false;

		int i = currentLeftDesignators.size() - 1;
		Collections.reverse(currentLeftDesignators);
		for (Designator desig : currentLeftDesignators) {
			if (desig != null) {
				// ovde treba load iz niza
				// adr, i
				if (!setJmp) {
					Code.fixup(jmpPc + 1);
					setJmp = true;
				}

				Code.load(rightDesignator.obj);
				Code.loadConst(i);
				Code.put(Code.aload); // ucitaj ga sa pozicije i

				System.out.println("codegen DESIGMultiple: " + desig.obj.getType().getKind());

				if (desig.obj.getKind() == Obj.Elem) {
					//System.out.println(
					//		"codegen desigmultiple: trenutni: levi je elem: " + desig.getDesigName().getDesigName());
					Code.put(Code.astore);
				} else {
					//System.out.println(
					//		"codegen desigmultiple: trenutni: levi nije elem: " + desig.getDesigName().getDesigName());
					Code.store(desig.obj);
				}
			}

			i--;
		}

		currentLeftDesignators.clear();
	}

	public void visit(AddTermA addTerm) {
		SyntaxNode op = addTerm.getAddOp();
		if (op instanceof AddOpPLUS)
			Code.put(Code.add);
		if (op instanceof AddOpMINUS)
			Code.put(Code.sub);
	}

	public void visit(StatementPrint stmPrint) {
		if (stmPrint.getExpr().struct == Tab.intType || stmPrint.getExpr().struct == MyTab.boolType) {
			Code.loadConst(5);
			Code.put(Code.print);
		} else {
			Code.loadConst(1);
			Code.put(Code.bprint);
		}
	}

	private Map<String, Integer> statementLabels = new HashMap<>();
	private Map<String, List<Integer>> gotoAdrs = new HashMap<>();

	@Override
	public void visit(LabelColon labelColon) {
		String ident = labelColon.getLabel().getI1();
		statementLabels.put(ident, Code.pc);
		
		// Ako je ovaj label pre bio trazen, sad moze da se njegova prava lokacija tamo i postavi
		if (gotoAdrs.containsKey(ident))
			while (gotoAdrs.get(ident).size() > 0) {
				Code.fixup(gotoAdrs.get(ident).remove(0));
			}
	}

	@Override
	public void visit(StatementGoto statementGoto) {
		String ident = statementGoto.getLabel().getI1(); // label name
		if (statementLabels.containsKey(ident))
			Code.putJump(statementLabels.get(ident)); // Vec imamo adresu ovog labela, skacemo na njega
		else {
			Code.putJump(0);

			int wrongOffset = Code.pc - 2;

			List<Integer> list;

			// Zapisujemo da ovaj goto nije jos resen
			if (gotoAdrs.containsKey(ident))
				list = gotoAdrs.get(ident);
			else {
				list = new ArrayList<Integer>();
				gotoAdrs.put(ident, list);
			}

			list.add(wrongOffset);
		}
	}

	/* len() */
	public void visit(FactorLen factorLen) {
		Designator niz = factorLen.getDesignator();

		Code.load(niz.obj);
		Code.put(Code.arraylength);
	}

	/* chr() - designator */
	public void visit(FactorChrDesig chrDesig) {
		Code.loadConst(48); // '0'
		Code.put(Code.add);
	}

	/* chr() - NumConst */
	public void visit(FactorChrNumber chrNumber) {
		NumConst nc = (NumConst) chrNumber.getConstVal();
		Code.loadConst(nc.getN1());
		Code.loadConst(48); // '0'
		Code.put(Code.add);
	}

	/* ord() - designator */
	public void visit(FactorOrdDesig ordDesig) {
		Code.loadConst(48); // '0'
		Code.put(Code.sub);
	}

	/* ord() - NumConst */
	public void visit(FactorOrdNumber ordNumber) {
		CHARACTERConst nc = (CHARACTERConst) ordNumber.getConstVal();
		Code.loadConst(nc.getC1());
		Code.loadConst(48); // '0'
		Code.put(Code.sub);
	}

	public void visit(StatementPrintEOL stmPrintEol) {
		Code.loadConst(13);
		Code.loadConst(1);
		Code.put(Code.bprint);

		Code.loadConst(10); // char
		Code.loadConst(1); // width
		Code.put(Code.bprint);
	}

	public void visit(StatementRead stmRead) {
		Code.put(Code.read);
		Code.store(stmRead.getDesignator().obj);
	}

	public void visit(TermM term) {
		SyntaxNode type = term.getMulOp();

		if (type instanceof MulOpMUL)
			Code.put(Code.mul);
		if (type instanceof MulOpDIV)
			Code.put(Code.div);
		if (type instanceof MulOpMOD)
			Code.put(Code.rem);
	}

	public void visit(OptMin neg) {
		// Code.put(Code.neg);
	}

	public void visit(ExprC expr) {
		if (expr.getOptMinus() instanceof OptMin)
			Code.put(Code.neg);
	}

	public void visit(CondFactR cond) {
		SyntaxNode type = cond.getRelOp();

		if (type instanceof RelOpE)
			Code.putFalseJump(Code.eq, 0);
		if (type instanceof RelOpD)
			Code.putFalseJump(Code.ne, 0);
		if (type instanceof RelOpL)
			Code.putFalseJump(Code.lt, 0);
		if (type instanceof RelOpEL)
			Code.putFalseJump(Code.le, 0);
		if (type instanceof RelOpG)
			Code.putFalseJump(Code.gt, 0);
		if (type instanceof RelOpEG)
			Code.putFalseJump(Code.ge, 0);
	}

	public void visit(CondFactE cond) {
		Code.put(Code.const_1);
		Code.putFalseJump(Code.eq, 0);
	}

	public void visit(DesigAddit desigAdditional) {
		Obj o;
		if (desigAdditional.getParent() instanceof Designator)
			o = ((Designator) desigAdditional.getParent()).obj;
		else
			o = ((DesigAddit) desigAdditional.getParent()).obj;

		o.getLocalSymbols().forEach(e -> {
			if (desigAdditional.getDesigParts() instanceof DesigId)
				if (e.getName().equals(((DesigId) desigAdditional.getDesigParts()).getPartName())) {
					System.out.println("desigaddit: loadujem " + e.getName());
					Code.load(e);
				}
		});
	}

	public void visit(FactorNewArray factorNewArray) {
		Code.put(Code.newarray);
		if (factorNewArray.getType().struct == Tab.charType)
			Code.put(0);
		else
			Code.put(1);
	}

	public void visit(DesigArr desigArr) {
		// Poslednji?
		if (desigArr.getParent().getParent() instanceof Designator) {
			SyntaxNode desig = desigArr.getParent().getParent();
			SyntaxNode parent = desig.getParent();
			if (!(parent instanceof DesigAssign) // additional -> load
					&& !(parent instanceof FactorDes && ((FactorDes) parent).getOptActPartsOpt() instanceof OActPO)
					&& !(parent instanceof StatementRead) && !(parent instanceof SingleOptDesignator)
					&& !(parent instanceof DesigINC) && !(parent instanceof DesigDEC))

			{
				//System.out.println("desigarr: loadujem, " + parent.getClass());
				Code.load(desigArr.obj);
			}

		} else {
			/*Code.load(desigArr.obj);
			if (((DesigAddit) desigArr.getParent()).getParent() instanceof DesigAddit
					&& ((DesigAddit) ((DesigAddit) desigArr.getParent()).getParent())
							.getDesigParts() instanceof DesigId) {
				Code.put(Code.dup);
				System.out.println("desig arr: USAO U TEMP HELP POMOC");
				Code.store(MyTab.tempHelp);
			}*/
		}
	}

	public void visit(DesigINC plusPlus) {
		if (plusPlus.getDesignator().obj.getName().equals("elem"))
		{
			System.out.println("plusplus za " + plusPlus.getDesignator().getDesigName().getDesigName());
			Code.put(Code.dup2);
			Code.put(Code.aload);
			Code.put(Code.const_1);
			Code.put(Code.add);
			Code.put(Code.astore);
		}
		else
		{
			Code.load(plusPlus.getDesignator().obj);
			Code.put(Code.const_1);
			Code.put(Code.add);
			Code.store(plusPlus.getDesignator().obj);
		}
	}

	public void visit(DesigDEC minusMinus) {
		if (minusMinus.getDesignator().obj.getName().equals("elem"))
		{
			System.out.println("minusminus za " + minusMinus.getDesignator().getDesigName().getDesigName());
			Code.put(Code.dup2);
			Code.put(Code.aload);
			Code.put(Code.const_1);
			Code.put(Code.sub);
			Code.put(Code.astore);
		}
		else
		{
			Code.load(minusMinus.getDesignator().obj);
			Code.put(Code.const_1);
			Code.put(Code.sub);
			Code.store(minusMinus.getDesignator().obj);
		}
	}
}