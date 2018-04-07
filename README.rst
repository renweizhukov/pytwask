pytwask
=======

A toy-twitter-clone frontend using Python and Flask.

To run this Flask application,

.. code:: bash

    $ pip install pytwask
    $ export FLASK_APP=autopytwask
    $ export PYTWASK_ENV=prod
    $ flask run

1. Features
-----------

This module implements the frontend for a simplified Twitter clone based
on Flask.

It supports the following features:

-  Register new users
-  Log in/out
-  Change user password
-  Get user profile
-  Post tweets
-  Follower/Following
-  General timeline for anonymous user
-  User timeline
-  Get tweets posted by one user

TODOs:

-  Search users
-  Delete a user
-  Recover user password
-  #hashtags
-  @mentions
-  Retweets
-  Replies
-  Conversations
-  Edit/Delete tweets
-  And more

2. Backend database
-------------------

Although currently we only have Redis as the only type of backend
database, we can easily switch to another type of backend database as
long as the backend module conforms to the same interface as the Redis
backend module ``pytwis``.

3. MTV architecture
-------------------

This Flask application follows the typical Flask Model-Template-View
pattern. Its directory layout follows the ones given at

-  http://flask.pocoo.org/docs/0.12/patterns/packages/
-  http://flask.pocoo.org/docs/0.12/patterns/appfactories/#app-factories
-  http://flask.pocoo.org/docs/0.12/cli/

Specifically,

::

    .
    ├── autopytwask.py    # The Flask script which creates this Flask application
    └── pytwask
        ├── auth          # The authentication blueprint
        ├── config.py     # The Flask application configuration file
        ├── __init__.py
        ├── main          # The main blueprint
        ├── models.py     # The data Model
        ├── static        # The HTML resources (css, images, javascript)
        ├── templates     # The HTML Templates
        └── tweets        # The tweets blueprint

4. Development
--------------

By default, this Flask application will run in the development mode
where the Flask DebugToolbar is enabled.

.. code:: bash

    $ git clone https://github.com/renweizhukov/pytwask.git
    $ cd pytwask
    $ pip install -e .
    $ export FLASK_APP=autopytwask
    $ flask run

5. README.rst
-------------

README.rst is generated from README.md via ``pandoc``.

.. code:: bash

    $ pandoc --from=markdown --to=rst --output=README.rst README.md
