import os
import importlib

import avalon.api
from avalon import lib


class ProjectManagerAction(avalon.api.Action):
    name = "projectmanager"
    label = "Project Manager"
    icon = "gear"
    order = 999     # at the end

    def is_compatible(self, session):
        return "AVALON_PROJECT" in session

    def process(self, session, **kwargs):
        return lib.launch(executable="python",
                          args=["-u", "-m", "avalon.tools.projectmanager",
                                session['AVALON_PROJECT']])


class LoaderAction(avalon.api.Action):
    name = "loader"
    label = "Loader"
    icon = "cloud-download"
    order = 998     # at the end

    def is_compatible(self, session):
        return "AVALON_PROJECT" in session

    def process(self, session, **kwargs):
        return lib.launch(executable="python",
                          args=["-u", "-m", "avalon.tools.cbloader",
                                "-project", session['AVALON_PROJECT'],
                                "-config", session.get("AVALON_CONFIG", "")])


def register_default_actions():
    """Register default actions for Launcher"""
    avalon.api.register_plugin(avalon.api.Action, ProjectManagerAction)
    avalon.api.register_plugin(avalon.api.Action, LoaderAction)


def register_config_actions():
    """Register actions from the configuration for Launcher"""

    module_name = os.environ["AVALON_CONFIG"]
    config = importlib.import_module(module_name)
    if not hasattr(config, "register_launcher_actions"):
        print("Current configuration `%s` has no 'register_launcher_actions'"
              % config.__name__)
        return

    config.register_launcher_actions()
