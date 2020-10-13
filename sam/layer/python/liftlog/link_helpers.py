from .sql_helpers import replace_null_sql_values, write_sql
from .sql_queries import ADD_LINK


def add_link(link_url, return_sql=False):
    if not link_url:
        return None

    link = {"link": link_url}
    sql = replace_null_sql_values(ADD_LINK, link)

    if return_sql:
        return sql

    link_id = write_sql(sql, link)

    return link_id