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

By default this Flask application will connect to the Redis database via
a TCP/IP connection. To connect to a local Redis database via a UNIX
domain socket, define the environment variable ``REDIS_DB_SOCKET`` as
the socket file (e.g., ``/tmp/redis.sock``) before running the
application.

.. code:: bash

    $ export REDIS_DB_SOCKET="/tmp/redis.sock"
    $ export FLASK_APP=autopytwask
    $ flash run

Note that the UNIX domain socket is by default disabled in Redis and you
need to manually enable it in the Redis configuration file (usually
``/etc/redis/redis.conf``) before use it.

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

4. Deployment
-------------

4.1. Deploy the Flask application in the cloud.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take the Amazon Web Service (AWS) as an example. Assume that we have
created an EC2 instance with Ubuntu 16.04LTS, exposed its HTTP port 80,
and SSH’ed into it.

4.1.1. Install Python 3.6, pip, pip3, virtualenvwrapper.

(1) Install Python 3.6 from source.

.. code:: bash

    # Download the latest source release of Python 3.6.
    $ wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz

    # Unpack the downloaded archive.
    $ tar -xvf Python-3.6.5.tgz

    # Build and install.
    $ cd Python-3.6.5
    $ ./configure
    $ make
    $ make install

    # Verify the installation.
    $ python3.6 -V
    Python 3.6.5

(2) Install pip and pip3.

.. code:: bash

    $ sudo apt install python-pip python3-pip

(3) Install virtualenvwrapper.

.. code:: bash

    $ sudo pip3 install virtualenvwrapper

4.1.2. Create a separate user which will run the Flask application.

We should never run the Flask application as root. If we do that, once
the Flask application is compromised somehow, the attacker will gain
access to the entire system.

.. code:: bash

    $ sudo adduser flask-apps

4.1.3. Create the virtual environment for running the Flask application.

(1) Set up ``virtualenvwrapper`` for the user ``flask-apps``.

.. code:: bash

    $ sudo su - flask-apps
    $ vi ~/.bashrc

Add the following lines in ``.bashrc``.

::

    export WORKON_HOME=$HOME/.virtualenvs
    export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
    source /usr/local/bin/virtualenvwrapper.sh

(2) Reload ``.bashrc`` and create a virtual environment for running the
    Flask application.

.. code:: bash

    $ cd
    $ source .bashrc
    $ mkvirtualenv -p /usr/bin/python3.6 pytwask

Note that the binary location of ``python3.6`` may vary on different
machines but it can be easily found by ``which python3.6``.

4.1.4. Install the Python WSGI HTTP server ``Gunicorn`` and the Flask
application ``pytwask`` in the above virtual environment ``flask-apps``.

.. code:: bash

    # After mkvirtualenv is done, the virtual environment flask-apps should be automatically activated. 
    # But if not, we can manually activate it.
    $ workon pytwask

    (pytwask) $ pip install gunicorn pytwask

4.1.5. Install and configure nginx.

(1) Install nginx.

.. code:: bash

    # Exit the user flask-apps
    $ exit

    $ sudo apt install nginx

(2) Configure nginx to proxy requests.

-  Create a configuration file for pytwask.

.. code:: bash

    $ sudo vi /etc/nginx/sites-available/pytwask

Note that we will pass requests to the socket we defined using the
``proxy_pass`` directive.

::

    server {
        listen      80;
        server_name [SERVER_DNS_NAME OR SERVER_IP];

        location / {
            include proxy_params;
            proxy_pass http://unix:/tmp/pytwask.sock;
        }
    }

-  Enable the above server configuration by linking the file to the
   ``sites-enabled`` directory.

.. code:: bash

    $ sudo ln -s /etc/nginx/sites-available/pytwask /etc/nginx/sites-enabled

-  Test the configuration file for syntax error.

.. code:: bash

    $ sudo nginx -t

-  Restart nginx to load the new configuration.

.. code:: bash

    $ sudo service nginx restart

4.1.6. Start a Gunicorn process to serve the Flask application.

.. code:: bash

    $ sudo su - flask-apps

    # Here we use the UNIX domain socket to connect to the Redis database.
    # If you want to use the TCP/IP connection, then don't define the environment variable REDIS_DB_SOCKET.
    $ export PYTWASK_ENV=prod
    $ export REDIS_DB_SOCKET="/tmp/redis.sock"
    $ export REDIS_DB_PASSWORD="[PASSWORD]"

    $ workon pytwask
    (pytwask) $ gunicorn -b unix:/tmp/pytwask.sock -m 007 -w 4 autopytwask:app &

Note that the ampersand “&” will set the Gunicorn process off running in
the background.

4.1.7. (Optional) Create a systemd unit file and enable the Gunicorn
process as a service.

(1) Create a unit file ending in ``.service`` within the directory
    ``/etc/systemd/system``.

.. code:: bash

    $ sudo vi /etc/systemd/system/pytwask.service

(2) Add the section ``[Unit]`` to specify metadata and dependencies.

::

    [Unit]
    Description=Gunicorn instance to serve pytwask
    After=network.target

(3) Add the section ``[Service]`` to specify:

-  the user ``flask-apps`` and group ``www-data`` that we want the
   process to run under;
-  the working directory and set various environment variables;
-  the command to start the service.

Note that we give the group ownership to group ``www-data`` so that
nginx can communicate easily with the Gunicorn process.

::

    [Unit]
    Description=Gunicorn instance to serve pytwask
    After=network.target

    [Service]
    User=flask-apps
    Group=www-data
    WorkingDirectory=/home/flask-apps/.virtualenvs
    Environment="PATH=/home/flask-apps/.virtualenvs/pytwask/bin"
    Environment="PYTWASK_ENV=prod"
    Environment="REDIS_DB_SOCKET=/tmp/redis.sock"
    Environment="REDIS_DB_PASSWORD=[PASSWORD]"
    ExecStart=/home/flask-apps/.virtualenvs/pytwask/bin/gunicorn -b unix:/tmp/pytwask.sock -m 007 -w 4 autopytwask:app

(4) Add the section ``[Install]`` to tell systemd what to link this
    service to if we enable it to start at boot.

::

    [Unit]
    Description=Gunicorn instance to serve pytwask
    After=network.target

    [Service]
    User=flask-apps
    Group=www-data
    WorkingDirectory=/home/flask-apps/.virtualenvs
    Environment="PATH=/home/flask-apps/.virtualenvs/pytwask/bin"
    ExecStart=/home/flask-apps/.virtualenvs/pytwask/bin/gunicorn -b unix:/tmp/pytwask.sock -m 007 -w 4 autopytwask:app

    [Install]
    WantedBy=multi-user.target

(5) Start the Gunicorn service and enable it to start at boot.

.. code:: bash

    $ sudo systemctl start pytwask
    $ sudo systemctl enable pytwask

4.2. Deploy the Flask application via docker.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To be added.

4.3. Troubleshooting
~~~~~~~~~~~~~~~~~~~~

4.3.1. `Errors while reloading ``.bashrc`` for
``virtualenvwrapper`` <https://stackoverflow.com/questions/33216679/usr-bin-python3-error-while-finding-spec-for-virtualenvwrapper-hook-loader>`__.

::

    /usr/bin/python3: Error while finding spec for 'virtualenvwrapper.hook_loader' (<class 'ImportError'>: No module named 'virtualenvwrapper')

To fix this, install ``python3-pip`` and then install
``virtualenvwrapper`` from ``pip3``.

.. code:: bash

    $ sudo apt install python3-pip
    $ sudo pip3 install virtualwrapperenv

4.3.2. `Errors while installing
nginx <https://askubuntu.com/questions/764222/nginx-installation-error-in-ubuntu-16-04>`__.

To fix this, stop apache2 before installing nginx.

.. code:: bash

    $ sudo service apache2 stop

As a further step, we may disable apache2 from startup or even remove
apache2.

.. code:: bash

    # To disable apache2
    $ sudo update-rc.d apache2 disable

    # To remove apache2
    $ sudo update-rc.d -f apache2 remove

5. Development
--------------

By default, this Flask application will run in the development mode
where the Flask DebugToolbar is enabled.

.. code:: bash

    $ git clone https://github.com/renweizhukov/pytwask.git
    $ cd pytwask
    $ pip install -e .
    $ export FLASK_APP=autopytwask
    $ flask run

6. README.rst
-------------

README.rst is generated from README.md via ``pandoc``.

.. code:: bash

    $ pandoc --from=markdown --to=rst --output=README.rst README.md
