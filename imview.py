class Imview :
    """An interface for using imview from python/itk"""
    import Imview
    def __init__(self, input=None) :
        """ Create the imview process and transmit an image to it if desired"""
        # start imview, retrieving port number
        self.__StartImview__()
        self.connected = False
        if not input is None:
            self.Show(input)
    #
    def __StartImview__(self):
        """ for internal use only"""
        import os
        import re
        imviewCommand = "imview -server -fork"
        imviewPipe = os.popen(imviewCommand)
        resp = imviewPipe.readline()
        rePort = re.compile("Port:")
        self.portNum = int(rePort.sub("", resp))
    #   
    def Summary(self) :
        print self.portNum
    #
    def GetConnection(self):
        return self.Connection
    #
    def Show(self, itkIm, title="noname") :
        """ Display an image, with optional title
        If different titles are used then multiple images will be available in imview.
        Flip between them with the menu or space bar
        """
        if not self.connected :
            # do the login now that we have an image type
            self.imviewObj = itk.Imview[itkIm]
            self.Connection = self.imviewObj.ImviewLogin(self.portNum)
            self.connected = True
            print "Connected"
            print self.Connection
        # transmit the image
        status = self.imviewObj.ImviewPutImage(itkIm, self.Connection, title)
        if (status != 0):
            # Failed to send image. Assume that imview has died
            self.__StartImview__()
            status = self.imviewObj.ImviewPutImage(itkIm, self.Connection, title)
            if (status != 0):
                print "Something seriously wrong - give up on this Imview instance"
    #
    def Overlay(self, itkIm, title="noname") :
        """Send an overlay to image with specified title"""
        if not self.connected :
            print "No image being viewed - send one first"
        else:
            status = self.imviewObj.ImviewPutOverlay(itkIm, self.Connection, title)
    #
    def GetPointfile(self):
        """Retrieve a pointfile from imview"""
        if not self.connected :
            print "No image being viewed - send one first"
            return(None)
        else:
            response = self.imviewObj.ImviewSendCommand("pf\r\n", self.Connection)
            # convert pointfile to sensible structure
            return response
    #
    def Kill(self):
        """Kill the imview process"""
        if not self.connected :
            print "No image being viewed - send one first"
        else:
            self.imviewObj.ImviewSendCommand("kill\r\n", self.Connection)
    #
    def ColorMap(self, mapname):
        """Select the colourmap - the possiblities are visible on the menu"""
        if not self.connected :
            print "No image being viewed - send one first"
        else:
            cmd = "cmap " + mapname + "\r\n"
            resp = self.imviewObj.ImviewSendCommand(cmd, self.Connection)
            return resp
    #
    def Close(self, title="<overlay>"):
        """Close an image defined by title - the default action closes the overlay"""
        if not self.connected :
            print "No image being viewed - send one first"
        else:
            cmd = "close " + title + "\r\n"
            resp = self.imviewObj.ImviewSendCommand(cmd, self.Connection)
    #
    def ZoomFactor(self, factor):
        """Select a zoom value"""
        if not self.connected :
            print "No image being viewed - send one first"
        else:
            cmd = "zoom factor " + factor + "\r\n"
            resp = self.imviewObj.ImviewSendCommand(cmd, self.Connection)
    #
    def ZoomDefault(self, factor):
        """Set the default zoom factor"""
        if not self.connected :
            print "No image being viewed - send one first"
        else:
            cmd = "zoom default " + factor + "\r\n"
            resp = self.imviewObj.ImviewSendCommand(cmd, self.Connection)
    def Link(self,imviewList):
        """Link this imview with the others"""
        connlist=[]
        connlist.append(self.GetConnection())
        for i in range(len(imviewList)):
            connlist.append(imviewList[i].GetConnection())
        for i in range(len(connlist)):
            for j in range(i+1, len(connlist)):
                self.imviewObj.ImviewLink(connlist[i], connlist[j])
                self.imviewObj.ImviewLink(connlist[j], connlist[i])
