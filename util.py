"""This module provides utilities."""


def parse_str_queries(queries_str: str) -> dict:
    """str型で与えられるqueryのsetをdictに変換する.

        Example:
            'mkt=ja-jp, offset=10' -> {"mkt":"ja-jp", "offset":10}
        Args:
            queries_str: query set whose type is string.
        Return:
            dict of queries.

    """
    if queries_str == '':
        return {}

    # Remove space and split to pairs of query.
    query_set = queries_str.replace(' ', '').split(',')
    query_dict = {}
    for query in query_set:
        k, v = query.split('=')
        # if positive integer, convert to int
        if v.isdigit():
            v = int(v)
        query_dict[k] = v
    return query_dict


def check_int(s: str) -> bool:
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def extract(input: dict, annotation: str) -> dict:
    """与えられたinput辞書のkeys()でannotation文字列を含むものだけ抽出する.

        整数に変換できる文字列値は文字列に変換する.
    """
    output = {}
    for k, v in input.items():
        if k.find(annotation) > -1:
            k = k.replace(annotation, '')
            v = int(v) if check_int(v) else str(v)
            output[k] = v
    return output
