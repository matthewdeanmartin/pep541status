# https://stackoverflow.com/a/34366589/33264
import requests
import json
try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse


URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_version(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json."""
    req = requests.get(url_pattern.format(package=package))
    version = parse('0')
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding))
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version


import urllib.request
import packaging.version
import distutils.version
def alternative_max(package):
    data = json.loads(urllib.request.urlopen('https://pypi.python.org/pypi/{package}}/json').readall().decode('utf-8'))
    max([distutils.version.LooseVersion(release) for release in data['releases'] if not packaging.version.parse(release).is_prerelease])

if __name__ == '__main__':
    print("sqlalchemy==%s" % get_version('sqlalchemy'))
    print("sqlalchemy==%s" % get_version('sqlalchemy'))

