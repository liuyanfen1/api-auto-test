from Common import Request, Assert, Tools
import allure
import pytest
phone=Tools.phone_num()
pwd=Tools.random_str_abc(2)+Tools.random_123(4)
rePwd=pwd
userName=Tools.random_str_abc(3)+Tools.random_123(2)
newPwd=Tools.random_str_abc(3)+Tools.random_123(4)
oldPwd=pwd
reNewPwd=newPwd

request = Request.Request()
assertion = Assert.Assertions()

url='http://192.168.1.137:1811/'
head={}
@allure.feature('注册登录测试')
class Test_logon:
    @allure.story('注册测试')
    def test_signup(self):
        json={"phone": phone,"pwd": pwd,"rePwd": rePwd,"userName": userName}
        signup_resp = request.post_request(url=url + '/user/signup',json=json)
        resp_json = signup_resp.json()
        assertion.assert_code(signup_resp.status_code, 200)
        assertion.assert_in_text(resp_json['respBase'], '成功')
    @allure.story('登录测试')
    def test_login(self):
        login_resp = request.post_request(url=url + 'user/login',json={"pwd": pwd,"userName": userName})
        resp_dict = login_resp.json()
        print(type(resp_dict))
        assertion.assert_code(login_resp.status_code, 200)
        assertion.assert_in_text(resp_dict['respDesc'], '成功')

    @allure.story('修改密码测试')
    def test_update_pwd_login(self):
        update_pwd_resp = request.post_request(url=url + 'user/changepwd',
                                            json={"newPwd": newPwd, "oldPwd": pwd, "reNewPwd": newPwd,
                                                  "userName": userName})
        resp_json = update_pwd_resp.json()
        assertion.assert_code(update_pwd_resp.status_code, 200)
        assertion.assert_in_text(resp_json['respDesc'], '成功')
    @allure.story('验证登录')
    def test_login1(self):
        login1_resp = request.post_request(url=url + 'user/login', json={"pwd": newPwd, "userName": userName})
        resp_dict = login1_resp.json()
        print(type(resp_dict))
        assertion.assert_code(login1_resp.status_code, 200)
        assertion.assert_in_text(resp_dict['respDesc'], '成功')

    @allure.story("冻结用户")
    def test_lock(self):
        lock_resp = request.post_request(url=url + '/user/lock', params={'userName': userName},
                                            headers={'Content-Type': 'application/x-www-form-urlencoded'})

        resp_dict = lock_resp.json()
        assertion.assert_code(lock_resp.status_code, 200)
        assertion.assert_in_text(resp_dict['respDesc'], '成功')

    @allure.story("解冻用户")
    def test_accunlock(self):
        ccunlock_resp = request.post_request(url=url + '/user/unLock', params={'userName': userName},
                                            headers={'Content-Type': 'application/x-www-form-urlencoded'})

        resp_dict = ccunlock_resp.json()
        assertion.assert_code(ccunlock_resp.status_code, 200)
        assertion.assert_in_text(resp_dict['respDesc'], '成功')










