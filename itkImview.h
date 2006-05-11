#ifndef _itkImview_h
#define _itkImview_h

#include "itkObject.h"
#include "itkObjectFactory.h"
#include "liarwrap.h"

namespace itk
{

/** \Class Imview
 *  \brief Transmit itk images to imview
 * 
 *
 */

template <typename TImage>
class Imview
{
public:
  ///! Standard "Self" typedef.
  typedef Imview         Self;

  /// Type of the image from where the buffer will be converted
  typedef TImage                              ImageType;
  typedef typename ImageType::PixelType       PixelType;
  typedef typename ImageType::SizeType        SizeType;
  typedef typename ImageType::IndexType       IndexType;
  typedef typename ImageType::RegionType      RegionType;
  typedef typename ImageType::PointType       PointType;
  typedef typename ImageType::SpacingType     SpacingType;
  typedef typename ImageType::Pointer         ImagePointer;

   /** Image dimension. */
  itkStaticConstMacro(ImageDimension, unsigned int,
                      ImageType::ImageDimension);


  static int ImviewLogin(int port);
 
  static int ImviewPutImage(ImageType *image, int connection, const char *title);
  static int ImviewPutOverlay(ImageType *image, int connection, const char *title);
  static char *ImviewSendCommand(const char *cmd, int conn_id);
  static int ImviewLink(const int conn_id1, const int conn_id2);

protected:
  
  Imview(const Self&);     // Not implemented.
  void operator=(const Self&); // Not implemented.
  
  static pixtype GetPixType(void);
  static IMAGE mkImage(ImageType *image);
};


} // namespace itk

#ifndef ITK_MANUAL_INSTANTIATION
#include "itkImview.txx"
#endif

#endif // _itkImview_h

