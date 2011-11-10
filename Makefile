dist:
	mkdir PieTree-0.4/
	rm -f src/*.pyc
	rm -f examples/*.png
	cp -r CHANGES COPYING examples README src PieTree-0.4/
	cp doc/sphinx/_build/latex/PieTree.pdf PieTree-0.4/PieTree_manual.pdf
