# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QVetTool
   A QGIS plugin 
   Spatial functions for vet epidemiology
                              -------------------
        begin                : 2015-11-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Norbert Solymosi
        email                : solymosi.norbert@gmail.com
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QVetTool class from file QVetTool.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .qvet_tool import QVetTool
    return QVetTool(iface)
