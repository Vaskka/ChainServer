# ChainServer后台接口文档
   ## 转账 
   ### a用户发起转账
   #### 功能说明
   a用户发起转账，收款方是b用户
   #### 接口url
   /transfer/?a_user_phone=01234567891&b_user_phone=01234567891&money=123.45
   #### 参数说明
   
   | 参数        | 名字              | 是否必须 | 说明          | 示例                     |
   | :---------- | :--------------- | :------ | :-------------| :----------------------- |
   | a_user_phone | 转账用户的电话号码 | 是      | 代表用户唯一id | &a_user_phone=12345678910|
   | b_user_phone | 收款用户的电话号码 | 是      | 代表用户唯一id | &a_user_phone=12345678910|
   | money       | 转账金额          | 是      | 转账金额       | &money=123.45            |
   
   #### 返回参数
   ```
    {
     "code":0,// 返回值 0 代表成功 1 代表错误或失败
     "msg" : "success", // 信息描述
     "status" : "wait_verify", // 状态
     "a_user_phone" : "12345678910", // 付款方的电话
     "b_user_phone" : "12345678910" // 收款方的电话
    }
   ```
   
   ### 验证完成 
   #### 功能说明
   收款用户完成验证
   #### 接口url
   /complete/?user_phone=01234567891&status=success
   #### 参数说明
   
   | 参数        | 名字              | 是否必须 | 说明           | 示例                     |
   | :---------- | :--------------- | :------ | :------------- | :----------------------- |
   | user_phone  | 转账用户的电话号码 | 是      | 代表用户唯一id  | &user_phone=12345678910  |
   | status      | 状态              | 是      | 验证结果       | &status=fail             |
   
   #### 返回参数
   ```
    {
     "code":0,// 返回值 0 代表成功 1 代表错误或失败
     "msg" : "success", // 信息描述, 错误为Unknown error
     "status" : "hold", // 状态
     "a_user_phone" : "0", // 固定为0
     "b_user_phone" : "0" // 固定为0
    }
   ```
   
   ## 轮询
   ### 功能说明
   指定事件向服务器查询数据
   ### 接口url
   /request/?user_phone=01234567891&status=request
   ### 参数说明
   
   | 参数        | 名字              | 是否必须 | 说明           | 示例                     |
   | :---------- | :--------------- | :------ | :------------- | :----------------------- |
   | user_phone  | 转账用户的电话号码 | 是      | 代表用户唯一id  | &user_phone=12345678910  |
   | status      | 状态              | 是      | 查询状态       | &status=request          |
   
   ### 返回参数
   ```
    {
     "code":0,// 返回值 0 代表成功 1 代表错误或失败
     "msg" : "success", // 信息描述
     "status" : "wait_verify", // 状态 wait_verify表示登待收款方的验证, hold表示正常状态,wait_to_verified表示等待本人验证身份
     "a_user_phone" : "0", // 付款方的电话
     "b_user_phone" : "0" // 收款方的电话
    }
   ```
   特别的，当查询到应该当前用户进行身份验证时
   ```
   {
        'code': 0,
        'msg': 'request for the verify',// 消息内容
        'status': 'wait_to_verified', // 等待当前用户验证
        'a_user_info': {
            'user_phone': a_user_phone, // 转账人信息
            'user_name': a_user_name 
        },
        'money': money // 转账金额
    }
   ```