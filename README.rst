Football stats
==============

.. image:: https://travis-ci.org/ferc255/football_stats.svg?branch=master
    :target: https://travis-ci.org/ferc255/football_stats

Some more interesting statistics about our regular matches.



1. How to deploy and run this application
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
