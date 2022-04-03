import cryptocompare
import json
from app.models import Crypto
from app import db
from pycoingecko import CoinGeckoAPI
import time

cg = CoinGeckoAPI()


def get_price(ticker_id):
	return cg.get_price(ids=ticker_id, vs_currencies='usd')


def get_trending():
	trending_dict = {}
	trending = cg.get_search_trending()
	for coin in trending['coins']:
		trending_dict[coin['item']['id']] = coin['item']['symbol']
	return trending_dict

# print(get_price('vempire-ddao'))

# crypto_list = []
#
# file = 'static/cryptocurrencies.json'
#
# with open(file, 'w+') as f:
# 	json.dump(cg.get_coins_list(), f, indent=4)
#
# with open(file, 'r') as f:
# 	data = json.load(f)
# 	for e in data:
# 		new_crypto = Crypto(ticker=e['symbol'], cg_ticker_id=e['id'], name=e['name'])
# 		db.session.add(new_crypto)
#
# db.session.commit()

# print(get_price("0x-wormhole")['0x-wormhole'].get('usd'))

# cg.get_coin_by_id(id='0cash')
# if get_price(e['id'])[e['id']].get('usd') is None:
# 	continue
# else:


# all_tickers = Crypto.query.all()
#
# for ticker in all_tickers:
# 	market_cap = get_price(ticker.cg_ticker_id)[ticker.cg_ticker_id].get('usd_market_cap')
# 	ticker.market_cap = market_cap
# 	db.session.commit()
# 	time.sleep(.01)