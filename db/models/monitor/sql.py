# 数据表对应的model对象

from __future__ import annotations
from sqlalchemy import func
from db.engines.mysql import get_session
from db.models.monitor.models import MonitorUrlConfig

monitor_url_config_sort_dict = {"name":MonitorUrlConfig.name}

class MonitorSQL:

    # 资产流量查询列表
    @classmethod
    def list_monitor_url_config_page(cls, query_params, page=1, page_size=10, sort_keys=None, sort_dirs="ascend"):
        session = get_session()
        with session.begin():
            query = session.query(MonitorUrlConfig)
            # 数据库查询参数
            if "name" in query_params and query_params["name"]:
                query = query.filter(MonitorUrlConfig.name.like('%' + query_params["name"] + '%'))
            # 总数
            count = query.count()
            # 排序
            if sort_keys is not None and sort_keys in monitor_url_config_sort_dict:
                if sort_dirs == "ascend" or sort_dirs is None :
                    query = query.order_by(monitor_url_config_sort_dict[sort_keys].asc())
                elif sort_dirs == "descend":
                    query = query.order_by(monitor_url_config_sort_dict[sort_keys].desc())
            else:
                query = query.order_by(MonitorUrlConfig.create_date.desc())
            # 分页条件
            page_size = int(page_size)
            page_num = int(page)
            # 查询所有数据
            if page_size == -1:
                return count, query.all()
            # 页数计算
            start = (page_num - 1) * page_size
            query = query.limit(page_size).offset(start)
            url_list = query.all()
            # 返回
            return count, url_list

