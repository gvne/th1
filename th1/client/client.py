import datetime
import logging
import pathlib
import json
import typing as ty

import requests
import pydantic

import th1.client.constant as c
import th1.client.schema.auth as auth
import th1.client.schema.thermostat as ts
import th1.client.schema.smartphone as ss


class Auth:
    class Cache(pydantic.BaseModel):
        token: auth.Response
        received_at: datetime.datetime

    def __init__(self, cache_path: pathlib.Path | None = None):
        self.__cache_path = cache_path
        self.__token: auth.Response | None = None
        self.__received_at: datetime.datetime | None = None
        if self.__cache_path is not None:
            self.__load_from_cache()

    def __load_from_cache(self):
        if not self.__cache_path.exists():
            logging.info("[Auth] No cache found. Logging required")
            return

        with open(self.__cache_path, "r") as f:
            data = f.read()
            try:
                data_json = json.loads(data)
                cache = Auth.Cache.model_validate(data_json)
                self.__token = cache.token
                self.__received_at = cache.received_at
            except Exception as e:
                logging.warning(f"[Auth] Failed to load cache: {e}")

    def __save_to_cache(self):
        assert self.__token is not None and self.__received_at is not None
        with open(self.__cache_path, "w") as f:
            cache = Auth.Cache(token=self.__token, received_at=self.__received_at)
            f.write(cache.model_dump_json())

    def is_logged_in(self) -> bool:
        return self.__token is not None and self.__received_at is not None

    def login(self, username: str, password: str):
        req = auth.Request(
            client_id=c.CLIENT_ID,
            client_secret=c.CLIENT_SECRET,
            username=username,
            password=password,
        )
        resp = requests.post(c.AUTH_ENDPOINT, json=req.model_dump())
        resp.raise_for_status()

        self.__token = auth.Response.model_validate(resp.json())
        self.__received_at = datetime.datetime.now()
        self.__save_to_cache()

    def __refresh(self):
        if self.__token is None:
            raise RuntimeError("Auth error: token not initialized")

        req = auth.RefreshRequest(
            client_id=c.CLIENT_ID,
            client_secret=c.CLIENT_SECRET,
            refresh_token=self.__token.refresh_token,
        )
        resp = requests.post(c.AUTH_ENDPOINT, json=req.model_dump())
        resp.raise_for_status()

        self.__token = auth.Response.model_validate(resp.json())
        self.__received_at = datetime.datetime.now()
        self.__save_to_cache()

    @property
    def header(self) -> str:
        if self.__expired:
            self.__refresh()
        return f"{self.__token.token_type} {self.__token.access_token}"

    @property
    def __expires_at(self) -> datetime.datetime:
        if self.__token is None or self.__received_at is None:
            raise RuntimeError("Auth error: token not initialized")
        return self.__received_at + datetime.timedelta(seconds=self.__token.expires_in)

    @property
    def __refresh_after(self) -> datetime.datetime:
        # force refresh 10seconds before expirations
        return self.__expires_at - datetime.timedelta(seconds=10)

    @property
    def __expired(self) -> bool:
        return datetime.datetime.now() >= self.__refresh_after


class Client:
    def __init__(self, cache_path: pathlib.Path | None = pathlib.Path(".th1_cache")):
        self.__auth = Auth(cache_path)

        self.__previous_thermostat_info: dict[str, ty.Any] | None = None
        self.__previous_thermostat_info_id: str | None = None
        self.__previous_thermostat_info_smartphone_id: str | None = None

    def login(self, username: str, password: str):
        self.__auth.login(username, password)

    @property
    def __default_request_headers(self) -> dict[str, str]:
        return {
            "user-agent": "okhttp/4.9.0",
            "authorization": self.__auth.header,
        }

    def get_thermostats(self) -> ts.Response:
        resp = requests.get(
            f"{c.API_ENDPOINT}/api/thermostats", headers=self.__default_request_headers
        )
        resp.raise_for_status()
        return ts.Response.model_validate(resp.json())

    def get_smartphones(self, thermostat_id: str) -> list[ss.Smartphone]:
        resp = requests.get(
            f"{c.API_ENDPOINT}/api/thermostats/{thermostat_id}/smartphones",
            headers=self.__default_request_headers,
        )
        resp.raise_for_status()
        return [ss.Smartphone.model_validate(v) for v in resp.json()]

    def get_thermostat_info(
        self, thermostat_id: str, smartphone_vendor_id: str
    ) -> ts.Info:
        # determine if we need can just ask for a partial update
        complete_query = (
            self.__previous_thermostat_info_id != thermostat_id
            or self.__previous_thermostat_info_smartphone_id != smartphone_vendor_id
        )

        # Run the query
        resp = requests.get(
            f"{c.API_ENDPOINT}/api/smartphones/{smartphone_vendor_id}/thermostats/{thermostat_id}/all_informations?timestamp={0 if complete_query else 1}",
            headers=self.__default_request_headers,
        )
        resp_json = resp.json()
        resp.raise_for_status()

        if complete_query:  # if we asked for a complete info
            info_json = resp_json
        else:  # for partial ones
            # merge the previous response and the current one
            logging.debug(f"[TH1][Client] latest diff: {resp_json}")
            info_json = {**self.__previous_thermostat_info, **resp_json}

        self.__previous_thermostat_info_id = thermostat_id
        self.__previous_thermostat_info_smartphone_id = smartphone_vendor_id
        self.__previous_thermostat_info = info_json

        return ts.Info.model_validate(info_json)
