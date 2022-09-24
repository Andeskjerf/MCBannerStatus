import os


class ImageRotator:

    path: str = f"{os.getcwd()}/images"
    files_path: list = []

    def __init__(self) -> None:
        self.set_files()
        pass

    def set_files(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                self.files_path.append(os.path.join(root, file))

        print(self.files_path)
