from pydantic import Field

nickname = Field(..., title="昵称", description="用户的昵称，展示在用户的主界面")
mobile = Field(None, title="手机号码", description="用户认证使用的手机号码")
token = Field(..., title="认证令牌(TOKEN)", description="其他请求可能需要附带这个认证令牌,保证用户已经登陆")
tao_id = Field(None, title="用户绑定的淘宝ID")
