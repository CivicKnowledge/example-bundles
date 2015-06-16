'''
A very simple bundle. 

This is the simplest possible bundle with a build() loop to generate data. Bundles can also be built without a 
build() method, or another methods in the class, by using Sources configuration and a Loader class. See the 
example.com/loader bundle for an example. 

'''

from  ambry.bundle import BuildBundle
 
class Bundle(BuildBundle):
    ''' '''
 
    def __init__(self,directory=None):
        
        super(Bundle, self).__init__(directory)
 
    def build(self):
        import uuid
        import random

        p = self.partitions.new_partition(table="example")
        p.clean()
        
        with p.database.inserter() as ins:
            for i in range(10000):
                
                row = dict(
                   uuid = str(uuid.uuid4()),
                   int = random.randint(0,100),
                   float = random.random()*100
                )    

                ins.insert(row)
                
        p.close()
                
        return True


