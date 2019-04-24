from Common import Request, Assert
import allure
request = Request.Request()
assertion = Assert.Assertions()

url='http://192.168.1.137:8080/'
head={}

@allure.feature("登录功能")
class Test_login:

    @allure.story("登录")
    def test_login(self):

        login_resp = request.post_request(url=url+'admin/login',
                                            json={"username": "admin", "password": "123456"})

        resp_text = login_resp.text
        print(type(resp_text))

        resp_dict = login_resp.json()
        print(type(resp_dict))

        assertion.assert_code(login_resp.status_code,200)
        assertion.assert_in_text(resp_dict['message'],'成功')

        data_dict = resp_dict['data']
        token= data_dict['token']


        tokenHead=data_dict['tokenHead']
        global head
        head={'Authorization':tokenHead+token}

    @allure.story("获取用户信息")
    def test_info(self):
        info_resp = request.get_request(url=url + 'admin/info', headers=head)
        resp_dict=info_resp.json()

        assertion.assert_code(info_resp.status_code,200)
        assertion.assert_in_text(resp_dict['message'],'成功')