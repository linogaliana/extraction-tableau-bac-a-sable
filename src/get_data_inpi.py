import os
import argparse
import requests
import hvac


# RETRIEVING INFO FROM INPI API


def get_token(user, passwd):
    json = {"username": user, "password": passwd}
    r = requests.post(
        "https://registre-national-entreprises.inpi.fr/api/sso/login", json=json
    )
    r.status_code
    token = r.json()["token"]
    return token


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def get_documents_siren(siren: str, token: str):

    r = requests.get(
        f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}/attachments",
        auth=BearerAuth(token),
    )
    if r.status_code != 200:
        # Handle error: you can raise an exception or handle it in another way
        raise Exception(f"Request failed with status code {r.status_code}: {r.text}")

    documents = r.json()
    identifier = documents["bilans"][0]["id"]

    return documents, identifier


def download_pdf_bilan(identifier, token, binary_file_path="test.pdf"):
    r = requests.get(
        f"https://registre-national-entreprises.inpi.fr/api/bilans/{identifier}/download",
        auth=BearerAuth(token),
    )
    if r.status_code != 200:
        # Handle error: you can raise an exception or handle it in another way
        raise Exception(f"Request failed with status code {r.status_code}: {r.text}")
    with open(binary_file_path, "wb") as f:
        f.write(r.content)
