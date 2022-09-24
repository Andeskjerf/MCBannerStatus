from src import Canvas, Status
from src.argument_handler import ArgumentHandler
from src.data_cache import Cacher
from src.image_rotator import ImageRotator


def main():

    args = ArgumentHandler()

    cache = Cacher()

    status = Status(
        cache,
        args.host,
        args.port,
        args.online_text,
        args.offline_text,
        args.player_offline_text
    )

    updated = cache.has_changed()
    if updated:
        cache.write_cache()

    # Only update the image if there's any new data
    if not updated and not args.force_update:
        print("No new data, skipping")
        exit()

    ImageRotator()

    Canvas(
        status,
        args.image_path,
        args.font_regular_path,
        args.font_italic_path,
        args.font_size,
        args.x_offset,
        args.opacity,
        args.height
    ).save_image(args.target)


if __name__ == "__main__":
    main()
