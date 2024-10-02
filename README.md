# QLogin

`QLogin` 是一个用于通过二维码进行 QQ 登录的 Python 包。它使用 QQ 提供的接口生成二维码并检查登录状态，适用于需要快速登录 QQ 的应用。

## 特性

- 生成二维码用于 QQ 登录
- 检查二维码的登录状态
- 返回登录成功后的 cookies 信息

## 安装

请确保你已安装 Python 3.6 或更高版本。然后，你可以通过 pip 安装该包：

```bash
pip install qlogin
```

## 使用示例

```python
from qlogin import QLogin
# 创建实例
qlogin = QLogin()
# 获取二维码
qr_code_base64 = qlogin.get_qr_image()
# 检查登录状态
status = qlogin.check_login_status()
print(status)

```

## 方法

### `get_qr_image()`

获取用于 QQ 登录的二维码，并返回其 base64 编码字符串。

**返回值**: `str` - 二维码图片的 base64 编码。

### `check_login_status()`

检查二维码的登录状态。

**返回值**: `dict` - 包含登录状态和信息的字典，如果登录成功，则包含 cookies。

## 依赖

该项目依赖于以下 Python 包：

- `requests`

## 许可证

该项目采用 MIT 许可证。详细信息请参见 [LICENSE](LICENSE) 文件。