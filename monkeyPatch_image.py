""" Monkey patch para arreglar un bug que no permitia exportar la grafica como imagen """

from pyqtgraph.exporters.Exporter import Exporter
from pyqtgraph.parametertree import Parameter
from pyqtgraph.Qt import QtGui, QtCore, QtSvg, USE_PYSIDE
from pyqtgraph import functions as fn
import numpy as np

def export(self, fileName=None, toBytes=False, copy=False):
    if fileName is None and not toBytes and not copy:
        if USE_PYSIDE:
            filter = ["*."+str(f) for f in QtGui.QImageWriter.supportedImageFormats()]
        else:
            filter = ["*."+bytes(f).decode('utf-8') for f in QtGui.QImageWriter.supportedImageFormats()]
        preferred = ['*.png', '*.tif', '*.jpg']
        for p in preferred[::-1]:
            if p in filter:
                filter.remove(p)
                filter.insert(0, p)
        self.fileSaveDialog(filter=filter)
        return
            
    targetRect = QtCore.QRect(0, 0, self.params['width'], self.params['height'])
    sourceRect = self.getSourceRect()
        
        
    #self.png = QtGui.QImage(targetRect.size(), QtGui.QImage.Format_ARGB32)
    #self.png.fill(pyqtgraph.mkColor(self.params['background']))
    w, h = self.params['width'], self.params['height']
    if w == 0 or h == 0:
        raise Exception("Cannot export image with size=0 (requested export size is %dx%d)" % (w,h))
    
    # linea cambiada - se agregaron las funciones int()
    bg = np.empty((int(self.params['width']), int(self.params['height']), 4), dtype=np.ubyte)
    # -------------------------------------------------
    
    color = self.params['background']
    bg[:,:,0] = color.blue()
    bg[:,:,1] = color.green()
    bg[:,:,2] = color.red()
    bg[:,:,3] = color.alpha()
    self.png = fn.makeQImage(bg, alpha=True)
        
    ## set resolution of image:
    origTargetRect = self.getTargetRect()
    resolutionScale = targetRect.width() / origTargetRect.width()
    #self.png.setDotsPerMeterX(self.png.dotsPerMeterX() * resolutionScale)
    #self.png.setDotsPerMeterY(self.png.dotsPerMeterY() * resolutionScale)
        
    painter = QtGui.QPainter(self.png)
    #dtr = painter.deviceTransform()
    try:
        self.setExportMode(True, {'antialias': self.params['antialias'], 'background': self.params['background'], 'painter': painter, 'resolutionScale': resolutionScale})
        painter.setRenderHint(QtGui.QPainter.Antialiasing, self.params['antialias'])
        self.getScene().render(painter, QtCore.QRectF(targetRect), QtCore.QRectF(sourceRect))
    finally:
        self.setExportMode(False)
    painter.end()
        
    if copy:
        QtGui.QApplication.clipboard().setImage(self.png)
    elif toBytes:
        return self.png
    else:
        self.png.save(fileName)
