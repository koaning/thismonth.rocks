import json
import pathlib
from shutil import copyfile

import yaml
import click
from jinja2 import Environment, select_autoescape, FileSystemLoader

@click.group()
def main():
    """This cli is oke, okeh?"""
    pass


@click.command()
def to_json():
    """It's easy being green."""
    glob = pathlib.Path("src/ideas").glob("*.yml")
    d = [yaml.load(p.read_text(), Loader=yaml.FullLoader) for p in glob]
    pathlib.Path("public/tips.json").write_text(json.dumps(d))


def handle_images():
    for p in pathlib.Path("src/img/icons/").glob("*"):
        p_towards = f"public/img/icons/{p.parts[-1]}"
        print(f"moving {p} -> {p_towards}")
        copyfile(p, pathlib.Path(p_towards))
    for p in pathlib.Path("src/img").glob("*.png"):
        p_towards = f"public/img/{p.parts[-1]}"
        print(f"moving {p} -> {p_towards}")
        copyfile(p, pathlib.Path(p_towards))

def handle_category_pages(env, ideas):
    flatten = lambda l: [item for sublist in l for item in sublist]
    uniq_tags = set(flatten([d['tags'] for d in ideas]))
    
    for tag in uniq_tags:
        idea_subset = [d for d in ideas if tag in d['tags']]
        with open(f'public/{tag}.html', 'w') as f:
            f.write(env.get_template('index.html').render(ideas=idea_subset, tag=tag))
            click.echo("created page: " + click.style(f"public/{tag}.html", "blue"))

@click.command()
def run_jinja():
    """It's not easy being red."""
    glob = pathlib.Path("src/ideas").glob("*.yml")
    ideas = [yaml.load(p.read_text(), Loader=yaml.FullLoader) for p in glob]
    env = Environment(
        loader=FileSystemLoader('src'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    with open('public/index.html', 'w') as f:
        f.write(env.get_template('index.html').render(ideas=ideas))
    handle_images()
    handle_category_pages(env, ideas=ideas)
    


main.add_command(run_jinja)
main.add_command(to_json)

if __name__ == "__main__":
    main()
