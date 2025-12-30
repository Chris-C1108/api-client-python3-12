"""
测试网络异常处理功能

这些测试验证 Gophish 客户端能够正确处理网络层异常，
使重试机制能够正常工作。
"""

import pytest
import requests
from unittest.mock import patch, Mock
from gophish import Gophish
from gophish.models import Page, Group, User


class TestNetworkExceptionHandling:
    """测试网络异常处理"""

    def setup_method(self):
        """设置测试客户端"""
        self.client = Gophish("test_key", "http://localhost:3333")

    def test_connection_error_handling_get(self):
        """测试 GET 请求的连接错误处理"""
        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError(
                "Connection failed"
            )

            with pytest.raises(ConnectionError) as exc_info:
                self.client.pages.get()

            assert "Failed to connect to Gophish server" in str(exc_info.value)

    def test_timeout_error_handling_get(self):
        """测试 GET 请求的超时错误处理"""
        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout("Request timed out")

            with pytest.raises(TimeoutError) as exc_info:
                self.client.pages.get()

            assert "Request to Gophish server timed out" in str(exc_info.value)

    def test_other_request_exceptions_get(self):
        """测试 GET 请求的其他请求异常"""
        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.RequestException(
                "Generic error"
            )

            with pytest.raises(Exception) as exc_info:
                self.client.pages.get()

            assert "Request failed" in str(exc_info.value)

    def test_connection_error_handling_post(self):
        """测试 POST 请求的连接错误处理"""
        page = Page(name="Test Page", html="<html></html>")

        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError(
                "Connection failed"
            )

            with pytest.raises(ConnectionError) as exc_info:
                self.client.pages.post(page)

            assert "Failed to connect to Gophish server" in str(exc_info.value)

    def test_timeout_error_handling_post(self):
        """测试 POST 请求的超时错误处理"""
        page = Page(name="Test Page", html="<html></html>")

        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout("Request timed out")

            with pytest.raises(TimeoutError) as exc_info:
                self.client.pages.post(page)

            assert "Request to Gophish server timed out" in str(exc_info.value)

    def test_connection_error_handling_put(self):
        """测试 PUT 请求的连接错误处理"""
        page = Page(id=1, name="Test Page", html="<html></html>")

        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError(
                "Connection failed"
            )

            with pytest.raises(ConnectionError) as exc_info:
                self.client.pages.put(page)

            assert "Failed to connect to Gophish server" in str(exc_info.value)

    def test_timeout_error_handling_put(self):
        """测试 PUT 请求的超时错误处理"""
        page = Page(id=1, name="Test Page", html="<html></html>")

        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout("Request timed out")

            with pytest.raises(TimeoutError) as exc_info:
                self.client.pages.put(page)

            assert "Request to Gophish server timed out" in str(exc_info.value)

    def test_connection_error_handling_delete(self):
        """测试 DELETE 请求的连接错误处理"""
        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError(
                "Connection failed"
            )

            with pytest.raises(ConnectionError) as exc_info:
                self.client.pages.delete(1)

            assert "Failed to connect to Gophish server" in str(exc_info.value)

    def test_timeout_error_handling_delete(self):
        """测试 DELETE 请求的超时错误处理"""
        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout("Request timed out")

            with pytest.raises(TimeoutError) as exc_info:
                self.client.pages.delete(1)

            assert "Request to Gophish server timed out" in str(exc_info.value)

    def test_successful_request_after_exception_handling(self):
        """测试异常处理不影响正常请求"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = []

        with patch("requests.request", return_value=mock_response):
            # 这应该正常工作，不抛出异常
            result = self.client.pages.get()
            assert result == []

    def test_different_endpoints_exception_handling(self):
        """测试不同端点的异常处理"""
        endpoints_to_test = [
            self.client.campaigns,
            self.client.groups,
            self.client.templates,
            self.client.smtp,
            self.client.webhooks,
        ]

        for endpoint in endpoints_to_test:
            with patch("requests.request") as mock_request:
                mock_request.side_effect = requests.exceptions.ConnectionError(
                    "Connection failed"
                )

                with pytest.raises(ConnectionError):
                    endpoint.get()

    def test_exception_chaining_preserved(self):
        """测试异常链保持完整"""
        original_error = requests.exceptions.ConnectionError(
            "Original connection error"
        )

        with patch("requests.request") as mock_request:
            mock_request.side_effect = original_error

            with pytest.raises(ConnectionError) as exc_info:
                self.client.pages.get()

            # 验证原始异常信息被保留
            assert "Original connection error" in str(exc_info.value)


class TestRetryCompatibility:
    """测试与重试机制的兼容性"""

    def test_exception_types_for_retry(self):
        """测试抛出的异常类型适合重试机制"""
        client = Gophish("test_key", "http://localhost:3333")

        # 测试 ConnectionError
        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError(
                "Connection failed"
            )

            try:
                client.pages.get()
            except Exception as e:
                # 验证异常类型是标准的 ConnectionError
                assert isinstance(e, ConnectionError)
                assert not isinstance(e, requests.exceptions.ConnectionError)

        # 测试 TimeoutError
        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout("Timeout")

            try:
                client.pages.get()
            except Exception as e:
                # 验证异常类型是标准的 TimeoutError
                assert isinstance(e, TimeoutError)
                assert not isinstance(e, requests.exceptions.Timeout)

    def test_retry_mechanism_simulation(self):
        """模拟重试机制的工作方式"""
        client = Gophish("test_key", "http://localhost:3333")

        # 模拟重试逻辑
        max_retries = 3
        retry_count = 0

        def should_retry(exception):
            return isinstance(exception, (ConnectionError, TimeoutError, Exception))

        with patch("requests.request") as mock_request:
            # 前两次失败，第三次成功
            mock_response = Mock()
            mock_response.ok = True
            mock_response.json.return_value = []

            mock_request.side_effect = [
                requests.exceptions.ConnectionError("Connection failed"),
                requests.exceptions.Timeout("Timeout"),
                mock_response,
            ]

            while retry_count < max_retries:
                try:
                    result = client.pages.get()
                    # 成功了，跳出循环
                    assert result == []
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise
                    if not should_retry(e):
                        raise
                    # 继续重试
                    continue

            # 验证重试了 2 次后成功
            assert retry_count == 2
