import uuid
import datetime
import requests

from app.core.config import settings
from app import log


class ComcastIntegrationException(Exception):
    pass


class IntegrationBase:
    def __init__(self, partner_id):
        if (
            not settings.COMCAST_TOKEN
            or settings.COMCAST_TOKEN_EXPIRES_AT <= datetime.datetime.now()
        ):
            self.pull_token()

        self.url = (
            settings.COMCAST_SERVER_BASE_URL + f"/v1/partners/{partner_id}/network"
        )

    @staticmethod
    def pull_token():
        headers = {
            "Content-Type": "application/json",
            "X-Client-Id": settings.COMCAST_AUTH_CLIENT_ID,
            "X-Client-Secret": settings.COMCAST_AUTH_CLIENT_SECRET,
        }
        response = requests.post(
            url=settings.COMCAST_AUTH_TOKEN_URL,
            headers=headers,
            data={"scope": settings.COMCAST_AUTH_SCOPE},
        )

        if response.status_code not in [200, 201]:
            raise ComcastIntegrationException("Failed to fetch token")

        settings.COMCAST_TOKEN = response.json()["access_token"]
        settings.COMCAST_TOKEN_EXPIRES_AT = (
            datetime.datetime.now()
            + datetime.timedelta(seconds=response.json().get("expires_in"))
        )

    @staticmethod
    def make_http_call(url, method: str, data: dict | None = None):
        headers = {"Authorization": f"Bearer {settings.COMCAST_TOKEN}"}
        response = requests.request(method=method, url=url, headers=headers, json=data)
        return response


class HubIntegration(IntegrationBase):
    def __init__(self, partner_id):
        super().__init__(partner_id=partner_id)
        self.url = self.url + "/hub"

    def create(self, data: dict) -> dict:
        return {"hub_id": uuid.uuid4()}

    def update(self, hub_id: uuid.UUID) -> dict:
        return dict()

    def delete(self, hub_id: uuid.UUID) -> None:
        return


class SiteIntentIntegration(IntegrationBase):
    def __init__(self, partner_id):
        super().__init__(partner_id=partner_id)
        self.url = self.url + "/siteIntent"

    def create(self, data: dict) -> dict:
        response = self.make_http_call(url=self.url, method="POST", data=data)
        if response not in [200, 201]:
            log.error(f"Failed to create site intent: {response.text}")
            raise ComcastIntegrationException(
                f"Failed to create site intent: {response.text}"
            )

        return response.json()

    def update(self, site_intent_id: uuid.UUID) -> dict:
        url = self.url + f"/{site_intent_id}"
        response = self.make_http_call(url=url, method="PUT")
        if response not in [200, 201]:
            log.error(f"Failed to update site intent: {response.text}")
            raise ComcastIntegrationException(
                f"Failed to update site intent: {response.text}"
            )

        return response.json()

    def delete(self, site_intent_id: uuid.UUID) -> None:
        url = self.url + f"/{site_intent_id}"
        response = self.make_http_call(url=url, method="DELETE")
        if response not in [200, 204]:
            log.error(f"Failed to delete site intent: {response.text}")
            raise ComcastIntegrationException(
                f"Failed to delete site intent: {response.text}"
            )


class PpodIntentIntegration(IntegrationBase):
    def __init__(self, partner_id):
        super().__init__(partner_id=partner_id)
        self.url = self.url + "/ppodIntent"

    def create(self, data: dict) -> dict:
        response = self.make_http_call(url=self.url, method="POST", data=data)
        if response not in [200, 201]:
            log.error(f"Failed to create ppod intent: {response.text}")
            raise ComcastIntegrationException(
                f"Failed to create ppod intent: {response.text}"
            )

        return response.json()

    def update(self, ppod_intent_id: uuid.UUID) -> dict:
        url = self.url + f"/{ppod_intent_id}"
        response = self.make_http_call(url=url, method="PUT")
        if response not in [200, 201]:
            log.error(f"Failed to update ppod intent: {response.text}")
            raise ComcastIntegrationException(
                f"Failed to update ppod intent: {response.text}"
            )

        return response.json()

    def delete(self, ppod_intent_id: uuid.UUID) -> None:
        url = self.url + f"/{ppod_intent_id}"
        response = self.make_http_call(url=url, method="DELETE")
        if response not in [200, 204]:
            log.error(f"Failed to delete ppod intent: {response.text}")
            raise ComcastIntegrationException(
                f"Failed to delete ppod intent: {response.text}"
            )
