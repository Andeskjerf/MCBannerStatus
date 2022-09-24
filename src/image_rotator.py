from datetime import datetime
import os

from src import utils
from src.data_cache import DataCache


class ImageRotator:

    path: str = f"{os.getcwd()}/images"
    files_path: list = []

    cache: DataCache = None
    enabled: bool = False

    def __init__(
        self,
        cache,
        enabled,
        interval
    ) -> None:
        self.cache = cache

        if enabled:
            then = cache.last_update
            now = datetime.now()
            difference = (now - then).total_seconds()

            if difference > interval:
                self.cache.last_update = now
                self.set_files()
                self.set_image()

    def set_files(self):
        for root, _, files in os.walk(self.path):
            for file in sorted(files):
                path = os.path.join(root, file)
                if utils.has_valid_extension(path):
                    self.files_path.append(path)
                else:
                    print("Invalid file extension: " + file)

    def set_image(self):
        if len(self.files_path) == 0:
            print(f"No images found in {self.path}\n"
                  "Add some images to the images folder to use this feature")
            exit()

        try:
            index = self.files_path.index(self.cache.last_image)
        except ValueError:
            index = None

        if index is not None \
                and index + 1 < len(self.files_path):
            self.cache.last_image = self.files_path[index + 1]
        else:
            self.cache.last_image = self.files_path[0]
