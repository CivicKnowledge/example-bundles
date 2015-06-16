""""""

from ambry.bundle.loader import CsvBundle


class Bundle(CsvBundle):

    @staticmethod
    def int_caster(v):
        """Remove 'NA' values from an int column"""
        if isinstance(v,int):
            return v

        if v.strip() == 'NA' :
            return -1
        else:
            return int(v)
       
    @staticmethod
    def real_caster(v):
        """Remove 'NA' values from a float column"""
        if v.strip() == 'NA' :
            return None
        else:
            return float(v)
            
    def build_modify_row(self, row_gen, p, source, row):
        """Make some random changes to the row to demonstrate build_modify_row"""
        import hashlib
        
        partition_name = str(p.identity.name)
        source_url = source.url
        
        if row['int'].strip() != 'NA' :
            row['int'] = int(row['int']) * 2
        
        row['uuid'] =  hashlib.md5(partition_name+source_url+row['id']).hexdigest()
        