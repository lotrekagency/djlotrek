from collections import OrderedDict


def group_queryset_by_attribute(queryset, attribute):
    grouped = dict()
    for obj in queryset:
        grouped.setdefault(getattr(obj, attribute), []).append(obj)
    return grouped


def order_dict_from_list(queue, key_order):
    new_queue = OrderedDict()
    for key in key_order:
        new_queue[key] = queue[key]
    return new_queue
