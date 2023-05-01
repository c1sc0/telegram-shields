#!/usr/bin/env python3

import os
import toml
from quart import Quart, request
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ServerTimeoutError
import json

app = Quart("Quart APIs")


@app.before_serving
async def init_session():
    app.session = ClientSession()


@app.route("/tgmembercount")
async def shields():
    chat_id = request.args.get("chat_id", None)
    if not chat_id: return "Example: tgmembercount?chat_id=pythontelegrambotgroup"
    if not chat_id.startswith("@"):
        chat_id = f"@{chat_id}"

    url = f"https://api.telegram.org/bot{config['telegram_api_key']}/getChatMembersCount?chat_id={chat_id}"

    try:
        async with app.session.get(url, timeout=ClientTimeout(total=10)) as r:
            _json = json.loads(await r.text())
    except ServerTimeoutError:
        return 500, "Timeout reached."

    if _json["ok"] == False:
        return 400, "Invalid chat_id."

    print(_json)

    members = _json["result"]

    shields_schema = {
        "color": "1d93d2",
        "label": "Telegram",
        "logoSvg": """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 240 240"><defs><linearGradient id="linear-gradient" x1="120" y1="240" x2="120" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#1d93d2"/><stop offset="1" stop-color="#38b0e3"/></linearGradient></defs><title>Telegram_logo</title><circle cx="120" cy="120" r="120" fill="url(#linear-gradient)"/><path d="M81.229,128.772l14.237,39.406s1.78,3.687,3.686,3.687,30.255-29.492,30.255-29.492l31.525-60.89L81.737,118.6Z" fill="#c8daea"/><path d="M100.106,138.878l-2.733,29.046s-1.144,8.9,7.754,0,17.415-15.763,17.415-15.763" fill="#a9c6d8"/><path d="M81.486,130.178,52.2,120.636s-3.5-1.42-2.373-4.64c.232-.664.7-1.229,2.1-2.2,6.489-4.523,120.106-45.36,120.106-45.36s3.208-1.081,5.1-.362a2.766,2.766,0,0,1,1.885,2.055,9.357,9.357,0,0,1,.254,2.585c-.009.752-.1,1.449-.169,2.542-.692,11.165-21.4,94.493-21.4,94.493s-1.239,4.876-5.678,5.043A8.13,8.13,0,0,1,146.1,172.5c-8.711-7.493-38.819-27.727-45.472-32.177a1.27,1.27,0,0,1-.546-.9c-.093-.469.417-1.05.417-1.05s52.426-46.6,53.821-51.492c.108-.379-.3-.566-.848-.4-3.482,1.281-63.844,39.4-70.506,43.607A3.21,3.21,0,0,1,81.486,130.178Z" fill="#fff"/></svg>""",
        "message": f"{members} members",
        "schemaVersion": 1
    }

    return shields_schema


if __name__ == "__main__":
    script_path = os.path.dirname(__file__)
    config_path = os.path.join(script_path, "config.toml")
    config = toml.load(config_path)

    app.run(debug=False, port=config["quart_port"])
