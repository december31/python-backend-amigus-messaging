import logging
import traceback

import firebase_admin
from django.apps import AppConfig
from firebase_admin import credentials

from project import settings

logger = logging.getLogger(__name__)


class FirebaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firebase'

    def ready(self):
        try:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
            default_app = firebase_admin.initialize_app(cred)
            logger.info(f"Firebase default app: {default_app.name}")
        except Exception as e:
            logger.error(f"init firebase admin failed: {str(e)}")
