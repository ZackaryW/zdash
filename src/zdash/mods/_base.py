from functools import cache
import os

class ZDashMod:
    @cache
    def get_icon(self):
        pass

    def on_path_click(self, path):
        pass

    def _cache_icon(self, url : str):
        import requests
        import os
        from zdash import zdash_dir
        filepath = os.path.join(zdash_dir, "cache", self.__class__.__name__)
        if os.path.exists(filepath):
            return filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(requests.get(url).content)
        return filepath

    def parse_existing(self, cfg):
        pass

    def get_name(self, path):
        return os.path.basename(path)
