import environ

root = environ.Path(__file__) - 3
environ.Env.read_env(env_file=root('.env'))
env = environ.Env()

TG_API_URL = env.str('TG_API_URL')
BOT_TOKEN = env.str('BOT_TOKEN')
BOT_WEBHOOK = env.str('BOT_WEBHOOK')
