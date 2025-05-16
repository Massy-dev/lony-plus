import requests

BASE_URL = "http://localhost:8000/api/users"

# Tes identifiants d'utilisateur
USERNAME = "Massy"
PASSWORD = "1833production"

def login():
    url = f"{BASE_URL}/login/"
    data = {"username": USERNAME, "password": PASSWORD}
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        tokens = resp.json()
        print("Login OK")
        print("Access token:", tokens['access'])
        print("Refresh token:", tokens['refresh'])
        return tokens
    else:
        print("Login failed:", resp.text)
        return None

def refresh_token(refresh):
    url = f"{BASE_URL}/login/refresh/"
    data = {"refresh": refresh}
    resp = requests.post(url, json=data)
    print("Refresh token response:", resp.status_code, resp.text)

def verify_token(token):
    url = f"{BASE_URL}/login/verify/"
    data = {"token": token}
    resp = requests.post(url, json=data)
    print("Verify token response:", resp.status_code, resp.text)

def logout(refresh, access):
    url = f"{BASE_URL}/logout/"
    headers = {"Authorization": f"Bearer {access}"}
    data = {"refresh": refresh}
    resp = requests.post(url, headers=headers, json=data)
    print("Logout response:", resp.status_code, resp.text)

def main():
    tokens = login()
    if not tokens:
        return

    verify_token(tokens['access'])
    refresh_token(tokens['refresh'])
    logout(tokens['refresh'], tokens['access'])

if __name__ == "__main__":
    main()
