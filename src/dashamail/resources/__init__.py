"""Resource classes, one per section of the DashaMail REST API v2."""

from .account import Account
from .automations import Automations
from .base import BaseResource
from .campaigns import Campaigns
from .dialogs import Dialogs
from .images import Images
from .lists import Lists
from .reports import Reports
from .router import Router
from .segments import Segments
from .templates import Templates
from .transactional import Transactional
from .workflows import Workflows

__all__ = [
    "BaseResource",
    "Lists",
    "Segments",
    "Campaigns",
    "Automations",
    "Workflows",
    "Templates",
    "Reports",
    "Transactional",
    "Account",
    "Dialogs",
    "Router",
    "Images",
]
