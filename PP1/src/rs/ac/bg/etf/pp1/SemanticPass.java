package rs.ac.bg.etf.pp1;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;

import org.apache.log4j.Logger;

import rs.ac.bg.etf.pp1.ast.*;
import rs.etf.pp1.symboltable.*;
import rs.etf.pp1.symboltable.Tab;
import rs.etf.pp1.symboltable.concepts.*;

public class SemanticPass extends VisitorAdaptor {
	Obj currentMethod = null;
	Struct currentType = null;
	boolean errorDetected = false;
	int formalParamCnt = 0;
	int nVars;
	Collection<Obj> actPartsRequired;
	ArrayList<Struct> actPartsPassed;

	Logger log = Logger.getLogger(getClass());
	private boolean isArray = false;
	
	public void report_error(String message, SyntaxNode info) {
		errorDetected = true;
		StringBuilder msg = new StringBuilder(message);
		int line = (info == null) ? 0 : info.getLine();
		if (line != 0)
			msg.append(" na liniji ").append(line);
		log.error(msg.toString());
	}

	public void report_info(String message, SyntaxNode info) {
		StringBuilder msg = new StringBuilder(message);
		int line = (info == null) ? 0 : info.getLine();
		if (line != 0)
			msg.append(" na liniji ").append(line);
		log.info(msg.toString());
	}

	public boolean passed() {
		return !errorDetected;
	}

	public void visit(ProgName progName) {
		progName.obj = Tab.insert(Obj.Prog, progName.getProgName(), Tab.noType);
		Tab.openScope();
		//MyTab.tarabaPomoc = Tab.insert(Obj.Var, "#", Tab.intType);
	}

	public void visit(Program program) {
		nVars = Tab.currentScope.getnVars();

		Obj mainMeth = Tab.find("main");
		if (mainMeth != Tab.noObj && mainMeth.getKind() == Obj.Meth && mainMeth.getType() == Tab.noType
				&& mainMeth.getLevel() == 0)
			report_info("Postoji ispravan main!", program);
		else
			report_error("Ne postoji void main() globalna funkcija!!", program);

		Tab.chainLocalSymbols(program.getProgName().obj);
		Tab.closeScope();
	}

	public void visit(Type type) {
		Obj typeNode = Tab.find(type.getTypeName());
		if (typeNode == Tab.noObj) {
			report_error("Nije pronadjen tip " + type.getTypeName() + " u tabeli simbola!", null);
			type.struct = Tab.noType;
		} else {
			if (Obj.Type == typeNode.getKind()) {
				currentType = typeNode.getType();
				type.struct = currentType;
			} else {
				report_error("Greska: Ime " + type.getTypeName() + " ne predstavlja tip!", null);
				type.struct = Tab.noType;
			}
		}
	}

	public void visit(MethodTVoid type) {
		type.struct = Tab.noType;
		currentType = Tab.noType;
	}

	public void visit(MethodTypeName methodTypeName) {
		currentMethod = Tab.insert(Obj.Meth, methodTypeName.getMethName(), currentType);
		methodTypeName.obj = currentMethod;
		Tab.openScope();
	}

	public void visit(MethodDeclaration methodDec) {
		currentMethod.setLevel(formalParamCnt);
		Tab.chainLocalSymbols(currentMethod);
		Tab.closeScope();
		methodDec.obj = currentMethod;
		currentMethod = null;
		formalParamCnt = 0;
	}

	public void visit(FormalPar formalPar) {
		Struct type = formalPar.getType().struct;
		if (isArray)
			type = new Struct(Struct.Array, type);
		Tab.insert(Obj.Var, formalPar.getFormalParamName(), type);
		formalParamCnt++;
		isArray = false;
	}

	public void visit(NoFieldDecl noFieldDecl) {
	}

	public void visit(ConstType constType) {
		currentType = constType.getType().struct;
		if (currentType != Tab.intType && currentType != Tab.charType && currentType != MyTab.boolType)
			report_error("Greska: const mora biti  tipa int|char|bool", constType);
	}

	public void visit(ConstDecls constDecls) {
		currentType = null;
	}

	public void visit(ConstDeclaration constDeclar) {
		if (mozeDef(constDeclar.getConstName(), constDeclar))
			if (constDeclar.getConstVal().struct == currentType)
				constDeclar.obj = Tab.insert(Obj.Con, constDeclar.getConstName(), currentType);
			else
				report_error("Greska: losi tipovi definisanja konstante", constDeclar);

	}

	public void visit(NumConst numConst) {
		numConst.struct = Tab.intType;
	}

	public void visit(CHARACTERConst charConst) {
		charConst.struct = Tab.charType;
	}

	public void visit(BOOLEANConst boolConst) {
		boolConst.struct = MyTab.boolType;
	}

	public void visit(VarType varType) {
		currentType = varType.getType().struct;
	}
	
	private boolean mozeDef(String name, SyntaxNode info) {
		if (Tab.currentScope.findSymbol(name) == null)
			return true;

		report_error("Greska, postoji vec isto ime!" + name, info);
		return false;

	}

	public void visit(VarDeclaration varDeclar) {
		if (mozeDef(varDeclar.getVarName(), varDeclar)) {
			// ubaci promenljivu u tabelu
			if (isArray) {
				varDeclar.obj = Tab.insert(Obj.Var, varDeclar.getVarName(), new Struct(Struct.Array, currentType));
				isArray = false;
			} else
				varDeclar.obj = Tab.insert(Obj.Var, varDeclar.getVarName(), currentType);

		}
	}

	public void visit(Array array) {
		isArray = true;
	}

	private boolean checkDesigType(Designator designator) {
		int localKind = designator.obj.getKind();
		if (localKind == Obj.Var || localKind == Obj.Elem || localKind == Obj.Fld)
			return true;
		return false;
	}

	public void visit(DesigAssign desigAssign) {
		checkDesigType(desigAssign.getDesignator());
		
		Struct tempL = desigAssign.getDesignator().obj.getType();
		Struct tempR = ((ExprC) desigAssign.getExpr()).struct;
		
		if (tempR == null)
			return;

		if (tempL.getKind() != tempR.getKind())
			report_error("Greska: losi tipovi dodele", desigAssign);
	}

	public void visit(DesigName desigName) {
		desigName.obj = Tab.find(desigName.getDesigName());
	}

	private Obj getFirstLeft(DesigAddit desigAddit) {
		if (desigAddit.getDesigAdditional() instanceof NoDesigAddit) {
			SyntaxNode parent = desigAddit.getParent();
			while (parent instanceof DesigAddit)
				parent = parent.getParent();
			return ((Designator) parent).getDesigName().obj;
		} else
			return desigAddit.getDesigAdditional().obj;

	}

	public void visit(DesigId desigId) {
		Obj firstLeft = getFirstLeft((DesigAddit) desigId.getParent());

		if (firstLeft == Tab.noObj) // Greska
			desigId.obj = Tab.noObj;
		else {
			desigId.obj = Tab.noObj;
			firstLeft.getType().getMembers().forEach(e -> {
				if (e.getName().equals(desigId.getPartName())) {
					desigId.obj = e;
					report_info("pristup polju/metodi " + desigId.getPartName() + " ", desigId);
					return;
				}
			});
			
			if (desigId.obj == Tab.noObj)
				report_error("Greska: Ne postoji metod/polje ", desigId);
		}
	}

	public void visit(Designator desig) {
		Obj temp = desig.getDesigName().obj;

		if (desig.getDesigAdditional() instanceof NoDesigAddit) {
			desig.obj = temp;
			if (desig.obj.getKind() == Obj.Con)
				report_info("Pristup konstanti " + desig.obj.getName(), desig);
			else if (desig.obj.getKind() == Obj.Var)
				report_info("Pristup promenljivoj " + desig.obj.getName(), desig);
			return;
		}

		if (desig.getDesigAdditional() instanceof NoDesigAddit)
			desig.obj = desig.getDesigName().obj;
		else
			desig.obj = desig.getDesigAdditional().obj;
	}

	public void visit(DesigAddit desigAddit) {
		desigAddit.obj = desigAddit.getDesigParts().obj;
	}

	public void visit(DesigMultiple desigMultiple) {
		if (desigMultiple.getDesignator().obj.getType().getKind() != Struct.Array) {
			report_error("Greska: za dekomponovanje niza mora biti niz sa desne strane!", desigMultiple);
		}
	}

	public void visit(FactorLen factorLen) {
		if (factorLen.getDesignator().obj.getType().getKind() != Struct.Array) {
			report_error("Greska: len()-u mora biti prosledjen niz!", factorLen);
		}
	}

	public void visit(FactorChrDesig factorChr) {
		if (factorChr.getDesignator().obj.getType().getKind() != Struct.Int) {
			report_error("Greska: chr()-u mora biti prosledjen broj!", factorChr);
		}
	}

	public void visit(FactorChrNumber factorChr) {
		if (!(factorChr.getConstVal() instanceof NumConst)) {
			report_error("Greska: chr()-u mora biti prosledjen broj!", factorChr);
		}
	}

	public void visit(FactorOrdDesig factorOrd) {
		if (factorOrd.getDesignator().obj.getType().getKind() != Struct.Char) {
			report_error("Greska: ord()-u mora biti prosledjen char!", factorOrd);
		}
	}

	public void visit(FactorOrdNumber factorOrd) {
		if (!(factorOrd.getConstVal() instanceof CHARACTERConst)) {
			report_error("Greska: ord()-u mora biti prosledjen char!", factorOrd);
		}
	}

	public void visit(DesigArr desigArr) {
		Obj firstLeft = getFirstLeft((DesigAddit) desigArr.getParent());

		if (firstLeft == Tab.noObj)
			desigArr.obj = Tab.noObj;
		else {
			if (desigArr.getExpr().struct != Tab.intType)
				report_error("Greska: u [] mora biti int", desigArr);

			if (firstLeft.getType().getKind() == Struct.Array)
				desigArr.obj = new Obj(Obj.Elem, "elem", firstLeft.getType().getElemType()); // element niza, tog i tog
																								// tipa
			else {
				report_error("Greska: " + firstLeft.getName() + " nije niz ", desigArr);
				desigArr.obj = Tab.noObj;
			}
		}
	}

	public void visit(DesigINC desigPlusPlus) {
		if (!checkDesigType(desigPlusPlus.getDesignator())
				|| desigPlusPlus.getDesignator().obj.getType() != Tab.intType)
			report_error("Greska: plus plus nije var int", desigPlusPlus);
	}

	public void visit(DesigDEC desigMinusMinus) {
		if (!checkDesigType(desigMinusMinus.getDesignator())
				|| desigMinusMinus.getDesignator().obj.getType() != Tab.intType)
			report_error("Greska: minus minus nije var int", desigMinusMinus);
	}

	public void visit(StatementRead statementRead) {
		Designator d = statementRead.getDesignator();
		if (checkDesigType(d))
			if (d.obj.getType() == MyTab.intType || d.obj.getType() == MyTab.charType
					|| d.obj.getType() == MyTab.boolType) {
				report_info("read()", statementRead);
				return;
			}
		report_error("Greska: read nema dobre parametre", statementRead);
	}

	public void visit(StatementPrint statementPrint) {
		Struct kind = statementPrint.getExpr().struct;
		if (kind != Tab.intType && kind != Tab.charType && kind != MyTab.boolType)
			report_error("Greska: print mora imati int/char/bool", statementPrint);
	}

	private boolean checkParams(Designator desig) {

		if (actPartsPassed.size() == actPartsRequired.size()) {
			int i = 0;
			for (Obj req : actPartsRequired) {
				if (req.getType() != actPartsPassed.get(i))
					if (!(req.getType().getKind() == Struct.Array && actPartsPassed.get(i).getKind() == Struct.Array)) {
						i = -1;
						break;
					}
				i++;
			}
			if (i != -1)
				return true;
		}
		/*
		if (actPartsPassed.size() + 1 == actPartsRequired.size()) {
			int i = 0;
			boolean prvi = true;
			for (Obj req : actPartsRequired) {
				if (prvi) {
					prvi = false;
					continue;
				}
				if (req.getType() != actPartsPassed.get(i))
					if (!(req.getType().getKind() == Struct.Array && actPartsPassed.get(i).getKind() == Struct.Array)) {
						i = -1;
						break;
					}
				i++;
			}
			if (i != -1)
				return true;
		}
		*/

		return false;
	}

	public void visit(DesigMethod desigMethod) {
		// Obj localObj = Tab.find(desigMethod.getDesignator().obj.getName());

		if (desigMethod.getDesignator().obj.getKind() != Obj.Meth) {
			report_error("Ne postoji metoda " + desigMethod.getDesignator().obj.getName(), desigMethod);
		} else {
			report_info("Poziv funkcije " + desigMethod.getDesignator().obj.getName(), desigMethod);
		}
		actPartsPassed = null;
		actPartsRequired = null;
	}

	public void visit(FactorConst factorConst) {
		factorConst.struct = factorConst.getConstVal().struct;
	}

	public void visit(FactorNewClass factorNewClass) {
		if (factorNewClass.getType().struct.getKind() != Struct.Class) {
			report_error("nije klasa", factorNewClass);
		} else
			report_info("Nov objekat tipa " + factorNewClass.getType().getTypeName(), factorNewClass);
		factorNewClass.struct = factorNewClass.getType().struct;
	}

	public void visit(FactorNewArray factorNewArray) {
		factorNewArray.struct = new Struct(Struct.Array, factorNewArray.getType().struct);

		if (factorNewArray.getExpr().struct != Tab.intType)
			report_error("Greska: u [] mora stajati int ", factorNewArray);
	}

	public void visit(FactorExpr factorExpr) {
		factorExpr.struct = ((ExprC) factorExpr.getExpr()).struct;
	}

	public void visit(FactorDes factorDes) {
		factorDes.struct = factorDes.getDesignator().obj.getType();
		if (factorDes.getOptActPartsOpt() instanceof NoOptActParts)
			return;
		if (factorDes.getDesignator().obj.getKind() != Obj.Meth) {
			report_error("Greska: " + factorDes.getDesignator().getDesigName().getDesigName() + " nije funkcija/metoda",
					factorDes);
			return;
		}

		actPartsRequired = factorDes.getDesignator().obj.getLocalSymbols();

		if (!checkParams(factorDes.getDesignator()))
			report_error("Greska: losi parametri pri pozivu methode "
					+ factorDes.getDesignator().getDesigName().getDesigName(), factorDes);

		factorDes.struct = factorDes.getDesignator().obj.getType();

		actPartsRequired = null;
		actPartsPassed = null;
	}

	public void visit(NoActParts na) {
		actPartsPassed = new ArrayList<Struct>();
	}

	public void visit(ActPartsC actPart) {
		if (actPartsPassed == null)
			actPartsPassed = new ArrayList<Struct>();
		actPartsPassed.add(actPart.getExpr().struct);
	}

	public void visit(ActPartsE actPart) {
		if (actPartsPassed == null)
			actPartsPassed = new ArrayList<Struct>();
		actPartsPassed.add(actPart.getExpr().struct);
	}
/*
	public void visit(CondCond condCond) {
		condCond.struct = condCond.getCondition().struct;

		if (condCond.struct == MyTab.boolType) {
			report_info("Dobar uslov", condCond);
		} else
			report_error("Greska: uslov nije bool", condCond);
	}

	public void visit(CondTer condTer) {
		condTer.struct = condTer.getTernary().struct;
		if (condTer.struct == MyTab.boolType)
			report_error("Dobar uslov", condTer);
		else
			report_info("Greska: uslov nije bool", condTer);
	}

	public void visit(ConditionC cond) {
		if (cond.getCondition().struct == MyTab.boolType && cond.getCondTerm().struct == MyTab.boolType)
			cond.struct = MyTab.boolType;
		else
			report_error("Greska: uslov nije bool", cond);
	}

	public void visit(ConditionT cond) {
		cond.struct = cond.getCondTerm().struct;
	}

	public void visit(CondTermC cond) {
		if (cond.getCondFact().struct == MyTab.boolType && cond.getCondTerm().struct == MyTab.boolType)
			cond.struct = MyTab.boolType;
	}

	public void visit(CondTermT cond) {
		cond.struct = cond.getCondFact().struct;
	}

	public void visit(CondFactE cond) {
		cond.struct = cond.getExprNonTer().struct;
		if (cond.struct != MyTab.boolType)
			report_error("Greska: uslov nije bool", cond);
	}
	*/

	public void visit(ExprC expr) {
		expr.struct = expr.getTerm().struct;
		if (expr.getOptMinus() instanceof OptMin)
			if (expr.struct != Tab.intType) {
				report_error("Greska: expr mora biti tipa int", expr);
				expr.struct = Tab.noType;
			}

		if (!(expr.getAddTerm() instanceof NoAddTerm) && expr.getTerm().struct != Tab.intType) {
			report_error("Greska: sabiranje nije tipa int", expr.getParent());
		}
	}

	public void visit(TermM term) {
		if (term.getTerm().struct != Tab.intType || term.getFactor().struct != Tab.intType)
			report_error("Greska: mnozenje nije tipa int", term);
		term.struct = term.getTerm().struct;
	}

	public void visit(TermF term) {
		term.struct = term.getFactor().struct;
	}

	public void visit(AddTermA addTerm) {
		addTerm.struct = addTerm.getTerm().struct;
		if ((addTerm.getAddTerm() instanceof AddTermA && addTerm.getAddTerm().struct != Tab.intType)
				|| addTerm.getTerm().struct != Tab.intType) {
			report_error("Greska: sabiranje nije tipa int", addTerm.getParent());
			addTerm.struct = Tab.noType;
		}
	}

	@Override
	public void visit(StatementReturn stmReturn) {
		// TODO Auto-generated method stub
	}

	@Override
	public void visit(StmtLabelColon StmtLabelColon) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void visit(MatchedStmt MatchedStmt) {
		// TODO Auto-generated method stub
		
	}
}