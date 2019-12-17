from __future__ import print_function
from __future__ import division
import os
import sys
import time
import psana
import numpy as np

NO_PARAM_CALIB_STORE_METHODS_TO_SAVE = ['pedestals', 'gain', 'common_mode']
# will also save mask but pass status=True

def warning(msg):
    sys.stderr.write('WARNING: %s: %s\n' % (os.path.basename(__file__), msg))
    sys.stderr.flush()

def info(msg):
    sys.stdout.write('INFO: %s: %s\n' % (os.path.basename(__file__), msg))
    sys.stdout.flush()

def callDetMethodTakingJustEvent(det, method, evt):
    arr = None
    try:
        arr = getattr(det, method)(evt)
    except AttributeError:
        warning("area det %s doesn't have method %s" % \
                (alias, method))
    return arr

class AliasedSrc(object):
    def __init__(self, src, alias, detector, evtnum):
        self.src=src
        self.alias=alias
        self.detector=detector
        self.evtnum=evtnum
        self.detxface_time = 0
        self.convert_int16_time = 0

class PsanaModuleDetectorXface(object):
    def __init__(self):
        self.raw_freq = self.configInt("raw_freq")
        self.detmethod = self.configStr('detmethod')
        assert self.detmethod in ['image','raw','calib'], \
            'detmethod must be set to image, raw or calib'
        self.convert_to_int16 = self.configBool("convert_to_int16")

    def beginjob(self, evt, env):
        pass
    
    def beginrun(self, evt, env):
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
                                                     detector=det,
                                                     evtnum=-1))
            calib_data_to_save = []
            for method in NO_PARAM_CALIB_STORE_METHODS_TO_SAVE:
                arr = callDetMethodTakingJustEvent(det, method, evt)
                if arr is None:
                    info("method %s for area det %s returned None, not storing" % \
                         (method, alias))
                else:
                    calib_data_to_save.append((arr, method))
            arr = det.mask(evt, status=True)
            if arr is None:
                info("method mask, with status=True for area det %s returned None, not storing" % \
                     alias)
            else:
                calib_data_to_save.append((arr, 'status_mask'))
            
            for arr, nm in calib_data_to_save:
                env.configStore().put(arr, src, '%s:%s' % (alias, nm))

        
    def event(self, evt, env):
        for srd in self.imageDetectorList:
            src, det, alias = srd.src, srd.detector, srd.alias
            t0 = time.time()
            if self.detmethod == 'image':
                arr = det.image(evt)
            elif self.detmethod == 'calib':
                arr = det.calib(evt)
            elif self.detmethod == 'raw':
                arr = det.raw(evt)
            if arr is None and self.detmethod != 'raw':
                raw = det.raw(evt)
                if raw is not None:
                    raise Exception("%s method for detector %s is None, however raw is "
                                    "NOT None. Make sure geometry calibration is "
                                    "deployed for this run" % (detmethod,alias))
            
                continue
            srd.detxface_time += time.time()-t0
            if self.convert_to_int16:
                t0 = time.time()
                arr[arr >= 32767]=32767.0
                arr[arr <= -32768]=-32768.0
                arr = arr.astype(np.int16)
                srd.convert_int16_time += time.time()-t0
            evt.put(arr, src, '%s:image' % alias)
            srd.evtnum += 1
            if (self.raw_freq <= 0) or (srd.evtnum % self.raw_freq != 0):
                evt.put(str(""), src, "src_do_not_translate")

    def endrun(self, evt, env):
        for srd in self.imageDetectorList:
            src, det, alias, totaltime, numevents = \
               srd.src, srd.detector, srd.alias, srd.detxface_time, srd.evtnum
            hz = float(numevents)/totaltime
            print("detetor=%s method=%s timed %.2f hz, %.2f sec (src=%s)" % \
               (alias, self.detmethod, hz, totaltime, src))
            if srd.convert_int16_time > 0:
                print("   convert to int16 at %.2f hz (%.2f sec)" % \
                    (numevents/srd.convert_int16_time, srd.convert_int16_time))
