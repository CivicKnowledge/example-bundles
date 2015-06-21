""""""

from ambry.bundle.loader import CsvBundle


class Bundle(CsvBundle):

    """"""

    @staticmethod
    def int_na_caster(v):
        try:
            return int(v)
        except ValueError:
            return None

    def line_mangler(self, source, l):

        return l.replace('\0', '')
