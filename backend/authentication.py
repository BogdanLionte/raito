import os
import base64
import urllib.request
import urllib.parse
import json
from django.http import HttpResponse
import requests
from google.auth import jwt
from google.auth import crypt
import time

client_id = "477803517223-82lkjk4c26kfrn5hp14vjlmgnpl8a7pk.apps.googleusercontent.com"
client_secret = "NgMWQNjbMpB6dsxJmk_GxTP-"
redirect_uri = "http://localhost:8000/code"

csrf_tokens = set()
r = urllib.request.urlopen('https://accounts.google.com/.well-known/openid-configuration')
discovery_doc = json.loads(r.read())
r = urllib.request.urlopen('https://www.googleapis.com/oauth2/v1/certs')
certs = json.loads(r.read().decode("utf-8"))


def http_method_list(methods):
    def http_methods_decorator(func):
        def function_wrapper(request, **kwargs):
            upper_methods = [method.upper() for method in methods]
            if not request.method.upper() in upper_methods:
                return HttpResponse(status=405) # not allowed

            return func(request, **kwargs)
        return function_wrapper
    return http_methods_decorator


def create_claims(user_email, exp_time):
    now = int(time.time())
    return {
        "sub": user_email,
        "iat": now,
        "exp": now + exp_time,
        "nbf": now + exp_time
    }


def create_access_token(user_email):
    with open("secrets/access_token.key", 'r') as f:
        rsa_private_key = f.read()
        claims = create_claims(user_email, 60 * 60 * 24 * 7 * 4 * 12)
        claims["aud"] = "access"
        signer = crypt.RSASigner.from_string(rsa_private_key)
        return jwt.encode(signer, claims).decode("ascii")


def create_refresh_token(user_email):
    with open("secrets/refresh_token.key", 'r') as f:
        rsa_private_key = f.read()
        claims = create_claims(user_email, 3600)
        claims["aud"] = "refresh"
        signer = crypt.RSASigner.from_string(rsa_private_key)
        return jwt.encode(signer, claims).decode("ascii")


@http_method_list(["GET"])
def get_auth_uri(_request):
    csrf_token = base64.urlsafe_b64encode(os.urandom(60)).decode("utf-8")
    csrf_tokens.add(csrf_token)
    base_uri = discovery_doc['authorization_endpoint']
    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": "openid email",
        "redirect_uri": redirect_uri,
        "state": csrf_token
    }
    auth_uri = base_uri + "?" + urllib.parse.urlencode(params)
    html = f"""
        <html>
            <script>
                window.open("{auth_uri}");
            </script>
        </html>
    """
    response = HttpResponse(html)
    response["Content-Type"] = "text/html"
    response.status_code = 200
    return response


@http_method_list(["GET"])
def consume_auth_code(request):
    if request.GET['state'] not in csrf_tokens:
        response = HttpResponse()
        response.status_code = 401
        return response
    csrf_tokens.remove(request.GET['state'])
    code = request.GET['code']
    url = discovery_doc['token_endpoint']
    params = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    response = requests.post(url, data=params, headers={"Content-Type": "application/x-www-form-urlencoded"}).text
    id_token = json.loads(response)['id_token']
    user_email = jwt.decode(id_token, certs=certs)["email"]
    access_token = create_access_token(user_email)
    refresh_token = create_refresh_token(user_email)
    message = json.dumps({"access_token": access_token, "refresh_token": refresh_token})
    print(access_token)
    html = f"""
    <html>
        <script>
            window.opener.postMessage('{message}', 'http://localhost:4200');
            window.close();
        </script>
    </html>    
    """
    response = HttpResponse(html)
    response["Content-Type"] = "text/html"
    response.status_code = 200
    return response


def validate_refresh_token(refresh_token):
    with open("secrets/refresh_token.cert", "r") as f:
        rsa_public_key = f.read()
        return jwt.decode(refresh_token, certs=rsa_public_key)["sub"]


def validate_access_token(access_token):
    with open("secrets/access_token.cert", "r") as f:
        rsa_public_key = f.read()
        return jwt.decode(access_token, certs=rsa_public_key)["sub"]


@http_method_list(["POST"])
def refresh_tokens(request):
    body = json.loads(request.body)
    if "refresh_token" not in body:
        return HttpResponse(status=401)
    try:
        user_email = validate_refresh_token(body["refresh_token"])
        result = {
            "refresh_token": create_refresh_token(user_email),
            "access_token": create_access_token(user_email)
        }
        result = json.dumps(result)
        response = HttpResponse(result, status=200)
        response['Content-Type'] = "application/json"
        return response
    except ValueError:
        return HttpResponse(status=401)


def is_authorized(func):
    def authorization_decorator(request, **kwargs):
        access_token = request.headers.get("Authorization")
        try:
            if access_token is not None:
                validate_access_token(access_token)
                return func(request, **kwargs)
            else:
                raise ValueError
        except ValueError:
            return HttpResponse(status=401)
    return authorization_decorator
