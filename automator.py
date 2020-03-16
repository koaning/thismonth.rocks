import json
import pathlib

import yaml
import click


@click.group()
def main():
    """This cli is oke, okeh?"""
    pass


@click.command()
def to_json():
    """It's easy being green."""
    d = [yaml.load(p.read_text(), Loader=yaml.FullLoader) for p in pathlib.Path("ideas").glob("*.yml")]
    print(json.dumps(d))


@click.command()
def run_jinja():
    """It's not easy being red."""
    from jinja2 import Environment, select_autoescape, FileSystemLoader
    d = [yaml.load(p.read_text(), Loader=yaml.FullLoader) for p in pathlib.Path("ideas").glob("*.yml")]
    print(d)
    env = Environment(
        loader=FileSystemLoader('src'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    with open('public/index.html', 'w') as f:
        f.write(env.get_template('index.html').render(ideas=d))


main.add_command(run_jinja)


if __name__ == "__main__":
    main()
