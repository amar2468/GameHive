import os

import django

from channels import AsgiHandler
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehive.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
})