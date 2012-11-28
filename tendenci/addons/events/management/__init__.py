from django.conf import settings
from django.utils.translation import ugettext_noop as _
from django.db.models.signals import post_syncdb

from tendenci.apps.notifications import models as notification

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type(
        'event_added',
        _('Event Added'),
        _('An event has been added'))

    notification.create_notice_type(
        'event_edited',
        _('Event Edited'),
        _('An event has been edited'))

    notification.create_notice_type(
        'event_deleted',
        _('Event Deleted'),
        _('An event has been deleted'))

    notification.create_notice_type(
        'event_registration_confirmation',
        _('Event Registration Confirmation'),
        _('The email you receive confirming your registration'))

    notification.create_notice_type(
        'event_registration_cancelled',
        _('Event Registration Cancelled'),
        _('Notify administrators that someone has cancelled their event registration'))

post_syncdb.connect(create_notice_types, sender=notification)
