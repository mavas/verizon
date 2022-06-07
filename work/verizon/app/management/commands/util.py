import datetime
import re
import os

from django.utils.timezone import utc


def _youtube_id_metadata(filename):
    """Extracts the Youtube video ID from the filename."""
    m = re.match(r'^(.+)-(.{11}).mp4$', filename)
    if m:
        youtube_id = m.group(2)
        return youtube_id
    return ''

def _path_related_metadata(file_path, root_path):
    """Computes file-related meta data."""
    dct = dict()
    f = os.path.abspath(file_path)
    dct['youtube_id'] = _youtube_id_metadata(f)
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
    return dct, f, fn


def _other_metadata(dct, f, fn):
    st = os.stat(fn)
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
    #dct['md5'], _ = MD5Hash.objects.get_or_create(
    #    content=compute_md5_filename(file_path))
    return dct
