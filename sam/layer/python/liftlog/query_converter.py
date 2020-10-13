from datetime import datetime
from string import Template

# q = {
#     'workout': {
#         'date': {
#             'value': ['2020-10-01', '2020-10-10'],
#             'operator': 'btwn'
#         }
#     },
#     'exercise': {
#         'name': {
#             'value': ['barbell squat', 'barbell deadlift'],
#             'operator': 'or'
#         }
#     },
#     'set': {
#         'weight': {
#             'value': 200,
#             'operator': '>='
#         },
#         'rpe': {
#             'value': 5.0,
#             'operator': ">="
#         }
#     }
# }


class QueryConverter:
    @staticmethod
    def sqlize(value, operator=None, tbl_col=None):
        # tbl_only required when doing a 'btwn' query with a list
        # TODO: remove this param
        formatter = QueryConverter.get_formatter(value)
        formatted_value = formatter(value, operator)

        if not formatted_value:
            raise ValueError(
                "Operator {} not supported for type {}".format(
                    operator, QueryConverter.get_value_type(value)
                )
            )

        if tbl_col:
            return formatted_value.format(TABLE_COL=tbl_col)
        return formatted_value

    @staticmethod
    def get_formatter(value):
        val_type = QueryConverter.get_value_type(value)
        if val_type == "list":
            return QueryConverter.format_list
        elif val_type == "dict":
            return QueryConverter.format_dict
        elif val_type in ["int", "float"]:
            return QueryConverter.format_number
        elif QueryConverter.is_date(value):
            return QueryConverter.format_date
        elif val_type == "str":
            return QueryConverter.format_string

    @staticmethod
    def format_list(items, operator=None):
        # assumes all items in list are of one type
        formatter = QueryConverter.get_formatter(items[0])

        items = [formatter(i) for i in items]

        if operator == "or":
            joined = ", ".join(items)
            return "IN ({})".format(joined)
        elif operator == "btwn":
            return Template(" BETWEEN '$min' AND '$max'").substitute(
                min=items[0], max=items[-1]
            )

    @staticmethod
    def format_dict(item, operator=None):
        raise ValueError("dict values in queries not yet supported")

    @staticmethod
    def format_date(item, operator=None):
        if not operator:
            return item
        return " ".join([operator, item])

    @staticmethod
    def format_string(item, operator=None):
        if not operator:
            return "'{}'".format(item)

        if operator == "=":
            return "= '{}'".format(item)

    @staticmethod
    def format_number(item, operator=None):
        stringified = str(item)
        if not operator:
            return stringified

        return " ".join([operator, stringified])

    @staticmethod
    def get_value_type(value):
        value_type = type(value).__name__
        return value_type

    @staticmethod
    def is_date(string):
        try:
            datetime.strptime(string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        except TypeError:
            return False


# constructs an sql WHERE statement from a provided query
def construct_where(q):
    table_names = [*q]
    parts = []

    for table_name in table_names:
        subqueries = q[table_name]
        for (column, params) in subqueries.items():
            tbl_col = table_name + "." + column
            operator, value = params["operator"], params["value"]
            formatted_val = QueryConverter.sqlize(value, operator, tbl_col)
            parts.append(" ".join([tbl_col, formatted_val]))

    result = "WHERE " + " AND ".join(parts)
    result = result.replace("set", "`set`")  # unfortunate choice of table name
    return result
