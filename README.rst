Football stats
==============

.. image:: https://travis-ci.org/ferc255/football_stats.svg?branch=master
    :target: https://travis-ci.org/ferc255/football_stats

Some more interesting statistics about our regular matches.



1. Deploying of virtual machine and OAuth
-----------------------------------------
First you should install virtualization tools:

.. sourcecode:: console

    $ sudo apt install virtualbox vagrant
    $ sudo apt install nfs-common nfs-kernel-server
..

Then run vagrant inside ``football_stats/`` directory:

.. sourcecode:: console

    $ vagrant up
    $ vagrant ssh
..

Now you are inside a virtual machine. Install your favourite text editor, 
tmux and other stuff.
Then install pip3 and application's requirements:

.. sourcecode:: console

    $ sudo apt install python3-pip
    $ pip3 install -r dev-requirements.txt
..

Now you can run all the tests. If it's done well, you're on a right way!

.. sourcecode:: console

    $ tox
..

Now you should do OAuth authentication. Do you have api keys? You can find it out in `google developers console
<https://console.developers.google.com/apis/credentials>`__.
If you don't have api keys, you can get them easily by following `this tutorial
<https://developers.google.com/adwords/api/docs/guides/authentication>`__.

Copy ``client_secret.json`` to ``CREDENTIALS_DIR`` (``~/app_credentials/google_api/`` by default). Remember, that you should put it into ``CREDENTIALS_DIR`` inside virtual machine, not on the host.

Then run:

.. sourcecode:: console

    $ foostats/components/build_credentials.py --noauth_local_webserver
..

You will see a link. Copy it and open in browser. After authentication paste your verification code into terminal.

Authentication is complete! Now you can use main functions of the application.

2. Running
----------
TBD
