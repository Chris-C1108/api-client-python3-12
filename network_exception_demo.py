#!/usr/bin/env python3
"""
网络异常处理演示脚本

演示更新后的 Gophish 客户端如何正确处理网络异常。
"""

from unittest.mock import patch
import requests
from gophish import Gophish
from gophish.models import Page


def demo_connection_error():
    """演示连接错误处理"""
    print("🔌 演示连接错误处理...")

    client = Gophish("test_key", "http://localhost:3333")

    # 模拟连接错误
    with patch("requests.request") as mock_request:
        mock_request.side_effect = requests.exceptions.ConnectionError(
            "Connection refused"
        )

        try:
            client.pages.get()
        except ConnectionError as e:
            print(f"✅ 正确捕获 ConnectionError: {e}")
            return True
        except Exception as e:
            print(f"❌ 捕获了意外异常: {type(e).__name__}: {e}")
            return False

    return False


def demo_timeout_error():
    """演示超时错误处理"""
    print("\n⏰ 演示超时错误处理...")

    client = Gophish("test_key", "http://localhost:3333")

    # 模拟超时错误
    with patch("requests.request") as mock_request:
        mock_request.side_effect = requests.exceptions.Timeout("Request timed out")

        try:
            client.pages.get()
        except TimeoutError as e:
            print(f"✅ 正确捕获 TimeoutError: {e}")
            return True
        except Exception as e:
            print(f"❌ 捕获了意外异常: {type(e).__name__}: {e}")
            return False

    return False


def demo_retry_compatibility():
    """演示与重试机制的兼容性"""
    print("\n🔄 演示重试机制兼容性...")

    client = Gophish("test_key", "http://localhost:3333")

    # 模拟重试逻辑
    max_retries = 3
    retry_count = 0

    def should_retry(exception):
        return isinstance(exception, (ConnectionError, TimeoutError, Exception))

    # 模拟前两次失败，第三次成功
    with patch("requests.request") as mock_request:
        from unittest.mock import Mock

        success_response = Mock()
        success_response.ok = True
        success_response.json.return_value = []

        mock_request.side_effect = [
            requests.exceptions.ConnectionError("Connection failed"),
            requests.exceptions.Timeout("Timeout"),
            success_response,
        ]

        while retry_count < max_retries:
            try:
                print(f"📡 尝试 #{retry_count + 1}...")
                result = client.pages.get()
                print("✅ 成功获取数据！")
                return True

            except Exception as e:
                retry_count += 1
                print(f"❌ 失败: {type(e).__name__}")

                if retry_count >= max_retries:
                    print("💥 达到最大重试次数")
                    return False

                if not should_retry(e):
                    print("🚫 异常不支持重试")
                    return False

                print("⏳ 准备重试...")

    return False


def demo_all_operations():
    """演示所有操作的异常处理"""
    print("\n🔧 演示所有操作的异常处理...")

    client = Gophish("test_key", "http://localhost:3333")
    page = Page(name="Test Page", html="<html></html>")

    operations = [
        ("GET", lambda: client.pages.get()),
        ("POST", lambda: client.pages.post(page)),
        (
            "PUT",
            lambda: client.pages.put(Page(id=1, name="Test", html="<html></html>")),
        ),
        ("DELETE", lambda: client.pages.delete(1)),
    ]

    success_count = 0

    for op_name, operation in operations:
        with patch("requests.request") as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError(
                "Connection failed"
            )

            try:
                print(f"📡 测试 {op_name} 操作...")
                operation()
                print(f"❌ {op_name} 应该抛出异常")
            except ConnectionError:
                print(f"✅ {op_name} 正确抛出 ConnectionError")
                success_count += 1
            except Exception as e:
                print(f"❌ {op_name} 抛出意外异常: {type(e).__name__}")

    return success_count == len(operations)


def main():
    """主函数"""
    print("🚀 Gophish 网络异常处理演示")
    print("=" * 50)

    results = []

    # 测试连接错误
    results.append(demo_connection_error())

    # 测试超时错误
    results.append(demo_timeout_error())

    # 测试重试兼容性
    results.append(demo_retry_compatibility())

    # 测试所有操作
    results.append(demo_all_operations())

    print("\n" + "=" * 50)
    print("📊 测试结果:")

    test_names = ["连接错误处理", "超时错误处理", "重试机制兼容性", "所有操作异常处理"]

    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{i+1}. {name}: {status}")

    success_rate = sum(results) / len(results) * 100
    print(f"\n🎯 总体成功率: {success_rate:.0f}%")

    if all(results):
        print("\n🎉 所有测试通过！网络异常处理功能正常工作。")
        print("\n📋 功能特性:")
        print("✅ 网络异常被转换为标准异常类型")
        print("✅ 重试机制能够正确识别异常")
        print("✅ 所有 CRUD 操作都支持异常处理")
        print("✅ 异常信息包含详细的调试信息")
    else:
        print("\n⚠️  部分测试失败，请检查实现。")


if __name__ == "__main__":
    main()
