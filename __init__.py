# -*- coding: utf-8 -*-
# Copyright (c) 2017 Benedict Dudel
# Copyright (c) 2023 Max
# Copyright (c) 2023 Pete-Hamlin

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
        return [
            # {"type": "checkbox", "property": "use_otp", "label": "Enable pass OTP extension"},
            # {
            #     "type": "lineedit",
            #     "property": "otp_glob",
            #     "label": "Glob pattern for OTP passwords",
            #     "widget_properties": {"placeholderText": "*-otp.gpg"},
            # },
        ]

    def items(self, context: QueryContext):
        q = context.query.strip()

        clients = subprocess.run(["hyprctl", "-j", "clients"], 
            capture_output=True,
            encoding="utf-8",
            check=True)
        clients = json.loads(clients.stdout)
        results = []
        for client in clients:
            print(client["title"])
            print(client["workspace"]["name"])
            print(client["monitor"])
            
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




#             {
#     "address": "0x55946cbace30",
#     "mapped": true,
#     "hidden": false,
#     "at": [624, 52],
#     "size": [772, 521],
#     "workspace": {
#         "id": 10,
#         "name": "10"
#     },
#     "floating": true,
#     "monitor": 0,
#     "class": "albert",
#     "title": "Albert",
#     "initialClass": "albert",
#     "initialTitle": "Albert",
#     "pid": 1236626,
#     "xwayland": false,
#     "pinned": true,
#     "fullscreen": 0,
#     "fullscreenClient": 0,
#     "overFullscreen": true,
#     "grouped": [],
#     "tags": [],
#     "swallowing": "0x0",
#     "focusHistoryID": 0,
#     "inhibitingIdle": false,
#     "xdgTag": "",
#     "xdgDescription": "",
#     "contentType": "none",
#     "stableId": "18000172"
# }]
