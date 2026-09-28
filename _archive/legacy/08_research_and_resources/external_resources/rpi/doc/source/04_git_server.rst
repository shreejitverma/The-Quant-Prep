
.. _git_server:

Git Server with Raspberry Pi
-------------------------------

The version control system **Git** (cf. the excellent documentation under http://git-scm.com/) has become really popular recently. One reason for this is the success of **Github** (cf. http:github.com) as a (open source) code hosting platform based on Git. There are now also similar, alternative platforms available, like **Codebreak** (http://codebreak.com).

While, for example, Codebreak let's you store as many private Git repositories as you like, with Github you have to pay for this feature. However, in principle, every server can serve as a Git server (even if not with the many nice, graphical features the aforementioned platforms provide).

To use the RPi as a **Git server** (or a "remote Git repository storage system") does not require software-wise anything more the **Git installed** on the RPi. It should be installed already, if not do::

    sudo apt-get install git

In addition, the RPi must be configured for **SSH access** (cf. :ref:`ssh_access`).

Using a USB Storage Device
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In what follows, we use a **USB storage device** to store the remote Git repositories. This allows to move your valuable backups/versions of your Git repositories and to access them from other devices as well.

Put a formatted USB stick into your RPi. The look up the **mounting information**::

    sudo blkid

In my case, it is mounted as ``/dev/sda1``. We want to **permanently link** the USB storage device to a directory in our home folder::

    mkdir /home/pi/usb

**Edit** the following file::

    sudo nano /etc/fstab

and **add** the line::

    /dev/sda1 /home/pi/usb ext4 uid=pi, gid=pi, umask=0022, sync, auto, nosuid, rw, nouser 0 0

where some parameters might need to be changed due to your configuration (e.g. the directory or ``vfat`` instead of ``ext4`` for the file system).

After a **reboot**, you should now be able to permanently access the ("any") USB drive plugged into your RPi via ``/home/pi/usb``.


Remote Repository on the RPi 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that we have a proper storage device configured, we can **add a remote repository** to an existing one (I assume you are working with Git already and have a few repositories to use now; if not see below).

In my case, I take the repository of this tutorial which you can also find under http://github.com/yhilpisch/rpi as an example. Now do **on the RPi** the following::

    cd /home/pi/usb
    mkdir rpi.git
    cd rpi.git
    git init --bare

Then navigate on your **local machine** to the Git repository you want to push to the remote RPi location and do (cf. also :ref:`fixip` for the domain name)::

    git remote add rpi pi@rpi.mydomain.net:/home/pi/usb/rpi.git

Then, you should be able to do something like::

    git push rpi master

You can then, for instance, **clone the repository** to some other location via::

    git clone pi@rpi.mydomain.net:/home/pi/usb/rpi.git

Of course, you can also generate a **new user**, say ``git``, whose credentials you can easily and safely share with members of your team or with friends. You only have to make sure that this new user has read (or even maybe write) rights to the respective Git repository/folder (e.g. ``sudo chmod -R 755 /home/pi/usb/rpi``).


Generating Local Git Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you **do not have** an example **Git repository** (but Git installed locally), you can do the following steps **locally** (assuming the the remote location was set up as above)::

    mkdir rpi
    cd rpi
    git init
    # copy now some files into the the new directory
    git add --all .
    git commit -am 'Initial commit message.'
    git remote add rpi pi@rpi.mydomain.net:/home/pi/usb/rpi.git
    git push rpi master
