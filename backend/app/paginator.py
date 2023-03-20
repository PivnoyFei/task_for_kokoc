from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from quiz.settings import PAGE


def paginator_obj(request: HttpRequest, object_list: QuerySet) -> Page:
    paginator = Paginator(object_list, PAGE)
    page = request.GET.get('page')

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
