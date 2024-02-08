from database.request_options import RequestOptions
from database.sqlite.queries import *


class QueryMaker:
    @staticmethod
    def make_query(request_options: RequestOptions) -> str:
        if request_options.operation_type == 'read':
            return QueryMaker._make_select_query(request_options)

    @staticmethod
    def _make_select_query(request_options: RequestOptions) -> str:
        select_from = QueryMaker._make_select_from(request_options)
        where_clause = QueryMaker._make_where_clause(request_options)

        query = select_from + where_clause
        query = query.strip()

        return query

    @staticmethod
    def _make_select_from(request_options: RequestOptions) -> str:
        if request_options.what_to_look_for:
            select_from = SELECT_SPECIFIC.format(
                column_name=request_options.what_to_look_for,
                table_name=request_options.where_to_look
            )
        else:
            select_from = SELECT_ALL.format(
                table_name=request_options.where_to_look
            )

        return select_from

    @staticmethod
    def _make_where_clause(request_options: RequestOptions) -> str:
        if request_options.where_clause:
            if len(request_options.where_clause) > 1:
                QueryMaker._make_multy_request_options(request_options)
            else:
                return QueryMaker._make_single_where_clause(request_options)

    @staticmethod
    def _make_multy_request_options(request_options: RequestOptions) -> str:
        where_clause = ""
        for column, value in request_options.where_clause.items():
            part_of_where_clause = WHERE_CLAUSE.format(column=column, value=value) + AND
            where_clause += part_of_where_clause

        where_clause = QueryMaker._remove_last_and(where_clause)
        return where_clause

    @staticmethod
    def _remove_last_and(where_clause: str) -> str:
        parts = where_clause.rsplit(" AND ", 1)
        result = parts[0] if len(parts) > 1 else where_clause

        return result

    @staticmethod
    def _make_single_where_clause(request_options: RequestOptions) -> str:
        column, value = next(iter(request_options.where_clause.items()))
        where_clause = WHERE_CLAUSE.format(column=column, value=value)
        return where_clause
