from xml.dom import minidom
import string
import sys
import traceback
import cgi
from StringIO import StringIO
import sys 
#sys.setdefaultencoding('UTF-8')

# class name is tag name 
# label is tag name
# name is tag name
# value is tag value

XMLcomplexContent = '''<tmp><div class="XMLcomplexContent" onclick="selectelm(this, event);" ondblclick="selectelm(this, event);">                                
                                  <fieldset class="%(tagName)s">
                                    <legend>- %(tagName)s</legend>
                                    <input type="hidden" value="%(tagName)s" name=".tg" ><span style="position:absolute;visibility:hidden;"><br/></span></input>
                                  </fieldset>                                 
                            </div>
                        </tmp>'''

                    
XMLcomplexContent_old = '''<tmp><div class="XMLcomplexContent" onclick="selectelm(this, event);" ondblclick="selectelm(this, event);"><div class="%(tagName)s">
                                    <input type="hidden" value="%(tagName)s" name=".tg" ><span style="position:absolute;visibility:hidden;"><br/></span></input>
                                </div>
                            </div>
                        </tmp>'''
                        
XMLsimpleContent = '''<tmp><div class="XMLsimpleContent" onclick="selectelm(this, event);" ondblclick="selectelm(this, event);"></div></tmp>'''

XMLsimpleTypeLong = '''<tmp><span class="XMLsimpleType" onclick="selectelm(this, event);" ondblclick="selectelm(this, event);">
                    <span class="%(tagName)s">
                        <label>%(tagName)s: 
                        </label><br></br>
                        <textarea row="3" cols="70" class="%(tagName)s" name="%(tagName)s" value="%(tagValue)s" onchange="textChanged(this);"  onfocus="focusGained(this)">%(tagValue)s</textarea>
                    </span>
                    <br></br>
                </span></tmp>'''
                
XMLsimpleTypeShort = '''<tmp><span class="XMLsimpleType" onclick="selectelm(this, event);" ondblclick="selectelm(this, event);">
                    <span class="%(tagName)s">
                        <label>%(tagName)s: 
                        </label>
                        <input type="text" class="%(tagName)s" name="%(tagName)s" value="%(tagValue)s" style="width:240px;" onchange="textChanged(this);" onfocus="focusGained(this)"><span style="position:absolute;visibility:hidden;"><br/></span></input>
                    </span>
                   <br></br>
                </span></tmp>'''
                
XMLattribute = '''<tmp><span class="XMLattribute" onclick="selectelm(this, event);" ondblclick="selectelm(this, event);">
                        <span class="%(attributeName)s">
                            <label>%(attributeName)s: 
                            </label>
                            <input type="text" class="%(attributeName)s" name="@%(attributeName)s" value="%(attributeValue)s" onchange="textChanged(this);" onfocus="focusGained(this)"><span style="position:absolute;visibility:hidden;"><br/></span></input>
                        </span>
                        <br></br>
                  </span></tmp> '''

class Convert:
    def __init__(self):
        self.mainXML = minidom.parseString('<?xml version="1.0"?><xmlform></xmlform>')        
        self.mainHTML = minidom.parseString('''<?xml version="1.0"?><html>
        <head>
            <title>metadata</title>            
            <style type="text/css">
                body { margin-top: 0; padding-top:0; }
                div#menuForm { overflow: hidden; background-color: #CDE2A7; border: 2px solid #74AE0B;  margin-top:3px; top:0px; left:0px;position:relative;}
                div#xmlForm {position:relative;width:100%;height:400px;overflow:auto; border: 2px solid #74AE0B;margin-top:3px;}                        
                div#lMetadataFeedback {top:0px; left:0px;position:relative;visibility:hidden;margin-bottom:5px;}
                .XMLattribute { margin-left: 10px; font-style: italic; }
                .customButton{width:110;}
                fieldset{border:thin solid gray;margin:6px;}
                label{margin:5px;}
            </style>      
        </head>
        <body onload="editorSetup()">
            <div id="lMetadataFeedback" >Feedback</div>
            <div id="menuForm" >
            <form id="menuForm" name="menuForm" onclick="clickFormBody(this, event);">   
                <table>
                    <tr>
                        <td><input class="customButton" type="button" name="duplicateSelected" value="Duplicate" onclick="menuChosen(this)"></input></td>
                        <td><input class="customButton" type="button" name="copySelected" value="Copy" onclick="menuChosen(this)"></input></td>
                        <td><input class="customButton" type="button" name="cutSelected" value="Cut" onclick="menuChosen(this)"></input></td>
                    </tr>                    
                    <!--<tr>
                        <td><input class="customButton" type="button" name="XMLcomplexContent" value="New Complex" onclick="makeElementChosen(this)"></input></td>
                        <td><input class="customButton" type="button" name="XMLsimpleContent" value="New Element " onclick="makeElementChosen(this)"></input></td>
                        <td><input class="customButton" type="button" name="XMLattribute" value="New Attribute" onclick="makeElementChosen(this)"></input></td>
                    </tr>-->
                    <tr>
                        <td><input class="customButton" type="button" name="pasteReplaceSelected" value="Paste Over" onclick="menuChosen(this)"></input></td>
                        <td><input class="customButton" type="button" name="pasteIntoSelected" value="Paste Into" onclick="menuChosen(this)"></input></td>
                        <td><input class="customButton" type="button" name="pasteBeforeSelected" value="Paste Before" onclick="menuChosen(this)"></input></td>
                        <td><input class="customButton" type="button" name="pasteAfterSelected" value="Paste After" onclick="menuChosen(this)"></input></td>
                    </tr>
                    <tr>
                        <td><input type="button" value="Save" onclick="save()"></input></td>
                        <td><input type="button" value="Validate" onclick="validate()"></input></td>
                    </tr>
                </table>                                                                                
                <input name="multiple" type="hidden" value="multiple"></input>                
            </form>
            </div>           
            
            <div id="xmlForm">
             <form name="xmlForm" action="" target="_blank" method="post"> </form>             
            </div>
            
        </body>
        </html>''')  
        
        #self.mainHTML = minidom.parseString('''<?xml version="1.0"?><html><body></body></html>''')  
         
        self.currentHTML = self.mainHTML.getElementsByTagName("form")[1]
        self.currentXML = self.mainXML.documentElement
    
    def convertToHTML(self,xml):
        ""            
        d = minidom.parseString(xml) 
        children = d.childNodes
        for child in children:
            print '>>>>', child
            self.toHTML(child, self.currentHTML)
        
        return self.mainHTML.toxml().replace('<?xml version="1.0"?>', "")
    
    def convertToHTMLView(self,xml):
        """
        """
        d = minidom.parseString(xml) 
        children = d.childNodes
        for child in children:
            self.toHTML(child, self.currentHTML)            
        
        theDiv = None
        divs = self.mainHTML.getElementsByTagName("div")
        for div in divs:
            if div.hasAttribute("id"):
                if div.getAttribute("id") == "xmlForm":
                    theDiv = div
        if theDiv != None:
            elms = theDiv.getElementsByTagName("input")
            for elm in elms:
                if elm.hasAttribute("type"):
                    if elm.getAttribute("type") == "text":
                        val = elm.getAttribute("value")
                        newElm = d.createElement("i")
                        tNode = d.createTextNode(val)
                        newElm.appendChild(tNode)
                        elm.parentNode.replaceChild(newElm, elm)
                        
            elms = theDiv.getElementsByTagName("textarea")
            for elm in elms:                
                textNode = elm.firstChild
                #print textNode.nodeValue
                newElm = d.createElement("i")
                tNode = d.createTextNode(textNode.nodeValue)
                newElm.appendChild(tNode)
                elm.parentNode.replaceChild(newElm, elm)                                  
        tmp = theDiv.toxml()
        tmp = tmp.replace('onclick="selectelm(this, event);"',"")
        return tmp        
    
    def toHTML(self,xmlNode, htmlParent):
        ""
        
        if xmlNode.nodeType == xmlNode.TEXT_NODE: # skip the TEXT_NODE types
            return
        
        if not xmlNode.hasChildNodes():
            if xmlNode.nodeName.lower().find("#comment") != -1:
                return                
            nextParent = self.createComplexContent(xmlNode.nodeName)
            
            if xmlNode.hasAttributes():
                attrsNodeList = xmlNode.attributes.values()
                for attrNode in attrsNodeList:
                    attributeNode = self.createAttribute(attrNode.name, attrNode.value)
                    nextParent.getElementsByTagName("fieldset")[0].appendChild(attributeNode)
            
            fieldsetElms = htmlParent.getElementsByTagName("fieldset")
            # user last fieldsetElm
            if len(fieldsetElms) == 0:
                htmlParent.appendChild(nextParent)
            else: 
                fieldsetElm = fieldsetElms[0]                
                fieldsetElm.appendChild(nextParent)   
                
#        if not xmlNode.hasChildNodes() and xmlNode.hasAttributes():    
#            nextParent = self.createComplexContent(xmlNode.nodeName)
#            attrsNodeList = xmlNode.attributes.values()
#            for attrNode in attrsNodeList:
#                attributeNode = self.createAttribute(attrNode.name, attrNode.value)
#                nextParent.getElementsByTagName("fieldset")[0].appendChild(attributeNode)
#            
#            fieldsetElms = htmlParent.getElementsByTagName("fieldset")
#            # user last fieldsetElm
#            if len(fieldsetElms) == 0:
#                htmlParent.appendChild(nextParent)
#            else: 
#                fieldsetElm = fieldsetElms[0]                
#                fieldsetElm.appendChild(nextParent)  
        
        if xmlNode.hasChildNodes():            
            # create complex type
            # check that childnode is not a text node, else it is a simpleType
            cNodes = xmlNode.childNodes
            if (cNodes[0].nodeType == cNodes[0].TEXT_NODE) and (len(cNodes) == 1): # its a simpleType                                
                # check if its a input or textarea
                
                if (cNodes[0].nodeValue.find("\n") != -1) or (len(cNodes[0].nodeValue) > 85):
                    input = False
                else:
                    input = True
                
                if xmlNode.hasAttributes():                    
                    simpleType = self.createSimpleType(xmlNode.nodeName, cNodes[0].nodeValue, input)
                    simpleContent = self.createSimpleContent()
                    simpleContent.appendChild(simpleType)                    
                    
                    attrsNodeList = xmlNode.attributes.values()
                    for attrNode in attrsNodeList:                        
                        attributeNode = self.createAttribute(attrNode.name, attrNode.value)
                        simpleContent.appendChild(attributeNode)                        
                    nextParent = simpleContent                
                
                else:
                    nextParent = self.createSimpleType(xmlNode.nodeName, cNodes[0].nodeValue, input)                    
                               
            else: #its a complexType                    
                if xmlNode.hasAttributes():                    
                    nextParent = self.createComplexContent(xmlNode.nodeName)
                    attrsNodeList = xmlNode.attributes.values()
                    for attrNode in attrsNodeList:
                        attributeNode = self.createAttribute(attrNode.name, attrNode.value)
                        nextParent.getElementsByTagName("fieldset")[0].appendChild(attributeNode)                        
                else:
                    nextParent = self.createComplexContent(xmlNode.nodeName)
                        
            fieldsetElms = htmlParent.getElementsByTagName("fieldset")
            # user last fieldsetElm
            if len(fieldsetElms) == 0:
                htmlParent.appendChild(nextParent)
            else: 
                fieldsetElm = fieldsetElms[0]                
                fieldsetElm.appendChild(nextParent)            
        
        children = xmlNode.childNodes
        for child in children:
            self.toHTML(child, nextParent)          

    def addNodeToParent(self,parent,node):
        ""
        cNodes = parent.childNodes
        if not node in cNodes:
            parent.appendChild(node)   
    
    
    def createComplexContent(self, tagName):
        ""
        print "tagName", tagName
        d = {"tagName": tagName}
        print '---------------'
        print XMLcomplexContent
        print '---------------'
        tDom = minidom.parseString(XMLcomplexContent %(d))        
        return tDom.documentElement.firstChild
    
    def createSimpleContent(self):
        ""
        tDom = minidom.parseString(XMLsimpleContent)
        return tDom.documentElement.firstChild
    
    def createSimpleType(self,tagName,tagValue="", input=True):
        ""         
        s = ""
        try:
            tagValue = tagValue.replace('"',"'")
            
            d = {"tagName":tagName, "tagValue":cgi.escape(tagValue)}
            
            if input:
                s = XMLsimpleTypeShort %(d)
                tDom = minidom.parseString(s.encode('utf-8'))
            else:
                s = XMLsimpleTypeLong %(d)
                tDom = minidom.parseString(s.encode('utf-8'))
                        
            return tDom.documentElement.firstChild
        except:
            traceback.print_exc(file=sys.stdout)
            print s
            
    
    def createAttribute(self,attributeName, attributeValue):
        ""
        #print "create attribute : " + attributeName + " : " + attributeValue
        attributeValue = attributeValue.replace('"',"'")
        d = {"attributeName":attributeName, "attributeValue":attributeValue}
        tDom = minidom.parseString(XMLattribute %(d))        
        return tDom.documentElement.firstChild
    
    
    # ============================TO XML========================================
    
    def removeRedundantTags(self, dom):
        """
        @param dom: the dom object to strip nodes off
        @return: a stripped version of the passed dom object
        """
        
        removeList = ["br","label","legend"]        
        for remove in removeList:
            elms = dom.getElementsByTagName(remove)
            for elm in elms:
                elm.parentNode.removeChild(elm) 
                
        tgElms = dom.getElementsByTagName("input")
        for tgElm in tgElms:
            if tgElm.getAttribute("name") == ".tg":
                tgElm.parentNode.removeChild(tgElm)             
                
        return dom
        
    def convertToXML(self, html):
        """
        @param html: the html string to convert to xml
        @return: an xml version of the html string
        """   
#        f = open("c:/temp/convertToXML.html","w")
#        f.write(html)
#        f.close()
        
        d = minidom.parseString(html)    
        d = self.removeRedundantTags(d)        
        formElm = d.getElementsByTagName("form")[0]           
        
        children = formElm.childNodes
        for child in children:
            self.toXML(child, self.currentXML)            
        
        
        first = self.mainXML.firstChild
        second = first.firstChild        
        return '<?xml version="1.0"?>' + second.toxml()
    
    def xmlToNode(self, xml):
        """
        @summary: convert given xml string into an xml node
        @param xml: xml string
        @return: xml node element
        """
        try:
            nodeTemplate = "<tmp>%s</tmp>"
            nodeStr = nodeTemplate % xml
            d = minidom.parseString(nodeStr)         
            return d.documentElement.firstChild
        except:
            print xml
            traceback.print_exc(file=sys.stdout)
            
    
    def buildNode(self, htmlNode, xmlParent):
        """
        @param htmlNode: the html node object to convert to xml node and append to the xmlParent
        @param xmlParent: the xml node to use as parent for the htmlNode
        """
        tagTemplate = "<%s></%s>"
        
        tagName = htmlNode.tagName
        
        if tagName == "fieldset":
            className = htmlNode.getAttribute("class")            
            tag = tagTemplate %(className, className)
            elm = self.mainXML.createElement(className)
            
            #newNode = self.xmlToNode(tag)
            #xmlParent.appendChild(newNode)
            xmlParent.appendChild(elm)
            return elm
            
        if tagName == "span":
            className = htmlNode.getAttribute("class")  
            if className == "XMLattribute":
                inputElms = htmlNode.getElementsByTagName("input")                
                attrName = inputElms[0].getAttribute("class")
                attrName = attrName.replace("@","") # remove the @ so that xml attributes are valid
                attrValue = inputElms[0].getAttribute("value")
                xmlParent.setAttribute(attrName, attrValue)
                return xmlParent
            
            if className == "XMLsimpleType":
                if htmlNode.parentNode.getAttribute("class") != "XMLsimpleContent":                    
                    #newNode = self.getNodeForSimpleType(htmlNode)
                    #xmlParent.appendChild(newNode)
                    tagAndValue = self.getTagAndValueForSimpleType(htmlNode)                    
                    elm = self.mainXML.createElement(tagAndValue[0])
                    elm.appendChild(self.mainXML.createTextNode(tagAndValue[1]))                    
                    xmlParent.appendChild(elm)
                    return elm
            
        if tagName == "div":
            className = htmlNode.getAttribute("class")
            if className == "XMLsimpleContent":
                spanElms = htmlNode.getElementsByTagName("span")
                for spanElm in spanElms:
                    if spanElm.getAttribute("class") == "XMLsimpleType":
                        #newNode = self.getNodeForSimpleType(htmlNode)
                        tagAndValue = self.getTagAndValueForSimpleType(htmlNode)
                        elm = self.mainXML.createElement(tagAndValue[0])
                        elm.appendChild(self.mainXML.createTextNode(tagAndValue[1]))
                        #xmlParent.appendChild(newNode)
                        xmlParent.appendChild(elm)
                        return elm  
        return xmlParent 
    
    def getTagAndValueForSimpleType(self,htmlNode):
        """
        """ 
        try:       
            inputElms = htmlNode.getElementsByTagName("input")
            textElms = htmlNode.getElementsByTagName("textarea")
            textElms2 = htmlNode.getElementsByTagName("textarea")
            
            if len(inputElms) > 0:
                tag = inputElms[0].getAttribute("class")
                value = inputElms[0].getAttribute("value")
                
            if len(textElms) > 0:            
                tag = textElms[0].getAttribute("class")                                        
                value = textElms[0].getAttribute("value")   
            if len(textElms2) > 0:            
                tag = textElms2[0].getAttribute("class")                                        
                value = textElms2[0].getAttribute("value")                        
            return [tag,value]        
        except:
            print htmlNode
            print htmlNode.toxml()
            io = StringIO()
            traceback.print_exc(file=io)
            io.seek(0)            
            trace = io.read()
            print trace          
    
    def getNodeForSimpleType(self,htmlNode):
        """
        """
        tagTemplate2 = "<%s>%s</%s>"
        
        inputElms = htmlNode.getElementsByTagName("input")
        textElms = htmlNode.getElementsByTagName("textarea")
        if len(inputElms) > 0:
            tag = inputElms[0].getAttribute("class")
            value = inputElms[0].getAttribute("value")
            
        if len(textElms) > 0:
            tag = textElms[0].getAttribute("class")
            value = textElms[0].nodeValue                        
                            
        tagS = tagTemplate2 %(tag, value ,tag)
        newNode = self.xmlToNode(tagS)
        return newNode
        
    def toXML(self,htmlNode, xmlParent):
        """
        @param htmlNode: html node object to convert to xml
        @param xmlParent: the dom node to use as htmlNode parent
        """
        if htmlNode.nodeType == htmlNode.TEXT_NODE: # skip the TEXT_NODE types
            return                
        
        nextParent = self.buildNode(htmlNode, xmlParent);        
    
        children = htmlNode.childNodes
        for child in children:
            self.toXML(child, nextParent)
        
    
if __name__ == "__main__":
        
    
    #htmlF = file(r"c:\!Projects\Python\XmlHtmlUtil\to_xml.html","r")
    #htmlF = file(r"c:\temp\saved.html","r")
    
    #htmlF = file(r"c:\!Projects\Python\XmlHtmlUtil\to_xml2.html","r")
    #html = htmlF.read()
    #htmlF.close()
    
    #f = file(r"c:\!Projects\NSIF\docs\metadata\eml\eml-2.0.1\eml-2.0.1\edit_template.xml","r")
    #f = file(r"c:\!Projects\Python\xml\test.xml","r")
    #f = file(r"c:\ftproot\xml\iso19115\iso_19115_sample0.xml","r")
    f = file(r"c:\ftproot\esvp200m_fgdc.xml","r")
    xml = f.read()       
    f.close()   
    
    c = Convert()
    #htmlData =  c.convertToHTML(xml)
    htmlData = c.convertToHTMLView(xml)
    #print htmlData
    f = file("c:/temp/xml2html.html","w")
    f.write(htmlData)
    f.close()
    
    #print c.convertToXML(html)   
    
    
    
    
    
    
    
    
    
    