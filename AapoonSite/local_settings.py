DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'gcrmsserver': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qa_gcrmserver',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
                    'charset': 'utf8mb4',
                    'sql_mode': 'traditional',
                }
    }
}