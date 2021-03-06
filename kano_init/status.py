#
# Setting/getting the status of the init flow
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
import json

from kano.utils import ensure_dir
from kano.utils.file_operations import open_locked
from kano.logging import logger

from kano_init.paths import STATUS_FILE_PATH


class StatusError(Exception):
    pass


class Status(object):
    DISABLED_STAGE = 'disabled'
    RESET_STAGE = 'reset'
    DELETE_USER_STAGE = 'delete-user'
    ADD_USER_STAGE = 'add-user'
    USERNAME_STAGE = 'username-stage'
    WHITE_RABBIT_STAGE = 'white-rabbit-stage'
    LIGHTUP_STAGE = 'light-up-stage'
    SWITCH_STAGE = 'switch-stage'
    LETTERS_STAGE = 'letters-stage'
    LOVE_STAGE = 'love-stage'
    FINAL_STAGE = 'final-stage'
    UI_INIT_STAGE = 'ui-init-stage'

    stages = [
        USERNAME_STAGE,
        WHITE_RABBIT_STAGE,
        LIGHTUP_STAGE,
        SWITCH_STAGE,
        LETTERS_STAGE,
        DISABLED_STAGE,
        RESET_STAGE,
        DELETE_USER_STAGE,
        ADD_USER_STAGE,
        LOVE_STAGE,
        FINAL_STAGE,
        UI_INIT_STAGE
    ]

    _status_file = STATUS_FILE_PATH

    _singleton_instance = None

    @staticmethod
    def get_instance():
        if not Status._singleton_instance:
            Status()

        return Status._singleton_instance

    def __init__(self):
        if Status._singleton_instance:
            raise Exception("This class is a singleton!")
        else:
            Status._singleton_instance = self

        self._initialise_variables()
        self._initialise_status_file()

    def _initialise_variables(self):
        self._stage = self.DISABLED_STAGE
        self._username = None

    def _initialise_status_file(self):
        ensure_dir(os.path.dirname(self._status_file))
        if not os.path.exists(self._status_file):
            self.save()
        else:
            self.load()

    def load(self):
        with open_locked(self._status_file, 'r', timeout=1.0) as status_file:
            try:
                data = json.load(status_file)
                self._stage = data['stage']
                self._username = data['username']
            except:
                # Initialise the file again if it is corrupted
                logger.warn("The status file was corrupted.")
                self.save()
                return

    def save(self):
        data = {
            'stage': self._stage,
            'username': self._username
        }

        with open_locked(self._status_file, 'w', timeout=1.0) as status_file:
            json.dump(data, status_file)
            status_file.flush()
            os.fsync(status_file.fileno())

    # -- stage
    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, value):
        if value not in self.stages:
            msg = _("'{string_app_stage_name}' is not a valid" \
                    " stage").format(string_app_stage_name=value)
            raise StatusError(msg)

        self._stage = value

    # -- last_update
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = str(value)
