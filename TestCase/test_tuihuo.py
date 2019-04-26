from Common import Request, Assert,read_excel
import allure
import pytest

request = Request.Request()
assertion = Assert.Assertions()
head={}
idsList=[]
tuihuo_id=0

excel_list = read_excel.read_excel_list('./document/退货原因.xlsx')
length = len(excel_list)
for i in range(length):
    idsList.append(excel_list[i].pop())

url='http://192.168.1.137:8080/'

@allure.feature('退货原因模块')
class Test_tuihuo:
    @allure.story('登录')
    def test_login(self):
        login_resp = request.post_request(url=url + 'admin/login', json={"username": "admin", "password": "123456"})
        resp_text = login_resp.text
        print(type(resp_text))
        resp_dict = login_resp.json()
        print(type(resp_dict))
        assertion.assert_code(login_resp.status_code, 200)
        assertion.assert_in_text(resp_dict['message'], '成功')

        data_dict = resp_dict['data']
        token = data_dict['token']
        tokenHead = data_dict['tokenHead']
        global head
        head = {'Authorization': tokenHead + token}

    @allure.story('查询退货原因')
    def test_sel_tuihuo(self):
        param={'pageNum':'1','pageSize':'5'}
        sel_tuihuo_resp = request.get_request(url=url + 'returnReason/list', params=param, headers=head)
        resp_json = sel_tuihuo_resp.json()

        assertion.assert_code(sel_tuihuo_resp.status_code, 200)
        assertion.assert_in_text(resp_json['message'], '成功')
        json_data = resp_json['data']
        data_list = json_data['list']
        item = data_list[0]
        global tuihuo_id
        tuihuo_id = item['id']

    @allure.story('删除退货数据')
    def test_del_tuihuo(self):

        del_tuihuo_resp = request.post_request(url=url + 'returnReason/delete?ids='+str(tuihuo_id), headers=head)
        resp_json = del_tuihuo_resp.json()

        assertion.assert_code(del_tuihuo_resp.status_code, 200)
        assertion.assert_in_text(resp_json['message'], '成功')

    @allure.story('添加退货原因')
    @pytest.mark.parametrize('name,sort,status,msg',excel_list,ids=idsList)
    def test_add_tuihuo_list(self,name,sort,status,msg):
        json={"name":name,"sort":sort,"status":status}
        add_tuihuo_resp = request.post_request(url=url + 'returnReason/create', json=json,headers=head)
        resp_json = add_tuihuo_resp.json()
        assertion.assert_code(add_tuihuo_resp.status_code, 200)
        assertion.assert_in_text(resp_json['message'], msg)



