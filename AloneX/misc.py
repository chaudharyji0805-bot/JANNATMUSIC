import os
import socket
import time

import heroku3
from pyrogram import filters

import config
from AloneX.core.mongo import mongodb
from .logging import LOGGER

# Always keep db defined so plugins don't crash on import
db = {}

# ✅ SPECIAL_ID (so plugins importing it won't crash)
# Priority:
# 1) ENV SPECIAL_ID
# 2) config.SPECIAL_ID (if exists)
# 3) config.OWNER_ID (fallback)
try:
    SPECIAL_ID = int(os.getenv("SPECIAL_ID", getattr(config, "SPECIAL_ID", config.OWNER_ID)))
except Exception:
    SPECIAL_ID = int(config.OWNER_ID)

SUDOERS = filters.user()

HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(config.HEROKU_API_KEY),
    "https",
    str(config.HEROKU_APP_NAME),
    "HEAD",
    "master",
]


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("Local Database Initialized.")


async def sudo():
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]

    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )

    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)

    LOGGER(__name__).info("Sudoers Loaded.")


def heroku():
    global HAPP
    # ✅ FIX: call is_heroku() (pehle function object check ho raha tha)
    if is_heroku():
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info("Heroku App Configured")
            except BaseException:
                LOGGER(__name__).warning(
                    "Please make sure your Heroku API Key and Your App name are configured correctly in the heroku."
                )
