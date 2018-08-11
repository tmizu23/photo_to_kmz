# -*- coding: utf-8 -*-
"""
/***************************************************************************
 photo_to_kmz
                                 A QGIS plugin
 get lat lng from photo to kmz file
                              -------------------
        begin                : 2015-02-04
        copyright            : (C) 2015 by surchai chantee/GIS HAII
        email                : surchai@haii.or.th
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from photo_to_kmzdialog import photo_to_kmzDialog

import os.path
import shutil, errno

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import os,sys,zipfile


head_kmz='<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2"><Document id="feat_1"><Schema name="GPSHeading" id="GPSHeadingId"><SimpleField type="double" name="Heading"><displayName><![CDATA[heading]]></displayName></SimpleField></Schema>'



def get_gps_direction(data):
    try:
        GPSImgDirection = data[17]
        direction = (GPSImgDirection[0] / GPSImgDirection[1])
        return direction
    except:
        return None

def get_drone_exif(fn):
    try:
        img = Image.open(fn)
        txt = ""
        Yaw = None
        for segment, content in img.applist:
            marker, body = content.split('\x00', 1)
            if segment == 'APP1' and marker == 'http://ns.adobe.com/xap/1.0/':
                txt = body
        xmp_start = txt.find('drone-dji:FlightYawDegree=')
        xmp_end = txt.find('drone-dji:FlightPitchDegree')
        if xmp_start != xmp_end:
            Yaw = float(txt[xmp_start+27:xmp_end-5])
        return Yaw
    except IOError:
        return None

def get_exif(fn):
    ret = {}
    try:
        i = Image.open(fn)
        info = i._getexif()
        if info is not None:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
            return ret
    except IOError:
        return None


    
class photo_to_kmz:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'photo_to_kmz_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        #self.dlg = photo_to_kmzDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/photo_to_kmz/icon.png"),
            u"Photo2KMZ", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        
        

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&photo2kmz", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&photo2kmz", self.action)
        self.iface.removeToolBarIcon(self.action)






    
    # run method that performs all the real work
    def run(self):
        self.dlg = photo_to_kmzDialog()
        QObject.connect(self.dlg.buttonBox, SIGNAL("accepted()"), self.validate_entries)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed

        #QMessageBox.information(self.iface.mainWindow(),"Info",str(self.dlg.textPath.toPlainText()))
        #QMessageBox.information(self.iface.mainWindow(),"Info",str(self.dlg.textEdit.toPlainText()))

        kml_output = self.dlg.checkBox.isChecked()

        path=self.dlg.textPath.toPlainText().encode('iso-8859-11')
        OutputFile=self.dlg.textPath.toPlainText().encode('iso-8859-11')+'/'+self.dlg.textEdit.toPlainText().encode('iso-8859-11')+'.kmz'
        
        '''
        if str(self.dlg.textEdit.toPlainText()) == '' :
            QMessageBox.information(self.iface.mainWindow(),"Info",'please fill output name')

        
        if str(self.dlg.label_2.text()) == '':
            QMessageBox.information(self.iface.mainWindow(),"Info",'please chooose images folder')
        '''
        shp_id=0
        aaa=''
        if result == 1:
            new_file = open(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11'))+".csv","w")
            new_file.write("name"+","+"lat"+","+"lng"+","+"direction"+"\n")

            
            #write the_kml
            the_kml=open(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11'))+".kml","w")
            the_kml.write(head_kmz+'\n')
            
            
            #process filter
            extens = ['jpg', 'jpeg','JPG','JPEG']
            found = {x: [] for x in extens}
            
            #kml = simplekml.Kml()
            for (dirpath, dirnames, filenames) in os.walk(path):
                for filename in filenames:
                    
                    ext = filename.lower().rsplit('.', 1)[-1]
                    if ext in extens:
                        fullpath = os.path.join(dirpath, filename)
                        if kml_output:
                            kmlimagepath = os.path.join(dirpath.replace(path,"."),filename.lower()).replace("\\","/")
                        else:
                            kmlimagepath = "files/" + filename.lower()
                        a=get_exif(fullpath)
                        try:
                            if 'GPSInfo' in a:
                                if a is not None and a['GPSInfo'] !={}:
                                    #gps direction
                                    direction = get_gps_direction(a['GPSInfo'])
                                    #try getting drone direction if no gps direction
                                    if direction is None:
                                        direction = get_drone_exif(fullpath)
                                    if direction is None:
                                        arrow_style = ''
                                    else:
                                        arrow_style = '<IconStyle><Icon><href>http://www.ecoris.co.jp/images/contents_img/arrow.png</href></Icon><heading>' + str(
                                            direction) + '</heading></IconStyle>'


                                    lat = [float(x)/float(y) for x, y in a['GPSInfo'][2]]
                                    latref = a['GPSInfo'][1]
                                    lon = [float(x)/float(y) for x, y in a['GPSInfo'][4]]
                                    lonref = a['GPSInfo'][3]

                                    lat = lat[0] + lat[1]/60 + lat[2]/3600
                                    lon = lon[0] + lon[1]/60 + lon[2]/3600

                                    if latref == 'S':
                                        lat = -lat
                                    if lonref == 'W':
                                        lon = -lon
                                    datetime = a['DateTime']
                                    dt1,dt2=datetime.split()
                                    if dt1 is None:
                                        dt1='Unknow'
                                    else:
                                        dt1=dt1.replace(":","-")
                                    if dt2 is None:
                                        dt2='Unknow'

                                    if lat:
                                        x, y = lat, lon

                                        the_kml.write('<Style id="stylesel_'+str(shp_id)+'">' + arrow_style + '<BalloonStyle><text>&lt;p&gt;&lt;b&gt;Latitude:&lt;/b&gt; '+str(lat)+' &lt;b&gt;Longitude:&lt;/b&gt; '+str(lon)+' &lt;br&gt;&lt;/br&gt;&lt;b&gt;Date:&lt;/b&gt; '+str(dt1) +' &lt;b&gt;Time:&lt;/b&gt; '+str(dt2)+' &lt;b&gt;direction:&lt;/b&gt; '+str(direction)+'&lt;/p&gt; &lt;table width=400 cellpadding=0 cellspacing=0"&gt;  &lt;tbody&gt;&lt;tr&gt;&lt;td&gt;&lt;img width=80%" src="'+str(kmlimagepath)+'"&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/tbody&gt;&lt;/table&gt;&lt;div align="left"&gt;&lt;font color="green"&gt;&lt;b&gt;Created by GIS-HAII&lt;/b&gt;&lt;/font&gt;&lt;/div&gt;</text><displayMode>default</displayMode></BalloonStyle></Style>'+'\n')
                                        aaa=aaa+'<Placemark id="feat_'+str(shp_id)+'"><name>'+str(filename.lower())+'</name><TimeStamp><when>'+str(dt1)+'T'+str(dt2)+'+09'+'</when></TimeStamp><styleUrl>#stylesel_'+str(shp_id)+'</styleUrl><Point id="geom_'+str(shp_id)+'"><coordinates>'+str(lon)+','+str(lat)+',0.0</coordinates></Point>'
                                        if direction is not None:
                                            aaa = aaa+'<ExtendedData><SchemaData schemaUrl="#GPSHeadingId"><SimpleData name="Heading">'+str(direction)+'</SimpleData></SchemaData></ExtendedData>'
                                        aaa=aaa+'</Placemark>'+'\n'
                                        #point = kml.newpoint(name = filename , coords = [(y,x)])
                                        #picpath = kml.addfile(fullpath)
                                        #fn = 'files/'+ os.path.splitext(filename)[0] + '.jpg' #Note: will not work if .JPG is used, must be lower case.
                                        #balstylestring = "<p><b>Latitude:</b> " + str(lat)+" "+ "<b>Longitude:</b> " + str(lon) +"<br></br><b>Date:</b> " + dt1+" "+ "<b>Time:</b> " + dt2 +"</p> <table width="+"400"+" cellpadding="+"0"+" cellspacing="+"0"+'"'+">  <tbody><tr><td><img width="+"80%"+'"'+" src=" + fn + "></td></tr></tbody></table><div align='left'><font color='green'><b>Created by GIS-HAII</b></font></div>"
                                        #point.style.balloonstyle.text = balstylestring




                                        #write csv process
                                        new_file.write(filename+","+str(lat)+","+str(lon)+","+str(direction)+"\n")

                                        shp_id=shp_id+1
                        except:
                            self.log("skip:{}".format(filename))
            the_kml.write(aaa)
            #the_kml.write('<ScreenOverlay>	<name>logo</name><Icon>	<href>http://www.haii.or.th/haii.png</href></Icon><overlayXY x="1" y="1" xunits="fraction" yunits="fraction"/>	<screenXY x="180" y="150" xunits="pixels" yunits="pixels"/><rotationXY x="0" y="0" xunits="fraction" yunits="fraction"/><size x="170" y="124" xunits="pixels" yunits="pixels"/>	</ScreenOverlay>')
            the_kml.write('</Document></kml>')
            the_kml.close()
            
            #kml.savekmz(OutputFile, format = False)

            new_file.close()

            #if not os.path.exists(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+'gis_kmz'):
                #os.makedirs(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+'gis_kmz')

            if not kml_output:
                #copy prepare kmz
                shutil.copytree(str(self.dlg.textPath.toPlainText().encode('iso-8859-11')), str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+'gis_kmz/files')
                shutil.copy(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11'))+".kml", str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/gis_kmz/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11'))+".kml")

                #create zip
                shutil.make_archive(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11')), "zip", str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/gis_kmz/')
                os.rename(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11'))+'.zip',str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11'))+'.kmz')
                shutil.rmtree(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/gis_kmz')
                os.remove(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11'))+".kml")
            QMessageBox.information( self.iface.mainWindow(),"Info", "Total export "+str(shp_id)+ " Points" +' || ' +"output folder: "+str(self.dlg.textPath.toPlainText().encode('iso-8859-11')) )
            #if shp_id > 0 :
            #    os.startfile(str(self.dlg.textPath.toPlainText().encode('iso-8859-11'))+'/'+str(self.dlg.textEdit.toPlainText().encode('iso-8859-11'))+".kmz")               
            #pass

    def validate_entries(self):
        # check to see that all fields have been entered
        msg = ''
        ui = self.dlg
        
        if ui.textEdit.toPlainText().encode('iso-8859-11') == '' or \
            ui.textPath.toPlainText().encode('iso-8859-11') == '' :
                msg = 'Some required fields are missing. Please complete the form.\n'
           
        if msg != '':
            QMessageBox.warning(self.dlg,
                                "Information missing or invalid",
                                msg)
            
        else:
            self.dlg.accept()
        
    def log(self,msg):
        QgsMessageLog.logMessage(msg, 'MyPlugin',QgsMessageLog.INFO)