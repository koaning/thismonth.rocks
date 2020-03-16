install:
	pip install -r requirements
	npm install http-server purgecss@1.4.2 uglifycss

website:
	python automator.py run-jinja
	npx tailwindcss build styles.css -o src/all.css
	npx purgecss --css src/all.css --content src/*.html --out public
	npx uglifycss --ugly-comments public/all.css > public/style.css

clean:
	rm -rm public/*