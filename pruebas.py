import hashlib
contraseña = input("Escribe tu contraseña: ")
contraseña = contraseña.encode()
h = hashlib.md5(contraseña)
print(h.digest())