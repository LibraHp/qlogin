import requests
import re
import time
import base64
import json
import random

class QLogin:
    def __init__(self):
        self.appid = '549000912'
        self.daid = '5'
        self.qrsig = None
        self.cookies = None
        self.uin = None
        self.g_tk = None
        self.ptqrtoken = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36'
        }

    @staticmethod
    def _bkn(p_skey: str) -> int:
        """
        Calculate bkn using p_skey.
        :param p_skey: The p_skey from cookies
        :return: The calculated bkn
        """
        t, n, o = 5381, 0, len(p_skey)
        while n < o:
            t += (t << 5) + ord(p_skey[n])
            n += 1
        return t & 2147483647

    @staticmethod
    def _ptqrToken(qrsig: str) -> int:
        """
        Calculate ptqrtoken using qrsig.
        :param qrsig: The qrsig from cookies
        :return: The calculated ptqrtoken
        """
        n, i, e = len(qrsig), 0, 0
        while n > i:
            e += (e << 5) + ord(qrsig[i])
            i += 1
        return e & 2147483647

    def get_qr_image(self) -> str:
        """
        Fetch the QR code image for QQ login and return it as a base64 encoded string.
        :return: The QR code image in base64 format
        """
        url = f'https://ssl.ptlogin2.qq.com/ptqrshow?appid={self.appid}&e=2&l=M&s=3&d=72&v=4&t={time.time()}&daid={self.daid}&pt_3rd_aid=0'
        try:
            r = requests.get(url, headers=self.headers)
            self.qrsig = requests.utils.dict_from_cookiejar(r.cookies).get('qrsig')
            if self.qrsig:
                self.ptqrtoken = self._ptqrToken(self.qrsig)
                # Convert image to base64
                qr_image_base64 = base64.b64encode(r.content).decode('utf-8')
                return qr_image_base64
            else:
                raise ValueError("Failed to retrieve qrsig from the QR code request.")
        except Exception as e:
            raise ConnectionError(f"Failed to retrieve QR code: {e}")

    def check_login_status(self):
        """
        Check the status of the QR code login.
        :return: Dictionary with status and message, and cookies if login is successful
        """
        if not self.qrsig or not self.ptqrtoken:
            raise ValueError("QR code or ptqrtoken not initialized. Please generate QR code first.")

        while True:
            url = f'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone' \
                  f'&ptqrtoken={self.ptqrtoken}&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-' \
                  f'{int(time.time())}&js_ver=20032614&js_type=1&login_sig=&pt_uistyle=40&aid={self.appid}&daid={self.daid}'

            cookies = {'qrsig': self.qrsig}
            try:
                r = requests.get(url, cookies=cookies,headers=self.headers)
                r.encoding = 'utf-8'
                response_text = r.text
                if '二维码未失效' in response_text:
                    return {"status": "waiting", "message": "二维码未失效"}

                elif '二维码认证中' in response_text:
                    return {"status": "scanned", "message": "二维码认证中"}

                elif '二维码已失效' in response_text:
                    return {"status": "expired", "message": "二维码已失效"}

                elif '登录成功' in response_text:
                    cookies = requests.utils.dict_from_cookiejar(r.cookies)
                    uin = cookies.get('uin')
                    sigx = re.search(r'ptsigx=(.*?)&', response_text).group(1)

                    check_sig_url = f'https://ptlogin2.qzone.qq.com/check_sig?pttype=1&uin={uin}&service=ptqrlogin' \
                                    f'&nodirect=0&ptsigx={sigx}&s_url=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone' \
                                    f'&f_url=&ptlang=2052&ptredirect=100&aid={self.appid}&daid={self.daid}'
                    try:
                        r = requests.get(check_sig_url, cookies=cookies, allow_redirects=False, headers=self.headers)
                        final_cookies = requests.utils.dict_from_cookiejar(r.cookies)
                        self.cookies = final_cookies
                        self.uin = re.sub(r'o0*', '', uin)
                        self.g_tk = self._bkn(self.cookies.get('p_skey'))
                        return {"status": "success", "cookies": final_cookies}
                    except Exception as e:
                        raise ConnectionError(f"Failed to retrieve final cookies after successful login: {e}")
                else:
                    return {"status": "error", "message": "Unexpected response during login process"}

            except Exception as e:
                raise ConnectionError(f"Error while checking login status: {e}")

    def get_login_user_info(self):
        """
        Get the user information after login.
        :return: Dictionary with user information or error message.
        """
        if not self.uin or not self.g_tk or not self.cookies:
            raise ValueError("Login information is incomplete. Please ensure login is successful before fetching user info.")

        params = {
            'uin': self.uin,
            'vuin': self.uin,
            'fupdate': '1',
            'rd': random.random(),
            'g_tk': self.g_tk,
        }
        url = 'https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all'
        
        try:
            response = requests.get(url, params=params, cookies=self.cookies, headers=self.headers, timeout=10)
            response.raise_for_status()  # Check for HTTP errors
        except requests.RequestException as e:
            return {"status": "error", "message": f"Network error: {e}"}
        
        try:
            # Parse and clean up the response text safely
            info_text = response.text.strip().lstrip('_Callback(').rstrip(');')
            user_info = json.loads(info_text)
            return {"status": "success", "user_info": user_info}
        except json.JSONDecodeError as e:
            return {"status": "error", "message": f"Failed to parse user info: {e}"}
