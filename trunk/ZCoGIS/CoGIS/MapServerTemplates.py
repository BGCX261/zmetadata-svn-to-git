
# generic mapfile template
mapBaseTemplate = """

MAP
    NAME GENERATED
    STATUS ON
    SIZE 400 400
    EXTENT %s
    UNITS DD
    IMAGECOLOR 255 255 255
    IMAGETYPE png    
    
    OUTPUTFORMAT
      NAME png
      DRIVER "GD/PNG"
      MIMETYPE "image/png"
      IMAGEMODE RGB
      EXTENSION "png"
      FORMATOPTION "INTERLACE=OFF"
    END


    
    PROJECTION
        "init=%s"
    END
    
    WEB
        IMAGEPATH "%s"
        IMAGEURL "%s"
        QUERYFORMAT text/html
        METADATA            
            "ows_abstract" "Generated"
            "ows_keywordlist" "Generated"
            "ows_title" "Generated"
            "ows_fees" "none"
            "ows_accessconstraints" "none"
            "ows_srs" "%s"
    
            "wms_title" "Generated"
            "wms_onlineresource" " "
            "wms_srs"       "%s"
            "wms_feature_info_mime_type" "text/html"
    
            "wfs_title"     "Generated"
            "wfs_onlineresource" " "
            "wms_srs"       "%s"
      END
    END
    
    QUERYMAP
      COLOR 255 255 0
      SIZE -1 -1
      STATUS ON
      STYLE HILITE
    END
    
    SCALEBAR
      COLOR 0 0 0
        IMAGECOLOR 255 255 255
        INTERVALS 2
        LABEL
          SIZE SMALL
          TYPE BITMAP
          BUFFER 0
          COLOR 0 0 0
          FORCE FALSE
          MINDISTANCE -1
          MINFEATURESIZE -1
          OFFSET 0 0
          PARTIALS TRUE
        END
        POSITION LL
        SIZE 150 3
        STATUS embed
        STYLE 1
        UNITS kilometers
    END
    
     LEGEND
      LABEL
       TYPE BITMAP
       SIZE MEDIUM
       COLOR 0 0 0
      END
     END
     
     SYMBOL
         NAME 'circle'
         TYPE ELLIPSE
         FILLED TRUE
         POINTS
          1 1
         END
     END
     
     SYMBOL
         NAME 'triangle'
         TYPE VECTOR
         FILLED TRUE
         POINTS
          0 1
          .5 0
          1 1
          0 1
         END
    END
   
   # all layers are loaded in here
   %s
END

"""

# generic template to be used for all layers
layerTemplate = """

LAYER
    TYPE %s
    STATUS OFF
    DEBUG ON
    NAME "%s"
    CONNECTIONTYPE WMS
    CONNECTION "%s"

      METADATA
      "wfs_onlineresource" "%s"
      "wms_onlineresource" "%s"
      
      "wms_title" "%s"
      "wfs_title"    "%s"
      "ows_title"    "%s"     
      "ows_srs" "%s"        
      "gml_include_items" "all"
      
    
      "wms_srs"             "%s"        
      "wms_name"            "%s"        
      "wms_server_version"  "1.1.0"
      "wms_formatlist"      "image/gif,image/png,image/jpeg,image/wbmp"        
      "wms_format"          "image/png"  
      
      END

    HEADER   "rsa_templates/rsa_regions_header.html"
    TEMPLATE "rsa_templates/rsa_regions.html"
    SIZEUNITS PIXELS

    PROJECTION
        "init=%s"
    END  

    TOLERANCE 3
    TOLERANCEUNITS PIXELS

    UNITS DD
    DUMP TRUE 
END

"""

classTemplate = """
    CLASS
        name "default"
        STYLE
            COLOR %s
            OUTLINECOLOR 0 0 0
            %s
        END          
    END

"""

#getFeatureTemplate = '<ogc:Filter xmlns:wfs="http://www.opengis.net/wfs" xmlns:ogc="http://ogc.org" xmlns:gml="http://www.opengis.net/gml"><ogc:BBOX><ogc:PropertyName>%s</ogc:PropertyName><gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml"><gml:coordinates>%s</gml:coordinates></gml:Box></ogc:BBOX></ogc:Filter>'
getFeatureTemplate = '<ogc:Filter><ogc:BBOX><ogc:PropertyName>%s</ogc:PropertyName><gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml"><gml:coordinates>%s</gml:coordinates></gml:Box></ogc:BBOX></ogc:Filter>'



wmsCapabilitiesTemplate = '''
<Layer queryable="%s">
    <Name>%s</Name>
    <Title>%s</Title>
    <Abstract>%s</Abstract>
    <KeywordList>
      <Keyword>%s</Keyword>
    </KeywordList>
    <SRS>%s</SRS>        
    <LatLonBoundingBox minx="%s" miny="%s" maxx="%s" maxy="%s"/>
    <Style>
      <Name>%s</Name>
      <Title>%s</Title>
      <LegendURL width="20" height="10">
         <Format>image/png</Format>
         <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="FACADE_URLversion=1.1.1&amp;service=WMS&amp;request=GetLegendGraphic&amp;layer=blockgroups&amp;format=image/png"/>
      </LegendURL>    
    </Style>
</Layer>
'''

#<!DOCTYPE WMT_MS_Capabilities SYSTEM "http://10.50.130.45:9080/geoserver/data/capabilities/wms/1.1.1/WMS_MS_Capabilities.dtd">
wmsCapabilitiesBodyTemplate = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE WMT_MS_Capabilities SYSTEM "http://10.50.130.45:9080/geoserver/data/capabilities/wms/1.1.1/WMS_MS_Capabilities.dtd">
<WMT_MS_Capabilities version="1.1.1">
  <Service>
    <Name>OGC:WMS</Name>
    <Title>My Generated WMS</Title>
    <Abstract>
        This is a description of your Web Map Server.
     </Abstract>
    <KeywordList>
      <Keyword>WFS</Keyword>
      <Keyword>WMS</Keyword>
      <Keyword>Spatial</Keyword>
    </KeywordList>
    <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://geoserver.sourceforge.net/html/index.php"/>
    <Fees>NONE</Fees>
    <AccessConstraints>NONE</AccessConstraints>
  </Service>
  <Capability>
    <Request>
      <GetCapabilities>
        <Format>application/vnd.ogc.wms_xml</Format>
        <DCPType>
          <HTTP>
            <Get>
              <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="FACADE_URL"/>
            </Get>
            <Post>
              <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="FACADE_URL"/>
            </Post>
          </HTTP>
        </DCPType>
      </GetCapabilities>
      <GetMap>
        <Format>image/png</Format>
        <Format>image/jpeg</Format>
        <Format>image/svg+xml</Format>
        <Format>image/gif</Format>
        <DCPType>
          <HTTP>
            <Get>
              <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="FACADE_URL"/>
            </Get>
          </HTTP>
        </DCPType>
      </GetMap>
      <GetFeatureInfo>
        <Format>text/plain</Format>
        <Format>text/html</Format>
        <Format>application/vnd.ogc.gml</Format>
        <DCPType>
          <HTTP>
            <Get>
              <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="FACADE_URL"/>
            </Get>
            <Post>
              <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="FACADE_URL"/>
            </Post>
          </HTTP>
        </DCPType>
      </GetFeatureInfo>
      <DescribeLayer>
        <Format>application/vnd.ogc.wms_xml</Format>
        <DCPType>
          <HTTP>
            <Get>
              <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="FACADE_URL"/>
            </Get>
          </HTTP>
        </DCPType>
      </DescribeLayer>
      <GetLegendGraphic>
        <Format>image/png</Format>
        <Format>image/jpeg</Format>
        <Format>image/gif</Format>
        <DCPType>
          <HTTP>
            <Get>
              <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="FACADE_URL"/>
            </Get>
          </HTTP>
        </DCPType>
      </GetLegendGraphic>
    </Request>
    <Exception>
      <Format>application/vnd.ogc.se_xml</Format>
    </Exception>
    <UserDefinedSymbolization SupportSLD="1" UserLayer="1" UserStyle="1" RemoteWFS="0"/>
     <Layer>
      <Name>AgileWMS Service</Name>
      <Title>AgileWMS Service</Title>
      <Abstract>
        This is a description of your Web Map Server.
     </Abstract>
     <SRS>EPSG:4326</SRS>      
     <LatLonBoundingBox minx="-180" miny="-90" maxx="180" maxy="90.0"/>
     %s     
    </Layer>    
  </Capability>
</WMT_MS_Capabilities>
'''

wfsCapabilities = '''
    <FeatureType>
      <Name>%s</Name>
      <Title>%s</Title>
      <Abstract>%s</Abstract>
      <Keywords>%s</Keywords>
      <SRS>%s</SRS>
      <LatLongBoundingBox minx="%s" miny="%s" maxx="%s" maxy="%s"/>
    </FeatureType>
'''

wfsCapabilitiesBody = '''
    <?xml version="1.0" encoding="UTF-8"?>
<WFS_Capabilities version="1.0.0" xmlns="http://www.opengis.net/wfs" xmlns:topp="http://www.openplans.org/topp" xmlns:sde="http://geoserver.sf.net" xmlns:lake="http://www.refractions.net/lakes" xmlns:cite="http://www.opengeospatial.net/cite" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://10.50.130.45:9080/geoserver/data/capabilities/wfs/1.0.0/WFS-capabilities.xsd">
  <Service>
    <Name>Spatial Server</Name>
    <Title>Spatial Server</Title>
    <Abstract>
Composite Spatial Server
     </Abstract>
    <Keywords>WFS, WMS, Spatial Server</Keywords>
    <OnlineResource>http://geoserver.sourceforge.net/html/index.php</OnlineResource>
    <Fees>NONE</Fees>
    <AccessConstraints>NONE</AccessConstraints>
  </Service>
  <Capability>
    <Request>
      <GetCapabilities>
        <DCPType>
          <HTTP>
            <Get onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
      </GetCapabilities>
      <DescribeFeatureType>
        <SchemaDescriptionLanguage>
          <XMLSCHEMA/>
        </SchemaDescriptionLanguage>
        <DCPType>
          <HTTP>
            <Get onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
      </DescribeFeatureType>
      <GetFeature>
        <ResultFormat>
          <GML2/>
        </ResultFormat>
        <DCPType>
          <HTTP>
            <Get onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
      </GetFeature>
      <Transaction>
        <DCPType>
          <HTTP>
            <Get onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
      </Transaction>
      <LockFeature>
        <DCPType>
          <HTTP>
            <Get onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
      </LockFeature>
      <GetFeatureWithLock>
        <ResultFormat>
          <GML2/>
        </ResultFormat>
        <DCPType>
          <HTTP>
            <Get onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="FACADE_URL"/>
          </HTTP>
        </DCPType>
      </GetFeatureWithLock>
    </Request>
  </Capability>
  <FeatureTypeList>
    <Operations>
      <Query/>
      <Insert/>
      <Update/>
      <Delete/>
      <Lock/>
    </Operations>    
    %s    
  </FeatureTypeList>
  <ogc:Filter_Capabilities>
    <ogc:Spatial_Capabilities>
      <ogc:Spatial_Operators>
        <ogc:Disjoint/>
        <ogc:Equals/>
        <ogc:DWithin/>
        <ogc:Beyond/>
        <ogc:Intersect/>
        <ogc:Touches/>
        <ogc:Crosses/>
        <ogc:Within/>
        <ogc:Contains/>
        <ogc:Overlaps/>
        <ogc:BBOX/>
      </ogc:Spatial_Operators>
    </ogc:Spatial_Capabilities>
    <ogc:Scalar_Capabilities>
      <ogc:Logical_Operators/>
      <ogc:Comparison_Operators>
        <ogc:Simple_Comparisons/>
        <ogc:Between/>
        <ogc:Like/>
        <ogc:NullCheck/>
      </ogc:Comparison_Operators>
      <ogc:Arithmetic_Operators>
        <ogc:Simple_Arithmetic/>
        <ogc:Functions>
          <ogc:Function_Names>
            <ogc:Function_Name nArgs="2">EqualInterval</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">Collection_Min</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">Area</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">Min</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">Max</ogc:Function_Name>
            <ogc:Function_Name nArgs="0">length</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">contains</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">isEmpty</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">parseDouble</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">parseInt</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">intersects</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">isClosed</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">geomFromWKT</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">toWKT</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">geomLength</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">isValid</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">geometryType</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">numPoints</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">isSimple</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">distance</ogc:Function_Name>
            <ogc:Function_Name nArgs="3">isWithinDistance</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">area</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">centroid</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">interiorPoint</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">dimension</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">boundary</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">boundaryDimension</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">envelope</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">disjoint</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">touches</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">crosses</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">within</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">overlaps</ogc:Function_Name>
            <ogc:Function_Name nArgs="3">relatePattern</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">relate</ogc:Function_Name>
            <ogc:Function_Name nArgs="3">bufferWithSegments</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">buffer</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">convexHull</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">intersection</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">union</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">difference</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">symDifference</ogc:Function_Name>
            <ogc:Function_Name nArgs="3">equalsExactTolerance</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">equalsExact</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">numGeometries</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">getGeometryN</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">getX</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">getY</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">pointN</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">startPoint</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">endPoint</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">isRing</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">exteriorRing</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">numInteriorRing</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">interiorRingN</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">strConcat</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">strEndsWith</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">strStartsWith</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">strEqualsIgnoreCase</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">strIndexOf</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">strLastIndexOf</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">strLength</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">strMatches</ogc:Function_Name>
            <ogc:Function_Name nArgs="3">strSubstring</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">strSubstringStart</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">strTrim</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">parseBoolean</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">roundDouble</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">int2ddouble</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">int2bbool</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">double2bool</ogc:Function_Name>
            <ogc:Function_Name nArgs="3">if_then_else</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">equalTo</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">notEqualTo</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">lessThan</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">greaterThan</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">greaterEqualThan</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">lessEqualThan</ogc:Function_Name>
            <ogc:Function_Name nArgs="2">isLike</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">isNull</ogc:Function_Name>
            <ogc:Function_Name nArgs="3">between</ogc:Function_Name>
            <ogc:Function_Name nArgs="1">not</ogc:Function_Name>
            <ogc:Function_Name nArgs="3">in2</ogc:Function_Name>
            <ogc:Function_Name nArgs="4">in3</ogc:Function_Name>
            <ogc:Function_Name nArgs="5">in4</ogc:Function_Name>
            <ogc:Function_Name nArgs="6">in5</ogc:Function_Name>
            <ogc:Function_Name nArgs="7">in6</ogc:Function_Name>
            <ogc:Function_Name nArgs="8">in7</ogc:Function_Name>
            <ogc:Function_Name nArgs="9">in8</ogc:Function_Name>
            <ogc:Function_Name nArgs="10">in9</ogc:Function_Name>
            <ogc:Function_Name nArgs="11">in10</ogc:Function_Name>
          </ogc:Function_Names>
        </ogc:Functions>
      </ogc:Arithmetic_Operators>
    </ogc:Scalar_Capabilities>
  </ogc:Filter_Capabilities>
</WFS_Capabilities>

'''

wfsDescribeFeatureTypeElement = '''
<element name="%s" type="%s" minOccurs="0" maxOccurs="1"/>'''

wfsDescribeFeatureTypeBodyTemplate = '''
<?xml version='1.0' encoding="ISO-8859-1" ?>
<schema targetNamespace="http://www.ttt.org/myns" xmlns:myns="http://www.ttt.org/myns" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.w3.org/2001/XMLSchema" xmlns:gml="http://www.opengis.net/gml" elementFormDefault="qualified" version="0.1" >
    <import namespace="http://www.opengis.net/gml" schemaLocation="http://schemas.opengeospatial.net/gml/2.1.2/feature.xsd" />
    <element name="%s" type="%sType" substitutionGroup="gml:_Feature" />
    <complexType name="%sType">
        <complexContent>
            <extension base="gml:AbstractFeatureType">
                <sequence>
                    %s
                </sequence>
            </extension>
        </complexContent>
    </complexType>
</schema>
'''

ogcServiceException = '''
<ServiceExceptionReport version="1.2.0">
<ServiceException>
    %s
</ServiceException>
</ServiceExceptionReport>'''

serverStatusTemplate = '''
<?xml version='1.0' encoding="ISO-8859-1" ?>
<status>
        %s
</status>
'''

discoveryMap = '''
MAP
NAME dummy
STATUS ON
SIZE 2 2
EXTENT 23.00 23.00 23.01 23.01
UNITS dd
IMAGECOLOR 255 255 255
IMAGETYPE jpeg
WEB
    IMAGEPATH "./"
    IMAGEURL "./"       
END
LAYER
  NAME "Dummy layer"
  TYPE %s
  STATUS OFF
  CONNECTIONTYPE WMS
  CONNECTION "%s"  
  METADATA    
      "wms_srs"             "EPSG:4326"        
      "wms_name"            "%s"        
      "wms_server_version"  "1.1.0"
      "wms_formatlist"      "image/gif,image/png,image/jpeg,image/wbmp"        
      "wms_format"          "image/png"        
  END
  CLASS
    NAME "Dummy layer"    
    COLOR 220 54 199
    OUTLINECOLOR 216 255 255
  END
END
END

'''

getFeatureQueryTemplate = '''
<wfs:GetFeature service="WFS" version="1.0.0" outputFormat="GML2" maxFeatures="%s" xmlns:wfs="http://www.opengis.net/wfs" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml">
<wfs:Query typeName="%s">%s</wfs:Query>
</wfs:GetFeature>
'''


