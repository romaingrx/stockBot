export:
	mkdir -p ~/bin
	cp stockBot ~/bin
	if test -f ~/.bash_profile; then
		echo 'export PATH=$PATH":$HOME/bin"' >> ~/.bash_profile
		source ~/.bash_profile
	else
		if test -f ~/.profile; then
			echo 'export PATH=$PATH":$HOME/bin"' >> ~/.profile
			source ~/.profile
		else
			echo 'Impossible to export stockBot'
		fi
	fi

test: unit_tests
	python unit_tests
