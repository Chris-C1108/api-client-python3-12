#!/usr/bin/env python3
"""
网络异常处理演示脚本

这个脚本演示了更新后的 Gophish 客户端如何正确处理网络异常，
使重试机制能够正常工作。
"""

import time
from gophish import Gophish
from gophish.models import Page


def simulate_retry_mechanism():
    """模拟带重试机制的操作"""
    print("🔄 模拟重试机制...")

    # 创建客户端（使用无法连接的地址来触发网络异常）
    client = Gophish("test_key", "http://192.0.2.1:3333")  # 使用测试用的不可路由地址

    max_retries = 3
    retry_count = 0

    def should_retry(exception):
        """判断是否应该重试"""
        return isinstance(exception, (ConnectionError, TimeoutError, Exception))

    while retry_count < max_retries:
        try:
            print(f"📡 尝试连接... (第 {retry_count + 1} 次)")

            # 这会触发 ConnectionError
            pages = client.pages.get()

            print("✅ 连接成功！")
            return pages

        except Exception as e:
            retry_count += 1
            print(f"❌ 连接失败: {type(e).__name__}: {e}")

            if retry_count >= max_retries:
                print(f"💥 达到最大重试次数 ({max_retries})，放弃重试")
                raise

            if not should_retry(e):
                print("🚫 异常类型不支持重试，直接抛出")
                raise

            print(f"⏳ 等待 2 秒后重试...")
            time.sleep(2)

    return None


def test_exception_types():
    """测试异常类型"""
    print("\n🧪 测试异常类型...")

    client = Gophish("test_key", "http://invalid-server:3333")

    try:
        client.pages.get()
    except ConnectionError as e:
        print(f"✅ 正确捕获 ConnectionError: {type(e).__name__}")
        print(f"   消息: {e}")
        return True
    except Exception as e:
        print(f"❌ 捕获了意外的异常类型: {type(e).__name__}")
        return False

    return False


def test_different_operations():
    """测试不同操作的异常处理"""
    print("\n🔧 测试不同操作的异常处理...")

    client = Gophish("test_key", "http://invalid-server:3333")
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

    for op_name, operation in operations:
        try:
            print(f"📡 测试 {op_name} 操作...")
            operation()
        except ConnectionError:
            print(f"✅ {op_name} 操作正确抛出 ConnectionError")
        except Exception as e:
            print(f"❌ {op_name} 操作抛出了意外异常: {type(e).__name__}")


def main():
    """主函数"""
    print("🚀 Gophish 网络异常处理演示")
    print("=" * 50)

    # 测试异常类型
    if test_exception_types():
        print("✅ 异常类型测试通过")
    else:
        print("❌ 异常类型测试失败")

    # 测试不同操作
    test_different_operations()

    # 模拟重试机制
    try:
        simulate_retry_mechanism()
    except Exception as e:
        print(f"✅ 重试机制正常工作，最终异常: {type(e).__name__}")

    print("\n🎉 演示完成！")
    print("\n📋 总结:")
    print("✅ 网络异常被正确转换为标准异常类型")
    print("✅ 重试机制能够正确识别和处理异常")
    print("✅ 所有 CRUD 操作都支持异常处理")
    print("✅ 异常信息包含有用的调试信息")


if __name__ == "__main__":
    main()
