# -*- coding: utf-8 -*-
# Copyright (c) 2017 Benedict Dudel
# Copyright (c) 2023 Max
# Copyright (c) 2023 Pete-Hamlin
# No copyright for Boris-rnd, I made it in 5 mins

import subprocess
import subprocess,json

from albert import *

md_iid = "5.0"
md_version = "0.7.2"
md_name = "Hyprland window switcher"
md_description = "Switch Hyprland windows"
md_license = "MIT"
md_url = "https://github.com/Boris-rnd/hyprland-window-switcher"
md_authors = ["@Boris-rnd"]
md_maintainers = ["@Boris-rnd"]
md_bin_dependencies = ["hyprctl"]

class Plugin(PluginInstance, GeneratorQueryHandler):
    def __init__(self):
        PluginInstance.__init__(self)
        GeneratorQueryHandler.__init__(self)

    @staticmethod
    def makeIcon():
        return Icon.theme("dialog-password")

    def defaultTrigger(self):
        return "hypr "

    def synopsis(self, query):
        return "<window-name>"

    def configWidget(self):
        return []

    def items(self, context: QueryContext):
        q = context.query.strip()

        clients = subprocess.run(["hyprctl", "-j", "clients"], 
            capture_output=True,
            encoding="utf-8",
            check=True)
        clients = json.loads(clients.stdout)
        results = []
        for client in clients:
            if client["title"] == "":
                continue
            if client["class"] == "albert":
                continue
            if q.lower() not in client["title"].lower():
                continue
            results.append(StandardItem(
                id=client["address"],
                text=client["title"],
                subtext=client["workspace"]["name"],
                icon_factory=Plugin.makeIcon,
                input_action_text="hypr %s" % client["title"],
                actions=[
                    Action(
                        "Move",
                        "Move to workspace",
                        lambda input_text=client["title"]: runDetachedProcess(["hyprctl", "dispatch", "focuswindow", "title:"+input_text]),
                    ),
                ],
            ))
        yield results
