import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app.models import Video, VideoScreenshot


def convert_video_to_numpy(video):
    """Perminently converts a video file on disk to a numpy array."""


def restore_video_file_from_numpy(video):
    """Perminently transforms a numpy array into its original video file."""


def read_video_width_height_from_video(v):
    """Reads a video's width and height from filename."""
    if isinstance(v, Video):
        fn = v.get_filename()
    else:
        fn = v
    with opencv_videocapture(fn) as vc:
        w = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return w, h

def _database_video_import(file_path, dct, update=True):
    v = get_video(file_path)
    if v and not update:
        db_created = False
        return v, db_created
    known = False
    #if not Video.objects.filter(**dct).exists():
    qs = Video.objects.filter(filename__iexact=dct['filename'])
    qs = qs.filter(file_extension__iexact=dct['file_extension'])
    if not qs.exists():
        v = Video.objects.create(**dct)
        log.info('Created video %s.' % v)
        db_created = True
    else:
        #v = Video.objects.get(**dct)
        qs = Video.objects.filter(filename__iexact=dct['filename'])
        qs = qs.filter(file_extension__iexact=dct['file_extension'])
        if len(qs) == 1:
            v = qs[0]
        else: raise MultipleObjectsReturned
        log.info('Video already exists (%s).' % v)
        if not v.end_frame: v.end_frame = dct['end_frame']
        if not v.end_frame_date: v.end_frame_date = dct['end_frame_date']
        if not v.atime: v.atime = dct['atime']
        if not v.mtime: v.mtime = dct['mtime']
        if not v.md5: v.md5 = dct['md5']
        if not v.file_path: v.file_path = dct['file_path']
        if not v.root_path: v.root_path = dct['root_path']
        if not v.root_path_name: v.root_path_name = dct['root_path_name']
        v.save()
        db_created = False
    return v, db_created

@transaction.atomic
def import_video_file(file_path, root_path=None, verbose=False,
        frame_count=None, db=True, pretend=False, md5=True, bucket=None,
        vector_file=False, samples_file=None, dataset=None, frames=None,
        rectangles=False, framecache=False, framecache=False):
    """
    Imports a video from a file.

    This function makes the database aware of a video file on disk, uploads the
    video to the cloud, uploads the video images, adds the images to vector
    file, etc.

    TODO: This function should be reliably predictable when it's importing a
    video it already knows about.

    :param file_path: The file path to the video.
    :param root_path: Consider the paths in file_path, if any, to 
    :param framecache: Whether or not to add the video frames to the local file
        system frame cache.
    :param framecache: Whether or not to add the video frames to the cloud
        video frame cache.
    """
    dct = dict()
    # Root paths.
    f = os.path.abspath(file_path)
    if root_path:
        if not root_path.startswith('/') and file_path.startswith(root_path):
            # 'smash'
            dct['root_path_name'] = root_path
            dct['root_path'] = file_path
        else:
            # '/home/tempuser/smash'
            dct['root_path'] = os.path.split(root_path)[0]
            dct['root_path_name'] = os.path.basename(root_path)
        file_path = file_path[
	    len(os.path.join(dct['root_path'], dct['root_path_name'])):]
        if file_path.startswith('/'): file_path = file_path[1:]
        dct['file_path'] = os.path.split(file_path)[0]
    else:
        dct['root_path_name'] = os.path.split(file_path)[0]
        dct['root_path'] = os.path.abspath(
            os.path.split(os.path.split(file_path)[0])[0])
        dct['file_path'] = os.path.split(file_path)[0]
    dct['filename'] = os.path.splitext(os.path.split(f)[1])[0]
    file_extension = os.path.splitext(os.path.split(f)[1])[1]
    if file_extension.startswith('.'):
        dct['file_extension'] = file_extension[1:]
    else: dct['file_extension'] = file_extension
    if os.path.split(os.path.split(file_path)[1])[0] != '':
        dct['file_path'] = os.path.split(os.path.split(file_path)[1])[0]
    if 'file_path' in dct:
        fn = os.path.abspath(os.path.join(dct['root_path'], dct['root_path_name'], dct['file_path'], dct['filename'] + '.' + dct['file_extension']))
    else:
        fn = os.path.abspath(os.path.join(dct['root_path'], dct['root_path_name'], dct['filename'] + '.' + dct['file_extension']))
    # Other stuff.
    st = os.stat(fn); del fn
    dct['atime'] =\
        datetime.datetime.fromtimestamp(st.st_atime).replace(tzinfo=utc)
    dct['mtime'] =\
        datetime.datetime.fromtimestamp(st.st_mtime).replace(tzinfo=utc)
    dct['size'] = st.st_size
    st = os.stat(f)
    dct['atime'] = datetime.datetime.fromtimestamp(st.st_atime).\
        replace(tzinfo=utc)
    dct['mtime'] = datetime.datetime.fromtimestamp(st.st_mtime).\
        replace(tzinfo=utc)
    dct['size'] = st.st_size
    dct['start_frame'] = 0
    dct['width'], dct['height'] = read_video_width_height_from_filename(f)
    dct['end_frame'] = count_video_frames(f)
    dct['end_frame_date'] = datetime.datetime.now()
    #dct['md5'], _ = MD5Hash.objects.get_or_create(
    #    content=compute_md5_filename(file_path))
    dct['md5'], _ = MD5Hash.objects.get_or_create(
        content=compute_md5_filename(f))
    v, db_created = _database_video_import(file_path, dct)
    # Done.
    return v, db_created


def create_video():
    """Creates a video programmatically."""


@transaction.atomic
def import_video_screenshot(filename, screenshot):
    """Imports items into the database."""
    v = Video.objects.create(filename)
    VideoScreenshot.objects.create(video=v, location=screenshot)


class Command(BaseCommand):
    help = "Utility"

    def add_arguments(s, p):
        p.add_argument('--label', action='store',
            dest='label', help='Label either yes or no.')
        p.add_argument('--input-file', action='store', dest='input_file',
            help='Which directory to process.')
        p.add_argument('--pretend', action='store_true', dest='pretend',
            help='Whether or not to pretend to do things.')
        p.add_argument('--init', action='store_true', dest='init',
            help='Do the initialization phasee of a journey.')
        p.add_argument('--count', dest='count', metavar='N', type=int,
            help='Perform N processing steps for a given journey.')
        p.add_argument('--count2', dest='count2', metavar='N', type=int,
            help='Perform N processing steps for a given journey.')
        p.add_argument('--video', dest='video', metavar='V',
            help='A particular video to process.')
        p.add_argument('--frame-number', dest='frame_number', type=int,
            help='The frame number to consider.')
        p.add_argument('--debug', action='store_true', dest='debug',
            help='Whether or not to produce lots of debugging output.')

    def handle(self, *args, **opts):
        """High-level interface, which can handle CTRL-C input."""
