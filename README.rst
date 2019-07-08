========
camtasia
========

A Python API for Camtasia projects.

Quickstart
==========

To work with an existing Camtasia project, first load it:

.. code-block:: python

    import camtasia
    proj = camtasia.load_project('path/to/project.cmproj')

The ``media_bin`` attribute of ``Project`` gives you access to elements in the media bin:

.. code-block:: python

    # list the Media in the MediaBin    
    for media in proj.media_bin:
        print(media.source)

    # add a new media to the media bin
    proj.media_bin.import_media('path/to/image/or/movie.mov')

The ``timeline`` attribute of ``Project`` gives you access to elements on the timeline:

.. code-block:: python

    # list the tracks on the timeline
    for track in proj.timeline.tracks:
        print(track.name)

    # list the timeline markers
    for marker in proj.timeline.markers:
        print(marker.name, marker.time)

    # print details of media on the timeline
    for track in proj.timeline.tracks:
        for media in track.medias:
            print(media.start, media.duration)
            for marker in media.markers:
                print(marker.name, marker.time)

And if you have edits to the project that you want to write to disk, use the ``save()`` method:

.. code-block:: python

    proj.save()
