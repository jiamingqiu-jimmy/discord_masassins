import asyncio

global gold_lock
global items_lock

gold_lock = asyncio.Lock()
items_lock = asyncio.Lock()