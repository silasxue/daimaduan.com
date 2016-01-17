DEBUG = True

# Enable Flask-Assets debug mode.
ASSETS_DEBUG = True

MONGODB_SETTINGS = {
    'host': '192.168.99.100',
    'db': 'daimaduan'
}

SECRET_KEY = 'Youshouldnotknowthis'

DISQUS = {
    'short_name': 'daimaduan-dev',
    'secret_key': 'sdgsadg'
}

DOMAIN = 'daimaduan.dev:8080'

OAUTH = {
    'github': {
        'name': 'github',
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'access_token_url': 'https://github.com/login/oauth/access_token',
        'base_url': 'https://api.github.com/',
        'callback_url': 'http://daimaduan.dev:8080/oauth/github/callback',
        'client_id': '1f8813d6e0535fbfff98',
        'client_secret': '085d8ac899e236e12feaceb528c9de63aa601d39',
        'scope': 'user:email'
    },
    'google': {
        'name': 'google',
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'access_token_url': 'https://accounts.google.com/o/oauth2/token',
        'base_url': 'https://www.googleapis.com/oauth2/v1/',
        'callback_url': 'http://daimaduan.dev:8080/oauth/google/callback',
        'client_id': '572596272656-9urgn16qjoj36c439pecjcjmsogs76au.apps.googleusercontent.com',
        'client_secret': '085d8ac899e236e12feaceb528c9de63aa601d39',
        'scope': 'email profile openid'
    }
}