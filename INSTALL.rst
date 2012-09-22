===============
Getting Started
===============

1. Get the code
===============

The development version
-----------------------

To be able to hack on the code::

    $ cd ~/git/
    $ git clone https://github.com/ionyse/ionyweb.git
    $ cd ionyweb
    $ mkvirtualenv ionyweb
    (ionyweb)$ python setup.py develop


To install the last stable version
----------------------------------

Using pip::

    $ pip install ionyweb

or::

    $ pip install -e git+git://github.com/ionyse/ionyweb.git#egg=ionyweb

2. Starts a new Ionyweb project
===============================

::

    $ workon ionyweb
    (ionyweb)$ ionyweb-quickstart <NewProject>
    # Configure your MySQL database autoconfigure in your settings.py
    (ionyweb)$ cd <NewProject>
    (ionyweb)$ make syncdb
    (ionyweb)$ make runserver

After that, you will have to set-up a themes for your website.
