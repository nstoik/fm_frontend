"""Simple helper to paginate query."""
from flask import request, url_for

DEFAULT_PAGE_SIZE = 50
DEFAULT_PAGE_NUMBER = 1


def paginate(query, schema):
    """Return all pagination details given a query, schema and request."""
    page = request.args.get("page", DEFAULT_PAGE_NUMBER)
    per_page = request.args.get("page_size", DEFAULT_PAGE_SIZE)
    page_obj = query.paginate(page=page, per_page=per_page)
    next_url = url_for(
        request.endpoint,
        page=page_obj.next_num if page_obj.has_next else page_obj.page,
        per_page=per_page,
        **request.view_args
    )
    prev_url = url_for(
        request.endpoint,
        page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        per_page=per_page,
        **request.view_args
    )
    return {
        "total": page_obj.total,
        "pages": page_obj.pages,
        "next": next_url,
        "prev": prev_url,
        "results": schema.dump(page_obj.items),
    }
