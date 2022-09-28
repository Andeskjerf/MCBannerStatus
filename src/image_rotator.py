from datetime import datetime
import os
import logging

from src import utils
from src.data_cache import DataCache


class ImageRotator:

    path: str = f"{os.getcwd()}/images"
    files_path: list

    cache: DataCache

    logger = None

    def __init__(
        self,
        cache,
        enabled,
        interval
    ) -> None:
        self.logger = logging.getLogger()
        self.files_path = []
        self.cache = cache

        if enabled:
            then = cache.last_update
            now = datetime.now()

            if not then:
                self.set_files()
                self.set_image()
                self.cache.last_update = now
            else:
                difference = (now - then).total_seconds()

                if difference > interval:
                    self.logger.debug("Image rotation interval reached, switching image")
                    self.set_files()

                    # No need to update the image if only a single image is present
                    if len(self.files_path) > 1:
                        self.set_image()
                        self.cache.last_update = now
                    else:
                        self.logger.debug("Only a single image present, skipping image rotation")

                # else:
                #     print("Time left until next image rotation: \n"
                #           f"    {int(interval - difference)} second(s)\n"
                #           f"    {round((interval - difference) / 60, 1)} minute(s)\n")

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
            self.logger.critical(f"No images found in {self.path} and image rotation is enabled, exiting")
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
