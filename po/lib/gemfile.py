import re


dependency_regex = re.compile('(?i)([-a-z0-9_]+) \((\d.*)\)')


class Gemfile(object):

    def __init__(self, content):
        self.content = content
        self._dependencies = None

    @property
    def dependencies(self):
        if self._dependencies is None:
            self._dependencies = []
            for line in self.content.split('\n'):
                self._parse_dependency(line.strip())
            self._dependencies = filter(None, self._dependencies)
        return self._dependencies

    def _parse_dependency(self, line):
        match = dependency_regex.match(line)
        if match:
            self._dependencies.append(match.groups())
