#ifndef TRANSLATOR_HDFWRITERFILTERMSG_H
#define TRANSLATOR_HDFWRITERFILTERMSG_H

#include <string>
#include <map>

#include "hdf5/hdf5.h"

#include "hdf5pp/Group.h"
#include "PSEvt/EventId.h"

#include "Translator/DataSetPos.h"
#include "Translator/DataSetCreationProperties.h"
#include "Translator/HdfWriterGeneric.h"

namespace Translator {

class HdfWriterFilterMsg {
 public:
  HdfWriterFilterMsg();
  ~HdfWriterFilterMsg();

  void make_dataset(hdf5pp::Group & group) { make_dataset(group.id()); }
  void make_dataset(hid_t groupId);

  void append(hdf5pp::Group & group, const std::string & msg) { append(group.id(),msg); }
  void append(hid_t groupId, const std::string & msg);

  const DataSetCreationProperties & dataSetCreationProperties() 
  { return m_dataSetCreationProperties; }
  void setDatasetCreationProperties(const DataSetCreationProperties & dataSetCreationProperties) 
  { m_dataSetCreationProperties = dataSetCreationProperties; }

  void closeDataset(hdf5pp::Group &group) { closeDataset(group.id()); }
  void closeDataset(hid_t groupId);

 private:
  DataSetCreationProperties m_dataSetCreationProperties;
  hid_t m_h5typeId;
  HdfWriterGeneric m_writer;
  size_t m_dsetPos;
};

} // namespace

#endif 
