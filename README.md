# QLogin

`QLogin` 是一个用于通过二维码进行 QQ 登录的 Python 包。它使用 QQ 提供的接口生成二维码并检查登录状态，适用于需要快速登录 QQ 的应用。

## 特性

- 生成二维码用于 QQ 登录
- 检查二维码的登录状态
- 返回登录成功后的 cookies 信息
- 获取当前登录用户的 QQ 资料

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
print("QR Code (Base64):", qr_code_base64)

# 检查登录状态
status = qlogin.check_login_status()
print("Login Status:", status)

# 获取用户信息
if status.get('status') == 'success':
    user_info = qlogin.get_login_user_info()
    print("User Info:", user_info)
```

## 属性

### `qrsig`
- 类型: `str`
- 描述: QR 码的签名，用于生成 QR 码和检查登录状态。

### `cookies`
- 类型: `dict`
- 描述: 登录成功后返回的 cookies 信息，包含用户的登录状态信息。

### `uin`
- 类型: `str`
- 描述: 用户的 QQ 号，在登录成功后从 cookies 中提取。

### `g_tk`
- 类型: `int`
- 描述: 用于进行用户请求的安全验证值。

## 方法

### `get_qr_image()`
获取用于 QQ 登录的二维码，并返回其 base64 编码字符串。

- **返回值**: `str` - 二维码图片的 base64 编码。
- **异常**: 
  - `ConnectionError`: 如果无法获取二维码，抛出连接错误。
  - `ValueError`: 如果未能成功获取 `qrsig`。

### `check_login_status(max_retries=60, interval=3)`
检查二维码的登录状态。

- **参数**:
  - `max_retries` (可选): 最大重试次数，默认值为 `60`。
  - `interval` (可选): 每次检查之间的等待时间（秒），默认值为 `3`。
  
- **返回值**: `dict` - 包含登录状态和信息的字典。
  - 可能的状态值：
    - `"waiting"`: QR 码未失效，用户尚未扫描。
    - `"scanned"`: QR 码已被扫描，正在认证中。
    - `"expired"`: QR 码已失效，用户需重新生成二维码。
    - `"success"`: 登录成功，包含 cookies 信息。
    - `"error"`: 遇到意外的响应。
- **异常**:
  - `ValueError`: 如果 QR 码或 `ptqrtoken` 未初始化。
  - `ConnectionError`: 如果在检查登录状态时发生错误。

### `get_login_user_info()`
获取登录的用户信息。

- **返回值**: `json` - 返回当前登录的 QQ 用户资料，格式为 JSON 对象。
- **异常**:
  - `ConnectionError`: 如果无法获取用户信息，抛出连接错误。
  - `ValueError`: 如果用户未登录。

## 依赖

该项目依赖于以下 Python 包：

- `requests`: 用于进行 HTTP 请求。

## 许可证

该项目采用 MIT 许可证。详细信息请参见 [LICENSE](https://github.com/LibraHp/qlogin/blob/main/LICENSE) 文件。