#
# add_user.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The task of adding a new user at boot.
#


from kano_init.status import Status, StatusError
from kano_init.utils import disable_ldm_autostart, unset_ldm_autologin


def schedule_add_user():
    status = Status.get_instance()

    if status.stage != Status.DISABLED_STAGE:
        msg = _("A different task has been scheduled already. Reboot to"
                " finish the task before scheduling another one.")
        raise StatusError(msg)

    disable_ldm_autostart()
    unset_ldm_autologin()

    print _("New user creation scheduled for the next system reboot.").encode('utf8')

    status.stage = Status.ADD_USER_STAGE
    status.save()


def do_add_user(flow_param):
    pass
