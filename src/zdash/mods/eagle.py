from functools import cache
import os
from zdash.mods._base import ZDashMod

class EagleMod(ZDashMod):
    @cache
    def get_icon(self):
        return "C:/Program Files/Eagle/eaglelibrary.ico"
    
    def on_path_click(self, path):
        from eaglewrap.api import EagleApi
        try:
            EagleApi.librarySwitch(path)
        except Exception as e:
            print(f"error switching eagle library: {e}")

    def parse_existing(self, cfg):
        from eaglewrap.cfg import EagleCfg
        # loop through all the opened libraries and add the pathes
        for lib in EagleCfg.settings()["libraryHistory"]:
            try:
                cfg.add_path(lib, "eagle")
                print(f"added eagle path: {lib}")
            except Exception as e:
                print(f"error adding eagle path: {lib} - {e}")

    def get_name(self, path):
        return os.path.basename(path).replace(".library","")
