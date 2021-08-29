install:
	pip install -r requirements.txt
	npm install http-server purgecss@1.4.2 uglifycss

css: website
	npx tailwindcss build styles.css -o src/all.css
	npx purgecss --css src/all.css --content src/*.html --out public
	npx uglifycss --ugly-comments public/all.css > public/style.css

website:
	python automator.py build

clean:
	rm -rm public/*

deploy: website
	git add . 
	git commit -m moar-stuff 
	git push origin master

serve: website
	python -m http.server 8000 --directory public

netlify:
	pip install -r requirements.txt
	python automator.py build
