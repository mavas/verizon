import datetime
import logging
import os
from contextlib import contextmanager
import pickle

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.timezone import utc
from django.core.cache import caches
import numpy as np
import youtube_dl
import cv2

from app.models import Video, VideoScreenshot


_HELP = """
This 'label' Django management command operates on video files, and is used for
machine learning (data curation).
"""

log = logging.getLogger('django.server')
cache = caches['default']
framecache = caches['framecache']


@contextmanager
def opencv_videocapture(f, vc=None):
    if isinstance(f, Video):
        f = f.get_local_file_path()
    if not os.path.isfile(f):
        raise Exception("%s is not a file." % f)
    log.debug("OpenCV VideoCapture opening %s.." % f)
    if not vc:
        vc = cv2.VideoCapture(f)
    if not vc.isOpened():
        m = "Could not open %s with OpenCV video capture." % f
        log.error(m)
        raise Exception(m)
    try:
        yield vc
    finally:
        log.debug("OpenCV VideoCapture closing %s.." % f)
        vc.release()

def get_random_video_frame(v):
    return random.sample(range(0, v.end_frame), 1)[0]
def _get_raw_video_frames_range(minimum, maximum):
    result_list = []
    for fn in range(minimum, maximum):
        key = '%d_%d' % (v.id, fn)
        result = framecache.get(key)
        if result is not None:
            result_list.append(result)
    return result_list
def get_raw_video_frames(v, frames, rectangle=None, vc=None, use_cache=True):
    """
    Returns the raw data of a video frame.

    This is the best function to use in regards to retrieving a video's frame
    data, as it incorporates caching, and is designed to be used universally
    wherever a video frame is needed.
    """
    # A single integer.
    if isinstance(frames, int):
        frame = frames
        if use_cache:
            # ..
            key = '%d_%d' % (v.id, frame)
            result = framecache.get(key)
            if result is not None:
                return result

        #if use_cache:
        #    if not os.path.exists(os.path.join(settings.DEVELOPMENT_MELEE_PATH, 
        rval, value = read_video_frame_number(v, frame, vc=vc)
        if rval and use_cache:
            framecache.set(key, value)
        return value
    # A range of integers, expressed as a 2-tuple.
    elif isinstance(frames, tuple) and len(frames) == 2:
        minimum, maximum = frames[0], frames[1]
        return _get_raw_video_frames_range(minimum, maximum)
    # ...
    elif is_number_range(frames):
        minimum, maximum = parse_number_range(frames)
        return _get_raw_video_frames_range(minimum, maximum)

def count_video_frames(f, add_frame_numbers=False):
    """Counts the number of video frames found in a file."""
    f = os.path.abspath(f)
    if os.path.isfile(f):
        with opencv_videocapture(f) as vc:
            count = vc.get(cv2.CAP_PROP_FRAME_COUNT)
            return int(count)
    else:
        raise Exception("Not a file.")

def convert_video_to_numpy_journey(v, j):
    frames_already_present = get_journey_frames(v)
    disjoint_frames = compute_disjoint_frames(v)
    with opencv_videocapture(v) as vc:
        pass

    if not journey_present(v):
        create_journey(v)
    else:
        journey = load_journey(v)

def convert_video_to_numpy(v):
    """Perminently moves/converts a video file on disk to a numpy array, while
    saving/preserving all metadata."""
    if isinstance(v, Video):
        w, h = v.width, v.height
        end_frame = v.end_frame
        v.end_frame = count_video_frames(v.get_filename())
    with opencv_videocapture(v) as vc:
        w = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        end_frame = count_video_frames(v)
        o = np.zeros(shape=(end_frame, h, w, 3), dtype=np.int32)
        c = 0
        rval = True
        while rval:
            rval, img = vc.read()
            if rval:
                o[c] = img
                c += 1
            else:
                raise Exception
    return o


def download_youtube_video():
    filename = 'file.movie'
    o = dict()
    o['outtmpl'] = filename
    with youtube_dl.YoutubeDL(o) as ydl:
        ydl.download([url])

    v = get_video(url)
    width, height = read_video_width_height_from_video(v)
    _IMAGE_SHAPE = (width, height, 1)
    _NAMES = ['melee', 'negative']
    import tensorflow_datasets.public_api as tfds
    features = tfds.features.FeaturesDict({
        'image': tfds.features.Image(shape=_IMAGE_SHAPE),
        'label': tfds.features.ClassLabel(names=_NAMES),
    }),

    with open(output_file, 'wb') as fh:
        pickle.dump(fh, d)


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
    qs = Video.objects.filter(filename__iexact=dct['filename'])
    qs = qs.filter(file_extension__iexact=dct['file_extension'])
    if not qs.exists():
        v = Video.objects.create(**dct)
        log.info('Created video %s.' % v)
        db_created = True
    else:
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

def read_video_width_height_from_filename(filename):
    with opencv_videocapture(filename) as vc:
        w = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return w, h

def video_file_metadata(file_path, root_path):
    """Computes meta data about a video file, as a dictionary."""
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
        fn = os.path.join(dct['root_path'], dct['root_path_name'], dct['file_path'], dct['filename'] + '.' + dct['file_extension'])
        fn = os.path.abspath(fn)
    else:
        fn = os.path.join(dct['root_path'], dct['root_path_name'], dct['filename'] + '.' + dct['file_extension'])
        fn = os.path.abspath(fn)
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
    return dct

@transaction.atomic
def import_video_file(file_path, root_path=None, verbose=False,
        frame_count=None, db=True, pretend=False, md5=True, bucket=None,
        vector_file=False, samples_file=None, dataset=None, frames=None,
        rectangles=False, framecache=False):
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
    dct = video_file_metadata(file_path, root_path)
    v, db_created = _database_video_import(file_path, dct)
    return v, db_created


def create_video():
    """Creates a video programmatically."""


@transaction.atomic
def import_video_screenshot(filename, screenshot):
    """Imports items into the database."""
    v = Video.objects.create(filename)
    VideoScreenshot.objects.create(video=v, location=screenshot)


class Command(BaseCommand):
    help = _HELP

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
        p.add_argument('--output_filename', dest='output_filename', type=str,
            help='The filename to output to.')
        p.add_argument('--filename', dest='filename', type=str,
            help='The filename to consider.')
        p.add_argument('--url', dest='url', type=str,
            help='The Youtube video URL to download.')

    def handle(self, *args, **opts):
        """High-level interface, which can handle CTRL-C input."""
        #url = opts['url']
        #output_filename = opts['output_filename']
        if opts['filename']:
            filename = opts['filename']
            v = import_video_file(filename)
            convert_video_to_numpy(v)
