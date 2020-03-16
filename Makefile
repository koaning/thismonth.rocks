install:
	pip install -r requirements
	npm install http-server purgecss@1.4.2 uglifycss

website:
	python automator.py run-jinja
	npx tailwindcss build styles.css -o public/all.css
	npx purgecss --css public/*.css --content src/*.html > public/style.css
	npx uglifycss --ugly-comments public/style.css > public/style-min.css
	rm public/all.css public/style.css

clean:
	rm -rm public/*