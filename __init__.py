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
 This script initializes the plugin, making it known to QGIS.
"""
def name():
	return 'Photo2Kmz'

def description():
	return 'get lat lng from photo to kmz file.'

def version():
	return '2.0'

def icon():
	return 'icon.png'

def qgisMinimumVersion():
	return '2.0'

def qgisMaximumVersion():
	return '2.9'

def author():
	return 'Surachai Chantee'

def email():
	return 'surachai@haii.or.th'

def category():
  return 'Vector'

def classFactory(iface):
    # load photo_to_kmz class from file photo_to_kmz
    from photo_to_kmz import photo_to_kmz
    return photo_to_kmz(iface)
