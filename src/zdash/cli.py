import click
import os
@click.group()
def cli():
    pass

@cli.command(help="start gui")
def gui():
    from zdash.gui import main
    main()

@cli.command(help="parse existing paths")
@click.option("-ne", "--no-eagle", is_flag=True, help="do not parse eagle paths")
@click.option("-no", "--no-obsidian", is_flag=True, help="do not parse obsidian paths")
def parse(no_eagle, no_obsidian):
    from zdash import config
    if not no_eagle:
        config.mods["eagle"].parse_existing(config)
    if not no_obsidian:
        config.mods["obsidian"].parse_existing(config)  

@cli.command(help="purge all pathes")
@click.option("-a", "--all", is_flag=True, help="purge all paths")
def purge(all):
    from zdash import config
    if all:
        config.config["pathes"] = []
    else:
        config.config["pathes"] = [p for p in config.config["pathes"] if p["type"] != "obsidian" and os.path.exists(p["path"])]
    config.save_config()

@cli.command(help="add path")
@click.argument("path")
@click.option("-t", "--type", type=click.Choice(["eagle", "obsidian"]), help="type of the path", required=True)
@click.option("-n", "--name", help="name of the path", required=False)
@click.option("-d", "--description", help="description of the path", required=False)
@click.option("-i", "--icon", help="icon of the path", required=False)
def add(path, type, name, description, icon):
    from zdash import config
    mod = config.mods[type]
    if name is None:
        name = mod.get_name(path)

    config.add_path(path, type, icon, description)

@cli.command(help="open config file")
def open():
    from zdash import config_file
    os.system(f"start {config_file}")

