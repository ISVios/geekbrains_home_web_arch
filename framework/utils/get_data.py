def parse_input_data(data: str) -> dict:
    if not data:
        return {}

    result = {}

    params = data.split("&")
    for item in params:
        k, v = item.split("=")
        result[k] = v

    return result


def get_wsgi_input_data(request: dict) -> bytes:
    content_length_data = request.get("CONTENT_LENGTH")
    content_length = int(content_length_data) if content_length_data else 0
    data = request["wsgi.input"].read(content_length) if content_length > 0 else b""
    return data


def parse_wsgi_input_data(data: bytes) -> dict:
    result = {}
    if data:
        data_str = data.decode(encoding="utf-8")
        result = parse_input_data(data_str)
    return result


def parse_get_method(request) -> dict:
    query_str = request.get("QUERY_STRING")
    if not query_str:
        return {}
    return parse_input_data(query_str)


def parse_post_method(request) -> dict:
    data = get_wsgi_input_data(request)
    return parse_wsgi_input_data(data)


def parse_args_by_method(request: dict, force_method: "str|None" = None) -> dict:
    result = {}

    if not request:
        return result

    # get method
    method = force_method or request.get("REQUEST_METHOD")

    if not method:
        return result

    if method.upper() == "GET":
        result.update(parse_get_method(request))
    elif method.upper() == "POST":
        result.update(parse_post_method(request))
    else:
        raise NotImplemented(f"no realised {method}")

    return result
