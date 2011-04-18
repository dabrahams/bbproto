#
# The real configuration goes in this file
#
print '** loading', __file__, 'as', __name__
import submodule
from submodule import main
BuildmasterConfig = {'schedulers':[],'builders':[],'slavePortnum':[],'slaves':[]}
