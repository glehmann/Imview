class imview :
    """An interface for using imview from python/itk"""
    def __init__(self, input=None, title="noname") :
        """ Create the imview process and transmit an image to it if desired"""
        # start imview, retrieving port number
        self.__StartImview__()
        self.connected = False
        if not input is None:
            self.Show(input, title)
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
        import itk
        itkIm = itk.image(itkIm)
        if not self.connected :
            # do the login now that we have an image type
            self.imviewObj = itk.Imview[itkIm]
            self.Connection = self.imviewObj.ImviewLogin(self.portNum)
            self.connected = True
            print "Connected"
            print self.Connection
            self.ImageTemp = itk.template(itkIm)[1]
        else:
            if itk.template(itkIm)[1] != self.ImageTemp:
                self.ImageTemp = itk.template(itkIm)[1] 
                self.imviewObj = itk.Imview[itkIm]
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
        import itk
        itkIm = itk.image(itkIm)
        if not self.connected :
            print "No image being viewed - send one first"
        else:
            if itk.template(itkIm)[1] != self.ImageTemp:
                self.ImageTemp = itk.template(itkIm)[1] 
                self.imviewObj = itk.Imview[itkIm]
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
            response = self.parsePointfile(response)
            return response
    #
    def parsePointfile(self, pfstring):
        import re
        if (pfstring == 'Empty\n'):
            return []
        eol=re.compile("\n")
        white=re.compile(r'\s+')
        lines = eol.split(pfstring)
        # if there is no comment line at the beginning, then it is an old
        # style pointfile for a grayscale image
        if (lines[0][0] == '#'):
            # advance pointfile
            result=[]
            # second line contains the column names
            thisGroup=[]
            groups = 0
            colnames=white.split(lines[2])[1:9]
            for i in range(3, len(lines)):
                if (len(lines[i]) > 0):
                    if (lines[i].find('break') >= 0):
                        result.append(thisGroup)
                        thisGroup=[]
                        groups = groups + 1
                    else:
                        sp = white.split(lines[i].strip())
                        ThisLine={}
                        for j in range(len(colnames)):
                            ThisLine[colnames[j]] = float(sp[j])
                        thisGroup.append(ThisLine)
            if (groups==0):
                result.append(thisGroup)
        else:
            # simple point file - 2d, grayscale
            # produce a list of dictionaries
            result=[]
            thisGroup=[]
            groups = 0
            for i in range(len(lines)):
                if (len(lines[i]) > 0):
                    if (lines[i] == 'break'):
                        result.append(thisGroup)
                        thisGroup=[]
                        groups = groups + 1
                    else:
                        sp = white.split(lines[i])
                        x = int(sp[0])
                        y = int(sp[1])
                        g = float(sp[2])
                        thisGroup.append({"X" : x, "Y" : y, "G" : g})
            if (groups==0):
                result.append(thisGroup)
        return result
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
            self.imviewObj.ImviewSendCommand(cmd, self.Connection)
    #
    def CloseOverlay(self):
        """Close an image defined by title - the default action closes the overlay"""
        if not self.connected :
            print "No image being viewed - send one first"
        else:
            title="<overlay>"
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
