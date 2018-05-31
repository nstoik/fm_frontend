===============================
fm_frontend
===============================

Farm Monitor front end client


Quickstart
----------

First, set your app's secret key as an environment variable. For example,
add the following to ``.flaskenv`` or ``.env``.

.. code-block::

    FM_FRONTEND_SECRET='something-really-secret'

Run the following commands to bootstrap your environment ::

    git clone https://github.com/nstoik/fm_frontend
    cd fm_frontend
    pipenv install --dev
    npm install
    npm start  # run the webpack dev server and flask server using concurrently

You will see a pretty welcome screen.

In general, before running shell commands, set the ``FLASK_APP`` and
``FLASK_DEBUG`` environment variables in .flaskenv file::

    FLASK_APP="fm_frontend.app:create_app"
    FLASK_ENV="debug"

Once you have installed your DBMS, run the following to start ::

    npm start


Deployment
----------

To deploy::

    FLASK_ENV="production"
    npm run build   # build assets with webpack
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_ENV`` environment
variable is set to ``production``, so that ``ProdConfig`` is used.


Shell
-----

To open the interactive shell, run ::

    fm_frontend shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    fm_frontend test


Asset Management
----------------

Files placed inside the ``assets`` directory and its subdirectories
(excluding ``js`` and ``css``) will be copied by webpack's
``file-loader`` into the ``static/build`` directory, with hashes of
their contents appended to their names.  For instance, if you have the
file ``assets/img/favicon.ico``, this will get copied into something
like
``static/build/img/favicon.fec40b1d14528bf9179da3b6b78079ad.ico``.
You can then put this line into your header::

    <link rel="shortcut icon" href="{{asset_url_for('img/favicon.ico') }}">

to refer to it inside your HTML page.  If all of your static files are
managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they
should cache all your assets forever by including the following line
in your ``settings.py``::

    SEND_FILE_MAX_AGE_DEFAULT = 31556926  # one year
