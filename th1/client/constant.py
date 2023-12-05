import base64


CLIENT_ID = base64.b64decode(
    "MWUyZDgzMGYtNGM2NS0xMWU3LWJkMGMtMDJkZDU5YmQzMDQxXzVuNzhyNW5ud2F3NHdjMGtza2tnMGNzb2drazhjd29jc3dnODRjMGdvd2Nnb3Nzb2d3"
).decode("utf-8")
CLIENT_SECRET = base64.b64decode(
    "NHR4dWN3c3YyOWE4bzBjbzhzOGt3OGdnc3dra3M4b3NzY2NvY2tnY2Nrb2t3OGNrMDA="
).decode("utf-8")

API_ENDPOINT = "https://th1.somfy.com/rest-api"
AUTH_ENDPOINT = "https://accounts.somfy.com/oauth/oauth/v2/token"
