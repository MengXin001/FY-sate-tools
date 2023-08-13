import xml.dom.minidom

def read_xml(filepath):
    xmldata = {}
    with open(filepath, "r", encoding="utf-8") as f:
        xmlf = xml.dom.minidom.parse(f)
        root = xmlf.documentElement
        keys = ['SatelliteID', 'SensorID', 'CenterTime', 'ImageGSD', 'TopLeftLatitude', 'TopLeftLongitude',
        'TopRightLatitude', 'TopRightLongitude', 'BottomRightLatitude', 'BottomRightLongitude',
        'BottomLeftLatitude', 'BottomLeftLongitude', 'SolarAzimuth', 'SolarZenith', 'SatelliteAzimuth', 'SatelliteZenith']
        for key in keys:
            xmldata[key] = filename_node = root.getElementsByTagName(key)[0].childNodes[0].data
        return xmldata