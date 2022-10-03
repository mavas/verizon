# A web administration interface for video and image data curation

The entire purpose of this web-based interface is to label, or curate, video and image data.  Of course, in machine learning, you often deal with data, and you manually have to label that data; this interface allows you to do that.  Behind the scenes, everything eventually executes a Django management command ([ref](https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/)).

## Example commands

```
# Says that the following video is an example of video-of-video, and also
# downloads a few frames of the video (if not done already):
python manage.py label --video QJHcWIXymHA --recording vov
```

## Models

Here are the custom models created with this repository:

- Binary classification, whether or not gameplay footage is present (menu, stages, etc.)

- Localization.  This is just like before, except now we can place a bounding box around where the model thinks gameplay footage is present.

- Multiclassification stages: 26 stages.  This is just like before, except now the model can distinguish between which of the 26 stages is present (or if it's a menu screen, etc.)

- Multiclassification stages and characters.  This is just like before, except now the model can also detect which characters are on the screen, in addition to which stage the game is played on.

- Multiclassification character moves.  This is just like before, except now the model can detect which moves the characters are performing.

## Docker-based demonstration

The primary user interface is the web browser at http://localhost:8000/.  Using it, you can import videos into the database, perform object detection on videos and images, etc..

There are 4 containers: a PostgreSQL database, a Django web server, a TensorBoard server, and an Ubuntu operating system.

```
git clone https://github.com/mavas/verizon
docker build
    -f verizon/work/verizon/Dockerfile
    -t verizon
    verizon/work/verizon
```

## (extra information)

The directory parent to this one was initially created by the command `django-admin startproject verizon`, with Django version 4.0.5.
