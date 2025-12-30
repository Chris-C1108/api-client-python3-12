import requests
from gophish.models import Error

"""
api.py

Base API endpoint class that abstracts basic CRUD operations.
"""


class APIEndpoint:
    """
    Represents an API endpoint for Gophish, containing common patterns
    for CRUD operations.
    """

    def __init__(self, api, endpoint=None, cls=None):
        """Creates an instance of the APIEndpoint class.

        Args:
            api - Gophish.client - The authenticated REST client
            endpoint - str - The URL path to the resource endpoint
            cls - gophish.models.Model - The Class to use when parsing results
        """
        self.api = api
        self.endpoint = endpoint
        self._cls = cls

    def _build_url(self, *parts):
        """Builds a path to an API resource by joining the individual parts
        with a slash (/).

        This is used instead of urljoin since we're given relative URL parts
        which need to be chained together.

        Returns:
            str -- The parts joined with a slash
        """

        return "/".join(str(part).rstrip("/") for part in parts)

    def request(
        self,
        method,
        body=None,
        resource_id=None,
        resource_action=None,
        resource_cls=None,
        single_resource=False,
    ):

        endpoint = self.endpoint

        if not resource_cls:
            resource_cls = self._cls

        if resource_id:
            endpoint = self._build_url(endpoint, resource_id)

        if resource_action:
            endpoint = self._build_url(endpoint, resource_action)

        try:
            response = self.api.execute(method, endpoint, json=body)
        except requests.exceptions.ConnectionError as e:
            # 网络连接错误 - 重新抛出为标准异常以便重试机制处理
            raise ConnectionError(f"Failed to connect to Gophish server: {e}")
        except requests.exceptions.Timeout as e:
            # 超时错误 - 重新抛出为标准异常以便重试机制处理
            raise TimeoutError(f"Request to Gophish server timed out: {e}")
        except requests.exceptions.RequestException as e:
            # 其他请求异常
            raise Exception(f"Request failed: {e}")

        if not response.ok:
            raise Error.parse(response.json())

        if resource_id or single_resource:
            return resource_cls.parse(response.json())

        return [resource_cls.parse(resource) for resource in response.json()]

    def get(
        self,
        resource_id=None,
        resource_action=None,
        resource_cls=None,
        single_resource=False,
    ):
        """Gets the details for one or more resources by ID

        Args:
            cls - gophish.models.Model - The resource class
            resource_id - str - The endpoint (URL path) for the resource
            resource_action - str - An action to perform on the resource
            resource_cls - cls - A class to use for parsing, if different than
                the base resource
            single_resource - bool - An override to tell Gophish that even
                though we aren't requesting a single resource, we expect a
                single response object

        Returns:
            One or more instances of cls parsed from the returned JSON
        """

        return self.request(
            "GET",
            resource_id=resource_id,
            resource_action=resource_action,
            resource_cls=resource_cls,
            single_resource=single_resource,
        )

    def post(self, resource):
        """Creates a new instance of the resource.

        Args:
            resource - gophish.models.Model - The resource instance

        """
        try:
            response = self.api.execute(
                "POST", self.endpoint, json=(resource.as_dict())
            )
        except requests.exceptions.ConnectionError as e:
            # 网络连接错误 - 重新抛出为标准异常以便重试机制处理
            raise ConnectionError(f"Failed to connect to Gophish server: {e}")
        except requests.exceptions.Timeout as e:
            # 超时错误 - 重新抛出为标准异常以便重试机制处理
            raise TimeoutError(f"Request to Gophish server timed out: {e}")
        except requests.exceptions.RequestException as e:
            # 其他请求异常
            raise Exception(f"Request failed: {e}")

        if not response.ok:
            raise Error.parse(response.json())

        return self._cls.parse(response.json())

    def put(self, resource):
        """Edits an existing resource

        Args:
            resource - gophish.models.Model - The resource instance
        """

        endpoint = self.endpoint

        if resource.id:
            endpoint = self._build_url(endpoint, resource.id)

        try:
            response = self.api.execute("PUT", endpoint, json=resource.as_dict())
        except requests.exceptions.ConnectionError as e:
            # 网络连接错误 - 重新抛出为标准异常以便重试机制处理
            raise ConnectionError(f"Failed to connect to Gophish server: {e}")
        except requests.exceptions.Timeout as e:
            # 超时错误 - 重新抛出为标准异常以便重试机制处理
            raise TimeoutError(f"Request to Gophish server timed out: {e}")
        except requests.exceptions.RequestException as e:
            # 其他请求异常
            raise Exception(f"Request failed: {e}")

        if not response.ok:
            raise Error.parse(response.json())

        return self._cls.parse(response.json())

    def delete(self, resource_id):
        """Deletes an existing resource

        Args:
            resource_id - int - The resource ID to be deleted
        """

        endpoint = f"{self.endpoint}/{resource_id}"

        try:
            response = self.api.execute("DELETE", endpoint)
        except requests.exceptions.ConnectionError as e:
            # 网络连接错误 - 重新抛出为标准异常以便重试机制处理
            raise ConnectionError(f"Failed to connect to Gophish server: {e}")
        except requests.exceptions.Timeout as e:
            # 超时错误 - 重新抛出为标准异常以便重试机制处理
            raise TimeoutError(f"Request to Gophish server timed out: {e}")
        except requests.exceptions.RequestException as e:
            # 其他请求异常
            raise Exception(f"Request failed: {e}")

        if not response.ok:
            raise Error.parse(response.json())

        return self._cls.parse(response.json())
