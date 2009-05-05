#ifndef _itkImview_txx
#define _itkImview_txx

#include "itkImview.h"
#include "itkPixelTraits.h"
#include "imclient.h"
#include <cstdio>

namespace itk
{

template<class TImage>
int
Imview<TImage>
::ImviewLogin( int port )
{
  // connect to the imview server using defaults
  int connectionID=-1;
  int status=0;

  status = imviewlogin(NULL, NULL, port, &connectionID);
  if (!status)
    {
    std::runtime_error("Login to imview failed");
    }
  return(connectionID);
}


template<class TImage>
int
Imview<TImage>
::ImviewPutImage(ImageType *image, int connection, const char *title )
{
  IMAGE hIMAGE;
  if( !image )
    {
    throw std::runtime_error("Input image is null");
    }

  image->Update();
  hIMAGE = mkImage(image);
  //LIAREnableDebug();
  int status = imviewputimage(&hIMAGE, title, connection);
  delete(hIMAGE.buff);
  return status;
}

template<class TImage>
int
Imview<TImage>
::ImviewPutOverlay(ImageType *image, int connection, const char *title )
{
  IMAGE hIMAGE;
  if( !image )
    {
    throw std::runtime_error("Input image is null");
    }

  image->Update();
  hIMAGE = mkImage(image);
  //LIAREnableDebug();
  int status = imviewputoverlay(&hIMAGE, title, connection);
  delete(hIMAGE.buff);
  return status;
}


template<class TImage>
char *
Imview<TImage>
::ImviewSendCommand(const char *cmd, int conn_id)
{
  return imviewsendcommand(cmd, conn_id);
}

template<class TImage>
int
Imview<TImage>
::ImviewLink(const int conn_id1, const int conn_id2)
{
  return imviewlink(conn_id1, conn_id2);
}

template<class TImage>
IMAGE
Imview<TImage>
::mkImage(ImageType *image)
{
  IMAGE hIMAGE;
  SizeType size = image->GetBufferedRegion().GetSize();
  IndexType start = image->GetBufferedRegion().GetIndex();
  hIMAGE.ox = start[0];
  hIMAGE.oy = start[1];
  if (ImageDimension == 3)
    hIMAGE.oz = start[2];
  else
    hIMAGE.oz = 0;
  hIMAGE.ot = 0; //imview can only handle 3D

  hIMAGE.nx = size[0];
  hIMAGE.ny = size[1];
  if (ImageDimension == 3)
    hIMAGE.nz = size[2];
  else
    hIMAGE.nz = 1;
  hIMAGE.nt = 1;
  hIMAGE.it = IM_SINGLE;  // nothing fancy at the moment
  hIMAGE.nc = 1;          // these will need to change for colour
			  // images
#if 0
  hImage.it = IM_RGB;
  hImage.nc = 3;
#endif
  hIMAGE.pt = GetPixType();
  //std::cout << size << " " << start << std::endl;
  typedef  void * vpoint;
  hIMAGE.buff = new vpoint[1];
  hIMAGE.buff[0] = static_cast < void * > (image->GetBufferPointer());
  return hIMAGE;
}

template<class TImage>
pixtype
Imview<TImage>
::GetPixType(void)
{
  pixtype item_type;
  typedef typename PixelTraits< PixelType >::ValueType    ScalarType;
  if(typeid(ScalarType) == typeid(double))
    {
    item_type = IM_DOUBLE;
    }
  else if(typeid(ScalarType) == typeid(float))
    {
    item_type = IM_FLOAT;
    }
  else if(typeid(ScalarType) == typeid(long))
    {
    item_type = IM_INT8;
    }
  else if(typeid(ScalarType) == typeid(unsigned long))
    {
    item_type = IM_UINT8;
    }
  else if(typeid(ScalarType) == typeid(int))
    {
    item_type = IM_INT4;
    }
  else if(typeid(ScalarType) == typeid(unsigned int))
    {
    item_type = IM_UINT4;
    }
  else if(typeid(ScalarType) == typeid(short))
    {
    item_type = IM_INT2;
    }
  else if(typeid(ScalarType) == typeid(unsigned short))
    {
    item_type = IM_UINT2;
    }
  else if(typeid(ScalarType) == typeid(signed char))
    {
    item_type = IM_INT1;
    }
  else if(typeid(ScalarType) == typeid(unsigned char))
    {
    item_type = IM_UINT1;
    }
  else
    {
    item_type = IM_BINARY; // no good reason for this
    throw std::runtime_error("Type currently not supported");
    }
  return item_type;
}

} // namespace itk

#endif

