# PyMongo-Gunicorn

### List of Errors and how I fixed them:

* _ModuleNotFoundError: No module named (While running gunicorn server)_ :
I had to installed gunicorn globally, hence the config was pointing to/usr/local/lib/python3.9/site-packages/gunicorn/app/wsgiapp.py.
gunicorn has to installed inside the venv of current project, so it points to the project level python configs . This works! 
