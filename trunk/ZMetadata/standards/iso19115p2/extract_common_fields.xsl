<xsl:stylesheet xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" xmlns:gco="http://www.isotc211.org/2005/gco"
						xmlns:gmd="http://www.isotc211.org/2005/gmd" version = "1.0" >          
    <xsl:output method = "text" />   
           
    <xsl:template match = "/" >               
      <xsl:apply-templates select="//idCitation/resTitle" mode="title"/>
	  <xsl:apply-templates select="//idCitation/resRefDate/refDate" mode="date"/>
	  <xsl:apply-templates select="//descKeys/keyword" mode="keywords"/>
	  <xsl:apply-templates select="//idAbs" mode="abstract"/>	  
	  <xsl:apply-templates select="//mdExtInfo/extOnRes/linkage" mode="online"/>	
	  <xsl:apply-templates select="//dataIdInfo/idPoC/role/RoleCd" mode="organization"/>	
	  <xsl:apply-templates select="//dataIdInfo/dataScale/equScale/rfDenom" mode="scale"/>	
    </xsl:template>
    
	<xsl:template match="*" mode="scale">
		<xsl:text>scale=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template> 
	
	<xsl:template match="*" mode="organization">
		<xsl:text>organization=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template> 
	
    <xsl:template match="*" mode="title">
		<xsl:text>title=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template> 
    
    <xsl:template match="*" mode="date">
		<xsl:text>date=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template>

 	<xsl:template match="*" mode="keywords">
		<xsl:text>keywords=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template>
	
	 <xsl:template match="*" mode="abstract">
		<xsl:text>abstract=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template>

	<xsl:template match="*" mode="purpose">
		<xsl:text>purpose=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template>  

	<xsl:template match="*" mode="online">
		<xsl:text>online=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template>  
	
	<xsl:template match="*" mode="onlinetype">
		<xsl:text>onlinetype=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template>  

	  
</xsl:stylesheet> 