from pydantic import Field

__all__ = ["page_field", "page_size_field", "cid_field", "sort_fields"]

token = Field(..., title="认证 TOKEN", description="用户用来认证的 token, 登陆的时候获取到的")
token_optional = Field(None, title="认证 TOKEN", description="用户用来认证的 token, 登陆的时候获取到的")

page_field = Field(1, gt=0, title="分页", description="第几页面")
page_size_field = Field(20, ge=10, le=50, title="每页数据条数", description="可自定义 10~50 之间")
cid_field = Field(
    None,
    title="一级商品分类",
    description="""一级商品分类
值为空：全部商品
1：女装
2：母婴
3：美妆
4：居家日用
5：鞋品
6：美食
7：文娱车品
8：数码家电
9：男装
10：内衣
11：箱包
12：配饰
13：户外运动
14：家装家纺
""",
)
sort_fields = Field(
    "new",
    title="商品排序方式",
    description="""
new：按照综合排序\n
total_sale_num_asc：按照总销量从小到大排序\n
total_sale_num_desc：按照总销量从大到小排序\n
sale_num_asc：按照月销量从小到大排序\n
sale_num_desc：按照月销量从大到小排序\n
commission_rate_asc：按照佣金比例从小到大排序\n
commission_rate_desc：按照佣金比例从大到小排序\n
price_asc：按照价格从小到大排序\n
price_desc：按照价格从大到小排序\n
coupon_info_money_asc：按照优惠券金额从小到大排序\n
coupon_info_money_desc：按照优惠券金额从大到小排序\n
shop_level_asc：按照店铺等级从低到高排序\n
shop_level_desc：按照店铺等级从高到低排序\n
tkfee_asc：按照返佣金额从低到高排序\n
tkfee_desc：按照返佣金额从高到低排序\n
code：按照code值从大到小排序\n
date_time：按照更新时间排序\n
random：按照随机排序\n
""",
)

tao_id_field = Field(
    ..., title="淘宝的商品 id", description="都是同一个意思: item_id/num_iid/tao_id"
)
order_type = Field(..., title="订单类型", description="")
