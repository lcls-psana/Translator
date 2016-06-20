import os
import sys
from collections import namedtuple
import psana
import numpy as np

CALIB_STORE_METHODS_TO_SAVE = ['pedestals', 'gain', 'gain_map']

def warning(msg):
    sys.stderr.write('WARNING: %s: %s\n' % (os.path.basename(__file__), msg))
    sys.stderr.flush()

def info(msg):
    sys.stdout.write('INFO: %s: %s\n' % (os.path.basename(__file__), msg))
    sys.stdout.flush()
    
class PsanaModuleDetectorXface(object):
    def __init__(self):
        pass

    def beginjob(self, evt, env):
        pass
    
    def beginrun(self, evt, env):
        AliasedSrc = namedtuple('AliasedSrc', 'src alias detector')

        amap=env.aliasMap()
        self.imageDetectorList = []
        for src in amap.srcs():
            alias = amap.alias(src)
            if not alias:
                info('src=%s has no alias, skipping' % src)
                continue
            det = psana.Detector(alias, env)
            if not hasattr(det, 'image'):
                info("alias=%s for src=%s does not have a 'image' method, skipping" %
                     (alias, src))
                continue
            info('identified an area detector: alias=%s src=%s' % (alias, src))
            self.imageDetectorList.append(AliasedSrc(src=src,
                                                     alias=amap.alias(src),
                                                     detector=det))
            for method in CALIB_STORE_METHODS_TO_SAVE:
                arr = None
                try:
                    arr = getattr(det, method)(evt)
                except AttributeError:
                    warning("area det %s doesn't have method %s" % \
                            (alias, method))
                    continue
                if arr is None:
                    info("method %s for area det %s returned None, not storing" % \
                         (method, alias))
                    continue
                env.configStore().put(arr, src, '%s:%s' % (alias, method))

        
    def event(self, evt, env):
        for srd in self.imageDetectorList:
            src, det, alias = srd.src, srd.detector, srd.alias
            arr = det.image(evt)
            if arr is None:
                raw = det.raw(evt)
                if raw is not None:
                    raise Exception("image for detector %s is None, however raw is "
                                    "NOT None. Make sure geometry calibration is "
                                    "deployed for this run" % alias)
            
                continue
            evt.put(arr, src, '%s:image' % alias)
