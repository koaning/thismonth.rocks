import json
import pathlib
from shutil import copyfile

import yaml
import click
import frontmatter
import mistune
import markdown
from jinja2 import Environment, select_autoescape, FileSystemLoader, Markup


@click.group()
def main():
    """This cli is okeh, okeh?"""
    pass


def load_md(appendix=False):
    glob = pathlib.Path("src/ideas").glob("*.md")
    results = []
    for p in glob:
        fm = frontmatter.load(p)
        d = dict(fm)
        md = mistune.create_markdown(escape=False)
        if appendix:
            d['appendix'] = md(fm.content)
        d['id'] = d['icon'].replace(".svg", "")
        results.append(d)
    return results


def handle_json_api():
    pathlib.Path("public/tips.json").write_text(json.dumps(load_md()))
    click.echo("created api: " + click.style(f"public/tips.json", "blue"))


def handle_images():
    for p in pathlib.Path("src/img/icons/").glob("*"):
        p_towards = f"public/img/icons/{p.parts[-1]}"
        click.echo(f"moving {p} -> " + click.style(str(p_towards), "blue"))
        copyfile(p, pathlib.Path(p_towards))
    for p in pathlib.Path("src/img").glob("*.*"):
        p_towards = f"public/img/{p.parts[-1]}"
        click.echo(f"moving {p} -> " + click.style(str(p_towards), "blue"))
        copyfile(p, pathlib.Path(p_towards))


def handle_index(env, ideas):
    with open('public/index.html', 'w') as f:
        f.write(env.get_template('index.html').render(ideas=ideas))


def handle_category_pages(env, ideas):
    flatten = lambda l: [item for sublist in l for item in sublist]
    uniq_tags = set(flatten([d['tags'] for d in ideas]))
    
    for tag in uniq_tags:
        idea_subset = [d for d in ideas if tag in d['tags']]
        with open(f'public/{tag}.html', 'w') as f:
            f.write(env.get_template('index.html').render(ideas=idea_subset, tag=tag))
            click.echo("created page: " + click.style(f"public/{tag}.html", "blue"))


def handle_idea_sites(env, ideas):
    for idea in ideas:
        with open(f'public/idea/{idea["id"]}.html', 'w') as f:
            f.write(env.get_template('index.html').render(ideas=ideas, open_link=idea["id"]))
            click.echo("created page: " + click.style(f'public/idea/{idea["id"]}.html', "blue"))

@click.command()
def build():
    """build the website"""
    ideas = load_md(appendix=True)
    md = markdown.Markdown(extensions=['meta'])
    env = Environment(
        loader=FileSystemLoader('src'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.filters['markdown'] = lambda text: Markup(md.convert(text))

    handle_index(env=env, ideas=ideas)
    handle_json_api()
    handle_images()
    handle_category_pages(env=env, ideas=ideas)
    handle_idea_sites(env=env, ideas=ideas)


main.add_command(build)

if __name__ == "__main__":
    main()
