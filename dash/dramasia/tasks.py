from __future__ import absolute_import, unicode_literals
import re
import requests
# Create your tasks here

from celery import shared_task

# from euphonime.models import Anime, Character, VoiceAct

from dramasia.services.sync_drama import get_data_mdl


@shared_task
def sync_mdl(mdl_id):

    get_data_mdl(mdl_id)

    return None