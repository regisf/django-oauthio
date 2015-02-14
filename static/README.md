# django-oauthio: static files

Here's the django-oauthio static files : 

* oauth.js and oauth.min.js : The oauth.io javascript
* oauthio.js and oauthio.min.js : The django-oauthio javascript
* oauth-io-full.min.js : Both files merged in their minimified version

The last one is the default when `DEBUG` key in `settings.py` is set to `False`.

## Settings

Add the static directory in the `STATICFILES_DIRS` tuple in the `settings.py` file.

## Installation

See [templatetags/README.md](../templatetags/README.md)

## Don't forget

Don't forget to collect the static files with:

```sh
$ python manage.py collectstatic
```

when the configuration is finished.

