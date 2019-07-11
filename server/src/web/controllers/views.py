# -*- encoding: utf-8 -*-

import json

import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPMovedPermanently

from context_holder import ContextHolder
from repositories import emoji_log_repository
from utils import emoji_url_utils
from web.request_utils import set_locale
from web.converters import emoji_log_converter


# Views
#~~~~~~~~~~~~~~~~~~

async def _render(request, template, *, locale='ja'):
    set_locale(request, locale)

    emoji_logs = await _fetch_emoji_logs()
    response = aiohttp_jinja2.render_template(
        template,
        request, {
            'emoji_logs': json.dumps(emoji_logs, ensure_ascii=False, separators=(',',':')),
            'locale': locale,
        })

    if request.app.debug:
        response.headers['Cache-Control'] = 'private, no-store, no-cache, must-revalidate'
    else:
        response.headers['Cache-Control'] = 'public, max-age={}'.format(10) # 10 sec

    return response


# Views : ja
#~~~~~~~~~~~~~~~~~~

async def index_ja(request):
    return await _render(request, 'home.html', locale='ja')

async def contact_ja(request):
    return await _render(request, 'contact.html', locale='ja')


# Views : en
#~~~~~~~~~~~~~~~~~~

async def redirect_index_en(request):
    return HTTPMovedPermanently('/en/', headers={
        'Cache-Control': 'public, immutable, max-age=31536000', # 1 year
    })

async def index_en(request):
    return await _render(request, 'home.html', locale='en')

async def contact_en(request):
    return await _render(request, 'contact.html', locale='en')


# Views : ko
#~~~~~~~~~~~~~~~~~~

async def redirect_index_ko(request):
    return HTTPMovedPermanently('/ko/', headers={
        'Cache-Control': 'public, immutable, max-age=31536000', # 1 year
    })

async def index_ko(request):
    return await _render(request, 'home.html', locale='ko')

async def contact_ko(request):
    return await _render(request, 'contact.html', locale='ko')


# DB
#~~~~~~~~~~~~~~~~~~

async def _fetch_emoji_logs():
    return {
        'en': await _fetch_emoji_logs_by_locale('en'),
        'ja': await _fetch_emoji_logs_by_locale('ja'),
        'ko': await _fetch_emoji_logs_by_locale('ko'),
    }

async def _fetch_emoji_logs_by_locale(locale):
    emoji_logs_records = await emoji_log_repository.filter_recently(locale)
    return [ emoji_log_converter.convert(v) for v in emoji_logs_records ]

