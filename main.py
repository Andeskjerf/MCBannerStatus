from src import Canvas, Status
from src.argument_handler import ArgumentHandler


def main():

    args = ArgumentHandler()

    status = Status(
        args.host,
        args.port,
        args.online_text,
        args.offline_text,
        args.player_offline_text
    )

    # Only update the image if there's any new data
    if not status.updated and not args.force_update:
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
