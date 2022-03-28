# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Hook for ...
"""

from tank import Hook
from tank import TankError
import os

class ExecuteActionHook(Hook):

    def execute(self, entity_type, entities, other_params, **kwargs):
        """
        Executes an action for the selected entities.

        :param entity_type: ...
        :param entities: ...
        :param other_params: ...

        :returns: dictionary withtre values: succes, errors, messages
        """

        self.parent.log_debug("Executing hook...")

        return {
            'succes': entities,
            'errors': [],
            'messages': ['Empty Action, no process were made to any entity']
        }