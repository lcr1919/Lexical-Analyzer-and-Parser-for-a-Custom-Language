.PHONY: archive clean


archive: 
	@make clean ; tar czf p3.tar.gz *

clean:
	@rm -R *.tar.gz *.pyc __pycache__ *~* *#* */*~* */*#* .DS_Store || true
