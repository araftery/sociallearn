from django.http import HttpResponse
import json as simplejson

def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = simplejson.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = simplejson.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator

def rank_descending(input_list, key):
    """
    Ranks an unordered list of dicts/objects descending based on key. Returns ordered list, with object.rank = rank
    """

    input_list.sort(reverse=True, key=key)
    current_rank = 0
    items_at_rank = 1
    for num, obj in enumerate(input_list):
        if input_list[num-1] and num != 0:
            if key(input_list[num-1]) == key(obj):
                obj.rank = current_rank
                items_at_rank += 1
                continue

        current_rank += items_at_rank
        obj.rank = current_rank
        items_at_rank = 1

    return input_list
