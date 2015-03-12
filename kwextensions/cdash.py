
from urllib import urlencode
from datetime import datetime, timedelta

class StringOp(object):
    CONTAINS = 63
    DOES_NOT_CONTAIN = 64
    IS = 61
    IS_NOT = 62
    STARTS_WITH = 65
    ENDS_WITH = 66

class DateOp(object):
    IS = 81
    IS_NOT = 82
    IS_AFTER = 83
    IS_BEFORE = 84

class Query(object):
    def __init__(self, project, filters=[], filtercombine="and"):
        self.project = project
        self.showfilters = 0
        self.limit = 100
        self.showfeed = 0
        self.__filtercombine = filtercombine
        self.__filters = filters

    def add_filter(self, filter, op="and"):
        if len(self.__filters) != 0 and self.__filtercombine != op:
            raise RuntimeError, "Incompatible filter combination specified (%s != %s)" % (self.__filtercombine, op)
        self.__filtercombine = op
        self.__filters.append(filter)

    def get_query_dict(self):
        query = {}
        query['project'] = self.project
        query['showfilters'] = self.showfilters
        query['limit'] = self.limit
        query['showfeed'] = self.showfeed
        query['filtercount'] = len(self.__filters)
        for i in range(len(self.__filters)):
            idx = i + 1
            field, compare, value = self.__filters[i]
            if isinstance(value, datetime):
                value = value.strftime("%Y%m%d")
            q = { 'field%d' % idx : field,
                  'compare%d' % idx : compare,
                  'value%d' % idx : value
                }
            query.update(q)
        return query

    def get_url(self, root):
        return root + "?" + urlencode(self.get_query_dict())

# print Query("ParaView", filters=[("buildname/string", StringOp.CONTAINS, "superbuild")]).get_url("https://open.cdash.org/index.php")
