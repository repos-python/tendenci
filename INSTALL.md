# Tendenci Installation

You can use the following installation instructions to install a local Tendenci site. This Django project is intended to help create a Tendenci site that you can deploy on a public hosting, but it's recommended that you install locally first in order to test your themes and designs.

## Setting up the database

Tendenci is designed for use with PostgreSQL. You will need to have a PostgreSQL server running locally. If you are on OS X, we recommend Postgres.app: [http://postgresapp.com/](http://postgresapp.com/) to get up and running fast.

With Postgres.app installed, you can create a database from Terminal:

    psql -h localhost -c "CREATE DATABASE tendenci"

You can also create a database in your GUI of choice (recommended: [http://www.pgadmin.org/](http://www.pgadmin.org/)).

For more on installing PostgreSQL for Django check the docs at: [https://docs.djangoproject.com/en/dev/ref/databases/#postgresql-notes](https://docs.djangoproject.com/en/dev/ref/databases/#postgresql-notes)

## Downloading Tendenci

Make a folder for your site and cd into it. Replace 'sitename' with the name of your site.
 
    mkdir sitename
    cd sitename

It's best practice to make a virtual environment for your site. You will need [virtualenv](http://www.virtualenv.org/) installed for the next step. If you don't have it, you can install it with `pip install virtualenv`. Make a virtual environment called 'venv' and activate it.

    virtualenv venv
    source venv/bin/activate

Install Tendenci. This download and install step may take a few minutes.

    pip install tendenci

Once this is done, you can setup django project with the following:

    create-tendenci-project

If you created a database with a name other than 'tendenci', you will need to edit the database name 'tendenci' inside the `.env` file that is created.

Next, we install requirements for the project. We add tendenci videos as an example to use.

    pip install -r requirements/dev.txt

Now we are ready to use our deploy script and setup our theme.

    python deploy.py
    python manage.py set_theme salonify

To create your login, run the following command and fill in the prompts:

    python manage.py createsuperuser

Finally, we can use the runserver command so that we can view the site in our browser:

    python manage.py runserver

Open http://127.0.0.1:8000/ in your browser to see your tendenci site!

**Optional:** You can add additional local environment variables to the `.env` file by defining them as `KEY='value'`. Settings that are sensitive (like passwords) or vary per environment should be added to this file. For example, to use Amazon's S3 service as a file storage backend, set the following key/value pairs in your `.env` file:

    AWS_ACCESS_KEY_ID='MY_ACCESS_KEY'
    AWS_SECRET_ACCESS_KEY='MY_SECRET_KEY'
    AWS_STORAGE_BUCKET_NAME='bucket_name'
    AWS_LOCATION='new-site-name'

----------

# Deploying on Heroku

You do not need to be able to run tendenci locally in order to deploy to Heroku. Simply follow the steps below if you do want to load your site on Heroku's server environment.

## Prerequisites

You need to have a Heroku account: [http://heroku.com](http://heroku.com), the heroku toolbelt: [https://toolbelt.heroku.com/](https://toolbelt.heroku.com/), and git: [http://git-scm.com/](http://git-scm.com/) installed. It is also recommended that you have your payment options configured, though all of the settings below allow your site to run for free.

## Cloning and pushing to Heroku

For the instructions below, please replace `sitename` with the name of your site. The name can contain dashes or underscores, but not spaces.

You can now create a new git repo from this code that will be specific to your site. Go to your sitename folder from the terminal and run the following:

    git init
    heroku create sitename
    git add .
    git commit -am "initial commit"
    git push heroku master

Your site will now be created on Heroku. The first build may take up to 15 minutes due to the initial download of all of the dependencies. Additional updates will not take as long.

## Configuring Heroku Addons

Heroku offers several addons: [https://addons.heroku.com/](https://addons.heroku.com/) for apps that include Database connections, Memcached caching, email servers, and other useful addons. We will use the database and the Memcached addons in the instructions below.

You can add on the free tier of the memcache addon: [https://addons.heroku.com/memcache](https://addons.heroku.com/memcache) by running the following command. This addon is free, but you need to have verified your account to add it:

    heroku addons:add memcache:5mb

To configure the database, we must add the database and then promote it as the main database. Database names from Heroku's Postgresql service: [https://postgres.heroku.com/](https://postgres.heroku.com/) follow the pattern `HEROKU_POSTGRESQL_COLOR` where `COLOR` is an actual color name like `TEAL` or `ORANGE`. This will vary per installation, but we can look this up by running `heroku config`. The second command below will find the default color name and use it.

To create and configure the database, run the following commands:

    heroku addons:add heroku-postgresql:dev
    heroku pg:promote `heroku config | grep POSTGRES | cut -d : -f 1`

## Setting up the database

Next, we can run the deploy script to populate the database. The theme `salonify` is used below by default, but you may create a custom theme and set your theme to that themes.

    heroku run python deploy.py
    heroku run python manage.py set_theme salonify
    heroku run python manage.py createsuperuser

## Configuring static assets

We have two options for static assets: serving them locally and loading from a remote location like Amazon S3: [http://aws.amazon.com/s3/](http://aws.amazon.com/s3/).

**WARNING** - If you use the local storage, any uploaded files may be **deleted** when you update your site. This is not recommended for a live website. You should setup S3 instead.

To configure S3, set the config options with the following command:

    heroku config:set AWS_ACCESS_KEY_ID='MY_ACCESS_KEY'
    heroku config:set AWS_SECRET_ACCESS_KEY='MY_SECRET_KEY'
    heroku config:set AWS_STORAGE_BUCKET_NAME='bucket_name'
    heroku config:set AWS_LOCATION='new-site-name'

Now, run the following command:

    heroku run python manage.py collectstatic --noinput

Finally, you can open your site!

    heroku open
