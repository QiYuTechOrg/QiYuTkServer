"""
注意:
    logic 里面的代码 所有的地方都可以抛出异常
    但是抛出的异常 必须在 core.exceptions 里面

    这样做主要是为了简化代码
    [如果需要特殊的函数，可以捕获异常自行处理]
"""
from .order_logic import OrderLogic
from .share_logic import ShareLogic
from .sys_logic import SysLogic
from .tao_bao_logic import TaoBaoLogic
from .user_logic import UserLogic
from .user_v2 import UserV2Logic
from .ztk_logic import ZTKLogic
