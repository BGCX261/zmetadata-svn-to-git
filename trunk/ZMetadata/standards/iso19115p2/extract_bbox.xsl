<xsl:stylesheet xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/" version = "1.0" >          
    <xsl:output method = "text" />          
    <xsl:template match = "/" >               
        <xsl:apply-templates select="/Metadata/dataIdInfo/geoBox/westBL" mode="latLon"/>
	  <xsl:apply-templates select="/Metadata/dataIdInfo/geoBox/eastBL" mode="latLon"/>
	  <xsl:apply-templates select="/Metadata/dataIdInfo/geoBox/southBL" mode="latLon"/>
	  <xsl:apply-templates select="/Metadata/dataIdInfo/geoBox/northBL" mode="latLon"/>
    </xsl:template>
    
    
    <xsl:template match="*" mode="latLon">
		<xsl:param name="name" select="name(.)"/>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>		
		
	</xsl:template>
     
    
</xsl:stylesheet> 