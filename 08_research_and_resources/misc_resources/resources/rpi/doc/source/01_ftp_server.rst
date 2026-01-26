
.. _ftp_server:

Raspberry Pi as FTP Server
-------------------------------

Setting up the RPi as an FTP server---over which you and you alone have full control---is quite a simple task. First, install the ``ProFTP`` software through::

    sudo apt-get install proftpd

Configure it to be "standalone". Second, **edit the config file** of the program as follows::

    sudo nano /etc/proftpd/proftpd.conf

Add the following **parameters**::

    DefaultRoot         ~
    AuthOrder           mod_auth_file.c  mod_auth_unix.c
    AuthUserFile        /etc/proftpd/ftpd.passwd
    AuthPAM             off
    RequireValidShell   off

**Restart** the service by::

    sudo /etc/init.d/proftpd restart

Third, **generate a new user** as follows::

    sudo adduser ftp --home /home/ftp --shell /bin/bash

Change ``ftp`` and ``/home/ftp`` to a user name and directory of your liking. Choose a password for the new user.

Using a **FTP client**, you can now connect to your RPi and, for example, store files on it. You can also ``ssh`` connect to the RPi using the new user credentials.

Generally SD cards hosting the OS of the RPi and serving as file/data storage are of course not that large. But investing e.g. **50 EUR for a 500 GB external USB drive** and connecting such a drive to the RPi is a simple way of using the RPi as a serious ``ftp`` server. 