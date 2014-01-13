/* Do not edit this file.  It is created from a code generator.
Edit the template which resides in 

psddl/data/templates/hdf5Translator.tmpl?hdfwritermap_cpp
*/

#include "PSEvt/EventKey.h"
#include "PSEvt/TypeInfoUtils.h"
#include "Translator/HdfWriterFromEvent.h"
#include "Translator/HdfWriterMap.h"
#include "MsgLogger/MsgLogger.h"
#include "psddl_hdf2psana/acqiris.ddl.h"
#include "psddl_hdf2psana/alias.ddl.h"
#include "psddl_hdf2psana/andor.ddl.h"
#include "psddl_hdf2psana/bld.ddl.h"
#include "psddl_hdf2psana/camera.ddl.h"
#include "psddl_hdf2psana/control.ddl.h"
#include "psddl_hdf2psana/cspad.ddl.h"
#include "psddl_hdf2psana/cspad2x2.ddl.h"
#include "psddl_hdf2psana/encoder.ddl.h"
#include "psddl_hdf2psana/epics.ddl.h"
#include "psddl_hdf2psana/epix.ddl.h"
#include "psddl_hdf2psana/epixsampler.ddl.h"
#include "psddl_hdf2psana/evr.ddl.h"
#include "psddl_hdf2psana/fccd.ddl.h"
#include "psddl_hdf2psana/fli.ddl.h"
#include "psddl_hdf2psana/gsc16ai.ddl.h"
#include "psddl_hdf2psana/imp.ddl.h"
#include "psddl_hdf2psana/ipimb.ddl.h"
#include "psddl_hdf2psana/l3t.ddl.h"
#include "psddl_hdf2psana/lusi.ddl.h"
#include "psddl_hdf2psana/oceanoptics.ddl.h"
#include "psddl_hdf2psana/opal1k.ddl.h"
#include "psddl_hdf2psana/orca.ddl.h"
#include "psddl_hdf2psana/pnccd.ddl.h"
#include "psddl_hdf2psana/princeton.ddl.h"
#include "psddl_hdf2psana/pulnix.ddl.h"
#include "psddl_hdf2psana/quartz.ddl.h"
#include "psddl_hdf2psana/rayonix.ddl.h"
#include "psddl_hdf2psana/timepix.ddl.h"
#include "psddl_hdf2psana/usdusb.ddl.h"
#include "Translator/HdfWriterNDArray.h"
#include "Translator/HdfWriterStringFromEvent.h"
 
using namespace std;

namespace {

const char *logger = "Translator.HdfWriterMap";
const int latestTypeSchema = -1;

using namespace Translator;
using namespace psddl_hdf2psana;
using namespace psddl_hdf2psana::Epix;
using namespace psddl_hdf2psana::UsdUsb;
using namespace psddl_hdf2psana::Rayonix;
using namespace psddl_hdf2psana::CsPad2x2;
using namespace psddl_hdf2psana::Pulnix;
using namespace psddl_hdf2psana::Imp;
using namespace psddl_hdf2psana::L3T;
using namespace psddl_hdf2psana::Camera;
using namespace psddl_hdf2psana::EvrData;
using namespace psddl_hdf2psana::Bld;
using namespace psddl_hdf2psana::EpixSampler;
using namespace psddl_hdf2psana::Quartz;
using namespace psddl_hdf2psana::Timepix;
using namespace psddl_hdf2psana::Encoder;
using namespace psddl_hdf2psana::CsPad;
using namespace psddl_hdf2psana::Opal1k;
using namespace psddl_hdf2psana::Princeton;
using namespace psddl_hdf2psana::ControlData;
using namespace psddl_hdf2psana::FCCD;
using namespace psddl_hdf2psana::Alias;
using namespace psddl_hdf2psana::Ipimb;
using namespace psddl_hdf2psana::Orca;
using namespace psddl_hdf2psana::Fli;
using namespace psddl_hdf2psana::Acqiris;
using namespace psddl_hdf2psana::Andor;
using namespace psddl_hdf2psana::Epics;
using namespace psddl_hdf2psana::Lusi;
using namespace psddl_hdf2psana::OceanOptics;
using namespace psddl_hdf2psana::PNCCD;
using namespace psddl_hdf2psana::Gsc16ai;


template<typename T>
class HdfWriterPsana : public HdfWriterFromEvent {
public:
  void make_datasets(DataTypeLoc dataTypeLoc, hdf5pp::Group & srcGroup, 
                     const PSEvt::EventKey & eventKey, 
                     PSEvt::Event & evt, PSEnv::Env & env,
                     bool shuffle, int deflate,
                     boost::shared_ptr<Translator::ChunkPolicy> chunkPolicy)
  {
    boost::shared_ptr<T> ptr = getFromEventStore<T>(eventKey, dataTypeLoc, evt, env);
    MsgLog(logger, trace, "HdfWriter<" << PSEvt::TypeInfoUtils::typeInfoRealName(& typeid(T) ) << ">::make_datasets in group: " << srcGroup.name());
    ::make_datasets(*ptr,srcGroup,*chunkPolicy,deflate,shuffle,latestTypeSchema);
  }

  void store(DataTypeLoc dataTypeLoc, 
             hdf5pp::Group & srcGroup, 
             const PSEvt::EventKey & eventKey, 
             PSEvt::Event & evt, 
             PSEnv::Env & env) 
  {
    boost::shared_ptr<T> ptr = getFromEventStore<T>(eventKey, dataTypeLoc, evt, env);
    ::store(*ptr,srcGroup,latestTypeSchema); 
  }
  
  void store_at(DataTypeLoc dataTypeLoc, 
                long index, hdf5pp::Group & srcGroup, 
                const PSEvt::EventKey & eventKey, 
                PSEvt::Event & evt, 
                PSEnv::Env & env) {
    boost::shared_ptr<T> ptr = getFromEventStore<T>(eventKey, dataTypeLoc, evt, env);
    ::store_at(ptr.get(),srcGroup, index, latestTypeSchema); 
  }

  void append(DataTypeLoc dataTypeLoc,
              hdf5pp::Group & srcGroup, const PSEvt::EventKey & eventKey, 
              PSEvt::Event & evt, PSEnv::Env & env) 
  {
    boost::shared_ptr<T> ptr = getFromEventStore<T>(eventKey, dataTypeLoc, evt, env);
    ::store_at(ptr.get(), srcGroup, indexForAppend, latestTypeSchema);
  }

  void addBlank(hdf5pp::Group & group)
  {
    T *ptrForBlank = NULL;
    ::store_at(ptrForBlank,group, indexForAppend, latestTypeSchema);
  }
  static const long indexForAppend = -1;
};  // class HdfWriterPsana<T>


} // local namespace 

namespace Translator {

boost::shared_ptr<HdfWriterFromEvent> getHdfWriter(HdfWriterMap & mapping, const std::type_info *typeInfoPtr) {
   HdfWriterMap::iterator pos = mapping.find(typeInfoPtr);
  if (pos == mapping.end()) {
    return boost::shared_ptr<Translator::HdfWriterFromEvent>();
  }
  return pos->second;
}

void initializeHdfWriterMap( HdfWriterMap & mapping) {
  mapping[ & typeid(Psana::Acqiris::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Acqiris::ConfigV1> >();
  mapping[ & typeid(Psana::Acqiris::DataDescV1) ] = boost::make_shared<HdfWriterPsana<Psana::Acqiris::DataDescV1> >();
  mapping[ & typeid(Psana::Acqiris::TdcConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Acqiris::TdcConfigV1> >();
  mapping[ & typeid(Psana::Acqiris::TdcDataV1) ] = boost::make_shared<HdfWriterPsana<Psana::Acqiris::TdcDataV1> >();
  mapping[ & typeid(Psana::Alias::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Alias::ConfigV1> >();
  mapping[ & typeid(Psana::Andor::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Andor::ConfigV1> >();
  mapping[ & typeid(Psana::Andor::FrameV1) ] = boost::make_shared<HdfWriterPsana<Psana::Andor::FrameV1> >();
  mapping[ & typeid(Psana::Bld::BldDataAcqADCV1) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataAcqADCV1> >();
  mapping[ & typeid(Psana::Bld::BldDataEBeamV0) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataEBeamV0> >();
  mapping[ & typeid(Psana::Bld::BldDataEBeamV1) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataEBeamV1> >();
  mapping[ & typeid(Psana::Bld::BldDataEBeamV2) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataEBeamV2> >();
  mapping[ & typeid(Psana::Bld::BldDataEBeamV3) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataEBeamV3> >();
  mapping[ & typeid(Psana::Bld::BldDataEBeamV4) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataEBeamV4> >();
  mapping[ & typeid(Psana::Bld::BldDataFEEGasDetEnergy) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataFEEGasDetEnergy> >();
  mapping[ & typeid(Psana::Bld::BldDataGMDV0) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataGMDV0> >();
  mapping[ & typeid(Psana::Bld::BldDataGMDV1) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataGMDV1> >();
  mapping[ & typeid(Psana::Bld::BldDataIpimbV0) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataIpimbV0> >();
  mapping[ & typeid(Psana::Bld::BldDataIpimbV1) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataIpimbV1> >();
  mapping[ & typeid(Psana::Bld::BldDataPhaseCavity) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataPhaseCavity> >();
  mapping[ & typeid(Psana::Bld::BldDataPimV1) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataPimV1> >();
  mapping[ & typeid(Psana::Bld::BldDataSpectrometerV0) ] = boost::make_shared<HdfWriterPsana<Psana::Bld::BldDataSpectrometerV0> >();
  mapping[ & typeid(Psana::Camera::FrameFccdConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Camera::FrameFccdConfigV1> >();
  mapping[ & typeid(Psana::Camera::FrameFexConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Camera::FrameFexConfigV1> >();
  mapping[ & typeid(Psana::Camera::FrameV1) ] = boost::make_shared<HdfWriterPsana<Psana::Camera::FrameV1> >();
  mapping[ & typeid(Psana::Camera::TwoDGaussianV1) ] = boost::make_shared<HdfWriterPsana<Psana::Camera::TwoDGaussianV1> >();
  mapping[ & typeid(Psana::ControlData::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::ControlData::ConfigV1> >();
  mapping[ & typeid(Psana::ControlData::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::ControlData::ConfigV2> >();
  mapping[ & typeid(Psana::ControlData::ConfigV3) ] = boost::make_shared<HdfWriterPsana<Psana::ControlData::ConfigV3> >();
  mapping[ & typeid(Psana::CsPad2x2::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad2x2::ConfigV1> >();
  mapping[ & typeid(Psana::CsPad2x2::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad2x2::ConfigV2> >();
  mapping[ & typeid(Psana::CsPad2x2::ElementV1) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad2x2::ElementV1> >();
  mapping[ & typeid(Psana::CsPad::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad::ConfigV1> >();
  mapping[ & typeid(Psana::CsPad::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad::ConfigV2> >();
  mapping[ & typeid(Psana::CsPad::ConfigV3) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad::ConfigV3> >();
  mapping[ & typeid(Psana::CsPad::ConfigV4) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad::ConfigV4> >();
  mapping[ & typeid(Psana::CsPad::ConfigV5) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad::ConfigV5> >();
  mapping[ & typeid(Psana::CsPad::DataV1) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad::DataV1> >();
  mapping[ & typeid(Psana::CsPad::DataV2) ] = boost::make_shared<HdfWriterPsana<Psana::CsPad::DataV2> >();
  mapping[ & typeid(Psana::Encoder::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Encoder::ConfigV1> >();
  mapping[ & typeid(Psana::Encoder::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::Encoder::ConfigV2> >();
  mapping[ & typeid(Psana::Encoder::DataV1) ] = boost::make_shared<HdfWriterPsana<Psana::Encoder::DataV1> >();
  mapping[ & typeid(Psana::Encoder::DataV2) ] = boost::make_shared<HdfWriterPsana<Psana::Encoder::DataV2> >();
  mapping[ & typeid(Psana::Epics::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Epics::ConfigV1> >();
  mapping[ & typeid(Psana::Epix::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Epix::ConfigV1> >();
  mapping[ & typeid(Psana::Epix::ElementV1) ] = boost::make_shared<HdfWriterPsana<Psana::Epix::ElementV1> >();
  mapping[ & typeid(Psana::EpixSampler::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::EpixSampler::ConfigV1> >();
  mapping[ & typeid(Psana::EpixSampler::ElementV1) ] = boost::make_shared<HdfWriterPsana<Psana::EpixSampler::ElementV1> >();
  mapping[ & typeid(Psana::EvrData::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::ConfigV1> >();
  mapping[ & typeid(Psana::EvrData::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::ConfigV2> >();
  mapping[ & typeid(Psana::EvrData::ConfigV3) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::ConfigV3> >();
  mapping[ & typeid(Psana::EvrData::ConfigV4) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::ConfigV4> >();
  mapping[ & typeid(Psana::EvrData::ConfigV5) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::ConfigV5> >();
  mapping[ & typeid(Psana::EvrData::ConfigV6) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::ConfigV6> >();
  mapping[ & typeid(Psana::EvrData::ConfigV7) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::ConfigV7> >();
  mapping[ & typeid(Psana::EvrData::DataV3) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::DataV3> >();
  mapping[ & typeid(Psana::EvrData::IOConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::IOConfigV1> >();
  mapping[ & typeid(Psana::EvrData::SrcConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::EvrData::SrcConfigV1> >();
  mapping[ & typeid(Psana::FCCD::FccdConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::FCCD::FccdConfigV1> >();
  mapping[ & typeid(Psana::FCCD::FccdConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::FCCD::FccdConfigV2> >();
  mapping[ & typeid(Psana::Fli::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Fli::ConfigV1> >();
  mapping[ & typeid(Psana::Fli::FrameV1) ] = boost::make_shared<HdfWriterPsana<Psana::Fli::FrameV1> >();
  mapping[ & typeid(Psana::Gsc16ai::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Gsc16ai::ConfigV1> >();
  mapping[ & typeid(Psana::Gsc16ai::DataV1) ] = boost::make_shared<HdfWriterPsana<Psana::Gsc16ai::DataV1> >();
  mapping[ & typeid(Psana::Imp::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Imp::ConfigV1> >();
  mapping[ & typeid(Psana::Imp::ElementV1) ] = boost::make_shared<HdfWriterPsana<Psana::Imp::ElementV1> >();
  mapping[ & typeid(Psana::Ipimb::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Ipimb::ConfigV1> >();
  mapping[ & typeid(Psana::Ipimb::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::Ipimb::ConfigV2> >();
  mapping[ & typeid(Psana::Ipimb::DataV1) ] = boost::make_shared<HdfWriterPsana<Psana::Ipimb::DataV1> >();
  mapping[ & typeid(Psana::Ipimb::DataV2) ] = boost::make_shared<HdfWriterPsana<Psana::Ipimb::DataV2> >();
  mapping[ & typeid(Psana::L3T::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::L3T::ConfigV1> >();
  mapping[ & typeid(Psana::L3T::DataV1) ] = boost::make_shared<HdfWriterPsana<Psana::L3T::DataV1> >();
  mapping[ & typeid(Psana::Lusi::DiodeFexConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Lusi::DiodeFexConfigV1> >();
  mapping[ & typeid(Psana::Lusi::DiodeFexConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::Lusi::DiodeFexConfigV2> >();
  mapping[ & typeid(Psana::Lusi::DiodeFexV1) ] = boost::make_shared<HdfWriterPsana<Psana::Lusi::DiodeFexV1> >();
  mapping[ & typeid(Psana::Lusi::IpmFexConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Lusi::IpmFexConfigV1> >();
  mapping[ & typeid(Psana::Lusi::IpmFexConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::Lusi::IpmFexConfigV2> >();
  mapping[ & typeid(Psana::Lusi::IpmFexV1) ] = boost::make_shared<HdfWriterPsana<Psana::Lusi::IpmFexV1> >();
  mapping[ & typeid(Psana::Lusi::PimImageConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Lusi::PimImageConfigV1> >();
  mapping[ & typeid(Psana::OceanOptics::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::OceanOptics::ConfigV1> >();
  mapping[ & typeid(Psana::OceanOptics::DataV1) ] = boost::make_shared<HdfWriterPsana<Psana::OceanOptics::DataV1> >();
  mapping[ & typeid(Psana::Opal1k::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Opal1k::ConfigV1> >();
  mapping[ & typeid(Psana::Orca::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Orca::ConfigV1> >();
  mapping[ & typeid(Psana::PNCCD::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::PNCCD::ConfigV1> >();
  mapping[ & typeid(Psana::PNCCD::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::PNCCD::ConfigV2> >();
  mapping[ & typeid(Psana::PNCCD::FramesV1) ] = boost::make_shared<HdfWriterPsana<Psana::PNCCD::FramesV1> >();
  mapping[ & typeid(Psana::Princeton::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Princeton::ConfigV1> >();
  mapping[ & typeid(Psana::Princeton::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::Princeton::ConfigV2> >();
  mapping[ & typeid(Psana::Princeton::ConfigV3) ] = boost::make_shared<HdfWriterPsana<Psana::Princeton::ConfigV3> >();
  mapping[ & typeid(Psana::Princeton::ConfigV4) ] = boost::make_shared<HdfWriterPsana<Psana::Princeton::ConfigV4> >();
  mapping[ & typeid(Psana::Princeton::ConfigV5) ] = boost::make_shared<HdfWriterPsana<Psana::Princeton::ConfigV5> >();
  mapping[ & typeid(Psana::Princeton::FrameV1) ] = boost::make_shared<HdfWriterPsana<Psana::Princeton::FrameV1> >();
  mapping[ & typeid(Psana::Princeton::FrameV2) ] = boost::make_shared<HdfWriterPsana<Psana::Princeton::FrameV2> >();
  mapping[ & typeid(Psana::Princeton::InfoV1) ] = boost::make_shared<HdfWriterPsana<Psana::Princeton::InfoV1> >();
  mapping[ & typeid(Psana::Pulnix::TM6740ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Pulnix::TM6740ConfigV1> >();
  mapping[ & typeid(Psana::Pulnix::TM6740ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::Pulnix::TM6740ConfigV2> >();
  mapping[ & typeid(Psana::Quartz::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Quartz::ConfigV1> >();
  mapping[ & typeid(Psana::Rayonix::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Rayonix::ConfigV1> >();
  mapping[ & typeid(Psana::Rayonix::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::Rayonix::ConfigV2> >();
  mapping[ & typeid(Psana::Timepix::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::Timepix::ConfigV1> >();
  mapping[ & typeid(Psana::Timepix::ConfigV2) ] = boost::make_shared<HdfWriterPsana<Psana::Timepix::ConfigV2> >();
  mapping[ & typeid(Psana::Timepix::ConfigV3) ] = boost::make_shared<HdfWriterPsana<Psana::Timepix::ConfigV3> >();
  mapping[ & typeid(Psana::Timepix::DataV1) ] = boost::make_shared<HdfWriterPsana<Psana::Timepix::DataV1> >();
  mapping[ & typeid(Psana::Timepix::DataV2) ] = boost::make_shared<HdfWriterPsana<Psana::Timepix::DataV2> >();
  mapping[ & typeid(Psana::UsdUsb::ConfigV1) ] = boost::make_shared<HdfWriterPsana<Psana::UsdUsb::ConfigV1> >();
  mapping[ & typeid(Psana::UsdUsb::DataV1) ] = boost::make_shared<HdfWriterPsana<Psana::UsdUsb::DataV1> >();

  // ndarrays
  mapping[ & typeid(ndarray< int8_t, 1>) ] = boost::make_shared<HdfWriterNDArray< int8_t, 1 > >();  
  mapping[ & typeid(ndarray< int8_t, 2>) ] = boost::make_shared<HdfWriterNDArray< int8_t, 2 > >();  
  mapping[ & typeid(ndarray< int8_t, 3>) ] = boost::make_shared<HdfWriterNDArray< int8_t, 3 > >();  
  mapping[ & typeid(ndarray< int8_t, 4>) ] = boost::make_shared<HdfWriterNDArray< int8_t, 4 > >();  
  mapping[ & typeid(ndarray< int16_t, 1>) ] = boost::make_shared<HdfWriterNDArray< int16_t, 1 > >();  
  mapping[ & typeid(ndarray< int16_t, 2>) ] = boost::make_shared<HdfWriterNDArray< int16_t, 2 > >();  
  mapping[ & typeid(ndarray< int16_t, 3>) ] = boost::make_shared<HdfWriterNDArray< int16_t, 3 > >();  
  mapping[ & typeid(ndarray< int16_t, 4>) ] = boost::make_shared<HdfWriterNDArray< int16_t, 4 > >();  
  mapping[ & typeid(ndarray< int32_t, 1>) ] = boost::make_shared<HdfWriterNDArray< int32_t, 1 > >();  
  mapping[ & typeid(ndarray< int32_t, 2>) ] = boost::make_shared<HdfWriterNDArray< int32_t, 2 > >();  
  mapping[ & typeid(ndarray< int32_t, 3>) ] = boost::make_shared<HdfWriterNDArray< int32_t, 3 > >();  
  mapping[ & typeid(ndarray< int32_t, 4>) ] = boost::make_shared<HdfWriterNDArray< int32_t, 4 > >();  
  mapping[ & typeid(ndarray< int64_t, 1>) ] = boost::make_shared<HdfWriterNDArray< int64_t, 1 > >();  
  mapping[ & typeid(ndarray< int64_t, 2>) ] = boost::make_shared<HdfWriterNDArray< int64_t, 2 > >();  
  mapping[ & typeid(ndarray< int64_t, 3>) ] = boost::make_shared<HdfWriterNDArray< int64_t, 3 > >();  
  mapping[ & typeid(ndarray< int64_t, 4>) ] = boost::make_shared<HdfWriterNDArray< int64_t, 4 > >();  
  mapping[ & typeid(ndarray< uint8_t, 1>) ] = boost::make_shared<HdfWriterNDArray< uint8_t, 1 > >();  
  mapping[ & typeid(ndarray< uint8_t, 2>) ] = boost::make_shared<HdfWriterNDArray< uint8_t, 2 > >();  
  mapping[ & typeid(ndarray< uint8_t, 3>) ] = boost::make_shared<HdfWriterNDArray< uint8_t, 3 > >();  
  mapping[ & typeid(ndarray< uint8_t, 4>) ] = boost::make_shared<HdfWriterNDArray< uint8_t, 4 > >();  
  mapping[ & typeid(ndarray< uint16_t, 1>) ] = boost::make_shared<HdfWriterNDArray< uint16_t, 1 > >();  
  mapping[ & typeid(ndarray< uint16_t, 2>) ] = boost::make_shared<HdfWriterNDArray< uint16_t, 2 > >();  
  mapping[ & typeid(ndarray< uint16_t, 3>) ] = boost::make_shared<HdfWriterNDArray< uint16_t, 3 > >();  
  mapping[ & typeid(ndarray< uint16_t, 4>) ] = boost::make_shared<HdfWriterNDArray< uint16_t, 4 > >();  
  mapping[ & typeid(ndarray< uint32_t, 1>) ] = boost::make_shared<HdfWriterNDArray< uint32_t, 1 > >();  
  mapping[ & typeid(ndarray< uint32_t, 2>) ] = boost::make_shared<HdfWriterNDArray< uint32_t, 2 > >();  
  mapping[ & typeid(ndarray< uint32_t, 3>) ] = boost::make_shared<HdfWriterNDArray< uint32_t, 3 > >();  
  mapping[ & typeid(ndarray< uint32_t, 4>) ] = boost::make_shared<HdfWriterNDArray< uint32_t, 4 > >();  
  mapping[ & typeid(ndarray< uint64_t, 1>) ] = boost::make_shared<HdfWriterNDArray< uint64_t, 1 > >();  
  mapping[ & typeid(ndarray< uint64_t, 2>) ] = boost::make_shared<HdfWriterNDArray< uint64_t, 2 > >();  
  mapping[ & typeid(ndarray< uint64_t, 3>) ] = boost::make_shared<HdfWriterNDArray< uint64_t, 3 > >();  
  mapping[ & typeid(ndarray< uint64_t, 4>) ] = boost::make_shared<HdfWriterNDArray< uint64_t, 4 > >();  
  mapping[ & typeid(ndarray< float, 1>) ] = boost::make_shared<HdfWriterNDArray< float, 1 > >();  
  mapping[ & typeid(ndarray< float, 2>) ] = boost::make_shared<HdfWriterNDArray< float, 2 > >();  
  mapping[ & typeid(ndarray< float, 3>) ] = boost::make_shared<HdfWriterNDArray< float, 3 > >();  
  mapping[ & typeid(ndarray< float, 4>) ] = boost::make_shared<HdfWriterNDArray< float, 4 > >();  
  mapping[ & typeid(ndarray< double, 1>) ] = boost::make_shared<HdfWriterNDArray< double, 1 > >();  
  mapping[ & typeid(ndarray< double, 2>) ] = boost::make_shared<HdfWriterNDArray< double, 2 > >();  
  mapping[ & typeid(ndarray< double, 3>) ] = boost::make_shared<HdfWriterNDArray< double, 3 > >();  
  mapping[ & typeid(ndarray< double, 4>) ] = boost::make_shared<HdfWriterNDArray< double, 4 > >();  
  // string               
  mapping[ & typeid(std::string) ] = boost::make_shared<HdfWriterStringFromEvent>();
}

} // Translator namespace
