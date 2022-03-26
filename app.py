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
App that launches a Publish from inside of Shotgun.

"""

from tank.platform import Application
from tank import TankError
import traceback
import tank
import sys
import os

class ExecuteAction(Application):

    def init_app(self):
        deny_permissions = self.get_setting("deny_permissions")
        deny_platforms = self.get_setting("deny_platforms")

        p = {
            "title": self.get_setting("display_name"),
            "deny_permissions": deny_permissions,
            "deny_platforms": deny_platforms,
            "supports_multiple_selection": \
                self.get_setting("supports_multiple_selection")
        }

        app_identifier = self.get_setting("display_name")

        self.engine.register_command(app_identifier, self.process_action, p)


    def process_action(self, entity_type=None, entity_ids=None):

        entities = None

        if entity_type and entity_ids:
            self.log_debug("Processing {0} {1}" \
                    .format((len(entity_ids), entity_type)))

            if entity_type not in self.get_setting("allowed_entities"):
                self.log_info(("Sorry, this app only works with entities "
                               "of type {0}.") \
                    .format(self.get_setting("allowed_entities")))
                return

            entity_fields_dict = self.shotgun.schema_field_read(entity_type)

            shotgun_fields = []

            for field in entity_fields_dict:
                shotgun_fields.append(field)

            extra_fields = self.get_setting('sg_extended_fields')
            if entity_type in extra_fields:
                for field in extra_fields[entity_type]:
                    shotgun_fields.append(field)

            entities = self.shotgun.find(
                entity_type,
                [["id", "in", entity_ids]],
                shotgun_fields
            )

        try:
            result = self.execute_hook(
                "action_hook",
                entity_type=entity_type,
                entities=entities,
                other_params=self.get_setting("other_params")
            )

        except:
            error = traceback.format_exc()
            self.log_error("Failed to process the action for this {0}:\n{1}" \
                .format(entity_type, error))
            return


        message = "There were {0} succesfully executed actions for {1}." \
            .format(len(result['succes']), entity_type)

        if len(result['messages']) != 0:
            message += "\n\nThe following messages were returned from the action:\n"
            for msg in result['messages']:
                message += "{0}\n".format(msg)

        if len(result['errors']) != 0:
            message += "\n\nThere were {0} errors for {1}, details:" \
                .format(len(result['errors']), entity_type)
            for er in result['errors']:
                message += "{0}\n".format(er)

        self.log_info(message)
