
import sys
import six
import collections.abc
import http.cookies
import urllib.parse
import runpy

# Compatibility aliases for Spyne
sys.modules["spyne.util.six.moves"] = six.moves
sys.modules["spyne.util.six.moves.collections_abc"] = collections.abc
sys.modules["spyne.util.six.moves.http_cookies"] = http.cookies
sys.modules["spyne.util.six.moves.urllib"] = six.moves.urllib
sys.modules["spyne.util.six.moves.urllib.parse"] = urllib.parse

# Run the original source API
runpy.run_path("main.py", run_name="__main__")
