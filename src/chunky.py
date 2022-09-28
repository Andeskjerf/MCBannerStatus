from src.argument_handler import ArgumentHandler
from src import utils
import os
import subprocess


class Chunky:

    threads: int
    jar: str
    scenes: list
    spp: int
    texture_pack: str
    output_path: str
    scene_path: str
    delete_dumps: bool

    def __init__(self, args: ArgumentHandler) -> None:
        self.threads = args.chunky_threads
        self.jar = args.chunky_jar
        self.spp = args.chunky_spp
        self.texture_pack = args.chunky_texture
        self.output_path = args.chunky_output
        self.delete_dumps = args.delete_dumps

        utils.file_exists(self.jar)
        utils.file_exists(self.texture_pack)

        if not self.java_exists():
            raise Exception("Java is not installed")

        self.set_scenes()
        self.render_all()

    def java_exists(self) -> bool:
        result = os.popen("java -version 2>&1")
        lines = result.readlines()
        if len(lines) == 3:
            return True
        return False

    def set_scenes(self):
        self.scenes = os.popen(
            f"java -jar {self.jar} -list-scenes 2>&1"
        ).read().replace("\t", "").split("\n")

        # First two lines aren't scene names
        self.scene_path = self.scenes.pop(0).replace("Scene directory: ", "")
        self.scenes.pop(0)

        if self.scenes[-1] == "":
            self.scenes.pop()

        if len(self.scenes) == 0:
            raise Exception("No scenes found")

    def render_all(self):
        for scene in self.scenes:
            self.delete_dump(scene)
            self.render_scene(scene)
            self.create_link(scene)

    def delete_dump(self, scene):
        if self.delete_dumps:
            scene_dir = f"{self.scene_path}/{scene}"

            if utils.file_exists(f"{scene_dir}/{scene}.dump", throw=False):
                os.remove(f"{scene_dir}/{scene}.dump")

            if utils.file_exists(f"{scene_dir}/{scene}.dump.backup", throw=False):
                os.remove(f"{scene_dir}/{scene}.dump.backup")

    def render_scene(self, scene):
        with open(f"logs/{scene}.log", "w") as file:
            subprocess.call([
                "java", "-jar", self.jar,
                "-render", scene, "-f",
                "-target", str(self.spp),
                "-texture", self.texture_pack,
                "-threads", str(self.threads)
            ], stdout=file, stderr=subprocess.PIPE, text=True)

    def create_link(self, scene):
        file = f"{scene}-{self.spp}.png"
        snapshot = f"{self.scene_path}/{scene}/snapshots/{file}"
        output = f"{self.output_path}/{file}"

        if not utils.file_exists(output, throw=False):
            if utils.file_exists(snapshot, throw=False):
                os.symlink(snapshot, output)


def start_chunky(args):
    Chunky(args)
