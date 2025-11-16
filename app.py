import os
import datetime
from typing import Any

import jwt
from dotenv import load_dotenv

load_dotenv()
users_db = [
	{'id': 1, 'login': 'xkadzama', 'password': '123', 'username': 'Xoce', 'role': 'admin'},
	{'id': 2, 'login': 'musasi', 'password': 'mus13', 'username': 'Musa', 'role': 'user'}
]
SECRET_JWT_KEY = os.getenv('SECRET_JWT_KEY', 'put-your-key')


class TokenFindError(Exception):
	def __init__(self, msg='You have not been authenticated.'):
		super().__init__(msg)


def jwt_required(func):
	def wrapper(*args):
		token = get_from_local_storage()
		if token:
			data = jwt.decode(token, SECRET_JWT_KEY, algorithms=['HS256'])
			return func(*args)
	return wrapper


def generate_jwt(user_id, **payload):
	username = payload.get('username', None)
	role = payload.get('role', None)
	token = jwt.encode({
		'user_id': user_id,
		'username': username,
		'role': role,
		'exp': datetime.datetime.now() + datetime.timedelta(hours=7)
	}, SECRET_JWT_KEY)
	return token


def auth():
	login = input('Введите логин: ')
	password = input('Введите пароль: ')

	if login and password:
		user: list[dict[str: Any]] = [user for user in users_db if user.get('login') == login]
		if user:
			user: dict = user[0]
			if user.get('password') == password:
				return generate_jwt(
					user.get('id'),
					username=user.get('username'),
					role=user.get('role')
				)
			else:
				print('Неправильный логин или пароль!')
		else:
			print('Пользователь не найден!')


def add_to_local_storage(token):
	with open('LocalStorage.txt', mode='w', encoding='UTF-8') as ls:
		ls.write(f'Authorization: Bearer {token}')


def get_from_local_storage():
	try:
		with open('LocalStorage.txt', mode='r', encoding='UTF-8') as ls:
			token = ls.read().replace('Authorization: Bearer ', '')
			if len(token) > 10:
				return token
			else:
				raise TokenFindError()
	except FileNotFoundError as e:
		print()
		print(e)
	except TokenFindError as e:
		print()
		print(e)


@jwt_required
def logout():
	with open('LocalStorage.txt', mode='w', encoding='UTF-8') as ls:
		ls.write('')


@jwt_required
def secret_materials():
	print()
	print('>>> Майкл Джексон жив! <<<')


def main():
	name = ''
	menu = '1. Авторизоваться\n2. Секретные материалы\n3. Выход\n0. Завершить программу'
	status = '❌ OFFLINE ❌'
	while True:
		print('---------------')
		print(status)
		print('---------------')
		print(menu)
		chosen = input('>>> ')
		if chosen == '1':
			token = auth()
			if token:
				add_to_local_storage(token)
				status = status.replace('❌ OFFLINE ❌', '✅ ONLINE ✅')
		if chosen == '2':
			secret_materials()
		if chosen == '3':
			status = status.replace('✅ ONLINE ✅', '❌ OFFLINE ❌')
			logout()
		if chosen == '0':
			break
		print()


if __name__ == '__main__':
	main()

