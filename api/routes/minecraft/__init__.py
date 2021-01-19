import config
from api import app, auth, privilege_required
from flask import make_response, jsonify, request, render_template
from mcstatus import MinecraftServer
from mcrcon import MCRcon
import requests
from pytechecker import check


@app.route("/v1/minecraft/serverinfo")
def v1_minecraft_serverinfo():
    try: 
        server = MinecraftServer(config.get_setting('minecraft-server-host', '127.0.0.1'), config.get_setting('minecraft-server-port', 25565))
        q = server.query()
        response = requests.get(f"https://api.mcsrvstat.us/2/{config.get_setting('minecraft-server-host', '127.0.0.1')}")

        obj = response.json()

        obj["players"]["online"] = q.players.online
        obj["players"]["list"] = q.players.names

        return make_response(obj, 200)
    except:
        return make_response(jsonify(["ERROR: The specified server is not online."]), 500)


@app.route("/v1/minecraft/command")
@privilege_required("minecraft_command")
def v1_minecraft_command():
    sample = {
        "cmd": {
            "required": True,
            "allowed_types": [str]
        }
    }
    query = request.args.to_dict(flat=True)
    succ, errors = check(sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    host = config.get_setting("minecraft-server-host", "127.0.0.1")
    port = config.get_setting("minecraft-server-rcon-port", 25575)
    password = config.get_setting("minecraft-server-password", "password")
    with MCRcon(host, password, port=port) as mcr:
        command = query["cmd"]
        resp = mcr.command(command)
        return make_response(jsonify(resp), 200)


@app.route("/v1/minecraft/whitelist")
@privilege_required("minecraft_whitelist")
def v1_minecraft_whitelist():
    sample = {
        "add": {
            "required": False,
            "allowed_types": [str]
        },
        "remove": {
            "required": False,
            "allowed_types": [str]
        }
    }
    query = request.args.to_dict(flat=True)
    succ, errors = check(sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)

    host = config.get_setting("minecraft-server-host", "127.0.0.1")
    port = config.get_setting("minecraft-server-rcon-port", 25575)
    password = config.get_setting("minecraft-server-password", "password")
    responses = list()
    with MCRcon(host, password, port=port) as mcr:
        if "add" in query:
            responses.append(mcr.command(f"whitelist add {query['add']}"))
        if "remove" in query:
            responses.append(mcr.command(f"whitelist remove {query['remove']}"))
    return make_response(jsonify(responses), 200)