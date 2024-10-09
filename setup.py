from setuptools import setup, find_packages

setup(
    name="qlogin",            # 包的名字
    version="0.1.2",                     # 初始版本号
    author="LibraHp",                  # 作者名字
    author_email="1941163264@qq.com",# 作者联系信息
    description="QQ空间登录组件",   # 简短描述
    long_description=open("README.md", encoding="utf-8").read(), # 详细描述，从 README 读取
    long_description_content_type="text/markdown",  # README 的格式
    url="https://github.com/LibraHp/Qlogin",  # 项目主页
    packages=find_packages(),            # 自动查找包
    classifiers=[                        # 分类信息
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',             # 支持的 Python 版本
    install_requires=[                   # 依赖包
        "requests",
        # 其他依赖包
    ],
)
