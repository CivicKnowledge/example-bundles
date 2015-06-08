'''

'''

from ambry.bundle.loader import ExcelBuildBundle
from ambry.util import memoize

class Bundle(ExcelBuildBundle):
    ''' '''


    @property
    @memoize # cached output of function after first call
    def county_map(self):
        """Return a memoized map of county names to GVIDs"""
        return { r['name'].replace(" County, California",'').lower(): r['gvid'] 
                     for r in  self.library.dep('counties').partition.rows  if int(r['state'] == 6)}


    def mangle_column_name(self, i, n):
        """Alter the column names from the source file"""
        import re
        
        n = re.sub('[\r\n]+',' ',n)

        m = re.match(r'^(P.I) \#(\d+)(.*)$', n)
        
        if not m:
            mangled =  n.lower()
            
        else:
            grp = m.group(1).lower()
            psi_no = m.group(2)
            ind_type = re.sub(r'[\W]+', '_', m.group(3).strip().lower())
            mangled =  "{}_{}_{}".format(grp, psi_no, ind_type)

        if mangled in self.col_map and self.col_map[mangled]['col'] :
            return self.col_map[mangled]['col']
        else:
            return mangled
    
    def build_modify_row(self, row_gen, p, source, row):
        """Looks up the county name to set the GVID"""
        try:
            row['gvid'] =  self.county_map[row['county'].lower()]
        except KeyError:
            pass
