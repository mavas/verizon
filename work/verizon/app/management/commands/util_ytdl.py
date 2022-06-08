import youtube_dl


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
    })
