DUMP_SRC=./swfdump.sh
EXTRACT_SRC=./extract.sh
DUMP_EXE=$(shell $(DUMP_SRC))
EXTRACT_EXE=$(shell $(EXTRACT_SRC))
UPPERCASE_SRC=./uppercase.sh
UPPERCASE_EXE=$(shell $(UPPERCASE_SRC))
SWF_FILES=$(wildcard rips/*.swf)
DAT_FILES=$(patsubst rips/%.swf, %.dat, $(SWF_FILES))
TXT_FILES=$(patsubst rips/%.swf, %.txt, $(SWF_FILES))

.PHONY : main
main: $(DAT_FILES) $(TXT_FILES) uppercase

.PHONY : dumps
dumps: $(DAT_FILES)

.PHONY : extract
extract: $(TXT_FILES)

uppercase: $(UPPERCASE_SRC) 
	@$(UPPERCASE_EXE)

%.dat: rips/%.swf $(DUMP_SRC)
	@echo $*.swf
	@$(DUMP_EXE) $< > dumps/$*.dat

%.txt: dumps/%.dat $(EXTRACT_SRC)
	@echo $*.dat
	@$(EXTRACT_EXE) $< | tee extracts/$*.txt

.PHONY : clean
clean:
	@rm -rf dumps
	@rm -rf extracts
	@mkdir -p dumps
	@mkdir -p extracts
	
.PHONY : variables
variables:
	@echo SWF_FILES: $(SWF_FILES)
	@echo DAT_FILES: $(DAT_FILES)
	@echo TXT_FILES: $(TXT_FILES)
	@echo DUMP_SRC: $(DUMP_SRC)
	@echo EXTRACT_SRC: $(EXTRACT_SRC)
	@echo UPPERCASE_SRC: $(UPPERCASE_SRC)