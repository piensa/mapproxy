import re
import datetime
from mapproxy.util.ext.wmsparse.isoformat import fromisoformat

xpath_elem = re.compile('(^|/)([^/]+:)?([^/]+)')
date_time_range = re.compile('(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\dZ)\/(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\dZ)\/PT(\d+)H')

def resolve_ns(xpath, namespaces, default=None):
    """
    Resolve namespaces in xpath to absolute URL as required by etree.
    """
    def repl(match):
        ns = match.group(2)
        if ns:
            abs_ns = namespaces.get(ns[:-1], default)
        else:
            abs_ns = default

        if not abs_ns:
            return '%s%s' % (match.group(1), match.group(3))
        else:
            return '%s{%s}%s' % (match.group(1), abs_ns, match.group(3))

    return xpath_elem.sub(repl, xpath)


def parse_datetime_range(datetime_range_str):
    """
    Only works for Z and PT??H for now.

    For example:
         2020-03-25T12:00:00Z/2020-03-27T00:00:00Z/PT12H
    """
    init_str, end_str, hours = date_time_range.match(datetime_range_str).groups()

    values = [ ]

    init = fromisoformat(init_str)
    end = fromisoformat(end_str)
    delta = datetime.timedelta(hours=int(hours))
    current = init
    while current < (end + delta):
        values.append(current.isoformat().replace('+00:00', 'Z'))
        current = current + delta

    return values
