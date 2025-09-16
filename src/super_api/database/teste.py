import jwt
print(jwt.__file__)    # Mostra de onde o módulo está sendo carregado
print(getattr(jwt, '__version__', 'sem versão'))  # Mostra a versão se existir