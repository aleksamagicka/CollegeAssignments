package rs.ac.bg.etf.pp1;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;

import java_cup.runtime.Symbol;

import org.apache.log4j.Logger;
import org.apache.log4j.xml.DOMConfigurator;

import rs.ac.bg.etf.pp1.ast.Program;
import rs.ac.bg.etf.pp1.util.Log4JUtils;
import rs.etf.pp1.mj.runtime.Code;

public class Compiler {

	static {
		DOMConfigurator.configure(Log4JUtils.instance().findLoggerConfigFile());
		Log4JUtils.instance().prepareLogFile(Logger.getRootLogger());
	}

	public static void main(String[] args) throws Exception {
		Logger log = Logger.getLogger(Compiler.class);

		Reader br = null;
		try {
			//File sourceCode = new File("test/test301.mj");
			File sourceCode = new File(args[0]);

			log.info("Compiling source file: " + sourceCode.getAbsolutePath());

			br = new BufferedReader(new FileReader(sourceCode));
			Yylex lexer = new Yylex(br);

			MJParser p = new MJParser(lexer);
			Symbol s = p.parse();

			if (p.errorDetected)
				log.info("Postoji sintaksna greska!");
			else {
				Program prog = (Program) (s.value);
				MyTab.myInit();
				MyTab.dump();

				log.info(prog.toString(""));
				log.info("===================================");

				SemanticPass v = new SemanticPass();
				prog.traverseBottomUp(v);

				log.info("===================================");

				if (!p.errorDetected && v.passed()) {
					//File objFile = new File("test/program.obj");
					File objFile = new File(args[1]);
					if (objFile.exists())
						objFile.delete();

					CodeGenerator codeGenerator = new CodeGenerator();
					Code.dataSize = v.nVars;
					prog.traverseBottomUp(codeGenerator);

					Code.mainPc = codeGenerator.getMainPc();
					Code.write(new FileOutputStream(objFile));

					log.info("Parsiranje uspesno zavrseno!");
				} else {
					log.error("Parsiranje NIJE uspesno zavrseno!");
				}
			}
		} finally {
			if (br != null)
				try {
					br.close();
				} catch (IOException e1) {
					log.error(e1.getMessage(), e1);
				}
		}
	}
}