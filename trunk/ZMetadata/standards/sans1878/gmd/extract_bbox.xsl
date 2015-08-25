<xsl:stylesheet xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" xmlns:gmd="http://www.isotc211.org/2005/gmd"
										xmlns:gco="http://www.isotc211.org/2005/gco"
										xmlns:gml="http://www.opengis.net/gml"
										xmlns:srv="http://www.isotc211.org/2005/srv"
										 version = "1.0" >          
    <xsl:output method = "text" />          
    <xsl:template match = "/" >               
        <xsl:apply-templates select="//gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal" mode="latLon"/>
	        <xsl:apply-templates select="//gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal" mode="latLon"/>
        <xsl:apply-templates select="//gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal" mode="latLon"/>
        <xsl:apply-templates select="//gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal" mode="latLon"/>
     </xsl:template>
    
<xsl:template match="*" mode="latLon">	
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	
	</xsl:template>
     
    
</xsl:stylesheet> 