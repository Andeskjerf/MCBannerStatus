from datetime import datetime
from src import Canvas, Status
from src.argument_handler import ArgumentHandler
from src.data_cache import Cacher
from src.image_rotator import ImageRotator


def main():

    args = ArgumentHandler()

    cache = Cacher()

    status = Status(
        cache.data,
        args.host,
        args.port,
        args.online_text,
        args.offline_text,
        args.player_offline_text
    )

    ImageRotator(
        cache.data,
        args.image_rotation,
        args.image_rotation_interval
    )

    # If image rotation is disabled and the cache contains data about it,
    # make sure to remove it and trigger an update by setting last_update
    if not args.image_rotation \
            and cache.data.last_image:
        cache.data.last_image = None
        cache.data.last_update = datetime.now()

    # Write data to cache only if it has changed
    updated = cache.has_changed()
    if updated:
        cache.write_cache()

    # Replace whatever image has been given if image rotation is enabled
    if cache.data.last_image:
        args.image_path = cache.data.last_image

    # Only update the image if there's any new data
    if not updated and not args.force_update:
        print("No new data, skipping")
        exit()

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
