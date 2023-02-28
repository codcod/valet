import json
import typing as tp

import aiofiles

from valet import settings


async def _read_file(filename: str):  # -> tp.Coroutine[tp.Any, tp.Any, str]:
    async with aiofiles.open(filename, mode='r') as f:
        contents = await f.read()
    return json.loads(contents)


async def _view(name: str):
    f = await _read_file(settings.BASE_DIR / 'valet/bot/static' / (name + '.json'))
    return f


async def view_home_tab():
    view = await _view('home_tab')
    view['blocks'][0]['text']['text'] = '* TODAY 1 January*'
    return view
