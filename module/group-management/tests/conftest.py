"""Pytest configuration."""

from os.path import join
import os
import shutil
import tempfile

import pytest
from flask import Flask
from group_management.api import blueprint as group_management_blueprint
from group_management.redis import RedisConnection

@pytest.fixture()
def instance_path():
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def base_app(instance_path):
    """Flask application fixture."""
    app_ = Flask(
        "testapp",
        instance_path=instance_path,
        static_folder=join(instance_path, "static"),
    )

    app_.config.update(
        CLIENT_CERT_SUFFIX = "_test_cert",
        MANAGEMENT_INFO_SUFFIX = "_test_management",
        CREATE_GROUP_ERR_SUFFIX = "_test_error",
        CREATE_GROUP_SUFFIX = "_test_group",
        CELERY_ALWAYS_EAGER=True,
        CELERY_CACHE_BACKEND="memory",
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        CELERY_RESULT_BACKEND="cache",
        CACHE_REDIS_URL="redis://redis:6379/0",
        CACHE_REDIS_DB=0,
        CACHE_REDIS_HOST="redis",
        REDIS_PORT="6379",
        JSONSCHEMAS_URL_SCHEME="http",
        SECRET_KEY="CHANGE_ME",
        SECURITY_PASSWORD_SALT="CHANGE_ME_ALSO",
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "SQLALCHEMY_DATABASE_URI", "sqlite:///test.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_ECHO=False,
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        DEPOSIT_SEARCH_API="/api/search",
        SECURITY_PASSWORD_HASH="plaintext",
        SECURITY_PASSWORD_SCHEMES=["plaintext"],
        SECURITY_DEPRECATED_PASSWORD_SCHEMES=[],
        ACCOUNTS_JWT_ENABLE=False,
        INDEXER_FILE_DOC_TYPE="content",
        INDEX_IMG="indextree/36466818-image.jpg",
        I18N_LANGUAGE=[("ja", "Japanese"), ("en", "English")],
        SERVER_NAME="TEST_SERVER",
        SEARCH_ELASTIC_HOSTS="elasticsearch",
        SEARCH_INDEX_PREFIX="test-",
        OAISERVER_XSL_URL=None,
    )
    app_.register_blueprint(group_management_blueprint)
    return app_


@pytest.fixture()
def app(base_app):
    """Flask application fixture."""
    with base_app.app_context():
        yield base_app

@pytest.fixture()
def redis_connect(app):
    redis_connection = RedisConnection().connection(db=app.config['CACHE_REDIS_DB'])
    return redis_connection

@pytest.fixture()
def client(app):
    """Get test client."""
    with app.test_client() as client:
        yield client

