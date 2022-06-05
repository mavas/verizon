# Computer vision programming challenge

## Challenge description

A recruitor contacted me about this job opportunity, and gave me a 1-page take-home challenge that Verizon crafted themselves.  This thing had all kinds of terms before that I never heard of, but of course it is all open and complete information, so I took my time and learned the bare minimum and did what I had to do to pass the challenge.

You're dealing with stereo cameras; these are essentially 2 cameras taking a picture of the same thing at the same time, but in just slightly different locations.  If you do this, there is obviously a difference in the images that you get when 2 different cameras take a picture of the same thing.  There is what's called a "disparity map" between 2 such images taken by 2 such cameras, and OpenCV has four functions for performing this calculation.  Disparity maps are used for all sorts of things in computer vision, as it turns out, and that's what this assignment is about.  Grab 2 images from this URL and perform the computation https://vision.middlebury.edu/stereo/data/scenes2003/ (it should be worth noting that the programming challenge was SPECIFIC to statements made at that URL, and not some other site or research paper).

Tasks to complete this assignment included 1.) minimally understanding the problem being solved and why it's being solved (knowing what and why a disparity map is, etc.), using some tool to compute it (OpenCV), and actually succeeding at the results.  This repository represents all of that effort, just to apply for a job at a company doing computer vision-like things.

Here are the specific instructions:

1. Go to that URL and download 2 images and use one of OpenCV's four functions to compute a disparity map between the 2 images.  Of course, I'm being vague: you have to find out which functions they are.  The disparity map values should adhere to the limits specified/stated by the folks found at that URL.
2. Use OpenGL to render the point cloud obtained, preferably in color.

Specific function calls are mentioned:

- `reprojectImageTo3D`
- `stereoRectify`

## CMake options

BUILD_SHARED_LIBS=OFF
CMAKE_BUILD_TYPE=Debug

## Extras

The original link linked to was `https://vision.middlebury.edu/stereo/data/scenes2003/`, but there's some good stuff at `https://vision.middlebury.edu/stero/` too, and I found this CMake-based project *cvkit* that I'm compiling right now, and could be useful.

## References

- The official coding challenge document I was given, for a job interview regarding a computer vision job I was applying for in April 2017.  It was a 1-page document which gave 2 main tasks, along with a bonus at the bottom.  It referenced this web page: https://vision.middlebury.edu/stereo/data/scenes2003/, and asked you to actually grab images from it in order to complete the assignment; that page also references a published research paper, more or less related to the assignment.  It was **academic-like**, and I respected it a lot.

- https://vision.middlebury.edu/stereo/data/scenes2003.  I learned a lot just reading that site and the research work.  I'm a big fan of research, and often wish I did that instead of merely doing software engineering like I usually do.

- I took a peak higher at the directory at https://vision.middlebury.edu/stereo/ and ended up finding this excellent Github repository, which helped in understanding just how much work went into the research.  That project has like 200+ stars and has official releases.  It could help you complete the programming challenge given by the company, but the assignment doesn't mention it in any way.

- OpenCV is specifically used by that coding challenge.  I compiled and used version 4.5.5.  In order to do `import cv2`, what I did was I manually went to www.OpenCV.org and downloaded the source code and compiled it and put the `cv2.so` file in the current directory like `ln -s ~/Downloads/opencv-4.5.5/build/lib/python3/cv2.cpython-38-x86_64-linux-gnu.so cv2.so`.

- The challenge also specifically asks you to use OpenGL to render a 3D point cloud.  This is the 2nd part of the 2-part assignment, and is just as important as the first part.

- A long time ago I purchased *Practical Python and OpenCV* by Dr. Adrian Rosebrock.  That was when it was the first edition, but the guy gives you free updates and so now I have the 4th edition which supports OpenCV v4 and Python 3+.  It's pretty tame compared to what I think *Learning OpenCV* is but it's good to get the basics down.  This 1-page coding challenge is more advanced than the entire book.
