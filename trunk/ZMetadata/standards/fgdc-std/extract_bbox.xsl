<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
   <xsl:output method="text" indent="yes" />   
   
   <xsl:template match="/">      
        <xsl:text></xsl:text>        
        <xsl:value-of select="//spdom/bounding/westbc"/>        
        <xsl:text >|</xsl:text>        
        <xsl:value-of select="//spdom/bounding/southbc"/>        
        <xsl:text >|</xsl:text>          
        <xsl:value-of select="//spdom/bounding/eastbc"/>        
        <xsl:text >|</xsl:text>        
        <xsl:value-of select="//spdom/bounding/northbc"/>
   </xsl:template>      
   
</xsl:stylesheet>