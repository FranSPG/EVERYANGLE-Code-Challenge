import os

APP_ENV = os.getenv('APP_ENV', 'development')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'franco123')
DATABASE_HOST = os.getenv('DATABASE_HOST', '192.168.0.101')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'media_library')
TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'test_media_library')
