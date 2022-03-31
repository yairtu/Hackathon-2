import cryptocompare
import json
from app.models import Crypto
from app import db

# print(cryptocompare.get_price('AEGIS'))


# print(cryptocompare.get_coin_list())

print(type(cryptocompare.get_price('ETHPR')))

file = 'static/cryptocurrencies.json'

# with open(file, 'w+') as f:
# 	json.dump(cryptocompare.get_coin_list(), f, indent=4)

# crypto_list = []
#
# with open(file, 'r') as f:
# 	data = json.load(f)
# 	for v in data.values():
# 		crypto_list.append(v['Symbol'])

# for e in crypto_list:
# 	new_crypto = Crypto(ticker=e)
# 	db.session.add(new_crypto)
#
# db.session.commit()

# print(crypto_list)
#
# def load_data():
# 	with open('./static/cryptocurrencies.json', 'r') as f:
# 		crypto = json.load(f)
# 	return crypto


# print(load_data())
