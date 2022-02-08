import os

APP_ENV = os.getenv('APP_ENV', 'development')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'fran')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'fran')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'db') # THIS IS FOR DOCKER
DATABASE_NAME = os.getenv('DATABASE_NAME', 'media_library')
TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'test_media_library')
