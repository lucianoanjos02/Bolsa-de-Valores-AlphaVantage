import os
import binascii

# SECRET_KEY - Utilizado na aplicação do Flask
SECRET_KEY = binascii.hexlify(os.urandom(24))
# API_KEY - Chave da API da Alpha Vantage
API_KEY = '7IEKBZD1IV0BSJQN'