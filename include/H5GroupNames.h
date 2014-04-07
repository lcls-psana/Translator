#ifndef TRANSLATOR_H5GROUPNAMES_H
#define TRANSLATOR_H5GROUPNAMES_H

#include <string>
#include <typeinfo>
#include "pdsdata/xtc/Src.hh"
#include "Translator/TypeAliases.h"

namespace Translator {

/**
 *  @ingroup Translator
 *
 *  @brief transforms C++ Psana types and src locations into hdf5 group names.
 *
 *  Also returns true if a C++ type is a NDArray, requires the set of 
 *  NDArray types recognized in the system to be passed in for this.
 *
 *  @note This software was developed for the LCLS project.  If you use all or 
 *  part of it, please give an appropriate acknowledgment.
 *
 *  @author David Schneider
 */
class H5GroupNames {
 public:
  H5GroupNames(bool short_bld_name, 
               const TypeAliases::TypeInfoSet & ndarrays);
  /**
   * @brief returns H5 group name for a C++ type
   *
   * This method returns the string used for the H5 group for data of this
   * type. The is Generally based on the C++ type name, however modifications
   * are made to be backward compatible with o2o-translate as well as to 
   * simplify some names. In particular all ndarrays go under a common name.
   *
   * @param[in] typeInfoPtr type of object for the group
   * @return a non empty string name for the h5 group
   */
  std::string nameForType(const std::type_info *typeInfoPtr);

  /**
   * @brief returns h5 group name for a Pds::Src
   *
   * This method returns the string used for the H5 group for data from the
   * given Pds::Src. This is most often the same as what the Psana Module
   * EventKeys prints, however adjustments are made for some sources to 
   * produce names appropriate for h5 files. In particular:
   *   @li no spaces or asterick's are returned.
   *   @li any src where the level is Control returns "Control"
   *   @li any src where the level is Event return "Event"
   *   @li the special values noSource and anySource return "noSrc"
   *
   * @param[in] src the Pds::Src for the group
   * @return non empty string name for the h5 group
   */
  std::string nameForSrc(const Pds::Src &src);

  /**
   * @brief returns h5 group name for a Pds::Src and key
   *
   * If the key is empty, just the src is returned. For a non empty
   * key, the H5 group name is a concatenation of the two. A special 
   * string is used to separate the src from the key in the concatenation. 
   * The key string checked for the "do not translate" string, as well as 
   * for characters that are problemeatic for h5 filenames. The cleaned key 
   * string is used in the group name. 
   *
   * @param[in] src the Pds::Src for the group
   * @param[in] key the key string for the group
   * @return non empty string name for the h5 group.
   */
  std::string nameForSrcKey(const Pds::Src &src, const std::string &key);

  /**
   * @brief returns h5 group name for a alias string and key
   *
   * If the alias is empty, and empty string is returned. Otherwise the H5 
   * group name for an alias,key pair is a concatenation of the two. 
   * Otherwise, a special string is used to separate the src
   * from the key in the concatenation. It the alias itself contains this
   * special substring, a warning is printed and an empty string is returned.
   * The alias string is further checked for the "do not translate" string, as 
   * well as for characters that are problemeatic for h5 filenames. The cleaned 
   * key string is used in the group name.
   *
   * @param[in] src the Pds::Src for the group
   * @return string name for the h5 group, empty if alias is empty.
   */
  std::string nameForAliasKey(const std::string &alias, const std::string &key);

  /**
   * @brief returns true if the type is one of the known NDArrays.
   *
   * @param[in] C++ type.
   * @return true if it is a known NDArray.
   */
  bool isNDArray(const std::type_info *typeInfoPtr) { 
    return m_ndarrays.find(typeInfoPtr) != m_ndarrays.end(); 
  }
  /**
   * @brief returns the string used to separate a src (or alias) from a key
   */
  std::string srcKeySep();

 private:

  bool m_short_bld_name;
  const TypeAliases::TypeInfoSet m_ndarrays;
}; // class H5GroupNames

} // namespace

#endif
