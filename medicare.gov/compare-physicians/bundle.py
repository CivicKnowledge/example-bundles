from ambry.bundle.loader import CsvBundle

class Bundle(CsvBundle):

    # The claims_based_hospital_affiliation_ccn_1 column has one entry with a character in it. 
    @staticmethod
    def int_na_caster(v):
        try:
            return int(v)
        except ValueError:
            return None

