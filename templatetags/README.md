# Django-OAuthio: templatetags

This is a convenient template tag. It include all scripts. You should put it and the end of your file
before the `</body>` tag.

## Settings

In your project `settings.py` file add the key `OAUTHIO_JAVASCRIPT_SRC` with the URL of the OAuth.io javascript. 

Example:

```OAUTHIO_JAVASCRIPT_SRC=STATIC_URL + "where/the/script/is/oauthio.min.js```

The app use the [RawGit service](https://rawgit.com/) to deliver the file as a fallback. But there's a limitation
of the number of time the file could be delivered per website. See [the RawGit FAQ]() for more information.

Django-oauthio provides three kinds of files:

* oauth.js and oauth.min.js : The oauth.io javascript
* oauthio.js and oauthio.min.js : The django-oauthio javascript
* oauth-io-full.min.js : Both files merged in their minimified version

The last one is the default when `DEBUG` key in `settings.py` is set to `False`.

## Automatic inclusion

At the end of your file add:
```{% oauthio_install_javascript %}```

Et voilà !


## By the hand inclusion

Add:
```<script type="application/javascript" src="{{ STATIC_URL }}oauth-io-full-min.js"></script>```

in your template file. For debug mode : 

```<script type="application/javascript" src="{{ STATIC_URL }}oauth.js"></script>
<script type="application/javascript" src="{{ STATIC_URL }}oauthio.js"></script>```

