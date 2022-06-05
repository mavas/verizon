from datascripts.models import Video


def import_video_file(filename):
    video = Video.objects.create(filename=filename)


@transaction.atomic
def import_video_screenshot(filename, screenshot):
    """Imports items into the database."""
    v = Video.objects.create(filename)
    VideoScreenshot.objects.create(video=v, location=screenshot)
