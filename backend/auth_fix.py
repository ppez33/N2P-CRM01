from passlib.context import CryptContext

# Verificar las contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Las contraseñas que deberían funcionar
passwords = {
    "admin": "admin123",
    "manager": "manager123", 
    "tech": "tech123"
}

# El hash que está en el código
stored_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p02T/oJjU9j.FYQ0TaR1rL/W"

for user, password in passwords.items():
    result = pwd_context.verify(password, stored_hash)
    print(f"{user}/{password}: {'✅ CORRECTO' if result else '❌ INCORRECTO'}")
    
# Generar nuevos hashes
print("\nNuevos hashes correctos:")
for user, password in passwords.items():
    new_hash = pwd_context.hash(password)
    print(f"{user}: {new_hash}")