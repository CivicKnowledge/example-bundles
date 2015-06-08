""""""

from ambry.bundle.loader import ExcelBuildBundle
from ambry.util import memoize

class Bundle(ExcelBuildBundle):

    """"""
    
    ##
    ## Casters are methods that cast an incoming value just before it is written into the partition
    ## They are set in the schema.csv file in the d_casters column. 
    @staticmethod
    def int_caster(v):
        """Remove commas from numbers and cast to int"""

        try:
            v = v.replace(',', '').replace('.','').strip()
            
            if not bool(v):
                return None
            
            return int(v)
        except AttributeError:
            return v
            
    @staticmethod
    def real_caster(v):
        """Remove commas and periods from numbers and cast to float"""

        try:
            v = v.replace(',', '')
            
            if not bool(v.replace('.','').strip()):
                return None
            
            return float(v)
        except AttributeError:
            return v
            
    @property
    @memoize # Memoizing caches the output of the function afer the first call. 
    def county_map(self):
        """A Map of county names used in the dataset to GVIDs for counties."""
        return { (int(r['state']), int(r['county'])) : r['gvid'] 
                 for r in  self.library.dep('counties').partition.rows }
            
    def build_modify_row(self, row_gen, p, source, row):
        """Set the time and gvid columns"""
        # If the table has an empty year, and the soruce has a time that converts to an int,
        # set the time as a year.
        if not row.get('year', False) and source.time:
            try:
                row['year'] = int(source.time)
            except ValueError:
                pass
             
        if 'postal_code' in row:
            pass 
            
        row['county_gvid'] =  self.county_map.get((int(row['state_fips']), int(row['county_fips'])), None)
            
            
    def mangle_header(self, header):
        """Transform the header as it comes from the raw row generator into a column name. 
        
        All of the columns for the upper and lower limits of the confidence interval have the same names, 
        so this function appends to the confidence interface columns the name of the closest leftward
        column that is not for a confidence interval. So:
        
            all_ages, 90%_ci_lower_bound, 90%_ci_upper_bound,
            
        becomes:
        
            all_ages, 90%_ci_lower_bound_all_ages, 90%_ci_upper_bound_all_ages,
            
        
        """  
        
        lh = None
        new_header = []
        for i,n in enumerate(header):
            
            if '90' not in n:
                ln = n
            else:
                n = n+'_'+ln
            
            new_header.append(self.mangle_column_name(i, n))
    
        return new_header


