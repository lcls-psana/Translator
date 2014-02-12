/* Do not edit this file.  It is created by a code generator. */

#include "Translator/TypeAliases.h"

#include "psddl_psana/acqiris.ddl.h"
#include "psddl_psana/alias.ddl.h"
#include "psddl_psana/andor.ddl.h"
#include "psddl_psana/bld.ddl.h"
#include "psddl_psana/camera.ddl.h"
#include "psddl_psana/control.ddl.h"
#include "psddl_psana/cspad.ddl.h"
#include "psddl_psana/cspad2x2.ddl.h"
#include "psddl_psana/encoder.ddl.h"
#include "psddl_psana/epics.ddl.h"
#include "psddl_psana/epix.ddl.h"
#include "psddl_psana/epixsampler.ddl.h"
#include "psddl_psana/evr.ddl.h"
#include "psddl_psana/fccd.ddl.h"
#include "psddl_psana/fli.ddl.h"
#include "psddl_psana/gsc16ai.ddl.h"
#include "psddl_psana/imp.ddl.h"
#include "psddl_psana/ipimb.ddl.h"
#include "psddl_psana/l3t.ddl.h"
#include "psddl_psana/lusi.ddl.h"
#include "psddl_psana/oceanoptics.ddl.h"
#include "psddl_psana/opal1k.ddl.h"
#include "psddl_psana/orca.ddl.h"
#include "psddl_psana/partition.ddl.h"
#include "psddl_psana/pnccd.ddl.h"
#include "psddl_psana/princeton.ddl.h"
#include "psddl_psana/pulnix.ddl.h"
#include "psddl_psana/quartz.ddl.h"
#include "psddl_psana/rayonix.ddl.h"
#include "psddl_psana/timepix.ddl.h"
#include "psddl_psana/usdusb.ddl.h"
#include "ndarray/ndarray.h"

using namespace Translator;
using namespace std;

TypeAliases::TypeAliases() {
  TypeInfoSet AcqTdc;
  AcqTdc.insert( & typeid(Psana::Acqiris::TdcConfigV1));
  AcqTdc.insert( & typeid(Psana::Acqiris::TdcDataV1));
  m_alias2TypesMap["AcqTdc"] = AcqTdc;

  TypeInfoSet AcqWaveform;
  AcqWaveform.insert( & typeid(Psana::Acqiris::ConfigV1));
  AcqWaveform.insert( & typeid(Psana::Acqiris::DataDescV1));
  m_alias2TypesMap["AcqWaveform"] = AcqWaveform;

  TypeInfoSet Alias;
  Alias.insert( & typeid(Psana::Alias::ConfigV1));
  m_alias2TypesMap["Alias"] = Alias;

  TypeInfoSet Andor;
  Andor.insert( & typeid(Psana::Andor::ConfigV1));
  Andor.insert( & typeid(Psana::Andor::FrameV1));
  m_alias2TypesMap["Andor"] = Andor;

  TypeInfoSet Control;
  Control.insert( & typeid(Psana::ControlData::ConfigV1));
  Control.insert( & typeid(Psana::ControlData::ConfigV2));
  Control.insert( & typeid(Psana::ControlData::ConfigV3));
  m_alias2TypesMap["Control"] = Control;

  TypeInfoSet Cspad;
  Cspad.insert( & typeid(Psana::CsPad::ConfigV1));
  Cspad.insert( & typeid(Psana::CsPad::ConfigV2));
  Cspad.insert( & typeid(Psana::CsPad::ConfigV3));
  Cspad.insert( & typeid(Psana::CsPad::ConfigV4));
  Cspad.insert( & typeid(Psana::CsPad::ConfigV5));
  Cspad.insert( & typeid(Psana::CsPad::DataV1));
  Cspad.insert( & typeid(Psana::CsPad::DataV2));
  m_alias2TypesMap["Cspad"] = Cspad;

  TypeInfoSet Cspad2x2;
  Cspad2x2.insert( & typeid(Psana::CsPad2x2::ConfigV1));
  Cspad2x2.insert( & typeid(Psana::CsPad2x2::ConfigV2));
  Cspad2x2.insert( & typeid(Psana::CsPad2x2::ElementV1));
  m_alias2TypesMap["Cspad2x2"] = Cspad2x2;

  TypeInfoSet DiodeFex;
  DiodeFex.insert( & typeid(Psana::Lusi::DiodeFexConfigV1));
  DiodeFex.insert( & typeid(Psana::Lusi::DiodeFexConfigV2));
  DiodeFex.insert( & typeid(Psana::Lusi::DiodeFexV1));
  m_alias2TypesMap["DiodeFex"] = DiodeFex;

  TypeInfoSet EBeam;
  EBeam.insert( & typeid(Psana::Bld::BldDataEBeamV0));
  EBeam.insert( & typeid(Psana::Bld::BldDataEBeamV1));
  EBeam.insert( & typeid(Psana::Bld::BldDataEBeamV2));
  EBeam.insert( & typeid(Psana::Bld::BldDataEBeamV3));
  EBeam.insert( & typeid(Psana::Bld::BldDataEBeamV4));
  m_alias2TypesMap["EBeam"] = EBeam;

  TypeInfoSet Encoder;
  Encoder.insert( & typeid(Psana::Encoder::ConfigV1));
  Encoder.insert( & typeid(Psana::Encoder::ConfigV2));
  Encoder.insert( & typeid(Psana::Encoder::DataV1));
  Encoder.insert( & typeid(Psana::Encoder::DataV2));
  m_alias2TypesMap["Encoder"] = Encoder;

  TypeInfoSet Epics;
  Epics.insert( & typeid(Psana::Epics::ConfigV1));
  m_alias2TypesMap["Epics"] = Epics;

  TypeInfoSet Epix;
  Epix.insert( & typeid(Psana::Epix::ConfigV1));
  Epix.insert( & typeid(Psana::Epix::ElementV1));
  m_alias2TypesMap["Epix"] = Epix;

  TypeInfoSet EpixSampler;
  EpixSampler.insert( & typeid(Psana::EpixSampler::ConfigV1));
  EpixSampler.insert( & typeid(Psana::EpixSampler::ElementV1));
  m_alias2TypesMap["EpixSampler"] = EpixSampler;

  TypeInfoSet Evr;
  Evr.insert( & typeid(Psana::EvrData::ConfigV1));
  Evr.insert( & typeid(Psana::EvrData::ConfigV2));
  Evr.insert( & typeid(Psana::EvrData::ConfigV3));
  Evr.insert( & typeid(Psana::EvrData::ConfigV4));
  Evr.insert( & typeid(Psana::EvrData::ConfigV5));
  Evr.insert( & typeid(Psana::EvrData::ConfigV6));
  Evr.insert( & typeid(Psana::EvrData::ConfigV7));
  Evr.insert( & typeid(Psana::EvrData::DataV3));
  m_alias2TypesMap["Evr"] = Evr;

  TypeInfoSet EvrIO;
  EvrIO.insert( & typeid(Psana::EvrData::IOConfigV1));
  m_alias2TypesMap["EvrIO"] = EvrIO;

  TypeInfoSet Evs;
  Evs.insert( & typeid(Psana::EvrData::SrcConfigV1));
  m_alias2TypesMap["Evs"] = Evs;

  TypeInfoSet FEEGasDetEnergy;
  FEEGasDetEnergy.insert( & typeid(Psana::Bld::BldDataFEEGasDetEnergy));
  m_alias2TypesMap["FEEGasDetEnergy"] = FEEGasDetEnergy;

  TypeInfoSet Fccd;
  Fccd.insert( & typeid(Psana::FCCD::FccdConfigV1));
  Fccd.insert( & typeid(Psana::FCCD::FccdConfigV2));
  m_alias2TypesMap["Fccd"] = Fccd;

  TypeInfoSet Fli;
  Fli.insert( & typeid(Psana::Fli::ConfigV1));
  Fli.insert( & typeid(Psana::Fli::FrameV1));
  m_alias2TypesMap["Fli"] = Fli;

  TypeInfoSet Frame;
  Frame.insert( & typeid(Psana::Camera::FrameV1));
  m_alias2TypesMap["Frame"] = Frame;

  TypeInfoSet FrameFccd;
  FrameFccd.insert( & typeid(Psana::Camera::FrameFccdConfigV1));
  m_alias2TypesMap["FrameFccd"] = FrameFccd;

  TypeInfoSet FrameFex;
  FrameFex.insert( & typeid(Psana::Camera::FrameFexConfigV1));
  m_alias2TypesMap["FrameFex"] = FrameFex;

  TypeInfoSet GMD;
  GMD.insert( & typeid(Psana::Bld::BldDataGMDV0));
  GMD.insert( & typeid(Psana::Bld::BldDataGMDV1));
  m_alias2TypesMap["GMD"] = GMD;

  TypeInfoSet Gsc16ai;
  Gsc16ai.insert( & typeid(Psana::Gsc16ai::ConfigV1));
  Gsc16ai.insert( & typeid(Psana::Gsc16ai::DataV1));
  m_alias2TypesMap["Gsc16ai"] = Gsc16ai;

  TypeInfoSet Imp;
  Imp.insert( & typeid(Psana::Imp::ConfigV1));
  Imp.insert( & typeid(Psana::Imp::ElementV1));
  m_alias2TypesMap["Imp"] = Imp;

  TypeInfoSet Ipimb;
  Ipimb.insert( & typeid(Psana::Ipimb::ConfigV1));
  Ipimb.insert( & typeid(Psana::Ipimb::ConfigV2));
  Ipimb.insert( & typeid(Psana::Ipimb::DataV1));
  Ipimb.insert( & typeid(Psana::Ipimb::DataV2));
  m_alias2TypesMap["Ipimb"] = Ipimb;

  TypeInfoSet IpmFex;
  IpmFex.insert( & typeid(Psana::Lusi::IpmFexConfigV1));
  IpmFex.insert( & typeid(Psana::Lusi::IpmFexConfigV2));
  IpmFex.insert( & typeid(Psana::Lusi::IpmFexV1));
  m_alias2TypesMap["IpmFex"] = IpmFex;

  TypeInfoSet L3T;
  L3T.insert( & typeid(Psana::L3T::ConfigV1));
  L3T.insert( & typeid(Psana::L3T::DataV1));
  m_alias2TypesMap["L3T"] = L3T;

  TypeInfoSet OceanOptics;
  OceanOptics.insert( & typeid(Psana::OceanOptics::ConfigV1));
  OceanOptics.insert( & typeid(Psana::OceanOptics::DataV1));
  m_alias2TypesMap["OceanOptics"] = OceanOptics;

  TypeInfoSet Opal1k;
  Opal1k.insert( & typeid(Psana::Opal1k::ConfigV1));
  m_alias2TypesMap["Opal1k"] = Opal1k;

  TypeInfoSet Orca;
  Orca.insert( & typeid(Psana::Orca::ConfigV1));
  m_alias2TypesMap["Orca"] = Orca;

  TypeInfoSet Partition;
  Partition.insert( & typeid(Psana::Partition::ConfigV1));
  m_alias2TypesMap["Partition"] = Partition;

  TypeInfoSet PhaseCavity;
  PhaseCavity.insert( & typeid(Psana::Bld::BldDataPhaseCavity));
  m_alias2TypesMap["PhaseCavity"] = PhaseCavity;

  TypeInfoSet PimImage;
  PimImage.insert( & typeid(Psana::Lusi::PimImageConfigV1));
  m_alias2TypesMap["PimImage"] = PimImage;

  TypeInfoSet Princeton;
  Princeton.insert( & typeid(Psana::Princeton::ConfigV1));
  Princeton.insert( & typeid(Psana::Princeton::ConfigV2));
  Princeton.insert( & typeid(Psana::Princeton::ConfigV3));
  Princeton.insert( & typeid(Psana::Princeton::ConfigV4));
  Princeton.insert( & typeid(Psana::Princeton::ConfigV5));
  Princeton.insert( & typeid(Psana::Princeton::FrameV1));
  Princeton.insert( & typeid(Psana::Princeton::FrameV2));
  m_alias2TypesMap["Princeton"] = Princeton;

  TypeInfoSet PrincetonInfo;
  PrincetonInfo.insert( & typeid(Psana::Princeton::InfoV1));
  m_alias2TypesMap["PrincetonInfo"] = PrincetonInfo;

  TypeInfoSet Quartz;
  Quartz.insert( & typeid(Psana::Quartz::ConfigV1));
  m_alias2TypesMap["Quartz"] = Quartz;

  TypeInfoSet Rayonix;
  Rayonix.insert( & typeid(Psana::Rayonix::ConfigV1));
  Rayonix.insert( & typeid(Psana::Rayonix::ConfigV2));
  m_alias2TypesMap["Rayonix"] = Rayonix;

  TypeInfoSet SharedAcqADC;
  SharedAcqADC.insert( & typeid(Psana::Bld::BldDataAcqADCV1));
  m_alias2TypesMap["SharedAcqADC"] = SharedAcqADC;

  TypeInfoSet SharedIpimb;
  SharedIpimb.insert( & typeid(Psana::Bld::BldDataIpimbV0));
  SharedIpimb.insert( & typeid(Psana::Bld::BldDataIpimbV1));
  m_alias2TypesMap["SharedIpimb"] = SharedIpimb;

  TypeInfoSet SharedPim;
  SharedPim.insert( & typeid(Psana::Bld::BldDataPimV1));
  m_alias2TypesMap["SharedPim"] = SharedPim;

  TypeInfoSet Spectrometer;
  Spectrometer.insert( & typeid(Psana::Bld::BldDataSpectrometerV0));
  m_alias2TypesMap["Spectrometer"] = Spectrometer;

  TypeInfoSet TM6740;
  TM6740.insert( & typeid(Psana::Pulnix::TM6740ConfigV1));
  TM6740.insert( & typeid(Psana::Pulnix::TM6740ConfigV2));
  m_alias2TypesMap["TM6740"] = TM6740;

  TypeInfoSet Timepix;
  Timepix.insert( & typeid(Psana::Timepix::ConfigV1));
  Timepix.insert( & typeid(Psana::Timepix::ConfigV2));
  Timepix.insert( & typeid(Psana::Timepix::ConfigV3));
  Timepix.insert( & typeid(Psana::Timepix::DataV1));
  Timepix.insert( & typeid(Psana::Timepix::DataV2));
  m_alias2TypesMap["Timepix"] = Timepix;

  TypeInfoSet TwoDGaussian;
  TwoDGaussian.insert( & typeid(Psana::Camera::TwoDGaussianV1));
  m_alias2TypesMap["TwoDGaussian"] = TwoDGaussian;

  TypeInfoSet UsdUsb;
  UsdUsb.insert( & typeid(Psana::UsdUsb::ConfigV1));
  UsdUsb.insert( & typeid(Psana::UsdUsb::DataV1));
  m_alias2TypesMap["UsdUsb"] = UsdUsb;

  TypeInfoSet pnCCD;
  pnCCD.insert( & typeid(Psana::PNCCD::ConfigV1));
  pnCCD.insert( & typeid(Psana::PNCCD::ConfigV2));
  pnCCD.insert( & typeid(Psana::PNCCD::FramesV1));
  m_alias2TypesMap["pnCCD"] = pnCCD;

  TypeInfoSet ndarray_types;
  ndarray_types.insert( & typeid(ndarray<int8_t,1>));
  ndarray_types.insert( & typeid(ndarray<int8_t,2>));
  ndarray_types.insert( & typeid(ndarray<int8_t,3>));
  ndarray_types.insert( & typeid(ndarray<int8_t,4>));
  ndarray_types.insert( & typeid(ndarray<int16_t,1>));
  ndarray_types.insert( & typeid(ndarray<int16_t,2>));
  ndarray_types.insert( & typeid(ndarray<int16_t,3>));
  ndarray_types.insert( & typeid(ndarray<int16_t,4>));
  ndarray_types.insert( & typeid(ndarray<int32_t,1>));
  ndarray_types.insert( & typeid(ndarray<int32_t,2>));
  ndarray_types.insert( & typeid(ndarray<int32_t,3>));
  ndarray_types.insert( & typeid(ndarray<int32_t,4>));
  ndarray_types.insert( & typeid(ndarray<int64_t,1>));
  ndarray_types.insert( & typeid(ndarray<int64_t,2>));
  ndarray_types.insert( & typeid(ndarray<int64_t,3>));
  ndarray_types.insert( & typeid(ndarray<int64_t,4>));
  ndarray_types.insert( & typeid(ndarray<uint8_t,1>));
  ndarray_types.insert( & typeid(ndarray<uint8_t,2>));
  ndarray_types.insert( & typeid(ndarray<uint8_t,3>));
  ndarray_types.insert( & typeid(ndarray<uint8_t,4>));
  ndarray_types.insert( & typeid(ndarray<uint16_t,1>));
  ndarray_types.insert( & typeid(ndarray<uint16_t,2>));
  ndarray_types.insert( & typeid(ndarray<uint16_t,3>));
  ndarray_types.insert( & typeid(ndarray<uint16_t,4>));
  ndarray_types.insert( & typeid(ndarray<uint32_t,1>));
  ndarray_types.insert( & typeid(ndarray<uint32_t,2>));
  ndarray_types.insert( & typeid(ndarray<uint32_t,3>));
  ndarray_types.insert( & typeid(ndarray<uint32_t,4>));
  ndarray_types.insert( & typeid(ndarray<uint64_t,1>));
  ndarray_types.insert( & typeid(ndarray<uint64_t,2>));
  ndarray_types.insert( & typeid(ndarray<uint64_t,3>));
  ndarray_types.insert( & typeid(ndarray<uint64_t,4>));
  ndarray_types.insert( & typeid(ndarray<float,1>));
  ndarray_types.insert( & typeid(ndarray<float,2>));
  ndarray_types.insert( & typeid(ndarray<float,3>));
  ndarray_types.insert( & typeid(ndarray<float,4>));
  ndarray_types.insert( & typeid(ndarray<double,1>));
  ndarray_types.insert( & typeid(ndarray<double,2>));
  ndarray_types.insert( & typeid(ndarray<double,3>));
  ndarray_types.insert( & typeid(ndarray<double,4>));
  m_alias2TypesMap["ndarray_types"] = ndarray_types;

  TypeInfoSet std_string;
  std_string.insert( & typeid(std::string));
  m_alias2TypesMap["std_string"] = std_string;


  Alias2TypesMap::iterator pos;
  for (pos = m_alias2TypesMap.begin(); pos != m_alias2TypesMap.end(); ++pos) {
    m_aliasKeys.insert(pos->first);
    TypeInfoSet & typeSet = pos->second;
    TypeInfoSet::iterator typePos;
    for (typePos = typeSet.begin(); typePos != typeSet.end(); ++typePos) {
      m_type2AliasMap[*typePos] = pos->first;
    }
  }  
}
