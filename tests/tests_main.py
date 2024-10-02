from qlogin import QLogin

# 创建实例
qlogin = QLogin()

# 获取二维码
qr_code_base64 = qlogin.get_qr_image()

# 检查登录状态
status = qlogin.check_login_status()

print(status)
