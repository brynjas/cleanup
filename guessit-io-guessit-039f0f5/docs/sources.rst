.. _sources:

Getting the source code
=======================

GuessIt is actively developed on `GitHub <https://github.com/guessit-io/guessit>`_.

You can either clone the public repository::

    $ git clone https://github.com/guessit-io/guessit.git

Download the `tarball <https://github.com/guessit-io/guessit/tarball/master>`_::

    $ curl -L https://github.com/guessit-io/guessit/tarball/master -o guessit.tar.gz

Or download the `zipball <https://github.com/guessit-io/guessit/zipball/master>`_::

    $ curl -L https://github.com/guessit-io/guessit/zipball/master -o guessit.zip


Once you have a copy of the source, you can embed it in your Python package,
install it into your site-packages folder like that::

    $ python setup.py install

or use it directly from the source folder for development::

    $ python setup.py develop
