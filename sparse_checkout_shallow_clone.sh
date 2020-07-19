#https://stackoverflow.com/a/28039894
if [[ ! -d ds/dynamic-search ]];
then
	git init ds
	cd ds
	git remote add origin https://github.com/allofphysicsgraph/dynamic-search
	git config core.sparsecheckout true
	echo "search_d3js_graph/*" >> .git/info/sparse-checkout
	git pull --depth=1 origin master
else
	cd ds/dynamic-search
	git pull

fi
