if os.environ.get('PROJECT_ENV') == 'production':
    REDIS_HOST = os.environ.get('REDIS_HOST')
else:
    REDIS_HOST = '127.0.0.1'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, 6379)],
        },
    },
}