#
# delete_user.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The task of removing a user at boot.
#

import os
from kano.logging import logger
from kano.utils import get_user_unsudoed

from kano_init.status import Status, StatusError
from kano_init.utils import disable_ldm_autostart, \
    unset_ldm_autologin, reconfigure_autostart_policy, start_lightdm
from kano_init.user import delete_user, user_exists, get_group_members


def schedule_delete_user(name=None):
    status = Status.get_instance()

    if status.stage != Status.DISABLED_STAGE:
        msg = _("A different task has been scheduled already. Reboot to"
                " finish the task before scheduling another one.")
        raise StatusError(msg)

    if not name:
        name = get_user_unsudoed()

    # Remove the user from the kano users
    # so it is not considered when reconfiguring the login
    cmd='usermod {} -G {}'.format(name, name)
    os.system(cmd)

    reconfigure_autostart_policy()

    status.stage = Status.DELETE_USER_STAGE
    status.username = name
    status.save()

    # Converting name to unicode for safety and then back to bytes for print.
    print _("The '{string_username}' user will be deleted on the next"
            " reboot.").format(string_username=unicode(name)).encode('utf8')


def do_delete_user(flow_param):
    status = Status.get_instance()

    user = status.username
    if user_exists(user):
        delete_user(user)
    else:
        logger.warn("Attempt to delete nonexisting user ({})".format(user))

    reconfigure_autostart_policy()

    # If this was the last user on the system,
    # we need to schedule a new one.
    kanousers = get_group_members('kanousers')
    if len(kanousers) == 0:
        status.stage = Status.ADD_USER_STAGE
    else:
        status.stage = Status.DISABLED_STAGE

    status.username = None
    status.save()
