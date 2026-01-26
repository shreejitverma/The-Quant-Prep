
.. _webcam:

Webcam Surveillance
---------------------

Since the RPi has two **USB slots** (model A & B) or even four (model B+) it is easy to connect and use a webcam with it. Modern, simple webcams---even with infrared light---start below 10 USD. More professional equipment can, of course, also be used.

This small project **focuses on the software side** of setting up an automated webcam surveillance system and not on the hardware side (which is probably determined by your specific purpose and maybe budget). I am using a rather small, simple USB webcam with infrared light to have some basic night filming capabilities available.


Installing Motion
~~~~~~~~~~~~~~~~~~~~

There is an excellent off-the-shelve, open source software called **Motion** available (cf. http://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome). It is installed as follows::

    sudo apt-get install motion

You find Motion **configuration files** generally in the directory ``/etc/motion``. We will only need the one called ``motion.conf``. You should make a **new folder** like::

    mkdir /home/pi/motion

and **copy** the configuration file to it::

    sudo cp /etc/motion/motion.conf /home/pi/motion

You should also create another folder like::

    mkdir /home/pi/motion/media

That's already it for the installation of Motion.


Basic Configurations
~~~~~~~~~~~~~~~~~~~~~~~~~

Motion is a powerful and mature system. However, in what follows we are mainly interested in the following **capabilities**:

* **detect a motion** defined by the number of pixels changed
* take **single pictures** and store them locally or do something else (e.g. sending by email, putting on a remote FTP server)
* make **video recordings** and store them locally or do something else (e.g. email, FTP)
* live **video transmission** via HTTP

Here is an example Motion **configuration file** ``motion.conf`` for :download:`download<./motion.conf>`. There is lots of inline documentation and the majority of **options** is self-explaining (e.g. resolution of pictures/videos).

Motion saves---if configured---pictures and videos locally. More interesting are options to define some **action** depending on a certain **event** starting or ending. There are multiple such events, like::

    on_event_start
    on_picture_save
    on_movie_end

These are the three that we want to use (for details see the configuration file). In particular, we want to **implement** the following:

* send an email on an event starting
* send a saved picture to a remote FTP server
* send an email with the video attached on a movie ended/saved

This provides a rather **high security level** since:

* you are notified as soon as some event is detected
* every single picture is transfered via FTP as soon as saved
* you get by email every saved video

In particular the **FTP transfer** (which is pretty quick since a typical picture will be relatively small with, say, 20kb) prevents a person to simply remove the whole RPi with the pictures and videos stored.

Send Email on Event Start
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Having Python available on the RPi allows us to use a Python script for sending emails. I assume that you have **two email accounts** which you use for this purpose, say ``rpi@mydomain.net`` to send email and ``me@mydomain.net`` to receive emails.

The following Python script provides the basic **functionality to send emails** (:download:`download link<./mail_simple.py>`; place it in the ``motion`` folder as created above):

.. literalinclude:: ./mail_simple.py

Having this script available, we can do the following configuration::

    on_event_start python mail_simple.py

Whenever an event starts, you then get notified by Motion about it.


Store Pictures on FTP Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following assumes that you have available a **server with FTP access** (maybe another RPi, cf. :ref:`ftp_server`). You should install the FTP uploader **wput** (cf. http://wput.sourceforge.net/wput.1.html) on the RPi first::

    sudo apt-get install wput

The **configuration** then is straightforward::

    on_picture_save wput -B ftp://user:password@mydomain.net %f

Here, ``%f`` is the placeholder for the **filename** of the picture provided by Motion (this can be configured as well in the configuration file).


Send Email on Movie End
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The final security measure we implement is **sending a saved video recording by email**. The following Python script allows to send **emails with attachement** (:download:`download link<./mail_attach.py>`; place it in the ``motion`` folder as created above):

.. literalinclude:: ./mail_attach.py

The configuration shouldn't now come as a suprise given the previous two::

    on_movie_end python mail_attach.py %f

This sends an email with the video/movie attached when it is save (the event ends).


Live Video Streaming
^^^^^^^^^^^^^^^^^^^^^^^

When you have a **fixed, public IP** (cf. :ref:`fixip`), you can easily **stream the video** as captured by the webcam in real-time. You might need or want to adjust the standard **port** for the streaming (by default 8081) to another port, say WXYZ, in the configuration file. You then should be able, when Motion is running, to access the live stream under::

    http://rpi.mydomain.net:WXYZ

Starting Motion
~~~~~~~~~~~~~~~~~~

To **start** Motion, simply navigate to the directory previously created::

    cd /home/pi/motion

and type::

    motion

Motion then takes the **local configuration file** for the execution. The **pictures and videos** should be saved in the sub-folder ``media``. In addition, **emails** are sent as configured and pictures transfered to the remote **FTP server**.