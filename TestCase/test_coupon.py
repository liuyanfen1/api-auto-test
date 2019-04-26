# 优惠券模块
from Common import Request, Assert,read_excel
import allure
import pytest

request = Request.Request()
assertion = Assert.Assertions()
head={}
idsList=[]
excel_list = read_excel.read_excel_list('./document/优惠券.xlsx')
length = len(excel_list)
for i in range(length):
    idsList.append(excel_list[i].pop())

url ='http://192.168.1.137:8080/'
item_id = 0
@allure.feature('优惠券模块')
class Test_coupon:
    @allure.story('登录')
    def test_login(self):
        login_resp = request.post_request(url=url + 'admin/login',json={"username": "admin", "password": "123456"})
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

    @allure.story('获取优惠券')
    def test_sel_coupon(self):
        param={'pageNum':'1','pageSize':'10'}
        sel_coupon_resp = request.get_request(url=url + 'coupon/list',params=param, headers=head)
        resp_json= sel_coupon_resp.json()
        json_data = resp_json['data']
        data_list = json_data['list']
        item=data_list[0]
        global item_id
        item_id=item['id']
        assertion.assert_code(sel_coupon_resp.status_code, 200)
        assertion.assert_in_text(resp_json['message'], '成功')

    @allure.story('删除优惠券')
    def test_del_coupon(self):
        del_coupon_resp = request.post_request(url=url + 'coupon/delete/'+str(item_id), headers=head)
        resp_json = del_coupon_resp.json()
        assertion.assert_code(del_coupon_resp.status_code, 200)
        assertion.assert_in_text(resp_json['message'], '成功')

    @allure.story('添加优惠券')
    @pytest.mark.parametrize('name,amount,minPoint,publishCount,msg',excel_list,ids=idsList)
    def test_add_coupon_list(self,name,amount,minPoint,publishCount,msg):
        json={"type":0,"name":name,"platform":0,"amount":amount,"perLimit":1,"minPoint":minPoint,"startTime":'',
              "endTime":'',"useType":0,"note":'',"publishCount":publishCount,"productRelationList":[],
              "productCategoryRelationList":[]}
        add_resp = request.post_request(url=url + 'coupon/create', json=json, headers=head)
        resp_json = add_resp.json()
        assertion.assert_code(add_resp.status_code, 200)
        assertion.assert_in_text(resp_json['message'], msg)





