from __future__ import unicode_literals

import logging
import os
import uuid
from random import sample

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _


log = logging.getLogger()
serv_log = logging.getLogger('django.server')


class VideoScreenshot(models.Model):
    """
    An image that was extracted from a video via mplayer's -vf screenshot
    option.

    'location' is the local filesystem location where the image file is stored.
    'video' is the associated video from which the image comes from.
    """
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True, blank=True)


class RectangleOrientation(models.Model):
    TOP_LEFT = 'TL'
    BOTTOM_LEFT = 'BL'
    ORIENT_CHOICES = (
        (TOP_LEFT, 'Top-left'),
        (BOTTOM_LEFT, 'Bottom-left'),
    )
    choice = models.CharField(max_length=2,\
        choices=ORIENT_CHOICES,default=TOP_LEFT,primary_key=True)

class RectangleManager(models.Manager):
    def get_by_natural_key(self, x1, y1, x2, y2):
        return self.get(x1=x1, y1=y1, x2=x2, y2=y2)
    def get2(s, x, y, w, h): pass
    @staticmethod
    def validate_rect(value): pass
    @staticmethod
    def from_string3(s):
        validate_rectangle_string(s)
        #x1, y1, x2, y2 = s.split()
        x1, y1, x2, y2 = map(int, re.split(r'\s+|_', s))
        o, _ = Rectangle.objects.get_or_create(x1=x1, y1=y1, x2=x2, y2=y2)
        return o
    @staticmethod
    def from_string2(s):
        regex = r'^(\d+) (\d+) (\d+) (\d+)(:(.+))?$'
        m = re.match(regex, s)
        if m:
            x1 = int(m.group(1))
            y1 = int(m.group(2))
            x2 = int(m.group(3))
            y2 = int(m.group(4))
            if m.group(6): comment = m.group(6)
    @staticmethod
    def from_string(obj, s):
        """
        Initializes a Rectangle from a string.

        Must be comma-delimited integers, and only 4 integers total.
        """
        if isinstance(s, tuple):
            rval, temp = Rectangle.to_string(s)
            if not rval:
                log.error("Could not convert: %s" % str(s))
                return False
            else: s = temp
        elif isinstance(s, Rectangle):
            if not s.x1 and s.x:
                s = Rectangle.from_width_height2(s.x,s.y,s.width,s.height)
                rval, temp = Rectangle.to_string(s)
                if not rval:
                    log.error("Could not convert: %s" % str(s))
                    return False
                else: s = temp
            elif s.x1 and s.y2 and s.x2 and s.y2: s = str(s)
            else:
                log.error("Incorrect rectangle spec.")
                return False
        regex = r'^(\d+) (\d+) (\d+) (\d+)(:(.+))?$'
        m = re.match(regex, s)
        if m:
            obj.x1 = int(m.group(1))
            obj.y1 = int(m.group(2))
            obj.x2 = int(m.group(3))
            obj.y2 = int(m.group(4))
            if m.group(6): obj.comment = m.group(6)
            return True
        else:
            log.error("Did not match: %s" % s)
            return False
    def create2(self, **kwargs):
        """Creates a Rectangle; optionally from a string."""
        if 'rect' in kwargs:
            obj = self.model(**kwargs)
            self._for_write = True
            #obj = RectangleManager.from_string(obj, kwargs['rect'])
            obj.save(force_insert=True, using=self.db)
            return obj
        else:
            #return self.get_queryset().create(**kwargs)
            return super(RectangleManager, self).create(**kwargs)

class Rectangle(models.Model):
    """
    A rectangle used to label images.

    Rectangles can be used to box/mark areas of an image.

    They are specified using one of 2 ways. using an X and Y coordinate along
    with width and height.
    """
    objects = RectangleManager()
    def __init__(self, *args, **kwargs):
        if 'rect' in kwargs:
            rect = kwargs.pop('rect')
            #objects.from_string
        super(Rectangle, self).__init__(*args, **kwargs)
    class Meta:
        unique_together = (('x1','y1','x2','y2'),)
        ordering = ['x1']
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    comment = models.CharField(max_length=100,blank=True,null=True)
    @staticmethod
    def to_string(atuple):
        """Converts a tuple representation of a rectangle into a string
        representation."""
        if len(atuple) == 4:
            rval = ''
            for item in atuple:
                rval += ' '
                rval += str(item)
            rval = rval[1:]
            return True, rval
        else:
            log.error("Could not convert: %s" % str(atuple))
            return False, None
    @staticmethod
    def compute_width_height(x1, y1, x2, y2): return (x2 - x1, y2 - y1)
    def from_width_height(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = width - x
        self.y2 = height - y
    @staticmethod
    def from_width_height2(x, y, width, height):
        x1 = x
        y1 = y
        x2 = width - x
        x2 = width + x
        y2 = height - y
        y2 = height + y
        return (x1,y1,x2,y2)
    def str(self):
        return u"%d %d %d %d" % (self.x1,self.y1,self.x2,self.y2)
    def __unicode__(self):
        if self.comment:
            msg = u"[%d %d %d %d]: %s"
            msg = msg % (self.x1,self.y1,self.x2,self.y2,self.comment)
        else: msg = u"[%d %d %d %d]" % (self.x1,self.y1,self.x2,self.y2)
        return msg
    def natural_key(self):
        return (self.x1, self.y1, self.x2, self.y2)


def extract_video_meta_data2(file_path, root_path=None, verbose=False, count=None):
    """Extracts less information than the other version."""
    dct = dict()
    f = os.path.abspath(file_path)
    if root_path:
        if not root_path.startswith('/') and file_path.startswith(root_path):
            #dct['root_path_name'] = root_path
            dct['root_path'] = os.path.split(os.path.abspath(root_path))[0]
            file_path = file_path[len(root_path):]
            if file_path.startswith('/'): file_path = file_path[1:]
            dct['file_path'] = os.path.split(file_path)[0]
        else:
            #dct['root_path_name'] = os.path.basename(root_path)
            dct['root_path'] = os.path.split(root_path)[0]
            file_path = file_path[len(root_path):]
            if file_path.startswith('/'): file_path = file_path[1:]
            dct['file_path'] = os.path.split(file_path)[0]
    else:
        def method1():
            temp = file_path
            while True:
                if os.path.isdir(os.path.split(temp)[0]):
                    temp = os.path.split(temp)[0]
                else: break
            if len(os.path.split(file_path)[0]) == 0: pass
        def method2(dct):
            #dct['root_path_name'] = os.path.abspath(os.path.split(file_path)[0])
            dct['root_path'] = os.path.abspath(os.path.split(os.path.split(file_path)[0])[0])
            #log.debug("root_path: %s" % dct['root_path'])
            return dct
        dct = method2(dct)
    dct['filename'] = os.path.splitext(os.path.split(f)[1])[0]
    #if os.path.abspath(root_path) == os.path.split(f)[0]:
    #file_extension = os.path.splitext(os.path.split(f)[1])[1]
    #if file_extension.startswith('.'):
    #    dct['file_extension'] = file_extension[1:]
    #else: dct['file_extension'] = file_extension
    if Video.objects.filter(filename=dct['filename']).exists():
        #filter(root_path_name=dct['root_path_name']).exists():
        raise VideoPresentError(file_path)
    dct['file_path'] = os.path.split(file_path)[0]
    return dct
def add_file_extension(filename, file_extension):
    return filename + u'.' + file_extension


class MD5HashManager(models.Manager):
    def get_by_natural_key(self, content):
        return self.get(content=content)
class MD5Hash(models.Model):
    class Meta:
        verbose_name = _('MD5 hash')
        verbose_name_plural = _('MD5 hashes')
    objects = MD5HashManager()
    content = models.CharField(max_length=32, primary_key=True)
    def __str__(self):
        return u'%s' % self.content
    def natural_key(self):
        return (self.content,)
    #def save(self, *args, **kwargs):
    #    super(MD5Hash, self).save(*args, **kwargs) # Call the "real" save() method.


class VideoManager(models.Manager):
    """
    What we are trying to do with this class is have methods that can tell if a
    video is unique; in other words, if a given query is refering to 'the same
    thing'
    """

    #def __init__(self, *args, **kwargs):
    #    post_save.connect(self.post_save_callback, sender=self.model)
        #super(WhooshManager, self).__init__(*args, **kwargs)
    #    super(VideoManager, self).__init__(*args, **kwargs)
 
    def video_exists(self, **dct):
        """Tells if a video/match is present in database."""

    def get_objects(self):
        return self.all()

    def get_random_v2(self, number=3):
        """Returns a set of random objects"""
        ids = self.get_objects().values_list('id', flat=True)
        amount = min(len(ids), number)
        picked_ids = sample(ids, amount)
        return self.filter(id__in=picked_ids)
    def get_random(self, n=None):
        """Returns a set of random objects."""
        ids = self.get_objects().values_list('id', flat=True)
        if not n:
            amount = min(len(ids), 1)
        else:
            amount = min(len(ids), n)
        ids = list(ids)
        picked_ids = sample(ids, amount)
        r = self.filter(id__in=picked_ids)
        if len(r) == 1:
            return r[0]
        return r

    def get_by_natural_key(self, short_name, filename):
        #return self.get(id=vid, uid=uid)
        return self.get(short_name=short_name, filename=filename)
    #def get_by_natural_key(self, uid):
    #    return self.get(uid=uid)

    #def post_save_callback(self, sender, instance, created, **kwargs):
        #log.debug("Calling compute_uid: %s" % instance)
        #log.debug("Calling compute_uid: %s" % instance.uid)
        #instance.compute_uid()
        #log.debug("Calling compute_uid: %s" % instance)
        #pass

    def get_video(self, filename=None, root_path=None):
        """
        Retrieves a Video object based on values.
        """
        if filename:
            dct = extract_video_meta_data2(filename, root_path=root_path)
            if Video.objects.filter(filename=dct['filename']).exists():
                return Video.objects.get(filename=dct['filename'])
            raise Exception("Could not find video.")
        def thing():
            dct = dict()
            dct['filename'] = os.path.splitext(os.path.basename(filename))[0]
            #dct['file_extension'] = os.path.splitext(os.path.basename(filename))[1]
            #if dct['file_extension'].startswith('.'):
            #    dct['file_extension'] = dct['file_extension'][1:]
            #dct['root_path'] = os.path.abspath(filename)
            #dct['root_path_name'] = os.path.dirname(filename)
            dct['root_path'] = os.path.split(os.path.abspath(os.path.dirname(filename)))[0]
            #dct = dict(filename=os.path.splitext(os.path.basename(filename))[0])
            return Video.objects.get(**dct)


class Video(models.Model):
    """
    A sequence of video frames.

    This object is intended to be rather abstract.  It could be that 2 video
    clips are what comprise a video computer file - this model should account
    for this situation.

    This object is intendend to record information about abstract continuous
    videos which are *not* intended to be broken.  A montage video, for
    example, is a composite video, which contains smaller (raw) videos, each of
    which you most probably would want to break down any further.

    While yes, of course, these RawVideo objects are intended to represent
    contiguous regions of video, intended for viewing by an audience, they
    could indeed be made by arbitrary frames, that don't necessarily look good
    in a given order.

    Tip: What we are trying to do: one video on disk might have many clips of
    videos in it; this is a common scenareo.  So there's a concrete video, and
    abstract videos embedded within; we're trying to represent this.
    """

    # Set Django model managers.
    if hasattr(settings, 'USE_WHOOSH_MANAGER') and settings.USE_WHOOSH_MANAGER:
        fields = ['filename', 'size', 'atime', 'mtime', 'description',
            'short_name']
        objects_whoosh = WhooshManager(real_time=settings.WHOOSH_REAL_TIME,
            fields=fields)
    #else:
    #    log.warn('settings does not have USE_WHOOSH_MANAGER setting.')
    #objects = VideoManager()

    # Other things..
    class Meta:
        verbose_name = _("video")
        verbose_name_plural = _("videos")
        unique_together = (('short_name', 'filename'),)

    # Fields.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200,blank=True)
    short_name = models.CharField(max_length=50,blank=True)
    filename = models.CharField(max_length=500, blank=True)
    file_path = models.CharField(max_length=500,blank=True)
    root_path = models.CharField(max_length=500,blank=True)
    size = models.BigIntegerField(null=True,blank=True)
    atime = models.DateTimeField(null=True,blank=True)
    mtime = models.DateTimeField(null=True,blank=True)
    description = models.CharField(max_length=1000,blank=True)
    #_filename = models.CharField(max_length=500, blank=True)
    #@property
    #def filename(self):
    #    return self.get_filename()
    #    return self._filename
    #@filename.setter
    #def filename(self, v):
    #    self._filename = v
    start_frame = models.IntegerField(null=True,blank=True)
    end_frame = models.IntegerField(null=True,blank=True)
    end_frame_date = models.DateTimeField(null=True,blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    md5 = models.ForeignKey('MD5Hash', on_delete=models.CASCADE, null=True,
        blank=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE,
        null=True, blank=True)

    #def natural_key(self):
    #    return (self.uid,)
    def natural_key(self):
        return (self.short_name, self.filename)

    def __str__(self):
        if self.filename:
            return u'%s' % (os.path.split(self.filename)[1],)
        elif hasattr(self, 'uid'):
            return u'%s' % self.uid
        return u'%s' % self.id
    def __unicode__(self):
        if self.filename:
            return u'%s' % (os.path.split(self.filename)[1],)
        elif self.uid:
            return u'%s' % self.uid
        return u'%s' % self.id

    def get_local_file_path(self):
        if self.filename and self.file_path and self.root_path:
            t = (self.root_path, self.file_path, self.filename)
            t = os.path.join(self.root_path, self.file_path, self.filename)
            #return os.path.join(settings.SAMPLES_DATA_PATH, t)
            return t
        elif self.filename and self.file_path:
            return os.path.join(self.file_path, self.filename)
        elif self.filename and self.root_path:
            return os.path.join(self.root_path, self.filename)
        return os.path.join(settings.SAMPLES_DATA_PATH, self.filename)
        raise Exception(str(self))

    def compute_uid2(self):
        if self.filename and self.md5:
            uid = os.path.split(self.filename)[1]
            uid = uid + ' ' + self.md5.content[0:10]
        elif self.filename and self.size:
            uid = os.path.split(self.filename)[1] + ' ' + str(self.size)
        elif self.short_name: uid = self.short_name
        elif self.filename: uid = os.path.split(self.filename)[1]
        else: uid = unicode('None')
        #log.debug("uid: %s" % uid)
        return uid
    def compute_uid(self, *args, **kwargs):
        """
        Computes and returns the universal identifier (UID) for this video.

        Some videos have information for certain fields while other videos do
        not.  This algorithm should account for generating IDs based on field
        information, given that some of it may be missing/incomplete.
        """
        if 'filename' in kwargs:
            f = kwargs['filename']
            players = Player.objects.all()
            players = '|'.join([p.name for p in players])
            player_regex = r'^(P<player>%s)$' % players
            character_regex = r'^$'
        if not self.uid: self.uid = self.compute_uid2()

    #def save(self, *args, **kwargs):
    #    super(Video, self).save(*args, **kwargs)
    #    self.compute_uid(*args, **kwargs)
    #def save(self, *args, **kwargs):
    #def save(self, force_insert=False, force_update=False, using=None,
    #         update_fields=None):
    #    super(Video, self).save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        #self.compute_uid(*args, **kwargs)
    #    super(Video, self).save(*args, **kwargs)
    def is_composite(self): return False
