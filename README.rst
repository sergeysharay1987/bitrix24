Local development environment
================================


Initial setup
+++++++++++++

Once initial setup is done only corresponding section should be performed
to get the latest version for development.

#. Install PyCharm to use as IDE
#. Install prerequisites::

    apt update
    apt install git

#. if you have not configured it globally configure git::

    git config user.name 'Firstname Lastname'
    git config user.email 'youremail@youremail_domain.com'

#. Install the Python build dependencies, as described at `<https://github.com/pyenv/pyenv/wiki#suggested-build-environment>`_.
#. Install pyenv according to `<https://github.com/pyenv/pyenv-installer#installation--update--uninstallation>`_.
#. Install python 3.9.2::

    pyenv install 3.9.2

#. Set a python version 3.9.2 in your directory with project (web_calculator/)::

    pyenv local 3.9.2


   After doing that a python-version file will appears in the directory with project.

8. Install `pip`. ::

    pip install pip==20.3.3

#. Install poetry, according to `<https://python-poetry.org/docs/#installation>`_.::

    pip install poetry

Run
++++

#. Run server::

    python manage.py runserver

