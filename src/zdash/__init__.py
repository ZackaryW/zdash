import os
import json

from zdash.mods.eagle import EagleMod
from zdash.mods.obsidian import ObsidianMod

# create .zdash folder in user's home directory
zdash_dir = os.path.expanduser("~/.zdash")
os.makedirs(zdash_dir, exist_ok=True)

# create .zdash/config.json file
config_file = os.path.join(zdash_dir, "config.json")

if not os.path.exists(config_file):
    with open(config_file, "w") as f:
        json.dump({"version": "0.1.0"}, f)


class ZDashConfig:
    def __init__(self):
        self.config = self.load_config()
        self.mods = {}

        self.mods["eagle"] = EagleMod()
        self.mods["obsidian"] = ObsidianMod()

    def load_config(self):
        with open(config_file, "r") as f:
            return json.load(f)

    def save_config(self):
        with open(config_file, "w") as f:
            json.dump(self.config, f)

  
    @property
    def version(self):
        return self.config["version"]

    @version.setter
    def version(self, value):
        self.config["version"] = value
        self.save_config()

    @property
    def pathes(self):
        if "pathes" not in self.config:
            self.config["pathes"] = []
        return self.config["pathes"]


    def add_path(self, path, type : str, icon : str = None, description : str = None):
        assert os.path.exists(path), f"Path {path} does not exist"
        if any(p["path"] == path for p in self.pathes):
            print(f"Path {path} already exists")
            return
        path = os.path.abspath(path)
        if path not in self.pathes:
            self.pathes.append({"path": path, "type": type, "icon": icon, "description": description})
            self.save_config()

    def remove_path(self, path):
        path = os.path.abspath(path)
        if path in self.pathes:
            self.pathes.remove(path)
            self.save_config()
        else:
            for p in self.pathes:
                if path == os.path.basename(p["path"]):
                    self.pathes.remove(p)
                    self.save_config()
                    return
            raise ValueError(f"Path {path} not found in config")


config = ZDashConfig()


