from xml.dom import minidom
from xml import xpath

class RequestResponseTranslatorProtocol:
    getMapTemplate = '''<params>
            <layers/>
            <width>400</width>
            <height>400</height>
            <transparent/>
            <styles/>
            <crs>EPSG:4326</crs>
            <bbox/>
            <format>image/png</format>
            <bgcolor>0xffffff</bgcolor>
            </params>'''
            
    getFeatureTemplate = '''<params>
        <typeName/>
        <filter/>
        <maxFeatures>10</maxFeatures>
        </params>'''
        
    getFeatureInfoTemplate = '''<params>
        <layers/>
        <width>400</width>
        <height>400</height>
        <transparent/>
        <styles/>
        <crs>EPSG:4326</crs>
        <bbox>0,0,0,0</bbox>
        <format>image/png</format>
        <bgcolor>0xffffff</bgcolor>
        <queryLayers/>
        <infoFormat/>
        <featureCount/>
        <i>0</i>
        <j>0</j>
        <exceptions/>
        </params>'''
    
    def getFeatureToXML(self, **params):
        return self._createXML(self.getFeatureTemplate, **params)
    
    def getFeatureFromXML(self, xml):
        return self._getParams(xml, self.getFeatureTemplate)

    def getFeatureInfoToXML(self, **params):
        return self._createXML(self.getFeatureInfoTemplate, **params)
    
    def getFeatureInfoFromXML(self, xml):
        return self._getParams(xml, self.getFeatureInfoTemplate)
        
    def getMapToXML(self, **params):
        return self._createXML(self.getMapTemplate, **params)
    
    def getMapFromXML(self, xml):
        return self._getParams(xml, self.getMapTemplate)
    
    def _createXML(self, template, **params):
        '''
        param params: dict containing param:value pairs
        returns: XML doc containing params
        '''
        d = minidom.parseString(template)
        for key, val in params.items():
            # get the node in the template
            try:
                el = xpath.Evaluate('//%s' %key,d)[0]
                # get the text node
                if el.childNodes:
                    textNode = el.childNodes[0]
                else:
                    textNode = minidom.Text()
                    el.childNodes.append(textNode)
                textNode.data = str(val)
            except IndexError:
                
                #TODO : what to do with unknown elements?
                pass                
        return d.toxml()
        
    def _getParams(self, xml, template):
        '''
        param xml: xml file containing params with values
        returns: python dict containing values (uncasted)
        '''
        td = minidom.parseString(template)
        d = minidom.parseString(xml)
        param = xpath.Evaluate('//params', td)[0]
        params = {}
        for paramNode in param.childNodes:
            try:
                if paramNode.nodeType==3:
                    # we ignore the text nodes
                    continue
                name = paramNode.nodeName
                defaultValue = paramNode.childNodes[0].data
            except (IndexError, AttributeError),e:
                defaultValue = ""
                
            try:
                valueParam = xpath.Evaluate('//%s' %name,d)[0]
                value = valueParam.childNodes[0].data
            except (IndexError,AttributeError),e:
                value = defaultValue
            # cast from unicode to string
            params[str(name)]=str(value)
        return params
        
requestResponseTranslatorProtocol = RequestResponseTranslatorProtocol()
        
if __name__ == '__main__':
    xml = requestResponseTranslatorProtocol.getMapToXML(width=500,height=300,transparent=True)
    #print xml
    #print requestResponseTranslatorProtocol.getMapFromXML(xml)
    
        
        
        