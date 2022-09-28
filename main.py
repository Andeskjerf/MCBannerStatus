import schedule
import time
import threading
import logging
import os

from datetime import datetime
from src import (
    Canvas,
    Status,
    start_chunky,
    Cacher,
    ArgumentHandler,
    ImageRotator
)

if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.exists("images"):
    os.makedirs("images")

logging.basicConfig(
    filename="logs/status.log",
    format="%(asctime)s %(levelname)s %(message)s",
    filemode="w",
    level=logging.INFO
)

logger = logging.getLogger()


def update_image(args, cache, status):
    logger.debug("Checking for status updates")

    status.fetch_status()

    ImageRotator(
        cache.data,
        args.image_rotation,
        args.image_rotation_interval
    )

    # If image rotation is disabled and the cache contains data about it,
    # make sure to remove it and trigger an update by setting last_update
    if not args.image_rotation \
            and cache.data.last_image:
        logger.debug("Image rotation disabled, removing last image")
        cache.data.last_image = None
        cache.data.last_update = datetime.now()

    # Write data to cache only if it has changed
    updated = cache.has_changed()
    if updated:
        logger.debug("Data changed, writing cache")
        cache.write_cache()

    # Replace whatever image has been given if image rotation is enabled
    if cache.data.last_image:
        args.image_path = cache.data.last_image

    # Only update the image if there's any new data
    if not updated and not args.force_update:
        logger.debug("No new data, skipping update")
        return

    Canvas(
        cache.data.active,
        status.get_status(),
        status.get_player_count(),
        cache.data.name,
        cache.data.favicon,
        args.image_path,
        args.font_regular_path,
        args.font_italic_path,
        args.font_size,
        args.x_offset,
        args.opacity,
        args.height
    ).save_image(args.target)


def run_threaded(job_func, name=None, *args, **kwargs):
    for job in threading.enumerate():
        if job.name == name:
            logger.debug(f"Job already running, skipping - Job: {name}")
            return

    job_thread = threading.Thread(target=job_func, name=name, args=args, kwargs=kwargs)
    job_thread.start()


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

    update_image(args, cache, status)

    if args.chunky_enabled:
        # schedule.every(args.interval).seconds.do(run_threaded, start_chunky, "chunky", args)
        schedule.every().monday.at("00:00").do(run_threaded, start_chunky, "chunky", args)

    schedule.every(args.interval).seconds.do(
        run_threaded,
        update_image,
        "data_update",
        args,
        cache,
        status
    )

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
