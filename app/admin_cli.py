import requests

API_URL = "http://127.0.0.1:8000"
TOKEN = None

def login():
    global TOKEN
    email = input("Email admin: ")
    password = input("Contraseña: ")
    r = requests.post(f"{API_URL}/auth/login", json={"email": email, "contraseña": password})
    if r.status_code == 200:
        TOKEN = r.json()["access_token"]
        print("✅ Login correcto\n")
    else:
        print("❌ Error en login:", r.json())

def auth_headers():
    return {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

def list_users():
    r = requests.get(f"{API_URL}/users", headers=auth_headers())
    print("\nUsuarios registrados:")
    for u in r.json():
        print(f" - {u['id']}: {u['nombre']} ({u['email']}) rol={u['rol']}")

def list_rooms():
    r = requests.get(f"{API_URL}/rooms", headers=auth_headers())
    print("\nSalas disponibles:")
    for r_ in r.json():
        print(f" - {r_['id']}: {r_['nombre']} | {r_['sede']} | Capacidad {r_['capacidad']}")

def list_reservations():
    r = requests.get(f"{API_URL}/reservations/date/2025-09-02", headers=auth_headers())
    print("\nReservas en 2025-09-02:")
    for res in r.json():
        print(f" - ID {res['id']} | Sala {res['sala_id']} | Usuario {res['usuario_id']} | {res['hora_inicio']} - {res['hora_fin']} | Estado {res['estado']}")

def cancel_reservation():
    res_id = input("ID de reserva a cancelar: ")
    r = requests.delete(f"{API_URL}/reservations/{res_id}", headers=auth_headers())
    print(r.json())

def menu():
    while True:
        print("\n--- Panel Admin ---")
        print("1. Listar usuarios")
        print("2. Listar salas")
        print("3. Ver reservas por fecha fija (ejemplo 2025-09-02)")
        print("4. Cancelar reserva")
        print("0. Salir")

        opt = input("Selecciona opción: ")
        if opt == "1":
            list_users()
        elif opt == "2":
            list_rooms()
        elif opt == "3":
            list_reservations()
        elif opt == "4":
            cancel_reservation()
        elif opt == "0":
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    login()
    if TOKEN:
        menu()
