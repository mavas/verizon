import pickle
import os
import random
import json
import pprint

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core import serializers

from app.models import Video, VideoScreenshot


def import_video_file(filename):
    video = Video.objects.create(filename=filename)


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
