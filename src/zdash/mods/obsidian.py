
from functools import cache
import json
import os
from zdash.mods._base import ZDashMod

class ObsidianMod(ZDashMod):
    @cache
    def get_icon(self):
        return self._cache_icon("https://dl.dropboxusercontent.com/s/qgise0g2yktwjb4/20201104175104_obsidian%20icon%20light.png?dl=1")
    
    def on_path_click(self, path):
        os.system(f"start obsidian://open?vault={path}")

    def get_name(self, path):
        name = os.path.basename(path)
        if name.endswith(".vault"):
            name = name[:-5]
        if name.endswith(".obs"):
            name = name[:-4]
        return name

    def parse_existing(self, cfg):
        # roaming folder
        path = os.path.join(os.getenv("APPDATA"), "obsidian", "obsidian.json")
        with open(path, "r") as f:
            data = json.load(f)
        for vault_data in data["vaults"].values():
            cfg.add_path(vault_data["path"], "obsidian")
            print(f"added obsidian path: {vault_data['path']}")
