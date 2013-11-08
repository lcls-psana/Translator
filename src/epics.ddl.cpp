#include <string.h>
#include "MsgLogger/MsgLogger.h"
#include "Translator/epics.ddl.h"

namespace {

char * logger = "epics.dll";

void copyEpicsPvCtrlEnumStrings(const Psana::Epics::EpicsPvCtrlEnum & sourceObject, 
                                Translator::Unroll::EpicsPvCtrlEnum & destObject)
{
  const Psana::Epics::dbr_ctrl_enum& dbr = sourceObject.dbr();
  for (uint16_t stringNumber = 0; stringNumber < dbr.no_str(); ++stringNumber) {
    strncpy(destObject.strs[stringNumber], dbr.strings(stringNumber), Psana::Epics::MAX_ENUM_STRING_SIZE);
  }
}

} // local namespace

namespace Translator {

void copyToUnrolled(const Psana::Epics::EpicsPvCtrlString &source, const int16_t element, 
                    Unroll::EpicsPvCtrlString &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  strncpy(dest.sPvName, source.pvName(), Psana::Epics::iMaxPvNameLength);
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  copyValueFldToUnrolled<Unroll::EpicsPvCtrlString>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvCtrlShort &source, const int16_t element, 
                    Unroll::EpicsPvCtrlShort &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  strncpy(dest.sPvName, source.pvName(), Psana::Epics::iMaxPvNameLength);
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  strncpy(dest.units, source.dbr().units(), Psana::Epics::MAX_UNITS_SIZE);
  dest.upper_disp_limit = source.dbr().upper_disp_limit();
  dest.lower_disp_limit = source.dbr().lower_disp_limit();
  dest.upper_alarm_limit = source.dbr().upper_alarm_limit();
  dest.upper_warning_limit = source.dbr().upper_warning_limit();
  dest.lower_warning_limit = source.dbr().lower_warning_limit();
  dest.lower_alarm_limit = source.dbr().lower_alarm_limit();
  dest.upper_ctrl_limit = source.dbr().upper_ctrl_limit();
  dest.lower_ctrl_limit = source.dbr().lower_ctrl_limit();
  copyValueFldToUnrolled<Unroll::EpicsPvCtrlShort>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvCtrlFloat &source, const int16_t element, 
                    Unroll::EpicsPvCtrlFloat &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  strncpy(dest.sPvName, source.pvName(), Psana::Epics::iMaxPvNameLength);
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.precision = source.dbr().precision();
  strncpy(dest.units, source.dbr().units(), Psana::Epics::MAX_UNITS_SIZE);
  dest.upper_disp_limit = source.dbr().upper_disp_limit();
  dest.lower_disp_limit = source.dbr().lower_disp_limit();
  dest.upper_alarm_limit = source.dbr().upper_alarm_limit();
  dest.upper_warning_limit = source.dbr().upper_warning_limit();
  dest.lower_warning_limit = source.dbr().lower_warning_limit();
  dest.lower_alarm_limit = source.dbr().lower_alarm_limit();
  dest.upper_ctrl_limit = source.dbr().upper_ctrl_limit();
  dest.lower_ctrl_limit = source.dbr().lower_ctrl_limit();
  copyValueFldToUnrolled<Unroll::EpicsPvCtrlFloat>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvCtrlEnum &source, const int16_t element, 
                    Unroll::EpicsPvCtrlEnum &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  strncpy(dest.sPvName, source.pvName(), Psana::Epics::iMaxPvNameLength);
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.no_str = source.dbr().no_str();
  copyEpicsPvCtrlEnumStrings(source, dest);
  copyValueFldToUnrolled<Unroll::EpicsPvCtrlEnum>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvCtrlChar &source, const int16_t element, 
                    Unroll::EpicsPvCtrlChar &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  strncpy(dest.sPvName, source.pvName(), Psana::Epics::iMaxPvNameLength);
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  strncpy(dest.units, source.dbr().units(), Psana::Epics::MAX_UNITS_SIZE);
  dest.upper_disp_limit = source.dbr().upper_disp_limit();
  dest.lower_disp_limit = source.dbr().lower_disp_limit();
  dest.upper_alarm_limit = source.dbr().upper_alarm_limit();
  dest.upper_warning_limit = source.dbr().upper_warning_limit();
  dest.lower_warning_limit = source.dbr().lower_warning_limit();
  dest.lower_alarm_limit = source.dbr().lower_alarm_limit();
  dest.upper_ctrl_limit = source.dbr().upper_ctrl_limit();
  dest.lower_ctrl_limit = source.dbr().lower_ctrl_limit();
  copyValueFldToUnrolled<Unroll::EpicsPvCtrlChar>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvCtrlLong &source, const int16_t element, 
                    Unroll::EpicsPvCtrlLong &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  strncpy(dest.sPvName, source.pvName(), Psana::Epics::iMaxPvNameLength);
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  strncpy(dest.units, source.dbr().units(), Psana::Epics::MAX_UNITS_SIZE);
  dest.upper_disp_limit = source.dbr().upper_disp_limit();
  dest.lower_disp_limit = source.dbr().lower_disp_limit();
  dest.upper_alarm_limit = source.dbr().upper_alarm_limit();
  dest.upper_warning_limit = source.dbr().upper_warning_limit();
  dest.lower_warning_limit = source.dbr().lower_warning_limit();
  dest.lower_alarm_limit = source.dbr().lower_alarm_limit();
  dest.upper_ctrl_limit = source.dbr().upper_ctrl_limit();
  dest.lower_ctrl_limit = source.dbr().lower_ctrl_limit();
  copyValueFldToUnrolled<Unroll::EpicsPvCtrlLong>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvCtrlDouble &source, const int16_t element, 
                    Unroll::EpicsPvCtrlDouble &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  strncpy(dest.sPvName, source.pvName(), Psana::Epics::iMaxPvNameLength);
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.precision = source.dbr().precision();
  strncpy(dest.units, source.dbr().units(), Psana::Epics::MAX_UNITS_SIZE);
  dest.upper_disp_limit = source.dbr().upper_disp_limit();
  dest.lower_disp_limit = source.dbr().lower_disp_limit();
  dest.upper_alarm_limit = source.dbr().upper_alarm_limit();
  dest.upper_warning_limit = source.dbr().upper_warning_limit();
  dest.lower_warning_limit = source.dbr().lower_warning_limit();
  dest.lower_alarm_limit = source.dbr().lower_alarm_limit();
  dest.upper_ctrl_limit = source.dbr().upper_ctrl_limit();
  dest.lower_ctrl_limit = source.dbr().lower_ctrl_limit();
  copyValueFldToUnrolled<Unroll::EpicsPvCtrlDouble>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvTimeString &source, const int16_t element, 
                    Unroll::EpicsPvTimeString &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.secPastEpoch = source.dbr().stamp().sec();
  dest.nsec = source.dbr().stamp().nsec();
  copyValueFldToUnrolled<Unroll::EpicsPvTimeString>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvTimeShort &source, const int16_t element, 
                    Unroll::EpicsPvTimeShort &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.secPastEpoch = source.dbr().stamp().sec();
  dest.nsec = source.dbr().stamp().nsec();
  copyValueFldToUnrolled<Unroll::EpicsPvTimeShort>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvTimeFloat &source, const int16_t element, 
                    Unroll::EpicsPvTimeFloat &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.secPastEpoch = source.dbr().stamp().sec();
  dest.nsec = source.dbr().stamp().nsec();
  copyValueFldToUnrolled<Unroll::EpicsPvTimeFloat>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvTimeEnum &source, const int16_t element, 
                    Unroll::EpicsPvTimeEnum &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.secPastEpoch = source.dbr().stamp().sec();
  dest.nsec = source.dbr().stamp().nsec();
  copyValueFldToUnrolled<Unroll::EpicsPvTimeEnum>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvTimeChar &source, const int16_t element, 
                    Unroll::EpicsPvTimeChar &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.secPastEpoch = source.dbr().stamp().sec();
  dest.nsec = source.dbr().stamp().nsec();
  copyValueFldToUnrolled<Unroll::EpicsPvTimeChar>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvTimeLong &source, const int16_t element, 
                    Unroll::EpicsPvTimeLong &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.secPastEpoch = source.dbr().stamp().sec();
  dest.nsec = source.dbr().stamp().nsec();
  copyValueFldToUnrolled<Unroll::EpicsPvTimeLong>(source,element,dest);
}

void copyToUnrolled(const Psana::Epics::EpicsPvTimeDouble &source, const int16_t element, 
                    Unroll::EpicsPvTimeDouble &dest) 
{
  dest.iPvId = source.pvId();
  dest.iDbrType = source.dbrType();
  dest.iNumElements = source.numElements();
  dest.status = source.dbr().status();
  dest.severity = source.dbr().severity();
  dest.secPastEpoch = source.dbr().stamp().sec();
  dest.nsec = source.dbr().stamp().nsec();
  copyValueFldToUnrolled<Unroll::EpicsPvTimeDouble>(source,element,dest);
}

 

template <>
void copyValueFldToUnrolled < Unroll::EpicsPvTimeString >
       (const Unroll::EpicsPvTimeString::PsanaSrc &psanaVar, int16_t el, 
        Unroll::EpicsPvTimeString & unrollBuffer) {
  strncpy(unrollBuffer.value, psanaVar.value(el), Psana::Epics::MAX_STRING_SIZE);
}

template <>
void copyValueFldToUnrolled < Unroll::EpicsPvCtrlString >
       (const Unroll::EpicsPvCtrlString::PsanaSrc &psanaVar, int16_t el, 
        Unroll::EpicsPvCtrlString & unrollBuffer) {
  strncpy(unrollBuffer.value, psanaVar.value(el), Psana::Epics::MAX_STRING_SIZE);
}

hid_t createH5TypeId_EpicsPvCtrlString(hid_t pvNameType, hid_t stringType) {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvCtrlString));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvCtrlString");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvCtrlString, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvCtrlString, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvCtrlString, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "pvname", offsetof(Unroll::EpicsPvCtrlString, sPvName), pvNameType));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvCtrlString, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvCtrlString, severity), H5T_NATIVE_INT16));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvCtrlString, value), stringType));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvCtrlString"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvCtrlShort(hid_t pvNameType, hid_t unitsType) {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvCtrlShort));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvCtrlShort");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvCtrlShort, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvCtrlShort, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvCtrlShort, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "pvname", offsetof(Unroll::EpicsPvCtrlShort, sPvName), pvNameType));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvCtrlShort, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvCtrlShort, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "units", offsetof(Unroll::EpicsPvCtrlShort, units), unitsType));
  status = std::min(status, H5Tinsert(typeId, "upper_disp_limit", offsetof(Unroll::EpicsPvCtrlShort, upper_disp_limit), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "lower_disp_limit", offsetof(Unroll::EpicsPvCtrlShort, lower_disp_limit), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "upper_alarm_limit", offsetof(Unroll::EpicsPvCtrlShort, upper_alarm_limit), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "upper_warning_limit", offsetof(Unroll::EpicsPvCtrlShort, upper_warning_limit), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "lower_warning_limit", offsetof(Unroll::EpicsPvCtrlShort, lower_warning_limit), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "lower_alarm_limit", offsetof(Unroll::EpicsPvCtrlShort, lower_alarm_limit), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "upper_ctrl_limit", offsetof(Unroll::EpicsPvCtrlShort, upper_ctrl_limit), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "lower_ctrl_limit", offsetof(Unroll::EpicsPvCtrlShort, lower_ctrl_limit), H5T_NATIVE_INT16));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvCtrlShort, value), H5T_NATIVE_INT16));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvCtrlShort"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvCtrlFloat(hid_t pvNameType, hid_t unitsType) {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvCtrlFloat));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvCtrlFloat");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvCtrlFloat, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvCtrlFloat, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvCtrlFloat, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "pvname", offsetof(Unroll::EpicsPvCtrlFloat, sPvName), pvNameType));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvCtrlFloat, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvCtrlFloat, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "precision", offsetof(Unroll::EpicsPvCtrlFloat, precision), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "units", offsetof(Unroll::EpicsPvCtrlFloat, units), unitsType));
  status = std::min(status, H5Tinsert(typeId, "upper_disp_limit", offsetof(Unroll::EpicsPvCtrlFloat, upper_disp_limit), H5T_NATIVE_FLOAT));
  status = std::min(status, H5Tinsert(typeId, "lower_disp_limit", offsetof(Unroll::EpicsPvCtrlFloat, lower_disp_limit), H5T_NATIVE_FLOAT));
  status = std::min(status, H5Tinsert(typeId, "upper_alarm_limit", offsetof(Unroll::EpicsPvCtrlFloat, upper_alarm_limit), H5T_NATIVE_FLOAT));
  status = std::min(status, H5Tinsert(typeId, "upper_warning_limit", offsetof(Unroll::EpicsPvCtrlFloat, upper_warning_limit), H5T_NATIVE_FLOAT));
  status = std::min(status, H5Tinsert(typeId, "lower_warning_limit", offsetof(Unroll::EpicsPvCtrlFloat, lower_warning_limit), H5T_NATIVE_FLOAT));
  status = std::min(status, H5Tinsert(typeId, "lower_alarm_limit", offsetof(Unroll::EpicsPvCtrlFloat, lower_alarm_limit), H5T_NATIVE_FLOAT));
  status = std::min(status, H5Tinsert(typeId, "upper_ctrl_limit", offsetof(Unroll::EpicsPvCtrlFloat, upper_ctrl_limit), H5T_NATIVE_FLOAT));
  status = std::min(status, H5Tinsert(typeId, "lower_ctrl_limit", offsetof(Unroll::EpicsPvCtrlFloat, lower_ctrl_limit), H5T_NATIVE_FLOAT));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvCtrlFloat, value), H5T_NATIVE_FLOAT));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvCtrlFloat"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvCtrlEnum(hid_t pvNameType, hid_t allEnumStrsType) {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvCtrlEnum));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvCtrlEnum");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvCtrlEnum, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvCtrlEnum, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvCtrlEnum, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "pvname", offsetof(Unroll::EpicsPvCtrlEnum, sPvName), pvNameType));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvCtrlEnum, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvCtrlEnum, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "no_str", offsetof(Unroll::EpicsPvCtrlEnum, no_str), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "strs", offsetof(Unroll::EpicsPvCtrlEnum, strs), allEnumStrsType));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvCtrlEnum, value), H5T_NATIVE_UINT16));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvCtrlEnum"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvCtrlChar(hid_t pvNameType, hid_t unitsType) {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvCtrlChar));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvCtrlChar");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvCtrlChar, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvCtrlChar, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvCtrlChar, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "pvname", offsetof(Unroll::EpicsPvCtrlChar, sPvName), pvNameType));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvCtrlChar, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvCtrlChar, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "units", offsetof(Unroll::EpicsPvCtrlChar, units), unitsType));
  status = std::min(status, H5Tinsert(typeId, "upper_disp_limit", offsetof(Unroll::EpicsPvCtrlChar, upper_disp_limit), H5T_NATIVE_UINT8));
  status = std::min(status, H5Tinsert(typeId, "lower_disp_limit", offsetof(Unroll::EpicsPvCtrlChar, lower_disp_limit), H5T_NATIVE_UINT8));
  status = std::min(status, H5Tinsert(typeId, "upper_alarm_limit", offsetof(Unroll::EpicsPvCtrlChar, upper_alarm_limit), H5T_NATIVE_UINT8));
  status = std::min(status, H5Tinsert(typeId, "upper_warning_limit", offsetof(Unroll::EpicsPvCtrlChar, upper_warning_limit), H5T_NATIVE_UINT8));
  status = std::min(status, H5Tinsert(typeId, "lower_warning_limit", offsetof(Unroll::EpicsPvCtrlChar, lower_warning_limit), H5T_NATIVE_UINT8));
  status = std::min(status, H5Tinsert(typeId, "lower_alarm_limit", offsetof(Unroll::EpicsPvCtrlChar, lower_alarm_limit), H5T_NATIVE_UINT8));
  status = std::min(status, H5Tinsert(typeId, "upper_ctrl_limit", offsetof(Unroll::EpicsPvCtrlChar, upper_ctrl_limit), H5T_NATIVE_UINT8));
  status = std::min(status, H5Tinsert(typeId, "lower_ctrl_limit", offsetof(Unroll::EpicsPvCtrlChar, lower_ctrl_limit), H5T_NATIVE_UINT8));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvCtrlChar, value), H5T_NATIVE_UINT8));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvCtrlChar"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvCtrlLong(hid_t pvNameType, hid_t unitsType) {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvCtrlLong));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvCtrlLong");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvCtrlLong, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvCtrlLong, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvCtrlLong, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "pvname", offsetof(Unroll::EpicsPvCtrlLong, sPvName), pvNameType));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvCtrlLong, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvCtrlLong, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "units", offsetof(Unroll::EpicsPvCtrlLong, units), unitsType));
  status = std::min(status, H5Tinsert(typeId, "upper_disp_limit", offsetof(Unroll::EpicsPvCtrlLong, upper_disp_limit), H5T_NATIVE_INT32));
  status = std::min(status, H5Tinsert(typeId, "lower_disp_limit", offsetof(Unroll::EpicsPvCtrlLong, lower_disp_limit), H5T_NATIVE_INT32));
  status = std::min(status, H5Tinsert(typeId, "upper_alarm_limit", offsetof(Unroll::EpicsPvCtrlLong, upper_alarm_limit), H5T_NATIVE_INT32));
  status = std::min(status, H5Tinsert(typeId, "upper_warning_limit", offsetof(Unroll::EpicsPvCtrlLong, upper_warning_limit), H5T_NATIVE_INT32));
  status = std::min(status, H5Tinsert(typeId, "lower_warning_limit", offsetof(Unroll::EpicsPvCtrlLong, lower_warning_limit), H5T_NATIVE_INT32));
  status = std::min(status, H5Tinsert(typeId, "lower_alarm_limit", offsetof(Unroll::EpicsPvCtrlLong, lower_alarm_limit), H5T_NATIVE_INT32));
  status = std::min(status, H5Tinsert(typeId, "upper_ctrl_limit", offsetof(Unroll::EpicsPvCtrlLong, upper_ctrl_limit), H5T_NATIVE_INT32));
  status = std::min(status, H5Tinsert(typeId, "lower_ctrl_limit", offsetof(Unroll::EpicsPvCtrlLong, lower_ctrl_limit), H5T_NATIVE_INT32));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvCtrlLong, value), H5T_NATIVE_INT32));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvCtrlLong"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvCtrlDouble(hid_t pvNameType, hid_t unitsType) {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvCtrlDouble));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvCtrlDouble");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvCtrlDouble, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvCtrlDouble, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvCtrlDouble, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "pvname", offsetof(Unroll::EpicsPvCtrlDouble, sPvName), pvNameType));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvCtrlDouble, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvCtrlDouble, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "precision", offsetof(Unroll::EpicsPvCtrlDouble, precision), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "units", offsetof(Unroll::EpicsPvCtrlDouble, units), unitsType));
  status = std::min(status, H5Tinsert(typeId, "upper_disp_limit", offsetof(Unroll::EpicsPvCtrlDouble, upper_disp_limit), H5T_NATIVE_DOUBLE));
  status = std::min(status, H5Tinsert(typeId, "lower_disp_limit", offsetof(Unroll::EpicsPvCtrlDouble, lower_disp_limit), H5T_NATIVE_DOUBLE));
  status = std::min(status, H5Tinsert(typeId, "upper_alarm_limit", offsetof(Unroll::EpicsPvCtrlDouble, upper_alarm_limit), H5T_NATIVE_DOUBLE));
  status = std::min(status, H5Tinsert(typeId, "upper_warning_limit", offsetof(Unroll::EpicsPvCtrlDouble, upper_warning_limit), H5T_NATIVE_DOUBLE));
  status = std::min(status, H5Tinsert(typeId, "lower_warning_limit", offsetof(Unroll::EpicsPvCtrlDouble, lower_warning_limit), H5T_NATIVE_DOUBLE));
  status = std::min(status, H5Tinsert(typeId, "lower_alarm_limit", offsetof(Unroll::EpicsPvCtrlDouble, lower_alarm_limit), H5T_NATIVE_DOUBLE));
  status = std::min(status, H5Tinsert(typeId, "upper_ctrl_limit", offsetof(Unroll::EpicsPvCtrlDouble, upper_ctrl_limit), H5T_NATIVE_DOUBLE));
  status = std::min(status, H5Tinsert(typeId, "lower_ctrl_limit", offsetof(Unroll::EpicsPvCtrlDouble, lower_ctrl_limit), H5T_NATIVE_DOUBLE));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvCtrlDouble, value), H5T_NATIVE_DOUBLE));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvCtrlDouble"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvTimeString(hid_t stringType) {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvTimeString));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvTimeString");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvTimeString, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvTimeString, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvTimeString, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvTimeString, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvTimeString, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "secPastEpoch", offsetof(Unroll::EpicsPvTimeString, secPastEpoch), H5T_NATIVE_UINT32));
  status = std::min(status, H5Tinsert(typeId, "nsec", offsetof(Unroll::EpicsPvTimeString, nsec), H5T_NATIVE_UINT32));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvTimeString, value), stringType));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvTimeString"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvTimeShort() {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvTimeShort));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvTimeShort");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvTimeShort, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvTimeShort, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvTimeShort, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvTimeShort, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvTimeShort, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "secPastEpoch", offsetof(Unroll::EpicsPvTimeShort, secPastEpoch), H5T_NATIVE_UINT32));
  status = std::min(status, H5Tinsert(typeId, "nsec", offsetof(Unroll::EpicsPvTimeShort, nsec), H5T_NATIVE_UINT32));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvTimeShort, value), H5T_NATIVE_INT16));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvTimeShort"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvTimeFloat() {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvTimeFloat));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvTimeFloat");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvTimeFloat, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvTimeFloat, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvTimeFloat, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvTimeFloat, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvTimeFloat, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "secPastEpoch", offsetof(Unroll::EpicsPvTimeFloat, secPastEpoch), H5T_NATIVE_UINT32));
  status = std::min(status, H5Tinsert(typeId, "nsec", offsetof(Unroll::EpicsPvTimeFloat, nsec), H5T_NATIVE_UINT32));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvTimeFloat, value), H5T_NATIVE_FLOAT));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvTimeFloat"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvTimeEnum() {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvTimeEnum));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvTimeEnum");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvTimeEnum, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvTimeEnum, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvTimeEnum, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvTimeEnum, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvTimeEnum, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "secPastEpoch", offsetof(Unroll::EpicsPvTimeEnum, secPastEpoch), H5T_NATIVE_UINT32));
  status = std::min(status, H5Tinsert(typeId, "nsec", offsetof(Unroll::EpicsPvTimeEnum, nsec), H5T_NATIVE_UINT32));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvTimeEnum, value), H5T_NATIVE_UINT16));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvTimeEnum"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvTimeChar() {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvTimeChar));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvTimeChar");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvTimeChar, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvTimeChar, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvTimeChar, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvTimeChar, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvTimeChar, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "secPastEpoch", offsetof(Unroll::EpicsPvTimeChar, secPastEpoch), H5T_NATIVE_UINT32));
  status = std::min(status, H5Tinsert(typeId, "nsec", offsetof(Unroll::EpicsPvTimeChar, nsec), H5T_NATIVE_UINT32));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvTimeChar, value), H5T_NATIVE_UINT8));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvTimeChar"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvTimeLong() {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvTimeLong));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvTimeLong");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvTimeLong, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvTimeLong, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvTimeLong, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvTimeLong, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvTimeLong, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "secPastEpoch", offsetof(Unroll::EpicsPvTimeLong, secPastEpoch), H5T_NATIVE_UINT32));
  status = std::min(status, H5Tinsert(typeId, "nsec", offsetof(Unroll::EpicsPvTimeLong, nsec), H5T_NATIVE_UINT32));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvTimeLong, value), H5T_NATIVE_INT32));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvTimeLong"); 

  return typeId;
}

hid_t createH5TypeId_EpicsPvTimeDouble() {
  hid_t typeId = H5Tcreate(H5T_COMPOUND, sizeof(Unroll::EpicsPvTimeDouble));
  if (typeId < 0) MsgLog(logger, fatal, "Failed to create h5 type id for EpicsPvTimeDouble");
  herr_t status = 0;
  status = std::min(status, H5Tinsert(typeId, "pvId", offsetof(Unroll::EpicsPvTimeDouble, iPvId), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "dbrType", offsetof(Unroll::EpicsPvTimeDouble, iDbrType), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "numElements", offsetof(Unroll::EpicsPvTimeDouble, iNumElements), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "status", offsetof(Unroll::EpicsPvTimeDouble, status), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "severity", offsetof(Unroll::EpicsPvTimeDouble, severity), H5T_NATIVE_INT16));
  status = std::min(status, H5Tinsert(typeId, "secPastEpoch", offsetof(Unroll::EpicsPvTimeDouble, secPastEpoch), H5T_NATIVE_UINT32));
  status = std::min(status, H5Tinsert(typeId, "nsec", offsetof(Unroll::EpicsPvTimeDouble, nsec), H5T_NATIVE_UINT32));
 
  status = std::min(status, H5Tinsert(typeId, "value", offsetof(Unroll::EpicsPvTimeDouble, value), H5T_NATIVE_DOUBLE));

  if (status < 0) MsgLog(logger, fatal, "error inserting field into h5 typeId for EpicsPvTimeDouble"); 

  return typeId;
}

 

} // Translator
