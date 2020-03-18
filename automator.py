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


@click.command()
def run_jinja():
    """It's not easy being red."""
    glob = pathlib.Path("src/ideas").glob("*.yml")
    d = [yaml.load(p.read_text(), Loader=yaml.FullLoader) for p in glob]
    env = Environment(
        loader=FileSystemLoader('src'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    with open('public/index.html', 'w') as f:
        f.write(env.get_template('index.html').render(ideas=d))
    
    for p in pathlib.Path("src/img").glob("*.svg"):
        copyfile(p, pathlib.Path(f"public/img/{p.parts[-1]}"))
    for p in pathlib.Path("src/img").glob("*.png"):
        copyfile(p, pathlib.Path(f"public/img/{p.parts[-1]}"))


main.add_command(run_jinja)
main.add_command(to_json)

if __name__ == "__main__":
    main()
