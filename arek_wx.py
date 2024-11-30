#// First things, first. Import the wxPython package.
#import wx
#
#// Next, create an application object.
#app = wx.App()
#
#// Then a frame.
#frm = wx.Frame(None, title="Hello World")
#
#// Show it.
#frm.Show()
#
#// Start the event loop.
#app.MainLoop()


import os
import wx
import time
from threading import Thread

#-------------------------------------------------------------------------------

# OBD variables
BACKGROUND_FILENAME = "bg_black.jpg"
LOGO_FILENAME 		= "cowfish.png"

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------

class OBDFrame(wx.Frame):
    """
    OBD frame.
    """

    def __init__(self):
        """
        Constructor.
        """
        wx.Frame.__init__(self, None, wx.ID_ANY, "OBD-Pi")

        image = wx.Image(BACKGROUND_FILENAME) 
        width, height = wx.GetDisplaySize() 
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        self.bitmap = wx.BitmapFromImage(image) 
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.panelLoading = OBDLoadingPanel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panelLoading, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.panelLoading.showLoadingScreen()
        self.panelLoading.SetFocus()

        
    def update(self, event):
        if self.panelLoading:
            connection = self.panelLoading.getConnection()
            sensors = self.panelLoading.getSensors()
            port = self.panelLoading.getPort()
            self.panelLoading.Destroy()
        self.panelGauges = OBDPanelGauges(self)
        
        if connection:
            self.panelGauges.setConnection(connection)

        if sensors:
            self.panelGauges.setSensors(sensors)
            self.panelGauges.setPort(port)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panelGauges, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.panelGauges.ShowSensors()
        self.panelGauges.SetFocus()
        self.Layout()

    def OnPaint(self, event): 
        self.Paint(wx.PaintDC(self)) 

    def Paint(self, dc): 
        dc.DrawBitmap(self.bitmap, 0, 0)     
        

#-------------------------------------------------------------------------------

class OBDApp(wx.App):
    """
    OBD Application.
    """

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        """
        Constructor.
        """
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        """
        Initializer.
        """
        # Main frame                                           
        frame = OBDFrame()
        self.SetTopWindow(frame)
        frame.ShowFullScreen(True)
        frame.Show(True)
        #frame.showLoadingPanel()

        # This frame is used only to set the full screen mode  
        # for the splash screen display and for transition with 
        # the loading screen.
        # This frame is not shown and will be deleted later on.
        #frame0 = OBDFrame0()
        #self.SetTopWindow(frame0)
        #frame0.ShowFullScreen(True)
        #self.SetTopWindow(frame0)

        # Splash screen
        #splash = OBDSplashScreen(frame0, frame0)
        #self.SetTopWindow(splash)
        #splash.Show(True)
        #splash.ShowFullScreen(True)

        return True

    def FilterEvent(self, event):
        if event.GetEventType == wx.KeyEvent:
            pass

#-------------------------------------------------------------------------------

app = OBDApp(False)
app.MainLoop()

#-------------------------------------------------------------------------------
