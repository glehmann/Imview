import itk
import Imview

# declare some image types
t1=itk.Image[itk.UC, 2]
t2=itk.Image[itk.US, 2]
t3=itk.Image[itk.UC, 3]
t4=itk.Image[itk.F, 3]

# load some images
reader1=itk.ImageFileReader[t1].New(FileName='images/cthead1.png')
reader2=itk.ImageFileReader[t2].New(FileName='images/cthead1.png')
reader3=itk.ImageFileReader[t3].New(FileName='images/ESCells.img')
reader4=itk.ImageFileReader[t4].New(FileName='images/ESCells.img')

# mess with the images so we have real float and short values
# an extended dynamic range image
m1 = itk.MultiplyImageFilter[t2, t2, t2].New(reader2, reader2)

f1 = itk.CosImageFilter[t4,t4].New(reader4)

# a 2d threshold image
thresh1 = itk.OtsuThresholdImageFilter[t1, t1].New(reader1)
thresh1.SetInsideValue(1)
thresh1.SetOutsideValue(0)

# a 3d threshold image
thresh2 = itk.OtsuThresholdImageFilter[t3, t3].New(reader3)
thresh2.SetInsideValue(1)
thresh2.SetOutsideValue(0)

# Should be no need to call the update - done by imview client interface

# create an imview instance

v1=itk.imview()
v1.Show(reader1, title="char image")
v1.Show(m1, title="short image")

# another instance - 3d this time
# Move between planes using "insert" and "delete"
v2 = itk.imview(reader3, title="ESCells raw")
v2.Show(f1, title="3d float")

# send the overlay - these will be placed over the currently visible image
v1.Overlay(thresh1)
v2.Overlay(thresh2)

# create another instance of imview for cthead
v1a=itk.imview(reader1)
# change the colourmap
v1a.ColorMap("inv_spiral.lut")
# link with v1
v1a.Link([v1])
# They are now syncronized - zoom in on one of the instances and watch
# the other match the view. Use the mouse for this

#close the overlay
v1.CloseOverlay()


# retrieve pointfiles
