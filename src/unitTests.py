from __future__ import print_function
#------------------------------------------------------------------------
# Description:
#   Test script for Translator/H5Output event processing
#   
#------------------------------------------------------------------------


#--------------------------------
#  Imports of standard modules --
#--------------------------------
import sys
import os
import time
import stat
import tempfile
import unittest
import subprocess as sb
import collections
import math
import numpy as np
import six
import glob
#-----------------------------
# Imports for other modules --
#-----------------------------
import psana
import h5py
import psana_test.psanaTestLib as ptl
from psana_test import obj2str
from psana_test.TestOutputDir import outputDir

# -----------------------------
# Test data
# -----------------------------
SIT_ROOT = os.path.expandvars('$SIT_ROOT')
assert SIT_ROOT != '$SIT_ROOT', '$SIT_ROOT is not defined. run sit_setup'
SPLITSCANDATADIR    = os.path.join(ptl.getMultiFileDataDir(), "test_002_xppd9714")
SPLITSCANDATADIRBUG = os.path.join(ptl.getMultiFileDataDir(), "test_006_xppd7114")
NDARRAYADDBLANKDATADIRBUG = os.path.join(ptl.getMultiFileDataDir(), "test_017_xppi0815")
XPPTUTDATADIR=os.path.join(ptl.getMultiFileDataDir(), "test_003_xpptut13")
TESTDATA_T1= os.path.join(ptl.getTestDataDir(), "test_042_Translator_t1.xtc")
TESTDATA_T1_INITIAL_DAMAGE = os.path.join(ptl.getTestDataDir(),"test_046_Translator_t1_initial_damage.xtc")
TESTDATA_T1_END_DAMAGE = os.path.join(ptl.getTestDataDir(),"test_045_Translator_t1_end_damage.xtc")
TESTDATA_T1_NEW_OUTOFORDER = os.path.join(ptl.getTestDataDir(),"test_047_Translator_t1_new_out_of_order.xtc")
TESTDATA_T1_PREVIOUS_OUTOFORDER = os.path.join(ptl.getTestDataDir(),"test_048_Translator_t1_previously_seen_out_of_order.xtc")
TESTDATA_AMO68413_r99_s2 = os.path.join(ptl.getTestDataDir(),"test_041_Translator_amo68413-r99-s02-userEbeamDamage.xtc")
TESTDATA_AMO64913_r182_s2_OUTOFORDER_FRAME = os.path.join(ptl.getTestDataDir(),'test_039_Translator_amo64913-r182-s02-OutOfOrder_Frame.xtc')
TESTDATA_AMO64913_r182_s2_NODAMAGE_DROPPED_OUTOFORDER = os.path.join(ptl.getTestDataDir(),"test_040_Translator_amo64913-r182-s02-noDamage-dropped-OutOfOrder_Frame.xtc")
TESTDATA_XCSCOM12_r52_s0 = os.path.join(ptl.getTestDataDir(),"test_049_Translator_xcscom12-r52-s0-dupTimes-splitEvents.xtc")
TESTDATA_T1_DROPPED_SRC = os.path.join(ptl.getTestDataDir(),"test_044_Translator_t1_dropped_src.xtc")
TESTDATA_T1_DROPPED = os.path.join(ptl.getTestDataDir(),"test_043_Translator_t1_dropped.xtc")
TESTDATA_ALIAS = os.path.join(ptl.getTestDataDir(),"test_050_sxr_sxrb6813_e363-r0069-s00-c00.xtc")
TESTDATA_PARTITION = os.path.join(ptl.getTestDataDir(),"test_051_sxr_sxrdaq10_e19-r057-s01-c00.xtc")
TESTDATA_EPICS = os.path.join(ptl.getTestDataDir(), "test_020_sxr_sxr33211_e103-r0845-s00-c00.xtc")
TESTDATA_CALIBDAMAGE = os.path.join(ptl.getTestDataDir(), "test_080_cxi_cxi83714_e379-r0121-s00-c00_calibdamage.xtc")
TESTDATA_TIMETOOL = os.path.join(ptl.getTestDataDir(), "test_081_xpp_xppi0214_e439-r0054-s00-c00.xtc")
TESTDATA_USDUSB_FEXCONFIGV1 = 'exp=xpp00316:run=384:dir=%s' % os.path.join(ptl.getMultiFileDataDir(),'test_020_xpp00316')
TESTDATA_OCEANOPTICS_DATAV3 = 'exp=xppi6115:run=31:dir=%s' % os.path.join(ptl.getMultiFileDataDir(), 'test_024_xppi6115')
TESTDATA_GENERIC1D_DATAV0 = 'exp=mfxc0116:run=66:dir=%s' % os.path.join(ptl.getMultiFileDataDir(), 'test_019_mfxc0116')

#------------------
# Utility functions / classes
#------------------
def makeMpiTransCmd(min_events_per_calib_file, 
                    num_events_check_done_calib_file, output_h5, dsString, 
                    downstreamModules=None, extraOptions=None, njobs=2, suppressWarnings=True):
    '''Makes a command line that uses mpirun to launch h5-mpi-translate to produce
    the given output file from the given input source. Defaults to use 2 jobs.

    returns the cmd
    '''
    mpiRunCmd = sb.check_output(['which','mpirun']).strip()
    if six.PY3:
        mpiRunCmd = mpiRunCmd.decode()
    assert mpiRunCmd.endswith('mpirun'), "no mpirun command found"

    # add -q since we don't have blt openib on local machines where we test, 
    # creates noise
    transCmd = '%s -q -n %d h5-mpi-translate' % ('mpirun', njobs)
    
    if suppressWarnings:
        transCmd += ' -q -q'

    transCmd += ' -m '
    if downstreamModules is not None:
        assert len(downstreamModules)>0
        transCmd += ','.join(downstreamModules)
        transCmd += ','
    transCmd += 'Translator.H5Output'
    transCmd += ' -o Translator.H5Output.output_file=%s' % output_h5
    transCmd += ' -o Translator.H5Output.overwrite=True'
    transCmd += ' -o Translator.H5Output.min_events_per_calib_file=%d' % min_events_per_calib_file
    transCmd += ' -o Translator.H5Output.num_events_check_done_calib_file=%d' % num_events_check_done_calib_file
    if extraOptions is not None:
        assert len(extraOptions)>0
        for opt in extraOptions:
            transCmd += ' -o %s' % opt
    transCmd += ' %s' % dsString

    return transCmd

class MpiTestHelper(object):
    '''Helper class that takes parameters for running mpi translate on input.
    It runs h5-mpi-translate on the input. Then it checks for errors in psana's output.
    Finally it will optionally dump the h5 and compare it to the xtc.

    When the object is deleted, it removes files if required to. 

    When checking the stderr output of psana, we used to filter out warnings. They
    were filtered out by parsing the stderr of the job, looking for the string 'warning'.
    However when  running 3 jobs, one can have that string be overwritten by the different ranks.
    Now we run with -q -q to suppress warnings. However if verbose=True is specified, you won't 
    see much. So setting verbose=True turns off the -q -q and the stderr check. In short, 
    don't check in a unit test with verbose=True as it won't test for errors.

    After initializing, one can look at:
    
    self.output_h5    # name of translated master h5 file
    self.xtc_dump     # dump of original xtc 
    self.h5_dump      # dump of h5

    self.cleanup()    # remove any of the expected output files, if they exist
    '''
    def __init__(self, outdir, testName, 
                 min_events_per_calib_file,
                 num_events_check_done_calib_file,
                 dataSourceString = 'exp=xppd9714:run=16:dir=%s' % SPLITSCANDATADIR,
                 njobs=2, transCmdTimeOut=3*60, cleanUp=True, verbose=False,
                 doDump=True, downstreamModules=None, extraOptions=None):

        self.output_h5 = outdir.fullpath('unit-test-%s.h5' % testName)
        if doDump:
            self.xtc_dump = outdir.fullpath('unit-test-%s.xtc.dump' % testName)
            self.h5_dump = outdir.fullpath('unit-test-%s.h5.dump' % testName)
        self.doCleanUp = cleanUp
        self.transCmd = \
            makeMpiTransCmd(min_events_per_calib_file = min_events_per_calib_file,
                            num_events_check_done_calib_file = num_events_check_done_calib_file,
                            output_h5 = self.output_h5,
                            dsString = dataSourceString,
                            downstreamModules = downstreamModules,
                            extraOptions = extraOptions,
                            njobs=njobs, suppressWarnings = not verbose)
        if verbose:
            print("------- trans cmd -------")
            print(self.transCmd)

        o,e = ptl.cmdTimeOut(self.transCmd, transCmdTimeOut)

        if verbose:
            print(" ------- trans stdout ------")
            print(o)
            print(" ------- trans stderr ------")
            print(e)
        else:
            eLns = e.split('\n')
            eLns = [ln for ln in eLns if not ptl.filterPsanaStderr(ln)]
            eLns = [ln for ln in eLns if len(ln.strip())>0]
            noWarningLns = []
            for ln in eLns:
                if ln[0:15].lower().find('warning')>=0:
                    continue
                noWarningLns.append(ln)
            assert len(noWarningLns)==0, "error running mpi translation. stderr=%s" % '\n'.join(noWarningLns)

        if doDump:
            cmd,err = ptl.psanaDump(dataSourceString, self.xtc_dump, dumpBeginJobEvt=True, verbose=verbose)
            assert err=='', "something wrong with cmd=%s\nerror:%s" % (cmd,err)

            cmd, err = ptl.psanaDump(self.output_h5, self.h5_dump, verbose=verbose)
            assert err=='', "something wrong with cmd=%s\nerror:%s" % (cmd,err)
        
    def __del__(self):
        if self.doCleanUp:
            self.cleanup()

    def cleanup(self):
        toDelete = [self.output_h5]
        if hasattr(self,'xtc_dump'):
            toDelete.append(self.xtc_dump)
        if hasattr(self,'h5_dump'):
            toDelete.append(self.h5_dump)
        ccPatternA = self.output_h5.replace('.h5','_cc*.h5')
        toDelete.extend(glob.glob(ccPatternA))
        ccFilesDir = self.output_h5.replace('.h5','_ccfiles')
        ccPatternB = os.path.join(ccFilesDir, self.output_h5.replace('.h5','_cc*.h5'))
        toDelete.extend(glob.glob(ccPatternB))
 
        for fname in toDelete:
            if fname is None: continue
            if os.path.exists(fname):
                os.unlink(fname)

        
def makeH5OutputNameFromXtc(outdir, xtcfile):
    xtcbase = os.path.basename(xtcfile)
    h5out = outdir.fullpath(os.path.splitext(xtcbase)[0]) + '.h5'
    assert h5out != xtcfile, "xtcfile ends with .h5, it is %s" % xtcfile
    return h5out

def testDatasetsAgainstExpectedOutput(tester,h5,testList,cmpPlaces=4,verbose=False):
    '''asserts that the specified datasets within the h5 object have the specified values.
    ARGS:
    tester - an instance of unittest.testcase
    h5     - the h5 object, typically as returned by h5py.File
    testList - a list where each entry is as follows:
               (dataset_path, datset_values, message_if_test_fails)
    cmpPlaces - all comparisons are done with almostEquals, pass the number of decimal places
                to compare.
    verbose - set to True to get output for debugging purposes

    for example, if testList is [('/group/datasetA', [(0.1,0),(1.3,2)], 'first dataset'),
                                 ('/group/datasetB',[(0,1,2.1,3),(5,4,5.1,4)], 'second dataset')]
    this function will read h5['/group/datasetA'], test for two rows, and test that the
    first row is within 4 decimal places (or what is passed into cmpPlaces) of (0.1,0), and 
    the second is within 4 decimal places of (1.3,2).  It carries out a similar test for datasetB.
    '''
    for dsname,dsCmpTo,msg in testList:
        ds = h5[dsname]
        if (verbose):
            print("ds: %s" % dsname)
        tester.assertEqual(len(ds),len(dsCmpTo), \
                         msg = "h5 dataset is wrong size.  ds.name=%s, len(ds)=%d len(dsCmpTo)=%d. %s" % (ds.name, len(ds), len(dsCmpTo), msg))
        for row in range(len(dsCmpTo)):
            if verbose:
                print("ds      row=%d: %r" % (row, ds[row]))
                print("dsCmpTo row=%d: %r" % (row, dsCmpTo[row]))
            if ds.dtype and ds.dtype.names:
                for i,fld in enumerate(ds.dtype.names):
                    if (verbose):
                        print("tester.assertAlmostEqual, dsCmpTo[%d][%d]=%r ds[%d][%s]=%r, places=%d" % \
                            (row,i,dsCmpTo[row][i],row,fld,ds[row][fld],cmpPlaces))
                    if fld == 'stamp':
                        tester.assertAlmostEqual(dsCmpTo[row][i][0],ds[row][fld][0],places=cmpPlaces, \
                                           msg="%s, dsname=%s, field is stamp.secsPastEpoch" % (msg,ds.name))
                        tester.assertAlmostEqual(dsCmpTo[row][i][1],ds[row][fld][1],places=cmpPlaces, \
                                           msg="%s, dsname=%s, field is stamp.nsec" % (msg,ds.name))
                    else:
                        a, b = dsCmpTo[row][i], ds[row][fld]
                        if six.PY3 and isinstance(b, bytes):
                            b = b.decode()
                        tester.assertAlmostEqual(a, b,places=cmpPlaces, \
                                                 msg="%s, dsname=%s" % (msg,ds.name))
            else:
                if (verbose):
                    print("tester.assertAlmostEqual, dsCmpTo[%d]=%r ds[%d]=%r, places=%d" % \
                            (row,dsCmpTo[row],row,ds[row],cmpPlaces))
                tester.assertAlmostEqual(dsCmpTo[row],ds[row],places=cmpPlaces, \
                                       msg = "%s, dsname=%s" % (msg,ds.name))

                
def writeCfgFile(input_file, output_h5, moduleList="Translator.H5Output", psanaCfg=''):
    '''Starts to write a psana cfg file.  This is a temporary file.
    Returns the file like object so the user may add more options. This starts to 
    fill out the H5Output module options.
    '''
    cfgfile = tempfile.NamedTemporaryFile(suffix='.cfg',prefix='translator-unit-test', mode='w')
    cfgfile.write("[psana]\n")
    cfgfile.write("modules = %s\n"%moduleList)
    cfgfile.write("files = %s\n" % input_file)
    if len(psanaCfg)>0:
        cfgfile.write("%s\n" % psanaCfg)
    cfgfile.write("[Translator.H5Output]\n")
    cfgfile.write("output_file = %s\n" % output_h5)
    cfgfile.write("overwrite = true\n")
    cfgfile.write("Epics=exclude\n")  # to exclude the epics::ConfigV1, to get things to look 
                                      # more like o2o-translate
    cfgfile.file.flush();
    return cfgfile


#-------------------------------
#  Unit test class definition --
#-------------------------------
class H5Output( unittest.TestCase ) :

    def setUp(self) :
        """ 
        Method called to prepare the test fixture. This is called immediately 
        before calling the test method; any exception raised by this method 
        will be considered an error rather than a test failure.  
        """
        assert os.path.exists(ptl.getTestDataDir()), "Data dir: %s does not exist, cannot run unit tests" % ptl.getTestDataDir()
        self.outdir = outputDir('trnut')
        
        self.cleanUp = True      # Several tests run psana to produce .h5 files.  
                                 # If cleanup is True the files are deleted when
                                 # the test is done.

        self.printPsanaOutput = False # if True, when a psana test  will write
                                      # it's output.  It will also call h5ls -r on
                                      # on the h5 file created.
    def tearDown(self) :
        """
        Method called immediately after the test method has been called and 
        the result recorded. This is called even if the test method raised 
        an exception, so the implementation in subclasses may need to be 
        particularly careful about checking internal state. Any exception raised 
        by this method will be considered an error rather than a test failure. 
        This method will only be called if the setUp() succeeds, regardless 
        of the outcome of the test method. 
        """
        pass

    def runPsanaOnCfg(self,cfgfile,output_h5=None,extraOpts='',printPsanaOutput=False, errorCheck=True):
        '''Runs psana on the given cfgfile and tests output for errors.
        Optionally specify an output hdf5 file. If the hdf5 file is given, this functions
        deletes the file if it already exists and tests to make sure that is was
        created after the psana run.

        extraOpts are passed to psana on the command line.
        
        tests that output_h5 is created.

        If errorCheck is True it tests that psana output does not include: fatal, error,
                        segmentation fault, seg falut, traceback

        '''
        if output_h5 is not None and os.path.exists(output_h5):
            os.unlink(output_h5)
            time.sleep(.3)
        cfgfile.flush()
        assert isinstance(extraOpts,str), "extraOpts for psana command line is %r, not a str" % extraOpts
        psana_cmd = "psana %s -c %s" % (extraOpts,cfgfile.name)
        p = sb.Popen(psana_cmd,shell=True,stdout=sb.PIPE, stderr=sb.PIPE)
        o,e = p.communicate()
        if six.PY3:
            o = o.decode()
            e = e.decode()
        if (output_h5 is not None) and (not os.path.exists(output_h5)):
            print("### h5 file was not created. cfg file: ###")
            print(file(cfgfile.name).read())
            print("### psana output: ###")
            print(o)
            print(e)
        if (output_h5 is not None):
            self.assertTrue(os.path.exists(output_h5),msg="h5 output file: %s not produced" % output_h5)
        allOutPut = o+'\n'+e
        if printPsanaOutput:
            print(allOutPut)
            sys.stdout.flush()
            if (output_h5 is not None):
                print("*** Running h5ls -r on output_h5 (%s)"% output_h5)
                os.system('h5ls -r %s | grep -v -i epics' % output_h5)
        if not errorCheck:
            return allOutPut
        lowerOutput = allOutPut.lower()
        self.checkOutputForErrors(lowerOutput)

    def checkOutputForErrors(self, lowerOutput):
        self.assertEqual(lowerOutput.find('fatal'),-1,msg="'fatal' found in psana output: ... %s ..." % lowerOutput[lowerOutput.find('fatal')-100:lowerOutput.find('fatal')+100])
        self.assertEqual(lowerOutput.find('error'),-1,msg="'error' found in psana output: ... %s ..."  % lowerOutput[lowerOutput.find('error')-100:lowerOutput.find('error')+100])
        self.assertEqual(lowerOutput.find('segmentation fault'),-1,msg="'segmentation fault' found in psana output: ... %s ..." % lowerOutput[lowerOutput.find('segmentation fault')-100:lowerOutput.find('segmentation fault')+100])
        self.assertEqual(lowerOutput.find('seg fault'),-1,msg="'seg fault' found in psana output: ... %s ..." % lowerOutput[lowerOutput.find('seg fault')-100:lowerOutput.find('seg fault')+100])
        self.assertEqual(lowerOutput.find('traceback'),-1,msg="'traceback' found in psana output: ... %s ..." % lowerOutput[lowerOutput.find('traceback')-100:lowerOutput.find('traceback')+100])

    def test_t1_initial_damage(self):
        '''check for initial blanks.
        The input file is a modified version of t1.xtc.
        Damage has been introduced for the first of the two Ipimb::Data types
        coming from the XppSb3_Ipm source.  Hence we should get a blank starting
        that dataset.  This will test the initial_blank logic of 
        H5Output::Event and TypeSrcKeyDirectory.
        '''
        input_file = TESTDATA_T1_INITIAL_DAMAGE
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir, input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            h5 = h5py.File(output_h5,'r')

            eventIds = [(1364147551, 107587445, 331318, 118410, 140, 0), 
                        (1364147551, 174323092, 331570, 118434, 12, 6)]
            blankDamage = [(4, 0, 0, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 0)]
            nonBlankDamage = [(0, 0, 0, 0, 0, 0, 0),
                              (0, 0, 0, 0, 0, 0, 0)]
            blankMask = [0,1]
            nonBlankMask = [1,1]
            blankData = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
                        (4369, 0, 31250, 65486, 65535, 65324, 65447, 42142, 41839, 42184, 42083, 42042, 4.99626, 5, 4.9839, 4.99329, 3.21523, 3.19211, 3.21843, 3.21073, 18135826)]
            nonBlankData = [(4369, 0, 31250, 65525, 65522, 65517, 65532, 41975, 41984, 41949, 41903, 44883, 4.99924, 4.99901, 4.99863, 4.99977, 3.20249, 3.20317, 3.2005, 3.19699, 18135819),
                            (4369, 0, 31250, 65462, 65483, 65523, 65508, 42069, 42050, 41978, 41927, 47071, 4.99443, 4.99603, 4.99908, 4.99794, 3.20966, 3.20821, 3.20272, 3.19883, 18135827)]

            testList = [('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/data', blankData, "data dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/_damage', blankDamage, "damage dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/time', eventIds, "time dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/_mask', blankMask, "mask dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/data', nonBlankData, "data dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/_damage', nonBlankDamage, "damage dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/time', eventIds, "time dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/_mask', nonBlankMask, "mask dataset with non blank")]
            testDatasetsAgainstExpectedOutput(self,h5,testList,cmpPlaces=4)

            if self.cleanUp:
                h5.close()
                os.unlink(output_h5)

    def test_t1_end_damage(self):
        '''Check for blanks at the end of the datasets.
        The input file is a modified version of t1.xtc.
        Damage has been introduced at the end of the Ipimb::Data types
        coming from the XppSb3_Ipm source.  Hence we should get a blank at the end
        of that dataset. 
        '''
        input_file = TESTDATA_T1_END_DAMAGE
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir, input_file)

            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            h5 = h5py.File(output_h5,'r')

            eventIds = [(1364147551, 107587445, 331318, 118410, 140, 0), 
                        (1364147551, 174323092, 331570, 118434, 12, 6)]
            blankDamage = [(0, 0, 0, 0, 0, 0, 0),
                           (4, 0, 0, 0, 0, 0, 0)]
            nonBlankDamage = [(0, 0, 0, 0, 0, 0, 0),
                              (0, 0, 0, 0, 0, 0, 0)]
            blankMask = [1,0]
            nonBlankMask = [1,1]
            blankData = [(4369, 0, 31250, 65535, 65535, 65535, 65535, 42105, 41813, 42024, 42019, 26799, 5, 5, 5, 5, 3.21241, 3.19013, 3.20623, 3.20584, 18135818),
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
            nonBlankData = [(4369, 0, 31250, 65525, 65522, 65517, 65532, 41975, 41984, 41949, 41903, 44883, 4.99924, 4.99901, 4.99863, 4.99977, 3.20249, 3.20317, 3.2005, 3.19699, 18135819),
                            (4369, 0, 31250, 65462, 65483, 65523, 65508, 42069, 42050, 41978, 41927, 47071, 4.99443, 4.99603, 4.99908, 4.99794, 3.20966, 3.20821, 3.20272, 3.19883, 18135827)]

            testList = [('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/data', blankData, "data dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/_damage', blankDamage, "damage dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/time', eventIds, "time dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/_mask', blankMask, "mask dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/data', nonBlankData, "data dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/_damage', nonBlankDamage, "damage dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/time', eventIds, "time dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/_mask', nonBlankMask, "mask dataset with non blank")]

            testDatasetsAgainstExpectedOutput(self,h5,testList,cmpPlaces=4)

            if self.cleanUp:
                h5.close()
                os.unlink(output_h5)

    def test_t1_new_outoforder(self):
        '''Check for proper handling of outoforder damage.
        The input file is a modified version of t1.xtc. If has out of order damage for the
        second event for ipimb data from sb32.
        '''
        input_file = TESTDATA_T1_NEW_OUTOFORDER
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir, input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            h5 = h5py.File(output_h5,'r')
            eventIds = [(1364147551, 107587445, 331318, 118410, 140, 0), 
                        (1364147551, 174323092, 331570, 118434, 12, 6)]
            blankDamage = [(0, 0, 0, 0, 0, 0, 0),
                           (4096, 0, 1, 0, 0, 0, 0)]
            nonBlankDamage = [(0, 0, 0, 0, 0, 0, 0),
                              (0, 0, 0, 0, 0, 0, 0)]
            blankMask = [1,0]
            nonBlankMask = [1,1]
            nonBlankData = [(4369, 0, 31250, 65535, 65535, 65535, 65535, 42105, 41813, 42024, 42019, 26799, 5, 5, 5, 5, 3.21241, 3.19013, 3.20623, 3.20584, 18135818),
                            (4369, 0, 31250, 65486, 65535, 65324, 65447, 42142, 41839, 42184, 42083, 42042, 4.99626, 5, 4.9839, 4.99329, 3.21523, 3.19211, 3.21843, 3.21073, 18135826) ]
            blankData = [(4369, 0, 31250, 65525, 65522, 65517, 65532, 41975, 41984, 41949, 41903, 44883, 4.99924, 4.99901, 4.99863, 4.99977, 3.20249, 3.20317, 3.2005, 3.19699, 18135819),
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]

            testList = [('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/data', blankData, "data dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/_damage', blankDamage, "damage dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/time', eventIds, "time dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/_mask', blankMask, "mask dataset with blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/data', nonBlankData, "data dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/_damage', nonBlankDamage, "damage dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/time', eventIds, "time dataset with non blank"),
                        ('Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/_mask', nonBlankMask, "mask dataset with non blank")]

            testDatasetsAgainstExpectedOutput(self,h5,testList,cmpPlaces=4)
            if self.cleanUp:
                h5.close()
                os.unlink(output_h5)

    def test_t1_previously_seen_out_of_order(self):
        '''check for proper damage handling.
        The input file is a modified version of t1.xtc. There are two L1Accept datagrams with the
        same time.  The first one has damage, and the second one says out of order.

        The datagrams:

        dg=    5 offset=0x0000FE98 tp=Event sv=       L1Accept ex=1 ev=1 sec=514F3D5F nano=0669A775 tcks=0050E36 fid=1CE8A ctrl=8C vec=0000 env=00000003
        dg=    6 offset=0x0001327C tp=Event sv=       L1Accept ex=0 ev=1 sec=514F3D5F nano=0669A775 tcks=0050F32 fid=1CEA2 ctrl=0C vec=0006 env=00000003
        
        The ipimb data is dg5:
        offset=0FED4 extent=034 dmg=00004 src=06003D77,00000025,level=6 typeid=22 vrn=2 val=20016 type_name=IpimbData
        offset=0FFD4 extent=034 dmg=00005 src=06003D77,00000024,level=6 typeid=22 vrn=2 val=20016 type_name=IpimbData
        
        In dg6:
        offset=132F0 extent=034 dmg=01000 src=06003D77,00000025,level=6 typeid=22 vrn=2 val=20016 type_name=IpimbData
        offset=133F0 extent=034 dmg=01000 src=06003D77,00000024,level=6 typeid=22 vrn=2 val=20016 type_name=IpimbData

        psana appears to sort the datagrams so that we get dg6 before dg5.

        Since every entry is blank, the psana Translator never gets a chance to write the blanks.
        What it produces is the time, _damage and _mask datasets, but it does not write the
        data datasets.
        '''
        input_file = TESTDATA_T1_PREVIOUS_OUTOFORDER
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir, input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            h5 = h5py.File(output_h5,'r')
            sec = 1364147551
            nano = 107587445
            timeSb2 = h5['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/time']
            timeSb3 = h5['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/time']
            self.assertEqual(len(timeSb2),2,"should be two entries in ipimb data time")
            self.assertEqual(len(timeSb3),2,"should be two entries in ipimb data time")
            self.assertEqual(timeSb2['seconds'][0],sec)
            self.assertEqual(timeSb3['seconds'][0],sec)
            self.assertEqual(timeSb2['nanoseconds'][0],nano)
            self.assertEqual(timeSb3['nanoseconds'][0],nano)
            maskSb2 = h5['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm/_mask']
            maskSb3 = h5['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/_mask']
            self.assertEqual(len(maskSb2),2,"should be two entries in ipimb data mask")
            self.assertEqual(len(maskSb3),2,"should be two entries in ipimb data mask")
            self.assertTrue((maskSb2[...]==np.zeros(2)).all())
            self.assertTrue((maskSb3[...]==np.zeros(2)).all())
            self.assertFalse('data' in list(h5['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb2_Ipm'].keys()),msg="should not have a 'data' dataset for ipimb")
            self.assertFalse('data' in list(h5['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm'].keys()),msg="should not have a 'data' dataset for ipimb")
            if self.cleanUp:
                h5.close()
                os.unlink(output_h5)

    def test_userEBeamDamage(self):
        '''Runs the translator on a file that has EBeam user defined damage. 
        The input file, data/Translator/amo68413-r99-s02-userEbeamDamage.xtc,
        was obtained by taking a mix of datagrams from different chunks of 
        amo68413 r0099 s02.  
        The only damage in the file is dgram 5, and L1Accept, with 
        xtc d=2  offset=0x00033854 extent=00000068 dmg=04000 src=06000000,00000000,level=6 typeid=15 version=3 value=3000F compressed=0 compressed_version=3 type_name=EBeamBld
        The 
        xdmg=04000The first 5 datagrams from cover the damage.  The next two get the end
        of the calibcyle, and then we go into chunk 03 to get the end of the run.

        That is we put the stared datagrams from the list below, s is the sequence,
        c the chunk, dg the datagram number (1-up).
        
        * s=2 c=0 dg=    1 offset=0x00000000 tp=Event sv=      Configure ex=1 ev=0 sec=510EE016 nano=069CA483 tcks=0000000 fid=1FFFF ctrl=84 vec=0000 env=000007A2
        * s=2 c=0 dg=    2 offset=0x0000C2F0 tp=Event sv=       BeginRun ex=0 ev=0 sec=510EE332 nano=16D0CC0D tcks=0000000 fid=1FFFF ctrl=06 vec=0000 env=00000063
        * s=2 c=0 dg=    3 offset=0x0000C37C tp=Event sv=BeginCalibCycle ex=0 ev=0 sec=510EE332 nano=217CB9C0 tcks=0000000 fid=1FFFF ctrl=08 vec=0000 env=00000000
        * s=2 c=0 dg=    4 offset=0x0000C5D4 tp=Event sv=         Enable ex=0 ev=0 sec=510EE332 nano=2510C571 tcks=0000000 fid=1FFFF ctrl=0A vec=0000 env=800007D0
        * s=2 c=0 dg=    5 offset=0x0000C660 tp=Event sv=       L1Accept ex=1 ev=1 sec=510EE332 nano=2A2C740E tcks=00508A0 fid=11670 ctrl=8C vec=40CD env=00000003
          s=2 c=0 dg=    6 offset=0x00233A74 tp=Event sv=       L1Accept ex=1 ev=1 sec=510EE332 nano=2AAB8F9C tcks=005077A fid=11673 ctrl=8C vec=40CE env=00000003
        * s=2 c=0 dg= 2008 offset=0x10C853038 tp=Event sv=        Disable ex=0 ev=0 sec=510EE343 nano=29E1CCFD tcks=0000000 fid=1FFFF ctrl=0B vec=0000 env=00000000
        * s=2 c=0 dg= 2009 offset=0x10C8530C4 tp=Event sv=  EndCalibCycle ex=0 ev=0 sec=510EE343 nano=2C442175 tcks=0000000 fid=1FFFF ctrl=09 vec=0000 env=00000000
          s=2 c=0 dg= 2010 offset=0x10C853150 tp=Event sv=BeginCalibCycle ex=0 ev=0 sec=510EE343 nano=36576935 tcks=0000000 fid=1FFFF ctrl=08 vec=0000 env=00000000
          s0  c=3 dg=16053 offset=0x864011A14 tp=Event sv=       L1Accept ex=1 ev=1 sec=510EE5F9 nano=0115D1F4 tcks=0050F3E fid=0FDBC ctrl=8C vec=0197 env=00000003
        * s0  c=3 dg=16054 offset=0x864236B60 tp=Event sv=        Disable ex=0 ev=0 sec=510EE5F9 nano=14211335 tcks=0000000 fid=1FFFF ctrl=0B vec=0000 env=00000000
        * s0  c=3 dg=16055 offset=0x864236BEC tp=Event sv=  EndCalibCycle ex=0 ev=0 sec=510EE5F9 nano=171C0FDA tcks=0000000 fid=1FFFF ctrl=09 vec=0000 env=00000000
        * s0  c=3 dg=16056 offset=0x864236C78 tp=Event sv=         EndRun ex=0 ev=0 sec=510EE5F9 nano=1A16F021 tcks=0000000 fid=1FFFF ctrl=07 vec=0000 env=00000000

        This test revealed some differences in epics.  First o2o-translate records the
        epics source, and they come from two places in this xtc file:  
           EpicsArch.0:NoDevice.0.  and AmoVMI.0:Opal1000.0
        Translator.H5Output puts everything in EpicsArch.0:NoDevice.0
        We also find that there are several aliases that o2o writes that psana does not:
        
        piezo timing delay _ width-AMO:R14:EVR:21:CTRL.DG2W              we skipped because it has an empty target
        mirror bendersreg_g_pcds_package_epics_3.14-dev_screens_edm_amo  we skipped because it has an empty target
        piezo timing delay _ width                                       we skipped because it has an empty target
        AMO:R14:IOC:10:ao0:out1                                          we skipped because it was in the group list
        
        This file revealed a bug in o2o-translate, it was creating a group for AMO:R14:IOC:10:ao0:out1 that is
        wrong.

        In this test, we'll make sure AMO:R14:IOC:10:ao0:out1 has the correct data, as well as that 
        the user damaged ebeam data is present. psana has a switch to not store damaged user ebeam, but
        by default it is on, so it should be stored.
        '''
        input_file = TESTDATA_AMO68413_r99_s2
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir, input_file)
            cfgfile = writeCfgFile(input_file,output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5)
            cfgfile.close()
            f = h5py.File(output_h5,'r')
            testList = [('/Configure:0000/Run:0000/CalibCycle:0000/Bld::BldDataEBeamV3/EBeam/_damage',
                         [(0x4000,0,0,0,1,0,0)], 'ebeam damage'),
                        ('/Configure:0000/Run:0000/CalibCycle:0000/Bld::BldDataEBeamV3/EBeam/_mask',
                         [(1,)], 'ebeam mask'),
                        ('/Configure:0000/Run:0000/CalibCycle:0000/Bld::BldDataEBeamV3/EBeam/data',
                         [(256, 0.019605993696, 4813.759084237167, -0.21048433685050208, 0.008341444963823323, 0.032870595392491646, 0.0634931790398521, 15285.3740234375, 0.4098030626773834, 56.18963623046875, -0.2480001449584961)],
                         'ebeam data'),
                        ('/Configure:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/AMO:R14:IOC:10:VHS0:CH0:VoltageMeasure/data',
                         [ (44, 34, 1, 'AMO:R14:IOC:10:VHS0:CH0:VoltageMeasure', 5, 2, 3, 'V', 5000.0, 0.0, 5000.0, 5000.0, 0.0, 0.0, 5000.0, 0.0, 0.0)],
                         'config epics amo:r14:0c:10:vhs0:ch0:voltage measure'),
                        ('/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/AMO:R14:IOC:10:VHS0:CH0:VoltageMeasure/data',
                         [(44, 20, 1, 5, 2, (728768506, 940000000), 0.0)],
                         'config epics amo:r14:0c:10:vhs0:ch0:voltage measure')]

            testDatasetsAgainstExpectedOutput(self,f,testList)
            if self.cleanUp:
                f.close()
                os.unlink(output_h5)

    def test_outOfOrderFrame(self):
        '''Test proper damage handling. This file has
        dg1=config, dg2=beginRun, dg3=beginCalib, dg4=Enable
        dg5=L1Accept with:  sec=5159D9BB nano=37A715E2
          xtc extent=00000014 dmg=00002 src=01003A03,17010300,level=1 typeid= 0 version=0 value=00000 type_name=Any
        dg6=L1Accept with:  sec=5159D9BB nano=38A560D4
          xtc extent=00200024 dmg=01000 src=01003A03,17010300,level=1 typeid= 2 version=1 value=10002 type_name=Frame compressed=0 compressed_version=1 
        dg7=L1Accept with   sec=5159D9BB nano=39A38A8B 
          xtc extent=00200024 dmg=01000 src=01003A03,17010300,level=1 typeid= 2 version=1 value=10002 type_name=Frame compressed=0 compressed_version=1 

        Although we could keep track of the initial damage to an Any type at the given src, we presently do not.  
        initial damage to known types we do keep track of, but here we only know the src. When we see damage
        for sources where we have already seen data, we try to do more. So this data will
        produce a mis-aligned dataset with only two entries (both damaged).  Moreover, we will not 
        write the data dataset since we never see valid data for Frame.  

        If we find this kind of damage - src only in the inital datagrams - is happening, we could
        work on aligning this kind of dataset.
        '''
        input_file = TESTDATA_AMO64913_r182_s2_OUTOFORDER_FRAME
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir, input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            h5 = h5py.File(output_h5,'r')
            gr = h5["/Configure:0000/Run:0000/CalibCycle:0000/Camera::FrameV1/AmoEndstation.1:Opal1000.0"]
            self.assertEqual(set(gr.keys()),set(['time','_damage','_mask']))
            frameDamage = gr["_damage"]
            frameMask = gr["_mask"]
            self.assertEqual(len(frameDamage),2)
            self.assertEqual(len(frameMask),2)
            self.assertTrue((frameMask[...]==np.zeros(2)).all())
            self.assertEqual(frameDamage['bits'][0],4096)
            self.assertEqual(frameDamage['bits'][1],4096)
            self.assertEqual(frameDamage['OutOfOrder'][0],1)
            self.assertEqual(frameDamage['OutOfOrder'][1],1)
            if self.cleanUp:
                h5.close()
                os.unlink(output_h5)

    def test_noDamageDroppedOutOfOrder(self):
        '''Check proper damage handling. This file has
        dg1=config, dg2=beginRun, dg3=beginCalib, dg4=Enable
        dg5=L1Accept with:  sec=5159D9BB nano=36A8E830
          xtc extent=00200024 dmg=00000 src=01003A03,17010300, typeid= 2 type_name=Frame
        dg6=L1Accept with:  sec=5159D9BB nano=37A715E2 
          xtc extent=00000014 dmg=00002 src=01003A03,17010300, typeid= 0 type_name=Any
        dg7=L1Accept with:  sec=5159D9BB nano=38A560D4 
          xtc extent=00200024 dmg=01000 src=01003A03,17010300, typeid= 2 type_name=Frame
        dg8=L1Accept with:  sec=5159D9BB nano=39A38A8B
          xtc extent=00200024 dmg=01000 src=01003A03,17010300, typeid= 2 type_name=Frame

        Since we have seen the data from the dropped src with the Any xtc, we sould put a 
        blank in there.  So we should get a dataset of 4 here, with a mask of 1 0 0 0 
        '''
        input_file = TESTDATA_AMO64913_r182_s2_NODAMAGE_DROPPED_OUTOFORDER
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir, input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            h5 = h5py.File(output_h5,'r')
            gr = h5["/Configure:0000/Run:0000/CalibCycle:0000/Camera::FrameV1/AmoEndstation.1:Opal1000.0"]
            self.assertEqual(set(gr.keys()),set(['time','_damage','_mask', 'data','image']))
            damage = gr["_damage"]
            mask = gr["_mask"]
            self.assertEqual(len(damage),4)
            self.assertEqual(len(mask),4)
            self.assertTrue((mask[...]==np.array([1,0,0,0])).all())
            if self.cleanUp:
                h5.close()
                os.unlink(output_h5)
        
    def test_dupTimesSplitEvents(self):
        '''Check that we run without on error on file with split events.
        TODO: check for proper handling of split events.
        This file contains several pairs of datagrams with the same timestamps:
        dg=    8 sec=4F540ABB nano=0A5FC451  xtc dmg=00002 src=02001038,AC151974, type_name=Any
        dg=   11 sec=4F540ABB nano=0A5FC451  all xtc dmg=00002

        dg=    9 sec=4F540ABB nano=0D5B5A93 xtc dmg=00002 src=02001038,AC151974, type_name=Any
        dg=   14 sec=4F540ABB nano=0D5B5A93 all xtc dmg=00002

        dg=   10 sec=4F540ABB nano=1056D6A7 xtc dmg=00002 src=02001038,AC151974, type_name=Any
        dg=   15 sec=4F540ABB nano=1056D6A7 all xtc dmg=00002

        dg=   12 sec=4F540ABB nano=1352778B xtc dmg=00002 src=02001038,AC151974, type_name=Any
        dg=   16 sec=4F540ABB nano=1352778B all xtc dmg=00002

        dg=   13 sec=4F540ABB nano=164DEBBF xtc dmg=00002 src=02001038,AC151974, type_name=Any
        dg=   17 sec=4F540ABB nano=164DEBBF all xtc, smg=00002
        '''
        input_file = TESTDATA_XCSCOM12_r52_s0
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir,input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            if self.cleanUp:
                os.unlink(output_h5)

    def test_t1_dropped_src(self):
        '''Check that we run successful on this xtc file with damage.
        '''
        input_file = TESTDATA_T1_DROPPED_SRC
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir,input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            if self.cleanUp:
                os.unlink(output_h5)
        
    def test_t1_dropped(self):
        '''Check that we run successful on this xtc file with damage.
        '''
        input_file = TESTDATA_T1_DROPPED
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir,input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            if self.cleanUp:
                os.unlink(output_h5)

    def test_doNotTranslate_addKey(self):
        '''Test doNotTranslate with a key string like "mytest:do_not_translate"
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = self.outdir.fullpath('unit-test_doNotTranslate_addKey.h5')
            cfgfile = writeCfgFile(input_file,output_h5,"Translator.TestModuleDoNotTranslate Translator.H5Output")
            cfgfile.write("[Translator.TestModuleDoNotTranslate]\n")
            cfgfile.write("skip=0 1\n")
            msg0='message0'
            msg1='message1thisIsALongerMessage'
            cfgfile.write("messages=%s %s\n"% (msg0, msg1))
            cfgfile.write("key=mytest\n");
            cfgfile.file.flush()
            try:
                self.runPsanaOnCfg(cfgfile,output_h5)
            except:
                cfgfile.close()
                if os.path.exists(output_h5):
                    os.unlink(output_h5)
                raise
            f=h5py.File(output_h5,'r')
            # make sure event data is not present:
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/EvrData::DataV3']


            if self.cleanUp:
                f.close()
                os.unlink(output_h5)
        
    def test_chunks(self):
        '''make sure that ndarray ndarrayChunkSizeTargetObjects option works
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir,input_file).replace('.h5','_test_chunks.h5')
            cfgfile = writeCfgFile(input_file, output_h5, moduleList = "Translator.testModuleForNDarray Translator.H5Output")
            cfgfile.write('src_filter = exclude BldInfo(XppSb2_Ipm)\n')
            cfgfile.write('deflate = -1\n')
            cfgfile.write('shuffle = 0\n')
            cfgfile.write('ndarrayChunkSizeTargetObjects = 1\n')
            cfgfile.write('chunkSizeTargetObjects = 2\n')
            cfgfile.write('useControlData = 0\n')
            cfgfile.write('minObjectsPerChunk = 1\n')
            cfgfile.write('[Translator.testModuleForNDarray]\n')
            cfgfile.write('add_to_event_src = BldInfo(XppSb2_Ipm)\n')
            cfgfile.write('add_to_event_key = array\n')

            self.runPsanaOnCfg(cfgfile,output_h5, extraOpts='', printPsanaOutput=self.printPsanaOutput)        

            f = h5py.File(output_h5,'r')
            arrayDs=f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float64_2/XppSb2_Ipm__array/data']
            psanaDs = f['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2/XppSb3_Ipm/data']
            self.assertFalse(arrayDs.shuffle)
            self.assertFalse(psanaDs.shuffle)
            self.assertEqual(psanaDs.chunks[0],2)
            self.assertEqual(arrayDs.chunks[0],1)

            if self.cleanUp:
                f.close()
                os.unlink(output_h5)
        

        
    def test_doNotTranslate(self):
        '''Test doNotTranslate with a basic key string: "do_not_translate"
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = self.outdir.fullpath('unit_test_doNotTranslate.h5')
            cfgfile = writeCfgFile(input_file,output_h5,"Translator.TestModuleDoNotTranslate Translator.H5Output")
            cfgfile.write("[Translator.TestModuleDoNotTranslate]\n")
            cfgfile.write("skip=0 1\n")
            msg0='message0'
            msg1='message1thisIsALongerMessage'
            cfgfile.write("messages=%s %s\n"% (msg0, msg1))
            cfgfile.file.flush()
            try:
                self.runPsanaOnCfg(cfgfile,output_h5)
            except:
                cfgfile.close()
                if os.path.exists(output_h5):
                    os.unlink(output_h5)
                raise
            f=h5py.File(output_h5,'r')

            # make sure event data is not present:
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/Ipimb::DataV2']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/EvrData::DataV3']

            # we no longer write Filtered groups:
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/Filtered:0000']

            if self.cleanUp:
                f.close()
                os.unlink(output_h5)
        
    def test_ndarraysWriteRead(self):
        '''check that all ndarrays and strings written to the file.
        We test both the writing of the ndarrays to the hdf5 file, and then
        the reading back using psana. The latter should be a test of the
        psddl_hdf2psana package, but we do it here for convenience.
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = self.outdir.fullpath('unit_test_ndarraysWriteRead.h5')
            cfgfile = writeCfgFile(input_file,output_h5,"Translator.TestModuleNDArrayString Translator.H5Output")

            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_h5,printPsanaOutput=self.printPsanaOutput )
            f=h5py.File(output_h5,'r')

            double3D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float64_3/noSrc__my_double3D/data']
            float2Da = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2/noSrc__my_float2Da/data']
            float2Db = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2/noSrc__my_float2Db/data']
            int1D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_int32_1/noSrc__my_int1D/data']
            uint1D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_uint32_1/noSrc__my_uint1D/data']
            str1ar =f['/Configure:0000/Run:0000/CalibCycle:0000/std::string/noSrc__my_string1/data'][...]
            str2ar =f['/Configure:0000/Run:0000/CalibCycle:0000/std::string/noSrc__my_string2/data'][...]
            str1 = b' '.join(str1ar)
            str2 = b' '.join(str2ar)

            cdouble3D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float64_3/noSrc__cmy_double3D/data']
            cfloat2Da = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float32_2/noSrc__cmy_float2Da/data']
            cfloat2Db = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float32_2/noSrc__cmy_float2Db/data']
            cint1D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_int32_1/noSrc__cmy_int1D/data']
            cuint1D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_uint32_1/noSrc__cmy_uint1D/data']


            str1expected = b"This is event number: 1 This is event number: 2"
            str2expected = b"This is a second string.  10 * event number is 10 This is a second string.  10 * event number is 20"

            self.assertEqual(str1, str1expected, msg="str1=%s does not have expected value=%s" % (str1,str1expected))
            self.assertEqual(str2, str2expected, msg="str2=%s does not have expected value=%s" % (str2,str2expected))

            for ds,dims in zip([double3D,float2Da,float2Db,int1D,uint1D,cdouble3D,cfloat2Da,cfloat2Db,cint1D,cuint1D],
                                [3,      2,       2,       1,    1,     3,        2,        2,        1,     1]):
                for entry in range(ds.size):
                    ndarray = ds[entry]
                    dim0 = 2
                    expectedValue = 1+entry
                    if dims == 1:
                        expectedShape = (dim0,)
                        self.assertEqual(expectedShape, ndarray.shape, msg="H5OUT: shape not equal, expected=%s found=%s ds=%s" % \
                                         (expectedShape, ndarray.shape, ds.name))
                        for i in range(dim0):
                            self.assertAlmostEqual(expectedValue, ndarray[i], delta=1e-6, msg="not equal, expected = %r found=%r index=%d ds=ndarray%s" % \
                                                           (expectedValue, ndarray[i], i,ds.name.split('ndarray')[1]))
                            expectedValue += 1
                    elif dims == 2:
                        expectedShape = (dim0,2)
                        self.assertEqual(expectedShape, ndarray.shape, msg="H5OUT: shape not equal, expected=%s found=%s ds=%s" % \
                                         (expectedShape, ndarray.shape, ds.name))
                        for i in range(dim0):
                            for j in range(2):
                                self.assertAlmostEqual(expectedValue, ndarray[i,j], delta=1e-6, msg="not equal, expected = %r found=%r index=[%d,%d] ds=ndarray%s" % \
                                                           (expectedValue, ndarray[i,j], i,j,ds.name.split('ndarray')[1]))
                                expectedValue += 1
                    elif dims == 3:
                        expectedShape = (dim0,2,2)
                        self.assertEqual(expectedShape, ndarray.shape, msg="H5OUT: shape not equal, expected=%s found=%s ds=%s" % \
                                         (expectedShape, ndarray.shape, ds.name))
                        for i in range(dim0):
                            for j in range(2):
                                for k in range(2):
                                    self.assertAlmostEqual(expectedValue, ndarray[i,j,k], delta=1e-6, msg="H5OUT: not equal, expected = %r found=%r index=[%d,%d,%d] ds=ndarray%s" % \
                                                           (expectedValue, ndarray[i,j,k], i,j,k,ds.name.split('ndarray')[1]))
                                    expectedValue += 1

            f.close()

            # check that psana can read the arrays:
            psana.setConfigFile('')
            ds = psana.DataSource(output_h5)
            keyStr2PsanaType = { 'my_int1D': (psana.ndarray_int32_1,1),
                                 'cmy_int1D':(psana.ndarray_int32_1,1),
                                 'my_uint1D':(psana.ndarray_uint32_1,1),
                                 'cmy_uint1D':(psana.ndarray_uint32_1,1),
                                 'my_float2Da':(psana.ndarray_float32_2,2),
                                 'my_float2Db':(psana.ndarray_float32_2,2),
                                'cmy_float2Da':(psana.ndarray_float32_2,2),
                                 'cmy_float2Db':(psana.ndarray_float32_2,2),
                                 'my_double3D':(psana.ndarray_float64_3,3),
                                 'cmy_double3D':(psana.ndarray_float64_3,3) }
            for eventNumber, evt in enumerate(ds.events()):
                for keyStr, psanaTypeAndDim in keyStr2PsanaType.items():
                    psanaType, dims = psanaTypeAndDim
                    ndarray = evt.get(psanaType,keyStr)
                    self.assertFalse(ndarray is None, 
                                     msg="H5IN: ndarray for key=%s psanaType=%s is None" % (keyStr, psanaType))
                    dim0 = 2
                    expectedValue = 1+eventNumber
                    if dims == 1:
                        expectedShape = (dim0,)
                        self.assertEqual(expectedShape, ndarray.shape, 
                                         msg="H5IN: shape not equal, expected=%s found=%s key=%s" % \
                                         (expectedShape, ndarray.shape, keyStr))
                        for i in range(dim0):
                            self.assertAlmostEqual(expectedValue, ndarray[i], delta=1e-6, 
                                                   msg="H5IN: not equal, expected = %r found=%r index=%d keyStr=%s" % \
                                                   (expectedValue, ndarray[i], i, keyStr))
                            expectedValue += 1
                    elif dims == 2:
                        expectedShape = (dim0,2)
                        self.assertEqual(expectedShape, ndarray.shape, 
                                         msg="H5IN: shape not equal, expected=%s found=%s key=%s" % \
                                         (expectedShape, ndarray.shape, keyStr))
                        for i in range(dim0):
                            for j in range(2):
                                self.assertAlmostEqual(expectedValue, ndarray[i,j], delta=1e-6, 
                                                       msg="not equal, expected = %r found=%r index=[%d,%d] key=%s" % \
                                                           (expectedValue, ndarray[i,j], i,j,keyStr))
                                expectedValue += 1
                    elif dims == 3:
                        expectedShape = (dim0,2,2)
                        self.assertEqual(expectedShape, ndarray.shape, 
                                         msg="H5IN: shape not equal, expected=%s found=%s key=%s" % \
                                         (expectedShape, ndarray.shape, keyStr))
                        for i in range(dim0):
                            for j in range(2):
                                for k in range(2):
                                    self.assertAlmostEqual(expectedValue, ndarray[i,j,k], delta=1e-6, 
                                                           msg="not equal, expected = %r found=%r index=[%d,%d,%d] keyStr=%s" % \
                                                           (expectedValue, ndarray[i,j,k], i,j,k,keyStr))
                                    expectedValue += 1
            if self.cleanUp:
                os.unlink(output_h5)

    def test_vlenNdarraysWriteRead(self):
        '''check that vlen ndarrays are written to the file, and then read back from the file
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = self.outdir.fullpath('unit_test_vlenNdarraysWriteRead.h5')
            cfgfile = writeCfgFile(input_file,output_h5,"Translator.TestModuleNDArrayString Translator.H5Output")
            cfgfile.file.write("[Translator.TestModuleNDArrayString]\n")
            cfgfile.file.write("vary_array_sizes=true\n")
            cfgfile.file.write("vlen_prefix=true\n")

            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput = self.printPsanaOutput)
            f=h5py.File(output_h5,'r')

            double3D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float64_3_vlen/noSrc__my_double3D/data']
            float2Da = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2_vlen/noSrc__my_float2Da/data']
            float2Db = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2_vlen/noSrc__my_float2Db/data']
            int1D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_int32_1_vlen/noSrc__my_int1D/data']
            uint1D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_uint32_1_vlen/noSrc__my_uint1D/data']

            cdouble3D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float64_3_vlen/noSrc__cmy_double3D/data']
            cfloat2Da = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float32_2_vlen/noSrc__cmy_float2Da/data']
            cfloat2Db = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float32_2_vlen/noSrc__cmy_float2Db/data']
            cint1D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_int32_1_vlen/noSrc__cmy_int1D/data']
            cuint1D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_uint32_1_vlen/noSrc__cmy_uint1D/data']

            for ds,dims in zip([double3D,float2Da,float2Db,int1D,uint1D,cdouble3D,cfloat2Da,cfloat2Db,cint1D,cuint1D],
                                [3,      2,       2,       1,    1,     3,        2,        2,        1,     1]):
                for entry in range(ds.size):
                    ndarray = ds[entry]
                    dim0 = min(20,1+entry+2)  # the expected variation in ndarray sizes
                    expectedValue = 1+entry
                    if dims == 1:
                        expectedShape = (dim0,)
                        self.assertEqual(expectedShape, ndarray.shape, msg="shape not equal, expected=%s found=%s ds=%s" % \
                                         (expectedShape, ndarray.shape, ds.name))
                        for i in range(dim0):
                            self.assertAlmostEqual(expectedValue, ndarray[i], delta=1e-6, msg="not equal, expected = %r found=%r index=%d ds=ndarray%s" % \
                                                           (expectedValue, ndarray[i], i,ds.name.split('ndarray')[1]))
                            expectedValue += 1
                    elif dims == 2:
                        expectedShape = (dim0,2)
                        self.assertEqual(expectedShape, ndarray.shape, msg="shape not equal, expected=%s found=%s ds=%s" % \
                                         (expectedShape, ndarray.shape, ds.name))
                        for i in range(dim0):
                            for j in range(2):
                                self.assertAlmostEqual(expectedValue, ndarray[i,j], delta=1e-6, msg="not equal, expected = %r found=%r index=[%d,%d] ds=ndarray%s" % \
                                                           (expectedValue, ndarray[i,j], i,j,ds.name.split('ndarray')[1]))
                                expectedValue += 1
                    elif dims == 3:
                        expectedShape = (dim0,2,2)
                        self.assertEqual(expectedShape, ndarray.shape, msg="shape not equal, expected=%s found=%s ds=%s" % \
                                         (expectedShape, ndarray.shape, ds.name))
                        for i in range(dim0):
                            for j in range(2):
                                for k in range(2):
                                    self.assertAlmostEqual(expectedValue, ndarray[i,j,k], delta=1e-6, msg="not equal, expected = %r found=%r index=[%d,%d,%d] ds=ndarray%s" % \
                                                           (expectedValue, ndarray[i,j,k], i,j,k,ds.name.split('ndarray')[1]))
                                    expectedValue += 1

            f.close()

            # check that psana can read the arrays:
            psana.setConfigFile('')
            ds = psana.DataSource(output_h5)
            keyStr2PsanaType = { 'my_int1D': (psana.ndarray_int32_1,1),
                                 'cmy_int1D':(psana.ndarray_int32_1,1),
                                 'my_uint1D':(psana.ndarray_uint32_1,1),
                                 'cmy_uint1D':(psana.ndarray_uint32_1,1),
                                 'my_float2Da':(psana.ndarray_float32_2,2),
                                 'my_float2Db':(psana.ndarray_float32_2,2),
                                'cmy_float2Da':(psana.ndarray_float32_2,2),
                                 'cmy_float2Db':(psana.ndarray_float32_2,2),
                                 'my_double3D':(psana.ndarray_float64_3,3),
                                 'cmy_double3D':(psana.ndarray_float64_3,3) }
            for eventNumber, evt in enumerate(ds.events()):
                for keyStr, psanaTypeAndDim in keyStr2PsanaType.items():
                    psanaType, dims = psanaTypeAndDim
                    ndarray = evt.get(psanaType,keyStr)
                    self.assertFalse(ndarray is None, 
                                     msg="H5IN: ndarray for key=%s psanaType=%s is None" % (keyStr, psanaType))
                    dim0 = min(20,1+eventNumber+2)  # the expected variation in ndarray sizes
                    expectedValue = 1+eventNumber
                    if dims == 1:
                        expectedShape = (dim0,)
                        self.assertEqual(expectedShape, ndarray.shape, msg="shape not equal, expected=%s found=%s key=%s" % \
                                         (expectedShape, ndarray.shape, keyStr))
                        for i in range(dim0):
                            self.assertAlmostEqual(expectedValue, ndarray[i], delta=1e-6, msg="not equal, expected = %r found=%r index=%d key=%s" % \
                                                           (expectedValue, ndarray[i], i, keyStr))
                            expectedValue += 1
                    elif dims == 2:
                        expectedShape = (dim0,2)
                        self.assertEqual(expectedShape, ndarray.shape, msg="shape not equal, expected=%s found=%s key=%s" % \
                                         (expectedShape, ndarray.shape, keyStr))
                        for i in range(dim0):
                            for j in range(2):
                                self.assertAlmostEqual(expectedValue, ndarray[i,j], delta=1e-6, msg="not equal, expected = %r found=%r index=[%d,%d] key=%s" % \
                                                           (expectedValue, ndarray[i,j], i,j,keyStr))
                                expectedValue += 1
                    elif dims == 3:
                        expectedShape = (dim0,2,2)
                        self.assertEqual(expectedShape, ndarray.shape, msg="shape not equal, expected=%s found=%s key=%s" % \
                                         (expectedShape, ndarray.shape, keyStr))
                        for i in range(dim0):
                            for j in range(2):
                                for k in range(2):
                                    self.assertAlmostEqual(expectedValue, ndarray[i,j,k], delta=1e-6, msg="not equal, expected = %r found=%r index=[%d,%d,%d] key=%s" % \
                                                           (expectedValue, ndarray[i,j,k], i,j,k,keyStr))
                                    expectedValue += 1

            if self.cleanUp:
                os.unlink(output_h5)

    def test_filter_all_ndarray(self):
        '''check that we can filter out all ndarrays and strings
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit_test_filter_all_ndarray.h5")
            cfgfile = writeCfgFile(input_file,output_h5,"Translator.TestModuleNDArrayString Translator.H5Output")
            # first add any options to H5Output, then other modules
            cfgfile.write("ndarray_types = exclude\n")
            cfgfile.write("std_string = exclude\n")
            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_h5)
            f=h5py.File(output_h5,'r')

            # none of the ndarrays or strings should be in here:
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float64_3/noSrc__my_double3D']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2/noSrc__my_float2Da']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2/noSrc__my_float2Db']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_int32_1/noSrc__my_int1D']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/std::string/noSrc__my_string1']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/std::string/noSrc__my_string2']

            if self.cleanUp:
                f.close()
                os.unlink(output_h5)

    def test_filter_key_exclude(self):
        '''check that we can filter some ndarrays by excluding them
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit_test_filter_key_exclude.h5")
            cfgfile = writeCfgFile(input_file,output_h5,"Translator.TestModuleNDArrayString Translator.H5Output")
            # first add any options to H5Output, then other modules
            cfgfile.write("key_filter = exclude my_int1D my_float2Da my_string1\n")
            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_h5,extraOpts='',printPsanaOutput=False)
            f=h5py.File(output_h5,'r')

            # now these should not be here
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_int32_1/noSrc__my_int1D']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2/noSrc__my_float2Da']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/std::string/noSrc__my_string1']
            # but these should
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float64_3/noSrc__my_double3D/data']),2)
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2/noSrc__my_float2Db/data']),2)
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/std::string/noSrc__my_string2/data']),2)
            # and these should
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_int32_1/noSrc__cmy_int1D/data']),2)
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float32_2/noSrc__cmy_float2Da/data']),2)
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float64_3/noSrc__cmy_double3D/data']),2)
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float32_2/noSrc__cmy_float2Db/data']),2)
            if self.cleanUp:
                f.close()
                os.unlink(output_h5)

    def test_filter_key_include(self):
        '''check that we can filter some ndarrays by including them
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit_test_filter_key_include.h5")
            cfgfile = writeCfgFile(input_file,output_h5,"Translator.TestModuleNDArrayString Translator.H5Output")
            # first add any options to H5Output, then other modules
            cfgfile.write("key_filter = include my_int1D my_float2Da my_string1 cmy_int1D\n")
            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=False)
            f=h5py.File(output_h5,'r')

            # now these should not be here
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_uint32_1/noSrc__my_uint1D']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float64_3/noSrc__my_double3D']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2/noSrc__my_float2Db']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/std::string/noSrc__my_string2']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_uint32_1/noSrc__cmy_uint1D']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float64_3/noSrc__cmy_double3D']
            with self.assertRaises(KeyError):
                f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_float32_2/noSrc__cmy_float2Db']

            # but these should
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_const_int32_1/noSrc__cmy_int1D/data']),2)
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_int32_1/noSrc__my_int1D/data']),2)
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float32_2/noSrc__my_float2Da/data']),2)
            self.assertEqual(len(f['/Configure:0000/Run:0000/CalibCycle:0000/std::string/noSrc__my_string1/data']),2)

            if self.cleanUp:
                f.close()
                os.unlink(output_h5)

    def test_src_filter_include(self):
        '''check src filtering
        '''
        grpSrcList = [('EvrData::DataV3', 'NoDetector.0:Evr.0'),
                        ('Bld::BldDataEBeamV3','EBeam'),
                        ('Bld::BldDataPhaseCavity','PhaseCavity'),
                        ('Bld::BldDataFEEGasDetEnergy','FEEGasDetEnergy'),
                        ('Ipimb::DataV2/XppSb2_Ipm','XppSb2_Ipm'),
                        ('Ipimb::DataV2/XppSb3_Ipm','XppSb3_Ipm')]
        with self.outdir:
            for group,src in grpSrcList:
                output_h5 = self.outdir.fullpath("unit-test_src_filter_include.h5")
                cfgfile = writeCfgFile(TESTDATA_T1,output_h5)
                cfgfile.write("src_filter = include %s\n" % src)
                cfgfile.file.flush()
                self.runPsanaOnCfg(cfgfile,output_h5)
                f=h5py.File(output_h5,'r')

                fullGroup = '/Configure:0000/Run:0000/CalibCycle:0000/%s' % group
                h5group = f[fullGroup]  # should not throw exception

                filteredGroups = [grpSrc[0] for grpSrc in grpSrcList if grpSrc[1] != src]
                for filteredGroup in filteredGroups:
                    with self.assertRaises(KeyError):
                        f['/Configure:0000/Run:0000/CalibCycle:0000/%s' % filteredGroup]

            if self.cleanUp:
                f.close()
                os.unlink(output_h5)
        
    def test_src_filter_exclude(self):
        '''check src filtering
        '''
        grpSrcList = [('EvrData::DataV3', 'NoDetector.0:Evr.0'),
                        ('Bld::BldDataEBeamV3','EBeam'),
                        ('Bld::BldDataPhaseCavity','PhaseCavity'),
                        ('Bld::BldDataFEEGasDetEnergy','FEEGasDetEnergy'),
                        ('Ipimb::DataV2/XppSb2_Ipm','XppSb2_Ipm'),
                        ('Ipimb::DataV2/XppSb3_Ipm','XppSb3_Ipm')]
        with self.outdir:
            for group,src in grpSrcList:
                output_h5 = self.outdir.fullpath("unit-test_src_filter_exclude.h5")
                cfgfile = writeCfgFile(TESTDATA_T1,output_h5)
                cfgfile.write("src_filter = exclude %s\n" % src)
                cfgfile.file.flush()
                self.runPsanaOnCfg(cfgfile,output_h5)
                f=h5py.File(output_h5,'r')

                fullGroup = '/Configure:0000/Run:0000/CalibCycle:0000/%s' % group
                with self.assertRaises(KeyError):
                    h5group = f[fullGroup] 

                includedGroups = [grpSrc[0] for grpSrc in grpSrcList if grpSrc[1] != src]
                for includedGroup in includedGroups:
                    grp = f['/Configure:0000/Run:0000/CalibCycle:0000/%s' % includedGroup]

            if self.cleanUp:
                f.close()
                os.unlink(output_h5)

    def test_newWriter(self):
        '''check newWriter capability
        '''
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit-test_newwriter.h5")
            cfgfile = writeCfgFile(TESTDATA_T1,output_h5,
                                   moduleList='Translator.TestNewHdfWriter Translator.H5Output')
            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_h5)
            f=h5py.File(output_h5,'r')            
            MyData = f['/Configure:0000/Run:0000/CalibCycle:0000/Translator::MyData/noSrc__Translator.TestNewHdfWriter/data']
            self.assertEqual(len(MyData),2)
            self.assertEqual(MyData['eventCounter'][0],1)
            self.assertEqual(MyData['eventCounter'][1],2)

            if self.cleanUp:
                f.close()
                os.unlink(output_h5)

    def test_type_filter(self):
        '''check that the type_filter switch works
        '''
        with self.outdir:
            output_file = self.outdir.fullpath("unit-test-type_filter.h5")
            cfgfile = writeCfgFile(TESTDATA_T1, output_file)
            cfgfile.write("type_filter = exclude psana\n")
            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_file)
            h5 = h5py.File(output_file,'r')
            self.assertEqual(list(h5.keys()),['Configure:0000'])
            self.assertEqual(list(h5['Configure:0000'].keys()),['Run:0000'])
            # cpo removed these tests on 8/26/17 since they break
            # when PSXtcInput started adding EventId to the configstore,
            # which seems to cause an "EndData" dataset to be written
            # to the Configure output.
            #self.assertEqual(h5['Configure:0000/Run:0000'].keys(),['CalibCycle:0000'])
            #self.assertEqual(h5['Configure:0000/Run:0000/CalibCycle:0000'].keys(),[])

            # now check that if we exclude psana we see ndarrays
            cfgfile = writeCfgFile(TESTDATA_T1, output_file,
                                   moduleList='Translator.TestModuleNDArrayString Translator.H5Output')
            cfgfile.write("type_filter = exclude psana\n")
            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_file)
            h5 = h5py.File(output_file,'r')
            nddata = h5['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float64_3/noSrc__my_double3D/data']
            self.assertEqual(len(nddata),2)

            # now check that type_filter will pick out a few types:
            cfgfile = writeCfgFile(TESTDATA_T1, output_file)
            cfgfile.write("type_filter = include IpmFex Evr\n")
            cfgfile.write("store_epics = no\n")
            cfgfile.write("overwrite = true\n")
            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_file)
            cmd = 'h5ls -r %s | grep data' % output_file
            p = sb.Popen(cmd, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
            o,e = p.communicate()
            if six.PY3:
                o = o.decode()
                e = e.decode()
            self.assertEqual(e,'')
            hasTypes = [ ln.find('EvrData')>=0 or ln.find('IpmFex')>=0 for ln in o.strip().split('\n') ]
            self.assertTrue(all(hasTypes), "all lines are EvrData or IpmFex")
            if self.cleanUp:
                h5.close()
                os.unlink(output_file)
        
    def test_partition(self):
        '''check that partition type is getting written
        test_051 has partition object
        '''
        input_file = TESTDATA_PARTITION
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit-test_partition.h5")
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, extraOpts='-n 1',printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            f = h5py.File(output_h5,'r')
            cfg=f['Configure:0000/Partition::ConfigV1/Control/config']
            value=cfg.value
            expected=(67108871, 8)
            self.assertEqual(value[0],expected[0],msg="bldMask wrong: read=%s expected=%s" % (value[0],expected[0]) )
            self.assertEqual(value[1],expected[1],msg="number of groups: read=%s expected=%s" % (value[1],expected[1]) )
            sources=f['Configure:0000/Partition::ConfigV1/Control/sources']
            expectedSources = [((16788226, 256), 0),
                               ((16796544, 184551937), 1),
                               ((100682534, 0), 0),
                               ((100682534, 1), 0),
                               ((100682534, 2), 0),
                               ((100682534, 26), 0),
                               ((16796457, 184552706), 2),
                               ((16796017, 184552707), 3)]

            for source,expected in zip(sources,expectedSources):
                self.assertEqual(source[0][0],expected[0][0], "source logical wrong")
                self.assertEqual(source[0][1],expected[0][1], "source physical wrong")
                self.assertEqual(source[1],expected[1], "group wrong")
            if self.cleanUp:
                f.close()
                os.unlink(output_h5)
        
    def test_alias(self):
        '''check that filtering by src aliases works.

        test_050 has an aliasCfg object in the config, the aliases are:
        numAlias=7 
        0: EXS_OPAL -> SxrBeamline.0:Opal1000.1 
        1: Laser_OPAL_CVD02 -> SxrEndstation.0:Opal1000.2 
        2: Scienta_OPAL_CVD01A -> SxrEndstation.0:Opal1000.0 
        3: TSS_OPAL -> SxrBeamline.0:Opal1000.0 
        4: XES_OPAL_CVD01B -> SxrEndstation.0:Opal1000.1 
        5: acq01 -> SxrEndstation.0:Acqiris.0 
        6: acq02 -> SxrEndstation.0:Acqiris.2

        During the first 120 events that are in the test_050 file, we get data from 
        SxrEndstation.0:Acqiris.0 and SxrEndstation.0:Acqiris.2 but not the Opal1000
        sources.
        '''
        input_file = TESTDATA_ALIAS
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit-test_alias.h5")
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile,output_h5, extraOpts='-n 10',printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()

            # check that the Alias::ConfigV1 object got written:
            h5file=h5py.File(output_h5,'r')
            aliases=h5file['/Configure:0000/Alias::ConfigV1/Control/aliases']
            srcLog = aliases['src']['log']
            srcPhy = aliases['src']['phy']
            aliasName = aliases['aliasName']
            srcLogExpected=np.array([16782900, 16783349, 16779118, 16783350, 16779116, 16790217, 16790229], dtype=np.uint32)
            srcPhyExpected=np.array([184550145, 201327362, 201327360, 184550144, 201327361, 201327104, 201327106], dtype=np.uint32)
            aliasNameExpected=np.array(['EXS_OPAL', 'Laser_OPAL_CVD02', 'Scienta_OPAL_CVD01A', 'TSS_OPAL', 'XES_OPAL_CVD01B', 'acq01', 'acq02'], dtype='|S31')
            self.assertTrue(all(aliasName == aliasNameExpected), msg="Alias::ConfigV1 aliasName mismatch, expected=\n'%s'\nobserved=\n'%s'" % (aliasNameExpected,aliasName))
            self.assertTrue(all(srcPhy == srcPhyExpected), msg="Alias::ConfigV1 srcPhy mismatch, expected=\n'%s'\nobserved=\n'%s'" % (srcLog,srcLogExpected))
            self.assertTrue(all(srcLog == srcLogExpected), msg="Alias::ConfigV1 srcLog mismatch, expected=\n'%s'\nobserved=\n'%s'" % (srcPhy,srcPhyExpected))

            # check that if we uses aliases in the src_filter option, that it works
            cfgfile = writeCfgFile(input_file, output_h5)
            cfgfile.write("src_filter=exclude acq01 acq02\n")
            self.runPsanaOnCfg(cfgfile,output_h5, extraOpts='-n 10', printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            cmd = 'h5ls -r %s | grep "SxrEndstation.0:Acqiris.0\|SxrEndstation.0:Acqiris.2"' % output_h5
            p = sb.Popen(cmd,shell=True,stdout=sb.PIPE,stderr=sb.PIPE)
            o,e = p.communicate()
            if six.PY3:
                o = o.decode()
                e = e.decode()
            self.assertEqual(e.strip(),"",msg="There was a problem running h5ls: stderr=%s"%e.strip())
            self.assertEqual(o.strip(),"",msg="The src's were not filtered by the aliases, output of h5ls -r is: %s" % o)
            if self.cleanUp:
                h5file.close()
                os.unlink(output_h5)

    def test_calibstore(self):
        '''runs on xpptut data to see if calibration stuff gets written.
        '''
        input_file = "exp=xpptut13:run=71:dir=%s" % XPPTUTDATADIR
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit-test_xpptut13_r71.h5")
            cfgfile = writeCfgFile(input_file, output_h5, 
                                   moduleList="cspad_mod.CsPadCalib Translator.H5Output",
                                   psanaCfg='calib-dir=%s' % ptl.getTestCalibDir())
            cfgfile.write("deflate = -1\n")
            self.runPsanaOnCfg(cfgfile,output_h5, extraOpts='-n 2',printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            f = h5py.File(output_h5,'r')
            calibStore=f['/Configure:0000/CalibStore']
            self.assertEqual(set(calibStore.keys()), 
                             set([u'pdscalibdata::CsPad2x2PedestalsV1', 
                                  u'pdscalibdata::CsPad2x2PixelStatusV1',
                                  u'pdscalibdata::CsPadCommonModeSubV1',
                                  u'pdscalibdata::CsPad2x2PixelGainV1']),
                             msg = "calibStore does not contain only pdscalibdata::CsPad2x2PedestalsV1, pdscalibdata::CsPad2x2PixelStatusV1, pdscalibdata::CsPadCommonModeSubV1, pdscalibdata::CsPad2x2PixelGainV1")
            pedestalsA = calibStore['pdscalibdata::CsPad2x2PedestalsV1/XppGon.0:Cspad2x2.0/pedestals'][:]
            pedestalsB = calibStore['pdscalibdata::CsPad2x2PedestalsV1/XppGon.0:Cspad2x2.1/pedestals'][:]
            status = calibStore['pdscalibdata::CsPad2x2PixelStatusV1/XppGon.0:Cspad2x2.0/status'][:]
            commonMode = calibStore['pdscalibdata::CsPadCommonModeSubV1/XppGon.0:Cspad2x2.0/data']
            pixel_gain = calibStore['pdscalibdata::CsPad2x2PixelGainV1/XppGon.0:Cspad2x2.0/pixel_gain'][:]
            self.assertEqual(pedestalsA.shape,(185,388,2),msg="pedestals for 2x2 shape is not 185 388 2")
            self.assertEqual(pedestalsB.shape,(185,388,2),msg="pedestals for 2x2 shape is not 185 388 2")
            self.assertEqual(pixel_gain.shape,(185,388,2),msg="gain for 2x2 shape is not 185 388 2")
            self.assertEqual(status.shape,(185,388,2),msg="status for 2x2 shape is not 185 388 2")
            self.assertEqual(commonMode['mode'],1,msg="CsPadCommonModeSubV1.mode != 1, it was 1 when test was developed")
            self.assertEqual(commonMode['data'][0],24.,msg="CsPadCommonModeSubV1.data[0] != 24., it was 24. when test was developed")
            if self.cleanUp:
                f.close()
                os.unlink(output_h5)
            
    def test_calibrationDamage(self):
        '''Test that we can handle seeing calibrated cspad, and then damaged
        cspad, address bug that was found with naming groups. Trac ticket 302
        '''
        input_file = TESTDATA_CALIBDAMAGE
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit-test_calibdamage.h5")
            cfgfile = writeCfgFile(input_file, output_h5, moduleList="cspad_mod.CsPadCalib Translator.H5Output")
            cfgfile.write("deflate = -1\n")
            self.runPsanaOnCfg(cfgfile,output_h5, 
                               extraOpts=('--calib-dir %s' % ptl.getTestCalibDir()),
                               printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            f = h5py.File(output_h5,'r')  # will crash if file not present
            f.close()
            if self.cleanUp: os.unlink(output_h5)
        
#    @unittest.skip("disabled no data access")
    def test_calibration(self):
        '''runs on xpptut data to see if calibration occurs. We are testing against 
        calibrated values seen when running on 4/16/2014 - if different calibration 
        constants are deployed, this test may fail (or if the calib directory is moved or
        not found).

        Note - this data is not in the translator test directory. It has to be on disk
        for the test to succeed.
        '''
        idx = [100,100,0]  # the index for the below values
        cspad0raw = 499
        cspad0calib = 3
        cspad1raw = 409
        cspad1calib = 8

        cspad0DataPath = '/Configure:0000/Run:0000/CalibCycle:0000/CsPad2x2::ElementV1/XppGon.0:Cspad2x2.0/data'
        cspad1DataPath = '/Configure:0000/Run:0000/CalibCycle:0000/CsPad2x2::ElementV1/XppGon.0:Cspad2x2.1/data'

        input_file = "exp=xpptut13:run=71:dir=%s" % XPPTUTDATADIR
        with self.outdir:
            output_h5 = self.outdir.fullpath("unit-test_xpptut13_r71.h5")

            #######################################
            # test that calibrated data written where uncalibrated would be:
            cfgfile = writeCfgFile(input_file, output_h5, 
                                   moduleList="cspad_mod.CsPadCalib Translator.H5Output",
                                   psanaCfg='calib-dir=%s' % ptl.getTestCalibDir())
            cfgfile.write("deflate = -1\n")
            self.runPsanaOnCfg(cfgfile,output_h5, extraOpts='-n 2',printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            f = h5py.File(output_h5,'r')
            cspad0data = f[cspad0DataPath][0]
            cspad1data = f[cspad1DataPath][0]
            cspad0inH5 = cspad0data[idx[0],idx[1],idx[2] ]
            cspad1inH5 = cspad1data[idx[0],idx[1],idx[2] ]
            failMsg0 = "calibrated value should be %s but read %s. (uncalibrated value is %s)." % \
                      (cspad0calib, cspad0inH5, cspad0raw)
            failMsg0 += " dataset is: %s" % cspad0DataPath
            failMsg0 += " Perhaps calibration directory not found, or calibration data changed since test written"
            failMsg1 = "calibrated value should be %s but read %s. (uncalibrated value is %s)." % \
                      (cspad0calib, cspad0inH5, cspad0raw)
            failMsg1 += " dataset is: %s" % cspad1DataPath
            failMsg1 += " Perhaps calibration directory not found, or calibration data changed since test written"
            self.assertEqual( cspad0inH5, cspad0calib, msg=failMsg0)
            self.assertEqual( cspad1inH5, cspad1calib, msg=failMsg1)
            calibStore=f['/Configure:0000/CalibStore']
            self.assertEqual(set(calibStore.keys()), 
                             set([u'pdscalibdata::CsPad2x2PedestalsV1', 
                                  u'pdscalibdata::CsPad2x2PixelStatusV1',
                                  u'pdscalibdata::CsPad2x2PixelGainV1',
                                  u'pdscalibdata::CsPadCommonModeSubV1']),
                             msg = "calibStore does not contain only pdscalibdata::CsPad2x2PedestalsV1, pdscalibdata::CsPad2x2PixelStatusV1, pdscalibdata::CsPad2x2PixelGainV1, pdscalibdata::CsPadCommonModeSubV1")
            f.close()
            del f
            os.unlink(output_h5)

            #####################################################
            # test that uncalibrated data written when skip in place
            cfgfile = writeCfgFile(input_file, output_h5, moduleList="cspad_mod.CsPadCalib Translator.H5Output")
            cfgfile.write("deflate = -1\n")
            cfgfile.write("skip_calibrated = true\n")
            self.runPsanaOnCfg(cfgfile,output_h5, extraOpts='-n 2',printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            f = h5py.File(output_h5,'r')

            # check that no calibstore group made:
            with self.assertRaises(KeyError):
                calibStore=f['/Configure:0000/CalibStore']

            cspad0data = f[cspad0DataPath][0]
            cspad1data = f[cspad1DataPath][0]
            cspad0inH5 = cspad0data[idx[0],idx[1],idx[2] ]
            cspad1inH5 = cspad1data[idx[0],idx[1],idx[2] ]
            failMsg0 = "skipped calibrated value should be %s but read %s. (calibrated value is %s)." % \
                      (cspad0raw, cspad0inH5, cspad0calib)
            failMsg0 += " dataset is: %s" % cspad0DataPath
            failMsg0 += " problem with Translator code, not skipping calibrated?"
            failMsg1 = "skipped calibrated value should be %s but read %s. (calibrated value is %s)." % \
                      (cspad0raw, cspad0inH5, cspad0calib)
            failMsg1 += " dataset is: %s" % cspad1DataPath
            failMsg1 += " problem with Translator code, not skipping calibrated?"
            self.assertEqual( cspad0inH5, cspad0raw, msg=failMsg0)
            self.assertEqual( cspad1inH5, cspad1raw, msg=failMsg1)

            if self.cleanUp:
                f.close()
                os.unlink(output_h5)
            
    def test_keyAndSrcFilter(self):
        '''test that src filtering does not filter keys attached to that src.
        filter srcA in the translator, but have a module add an ndarray with the key
        srcA,key. The test succeeds if srcA data is not present, but
        srcA,key data is.
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir,input_file)
            cfgfile = writeCfgFile(input_file, output_h5, moduleList = "Translator.testModuleForNDarray Translator.H5Output")
            cfgfile.write('src_filter = exclude BldInfo(XppSb2_Ipm)\n')
            cfgfile.write('[Translator.testModuleForNDarray]\n')
            cfgfile.write('add_to_event_src = BldInfo(XppSb2_Ipm)\n')
            cfgfile.write('add_to_event_key = array\n')

            self.runPsanaOnCfg(cfgfile,output_h5,printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()
            cmd = 'h5ls -r %s' % output_h5
            p = sb.Popen(cmd, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
            o,e = p.communicate()
            if six.PY3:
                o = o.decode()
                e = e.decode()
            assert e==''
            lns = [ ln for ln in o.split('\n') if ln.find('XppSb2_Ipm')>=0]
            lnsWithNDarray = [ln for ln in lns if ln.lower().find('ndarray')>=0]
            self.assertEqual(len(lns), len(lnsWithNDarray), 
                             msg="There are %d lines with XppSb2_Ipm in it, but only %d of those have ndarray in it" % (len(lns), len(lnsWithNDarray)))
            if self.cleanUp:
                os.unlink(output_h5)

    def test_timetool(self):
        '''test_081 has three events with timetool data in all three.
        Check that all of the timetool data gets translated.
        '''
        input_file = TESTDATA_TIMETOOL
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir,input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile, output_h5)
            cfgfile.close()        
            h5=h5py.File(output_h5,'r')
            ttgroups = ['/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/TTSPEC:AMPL',
                        '/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/TTSPEC:AMPLNXT',
                        '/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/TTSPEC:FLTPOS',
                        '/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/TTSPEC:FLTPOSFWHM',
                        '/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/TTSPEC:FLTPOS_PS',
                        '/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/TTSPEC:REFAMPL']
            eventSeconds = [1402756826,1402756826,1402756826]
            eventNanoSeconds = [623769017,657148262,707163632]
            for ttgroup in ttgroups:
                gr = h5[ttgroup]
                tm = gr['time']
                data = gr['data']
                self.assertEqual(len(tm),3,msg="len(time) != 3 for %s" % ttgroup)
                self.assertEqual(len(data),3,msg="len(data) != 3 for %s" % ttgroup)
                tmData = tm[:]
                for idx,tmRec,sec,nano in zip(range(len(tmData)),tmData, eventSeconds, eventNanoSeconds):
                    self.assertEqual(tmRec['seconds'], sec, msg="seconds disagree for event=%d of time dataset, group=%s" % (idx,ttgroup))
                    self.assertEqual(tmRec['nanoseconds'], nano, msg="nanoseconds disagree for event=%d of time dataset, group=%s" % (idx,ttgroup))

            if self.cleanUp:
                h5.close()
                os.unlink(output_h5)

    def test_observeSkipEvents(self):
        '''if downstream module calls skips, does Translator see this and skip?
        '''
        input_file = TESTDATA_T1
        with self.outdir:
            output_h5 = self.outdir.fullpath('unit_test_observeSkipEvents.h5')
            cfgfile = writeCfgFile(input_file,output_h5,"Translator.TestModuleNDArrayString Translator.H5Output")
            cfgfile.file.write("[Translator.TestModuleNDArrayString]\n")
            cfgfile.file.write("skip_event=1\n")
            cfgfile.file.flush()
            self.runPsanaOnCfg(cfgfile,output_h5, printPsanaOutput=self.printPsanaOutput)
            f=h5py.File(output_h5,'r')
            double3D = f['/Configure:0000/Run:0000/CalibCycle:0000/ndarray_float64_3/noSrc__my_double3D/data']
            self.assertEqual(1,len(double3D),msg="downstream module skipped first event. Expected 1 translated event, but found %d" % len(double3D))
            if self.cleanUp:
                f.close()
                os.unlink(output_h5)

    def test_mpisplitscan(self):
        with self.outdir:
            mpiTest = MpiTestHelper(self.outdir,
                                    'mpiSplitScan',
                                    min_events_per_calib_file=1,
                                    num_events_check_done_calib_file=1,
                                    dataSourceString = 'exp=428:run=16:dir=%s' % SPLITSCANDATADIR,
                                    njobs=2,
                                    transCmdTimeOut = 5*60,
                                    cleanUp=self.cleanUp,
                                    verbose=False,
                                    doDump=True,
                                    downstreamModules=None,
                                    extraOptions=None)

            diff_cmd = 'diff %s %s' % (mpiTest.xtc_dump, mpiTest.h5_dump)
            p = sb.Popen(diff_cmd, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
            o,e = p.communicate()
            if six.PY3:
                o = o.decode()
                e = e.decode()
            self.assertEqual(o,'',msg='diff of xtc and mpi-splitscan translate h5 not the same.\ncmd: %s\nhas stdout=%s' % (diff_cmd, o))
            self.assertEqual(e,'',msg='diff of xtc and mpi-splitscan translate h5 not the same.\ncmd: %s\nhas stderr=%s' % (diff_cmd, e))

        
    @unittest.skip("kind of long")
    def test_mpiSplitScan_droppedSrc(self):
        '''This is a regression test for a bug that cropped up. The issue was due to moving where
        the MPIworker's do their translation of the initial configure. Because it was initially moved
        to beginCalibCycle - the ipimb config was added to the src group where the ipimb data was. 
        Ordinarily that config object would be in /Configure:00000/srcA, not in 
        /Configure:0000/Run:0000/CalibCycle:0000/srcA. Later in the xtc files, the ipimb data was 
        damaged. The Translator sees damaged from srcA - but it doesn't know which of the
        types - Ipimb::Config or Ipimb::Data that it should make a blank for. So it was trying to
        write a blank for both. However Ipimb::Config is of a scalar type, you can't add to it, so
        we crashed. There is enough information at hand to deduce that it is scalar and not write
        to it.

        This is also a good test because the ControlData is sent again during the BeginCalibCycle -
        it forces the mpiworkers to translate config during beginJob where they should.
        '''
        with self.outdir:
            mpiTest = MpiTestHelper(self.outdir,
                                    'mpiSplitScan_bug',
                                    min_events_per_calib_file=1,
                                    num_events_check_done_calib_file=1,
                                    dataSourceString = 'exp=xppd7114:run=130:dir=%s' % SPLITSCANDATADIRBUG,
                                    njobs=6,
                                    verbose=False,
                                    cleanUp = self.cleanUp)
    # can't do calibration if doing dump - will compare calibrated to uncalibrated
    #                                downstreamModules = ["cspad_mod.CsPadCalib"],
    #                                extraOptions=['psana.calib-dir=%s' % ptl.getTestCalibDir()])

            diff_cmd = 'diff %s %s' % (mpiTest.xtc_dump, mpiTest.h5_dump)
            p = sb.Popen(diff_cmd, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
            o,e = p.communicate()
            self.assertEqual(o,'',msg='cmd: %s\nhas stdout=%s' % (diff_cmd, o))
            self.assertEqual(e,'',msg='cmd: %s\nhas stderr=%s' % (diff_cmd, e))
        
    @unittest.skip("should be able to eliminate one of the oneCalib and twoCalib")
    def test_mpiSplitScan_oneCalibPerExternalFile(self):
        '''test that mpi split scan works when running similar to how non-mpi split scan worked.
        That is one calib cycle per external file"
        '''
        with self.outdir:
            mpiTest = MpiTestHelper(self.outdir,
                                    'mpiSplitScan_oneCalibPerCcFile',
                                    min_events_per_calib_file=1,
                                    num_events_check_done_calib_file=2,
                                    verbose=False,
                                    cleanUp = self.cleanUp)

            diff_cmd = 'diff %s %s' % (mpiTest.xtc_dump, mpiTest.h5_dump)
            p = sb.Popen(diff_cmd, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
            o,e = p.communicate()
            self.assertEqual(o,'',msg='cmd: %s\nhas stdout=%s' % (diff_cmd, o))
            self.assertEqual(e,'',msg='cmd: %s\nhas stderr=%s' % (diff_cmd, e))

    def test_mpiSplitScan_twoCalibPerExternalFile(self):
        '''two calib cycles per external file'''

        with self.outdir:
            mpiTest = MpiTestHelper(self.outdir,
                                    'mpiSplitScan_twoCalibPerCcFile',
                                    min_events_per_calib_file=2,
                                    num_events_check_done_calib_file=2,
                                    cleanUp = self.cleanUp,
                                    verbose = False)

            diff_cmd = 'diff %s %s' % (mpiTest.xtc_dump, mpiTest.h5_dump)
            p = sb.Popen(diff_cmd, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
            o,e = p.communicate()
            self.assertEqual(o,'',msg='cmd: %s\nhas stdout=%s' % (diff_cmd, o))
            self.assertEqual(e,'',msg='cmd: %s\nhas stderr=%s' % (diff_cmd, e))

    def test_mpiCalibStore(self):
        '''test if the calibstore gets translated in mpi mode
        '''
        inputString= "exp=xpptut13:run=71:dir=%s" % XPPTUTDATADIR
        with self.outdir:
            mpiTest = MpiTestHelper(self.outdir,
                                    'mpiSplitScan',
                                    min_events_per_calib_file=2,
                                    num_events_check_done_calib_file=2,
                                    dataSourceString = inputString,
                                    cleanUp = self.cleanUp,
                                    verbose = False,
                                    doDump = False,
                                    downstreamModules = ["cspad_mod.CsPadCalib"],
                                    extraOptions=['psana.calib-dir=%s' % ptl.getTestCalibDir()])

            f = h5py.File(mpiTest.output_h5,'r')
            calibStore=f['/Configure:0000/CalibStore']
            self.assertEqual(set(calibStore.keys()), 
                             set([u'pdscalibdata::CsPad2x2PedestalsV1', 
                                  u'pdscalibdata::CsPad2x2PixelStatusV1',
                                  u'pdscalibdata::CsPadCommonModeSubV1',
                                  u'pdscalibdata::CsPad2x2PixelGainV1']),
                             msg = "calibStore does not contain only pdscalibdata::CsPad2x2PedestalsV1, pdscalibdata::CsPad2x2PixelStatusV1, pdscalibdata::CsPadCommonModeSubV1, pdscalibdata::CsPad2x2PixelGainV1")
            if self.cleanUp:
                f.close()
                os.unlink(mpiTest.output_h5)

    def test_mpiSplitScan_endData(self):
        '''Test that end data is written during mpi split scan
        '''
        with self.outdir:
            mpiTest = MpiTestHelper(self.outdir,
                                    testName='mpiSplitScan_endData',
                                    min_events_per_calib_file=1,
                                    num_events_check_done_calib_file=1,
                                    dataSourceString = 'exp=xppd7114:run=130:dir=%s' % SPLITSCANDATADIRBUG,
                                    njobs=3,
                                    verbose=False,
                                    cleanUp = True,
                                    doDump = False,
                                    downstreamModules = ["cspad_mod.CsPadCalib,Translator.TestEndDataPsanaMod"],
                                    extraOptions=['psana.calib-dir=%s' % ptl.getTestCalibDir()])
            f=h5py.File(mpiTest.output_h5,'r')
            # the testing module Translator.TestEndDataPsanaMod will put the below string, and an array of 0.0, 1.0, 2.0
            # into the config store during begin/end job, run, and each endcalibcycle. It only puts it into the
            # first calib cycle it hits because psana won't let a python module replace keys visible to C++, 
            # so you have to be careful with testing with this. We are doing an mpi translate where the module
            # will run once per calib cycle, so it will in fact add a-new to the config store during each calib
            # cycle - a little weird.

            # We test that the data is written.
            strAnswer = 'configuration: threshold=5.2'
            arrAnswer = np.array([0,1,2], np.float)
            arrayDsets = []
            strDsets = []
            for cc in range(15):
                strDsetName = '/Configure:0000/Run:0000/CalibCycle:%4.4d/EndData/std::string/noSrc__endcalibcycle_str_cfgstore/data' % (cc,)
                arrDsetName = '/Configure:0000/Run:0000/CalibCycle:%4.4d/EndData/ndarray_float64_1/noSrc__endcalibcycle_ndarray_cfgstore/data' % (cc,)
                arrayDsets.append(arrDsetName)
                strDsets.append(strDsetName)
                strDsetName = '/Configure:0000/Run:0000/CalibCycle:%4.4d/std::string/noSrc__begincalibcycle_str_cfgstore/data' % (cc,)
                arrDsetName = '/Configure:0000/Run:0000/CalibCycle:%4.4d/ndarray_float64_1/noSrc__begincalibcycle_ndarray_cfgstore/data' % (cc,)
                arrayDsets.append(arrDsetName)
                strDsets.append(strDsetName)
            arrayDsets.append('/Configure:0000/Run:0000/EndData/ndarray_float64_1/noSrc__endrun_ndarray_cfgstore/data')
            arrayDsets.append('/Configure:0000/EndData/ndarray_float64_1/noSrc__endjob_ndarray_cfgstore/data')
            strDsets.append('/Configure:0000/Run:0000/std::string/noSrc__beginrun_str_cfgstore/data')
            strDsets.append('/Configure:0000/std::string/noSrc__beginjob_str_cfgstore/data')

            for dsetName in arrayDsets:
                try:
                    dset = f[dsetName]
                except KeyError as e:
                    print("couldn't open %s" % dsetName)
                    raise e
                self.assertTrue(all(arrAnswer == dset.value), msg="dset=%s but array=%r != expected=%r" % (dsetName,dset.value, arrAnswer))

            for dsetName in strDsets:
                try:
                    dset = f[dsetName]
                except KeyError as e:
                    print("couldn't open %s" % dsetName)
                    raise e
                self.assertEqual(dset.value, strAnswer, msg="dset=%s but str=%r != expected=%r" % (dsetName, dset.value, strAnswer))

            mpiTest.cleanup()

    def test_evKeyFilter(self):
        '''
        Test data is prepared from xpph6015 run 155. This has Camera::FrameV1 from four places.
        Test data includes these three datagrams:
        
        fid=125514 - stream 2
        fid=125520 - stream 0,80
        fid=125523 - stream 0,80,81

        # creation of the test data
        import psana_test.psanaTestLib as ptl
        ptl.copyToMultiTestDir('xpph6015',155,1,1,'/reg/g/psdm/data_test/multifile/test_016_xpph6015',[125514, 125520, 125523],True)

        # the 4 sources for FrameV1:

        EventKey(type=Psana::Camera::FrameV1, src=DetInfo(XppEndstation.0:Opal1000.0), alias="opal_0")
        EventKey(type=Psana::Camera::FrameV1, src=DetInfo(XppSb4Pim.1:Tm6740.1), alias="yag3")
        EventKey(type=Psana::Camera::FrameV1, src=DetInfo(XrayTransportDiagnostic.0:Opal1000.0), alias="xtcav")
        EventKey(type=Psana::Camera::FrameV1, src=DetInfo(XrayTransportDiagnostic.0:OrcaFl40.0), alias="FEE_Spec")
        
        '''
        cmd = 'psana -m Translator.H5Output'
        openTmpFile = tempfile.NamedTemporaryFile(prefix='tmp_test_evKeyFilter', suffix='.h5', 
                                                  delete=True)
        outputFile = openTmpFile.name
        print(outputFile)
        del openTmpFile
        cmd += ' -o Translator.H5Output.output_file=' 
        cmd += outputFile
        cmd += ' -o Translator.H5Output.overwrite=1'
        cmd += ''' -o 'Translator.H5Output.eventkey_filter=exclude Frame__xtcav Frame__yag3' '''
        cmd += ' exp=xpph6015:run=155:dir=/reg/g/psdm/data_test/multifile/test_016_xpph6015'
        ptl.cmdTimeOut(cmd, 5*60)
        f=h5py.File(outputFile)
        FrameTypeGroup = f['/Configure:0000/Run:0000/CalibCycle:0000/Camera::FrameV1']
        srcs = set(FrameTypeGroup.keys())
        expected = set()
        expected.add('XrayTransportDiagnostic.0:OrcaFl40.0')
        expected.add('XppEndstation.0:Opal1000.0')
        self.assertEqual(srcs, expected)
        f.close()
        os.unlink(outputFile)

    def test_addBlankNDarray(self):
       '''JIRA PSAS-172, if you filter out the cspad and write an array associated with its
       source, you can get a crash when the cspad source shows up as a dropped contribution. 
       When the Translator finds damage associated with the cspad source that does not specify 
       the cspad type (dropped contributions, i.e, split events), it will look at what it is 
       writing to that source. It will find the one ndarray. Then it will try to add a blank.

       Test data for this comes from exp=xppi0815:run=102. In calib cycle 0 events (0-up) 205 and 206 do not
       have cspad. The damage reads like:

       [info:psana_examples.DumpDamage]  event() run=0 calib=0 eventNumber=205 totalEvents= 205
        --- --- --- dmg 0x00008000 EventKey(type=Psana::CsPad::DataV1, src=DetInfo(XppGon.0:Cspad.0))
                    dropped=0 uninitialized=0 OutOfOrder=0 OutOfSynch=0 UserDefined=0 
                    IncompleteContribution=1 ContainsIncomplete=0 userBits=0x0

       [info:psana_examples.DumpDamage]  event() run=0 calib=0 eventNumber=206 totalEvents= 206
        -------- src damage with dropped contribs --------- 
        0x00000002  DetInfo(XppGon.0:Cspad.0)

       That is initially, we know there is damage for the cspad, but in the next event, it is damage 
       associated with the cspad source - the Translator will find that it is writing ndarrays to this 
       source and try to add a blank. We test that no exception is thrown, that we do not add blanks for 
       ndarrays.

       We prepare test data from xppi08 stream 5 [0,0x005AF120)  this gets first event, good cspad
         [0x0B40B460, 0x0B5D9518)  datagrams 39 and 40 -- both have damage
       '''
       input_file = 'exp=xppi0815:run=102:dir=%s' % NDARRAYADDBLANKDATADIRBUG
       with self.outdir:
           output_h5 = self.outdir.fullpath('test_addBlank_ndarray.h5')
           cmd = 'psana -m Translator.TestPutNDArray,Translator.H5Output'
           cmd += ' -o Translator.H5Output.output_file=%s' % output_h5
           cmd += ' -o Translator.H5Output.overwrite=1'
           cmd += ''' -o 'Translator.H5Output.src_filter=exclude opal_0 opal_1 opal_2 cspad cs140_0 cs140_1' '''
           cmd += ' -o Translator.H5Output.unknown_src_ok=1 -o Translator.H5Output.deflate=-1'
           cmd += ' -o Translator.TestPutNDArray.cspadsrc=cspad '
           cmd += input_file
           out, err = ptl.cmdTimeOut(cmd)
           assert os.path.exists(output_h5), "output_h5=%s doesn't exist in test" % output_h5
           os.unlink(output_h5)
           for ln in err.split('\n'):
             self.assertTrue(ptl.filterPsanaStderr(ln), msg="stderr output ln=%s obtained from cmd=%s" % (ln, cmd))

    def test_usdusb_fex(self):
        '''test translation of usdusb fex config, in particular name where 
        I did by hand translation
        '''
        with self.outdir:
            outputfile = self.outdir.fullpath('test_usdusb_fexconfig.h5')
            cmd = 'psana -n 1 -m Translator.H5Output -o Translator.H5Output.output_file=%s -o Translator.H5Output.overwrite=1 %s' % (outputfile, TESTDATA_USDUSB_FEXCONFIGV1)
            stdout, stderr = ptl.cmdTimeOut(cmd, 100)
            assert stderr.strip()=='', "errors with cmd=%s, stderr=%s" % (cmd, stderr)
            ds = psana.DataSource(outputfile)
            cfgStore = ds.env().configStore()
            fex = cfgStore.get(psana.UsdUsb.FexConfigV1, psana.Source('usbencoder'))
            self.assertEqual(fex.name(0), 'test1')
            self.assertEqual(fex.name(1), 'test2')
            self.assertEqual(fex.name(2), 'test3')
            self.assertEqual(fex.name(3), 'test4')
            os.unlink(outputfile)

    def test_oceanoptics_dataV3(self):
        def dumpType(evt, srcList, pstype):
            results = {}
            for src in srcList:
                obj = evt.get(pstype, psana.Source(src))
                assert obj is not None
                results[src]= obj2str(obj)
            return results

        ooAliases = ['oospec_0','oospec_1','oospec_2']
        dsXtc = psana.DataSource(TESTDATA_OCEANOPTICS_DATAV3)
        xtcDumps = dumpType(next(dsXtc.events()), ooAliases, psana.OceanOptics.DataV3)
        del dsXtc

        with self.outdir:
            outputfile = self.outdir.fullpath('test_openoptics_dataV3.h5')
            cmd = 'psana -n 1 -m Translator.H5Output -o Translator.H5Output.output_file=%s -o Translator.H5Output.overwrite=1 %s' % (outputfile, TESTDATA_OCEANOPTICS_DATAV3)
            stdout, stderr = ptl.cmdTimeOut(cmd, 100)
            assert stderr.strip()=='', "errors with cmd=%s, stderr=%s" % (cmd, stderr)
            dsH5 = psana.DataSource(outputfile)
            h5Dumps = dumpType(next(dsH5.events()), ooAliases, psana.OceanOptics.DataV3)
            del dsH5
            os.unlink(outputfile)

            for alias in ooAliases:
                xtcDump = xtcDumps[alias]
                h5Dump = h5Dumps[alias]
                assert(len(xtcDump)>0)
                assert(len(h5Dump)>0)
                self.assertEqual(xtcDump, h5Dump, msg='for alias=%s OceanOptics.DataV3 xtcDump != h5Dump.\ndataset=%s.\n.xtc=%s\nh5=%s' % 
                                 (alias, TESTDATA_OCEANOPTICS_DATAV3, xtcDump, h5Dump))

    def test_generic1d_dataV0(self):            
        cfgDepth = np.array([2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4], np.int)
        cfgLen = 4096
        cfgOffset = 10
        cfgSampleType = np.array([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2], np.int)
        cfgDataOffsets = np.array([0, 8192, 16384, 24576, 32768, 40960, 49152, 57344, 65536, 81920, 98304, 114688, 131072, 147456, 163840, 180224], np.int)

        evtChMeans = np.array([32332.8232421875, 32842.461181640625, 32787.649658203125, 32242.1279296875, 32728.6484375, 32775.515380859375, 32774.3291015625, 32712.96142578125, 
                               130722.67260742188, 129934.55932617188, 130061.32397460938, 129807.03295898438, 156133.08837890625, 156152.8046875, 133423.43676757812, 106196.09326171875], np.float)

        with self.outdir:
            outputfile = self.outdir.fullpath('test_generic1d_dataV0.h5')
            cmd = 'psana -n 4 -m Translator.H5Output -o Translator.H5Output.output_file=%s -o Translator.H5Output.overwrite=1 %s' % \
                  (outputfile, TESTDATA_GENERIC1D_DATAV0)
            stdout, stderr = ptl.cmdTimeOut(cmd, 100)
            assert stderr.strip()=='', "errors with cmd=%s, stderr=%s" % (cmd, stderr)
            h5 = h5py.File(outputfile,'r')

            self.assertTrue(all(cfgDepth == h5['Configure:0000/Generic1D::ConfigV0/MfxEndstation.0:Wave8.0/Depth'][:]), msg='cfgdepth !=')
            self.assertTrue(all(cfgSampleType == h5['Configure:0000/Generic1D::ConfigV0/MfxEndstation.0:Wave8.0/SampleType'][:]), msg='cfgSampleType !=')
            for ch in range(16):
                self.assertEqual(cfgLen, h5['Configure:0000/Generic1D::ConfigV0/MfxEndstation.0:Wave8.0/Length'][ch], msg='ch=%d len wrong' % ch)
                self.assertEqual(cfgOffset, h5['Configure:0000/Generic1D::ConfigV0/MfxEndstation.0:Wave8.0/Offset'][ch], msg='ch=%d offset wrong' % ch)
                chMeanH5evt0 = np.mean(h5['Configure:0000/Run:0000/CalibCycle:0000/Generic1D::DataV0/MfxEndstation.0:Wave8.0/channel:%2.2d' % ch][0])
                self.assertAlmostEqual(evtChMeans[ch], chMeanH5evt0 , places=1, msg='ch=%d evt expected=%.2f != h5=%.2f' % (ch, evtChMeans[ch], chMeanH5evt0))
            if self.cleanUp:
                h5.close()
                os.unlink(outputfile)

    def test_epics(self):
        '''Test epics translation. test_020 has 4 kinds of epics, string, short, enum, long and double.
        '''
        input_file = TESTDATA_EPICS
        with self.outdir:
            output_h5 = makeH5OutputNameFromXtc(self.outdir, input_file)
            cfgfile = writeCfgFile(input_file, output_h5)
            self.runPsanaOnCfg(cfgfile, output_h5, '-n 1', printPsanaOutput=self.printPsanaOutput)
            cfgfile.close()        
            h5=h5py.File(output_h5,'r')
            # long  data=1000
            cfgDbr33 = h5['/Configure:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/LAS:FS1:REG:kp_vcxo:rd/data']
            self.assertEqual(cfgDbr33['value'][0], 10000, msg="%s != %s  name=%s" % (cfgDbr33['value'][0], 10000, cfgDbr33.name))

            # string '08/23/2011 06:28:38'
            cfgDbr28 = h5['/Configure:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/SIOC:SYS0:ML00:TOD/data']
            self.assertEqual(cfgDbr28['value'][0], b'08/23/2011 06:28:38', msg="%s != %s name=%s" % (cfgDbr28['value'][0], '08/23/2011 06:28:38', cfgDbr28.name))

            # double data=-4.0000e+01
            cfgDbr34 = h5['/Configure:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/SXR:DFP:MMS:01.RBV/data']
            self.assertEqual('%.4e' % cfgDbr34['value'][0], '-4.0000e+01', msg="%s !=%s name=%s" % ('%.4e' % cfgDbr34['value'][0], '-4.0000e+01', cfgDbr34.name))

            # enum data=0x1, no_str=2 enum[0]=Unlocked enum[1]=Locked
            cfgDbr31 = h5['/Configure:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/SXR:EXP:AOT:02:Lock/data']
            self.assertEqual( cfgDbr31['value'][0], 1, msg="%s !=%s name=%s" % (cfgDbr31['value'][0], 1, cfgDbr31.name))
            self.assertEqual( cfgDbr31['no_str'][0], 2, msg="no_str: %s !=%s name=%s" % (cfgDbr31['no_str'][0], 2, cfgDbr31.name))
            self.assertEqual( cfgDbr31['strs'][0][0], b'Unlocked', msg="strs[0]: %s !=%s name=%s" % (cfgDbr31['strs'][0][0], 'Unlocked', cfgDbr31.name))
            self.assertEqual( cfgDbr31['strs'][0][1], b'Locked', msg="strs[1]: %s !=%s name=%s" % (cfgDbr31['strs'][0][1], 'Locked', cfgDbr31.name))

            # short data=0   upper_ctrl_limit=32767 lower_ctrl_limit=-32768
            cfgDbr29 = h5['/Configure:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/SXR:SPS:MMS:01.HLS/data']
            self.assertEqual( cfgDbr29['value'][0], 0, msg="%s !=%s name=%s" % (cfgDbr29['value'][0], 0, cfgDbr29.name))
            self.assertEqual( cfgDbr29['upper_ctrl_limit'][0], 32767, msg="upper_ctrl_limit: %s !=%s name=%s" % (cfgDbr29['upper_ctrl_limit'][0], 32767, cfgDbr29.name))
            self.assertEqual( cfgDbr29['lower_ctrl_limit'][0], -32768, msg="lower_ctrl_limit: %s !=%s name=%s" % (cfgDbr29['lower_ctrl_limit'][0], -32768, cfgDbr29.name))

            # long  data=10000 stamp.sec=682908957 stamp.nsec=393338000
            evtDbr19 = h5['/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/LAS:FS1:REG:kp_vcxo:rd/data']
            self.assertEqual( evtDbr19['value'][0], 10000, msg="%s !=%s name=%s" % (evtDbr19['value'][0], 10000, evtDbr19.name))
            self.assertEqual( evtDbr19['stamp']['secPastEpoch'][0], 682908957, msg="stamp.sec %s !=%s name=%s" % (evtDbr19['stamp']['secPastEpoch'][0], 682908957, evtDbr19.name))
            self.assertEqual( evtDbr19['stamp']['nsec'][0], 393338000, msg="stamp.nsec %s !=%s name=%s" % (evtDbr19['stamp']['nsec'][0], 393338000, evtDbr19.name))

            # string stamp.sec=682956951 stamp.nsec=227500000 data=['08/23/2011 07:15:51']
            evtDbr14 = h5['/Configure:0000/Run:0000//CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/SIOC:SYS0:ML00:TOD/data']
            self.assertEqual( evtDbr14['value'][0], b'08/23/2011 07:15:51', msg="%s !=%s name=%s" % (evtDbr14['value'][0], 10000, evtDbr14.name))
            self.assertEqual( evtDbr14['stamp']['secPastEpoch'][0], 682956951, msg="stamp.sec %s !=%s name=%s" % (evtDbr14['stamp']['secPastEpoch'][0], 682956951, evtDbr14.name))
            self.assertEqual( evtDbr14['stamp']['nsec'][0], 227500000, msg="stamp.nsec %s !=%s name=%s" % (evtDbr14['stamp']['nsec'][0], 227500000, evtDbr14.name))

            # double  stamp.sec=682954114 stamp.nsec=64595000 data=-4.0000e+01
            evtDbr20 = h5['/Configure:0000/Run:0000//CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/SXR:DFP:MMS:01.RBV/data']
            self.assertEqual( '%.4e' % evtDbr20['value'][0], '-4.0000e+01', msg="%s !=%s name=%s" % (evtDbr20['value'][0], 10000, evtDbr20.name))
            self.assertEqual( evtDbr20['stamp']['secPastEpoch'][0], 682954114, msg="stamp.sec %s !=%s name=%s" % (evtDbr20['stamp']['secPastEpoch'][0], 682954114, evtDbr20.name))
            self.assertEqual( evtDbr20['stamp']['nsec'][0], 64595000, msg="stamp.nsec %s !=%s name=%s" % (evtDbr20['stamp']['nsec'][0], 64595000, evtDbr20.name))

            # enum  stamp.sec=682853411 stamp.nsec=0 data=0x1
            evtDbr17 = h5['/Configure:0000/Run:0000//CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/SXR:EXP:AOT:02:Lock/data']
            self.assertEqual( evtDbr17['value'][0], 1, msg="%s !=%s name=%s" % (evtDbr17['value'][0], 10000, evtDbr17.name))
            self.assertEqual( evtDbr17['stamp']['secPastEpoch'][0], 682853411, msg="stamp.sec %s !=%s name=%s" % (evtDbr17['stamp']['secPastEpoch'][0], 682853411, evtDbr17.name))
            self.assertEqual( evtDbr17['stamp']['nsec'][0], 0, msg="stamp.nsec %s !=%s name=%s" % (evtDbr17['stamp']['nsec'][0], 0, evtDbr17.name))

            # short data=0   stamp.sec=682954118 stamp.nsec=384744000 data=0
            evtDbr15 = h5['/Configure:0000/Run:0000/CalibCycle:0000/Epics::EpicsPv/EpicsArch.0:NoDevice.0/SXR:SPS:MMS:01.HLS/data']
            self.assertEqual( evtDbr15['value'][0], 0, msg="%s !=%s name=%s" % (evtDbr15['value'][0], 0, evtDbr15.name))
            self.assertEqual( evtDbr15['stamp']['secPastEpoch'][0], 682954118, msg="stamp.sec %s !=%s name=%s" % (evtDbr15['stamp']['secPastEpoch'][0], 682954118, evtDbr15.name))
            self.assertEqual( evtDbr15['stamp']['nsec'][0], 384744000, msg="stamp.nsec %s !=%s name=%s" % (evtDbr15['stamp']['nsec'][0], 384744000, evtDbr15.name))


            if self.cleanUp:
                h5.close()
                os.unlink(output_h5)
        
#    In the future, I would like to translate ndarrays that are placed in the 
#    calibStore. Presently, we only translate known types associated with 
#    calibrated objects that were seen - that is we are not doing a general
#    translation of the calibstore. If we do that in the future, I can
#    develop the below test further.
# 
#    def test_ndarrayCalibStore(self):
#        '''place an ndarray in the calibstore, make sure it makes it to the hdf5
#        '''
#        input_file = TESTDATA_T1
#        with self.outdir:
    #        output_h5 = makeH5OutputNameFromXtc(self.outdir,input_file)
    #        cfgfile = writeCfgFile(input_file, output_h5, moduleList = "Translator.testModuleForNDarray Translator.H5Output")
    #        cfgfile.write('[Translator.testModuleForNDarray]\n')
    #        cfgfile.write('add_to_calib_src = BldInfo(XppSb2_Ipm)\n')
    #        self.runPsanaOnCfg(cfgfile,output_h5,printPsanaOutput=self.printPsanaOutput)
    #        cfgfile.close()
    #        h5 = h5py.File(output_h5,'r')
    #        if self.cleanUp:
    #            h5.close()
    #            os.unlink(output_h5)


#  run unit tests when imported as a main module
#
#  To run an individual test, do something like (from the release directory)
#  python -m unittest Translator.testing.H5Output.test_file_t1_translated_correctly

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0], '-v'])
