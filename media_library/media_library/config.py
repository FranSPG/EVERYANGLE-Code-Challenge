from fastapi import FastAPI
import databases
import sqlalchemy
import os

APP_ENV = os.getenv('APP_ENV', 'development')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'fran')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'media_library')
TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'test_media_library')
