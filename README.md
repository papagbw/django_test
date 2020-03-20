In order to run the code in this repository, there are a couple things you will need to do first.

# Install system and Python requirements
First run the following:
`./pre-requirements.sh`

This will require sudo privileges to install, and includes the system requirements for the Python database-related 
packages.

Next, to create the conda environment, navigate to the top directory of the module and create the conda environment
with `conda env create -f django_test.yml`. You can hereafter activate this environment with `conda activate cfdb-env`.

Finally, again from the top directory, install `django_test` in editable mode with the following command:
`pip install -e .`

in the home directory. This will let you `import django_test` in Python scripts. 

# Create the PostgreSQL user

* Switch to the `postgres` user with `su - postgres`. Note: `sudo` may be necessary here.  
* Enter the `postgres` command prompt with `psql`.  
* Type `\du` to see the current list of users and their permissions.  
* Create a new user with `CREATE USER superintendent;`.  
* Give the user permissions with `ALTER ROLE superintendent WITH SUPERUSER CREATEDB;`.  
* Give the user a password with `\password superintendent` and enter the password `almostsummer`.
* Create the database `CREATE DATABASE school_db;`  
* Change the owner of the database `ALTER DATABASE school_db OWNER TO superintendent;`.  
* Exit the environment with `\dq`.  
* Exit the user with `exit`.

# Generate the database

* Navigate to `django_test`.  
* Run `python manage.py migrate` to create all the tables.
