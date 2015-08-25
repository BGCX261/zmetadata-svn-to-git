<xsl:stylesheet xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" xmlns:gco="http://www.isotc211.org/2005/gco"
						xmlns:gmd="http://www.isotc211.org/2005/gmd" version = "1.0" >          
    <xsl:output method = "text" />   
           
    <xsl:template match = "/">
	
       <xsl:apply-templates select="//gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString" mode="title"/>
	  <xsl:apply-templates select="//gmd:date/gmd:CI_Date/gmd:date/gco:DateTime" mode="date"/>
	  <xsl:apply-templates select="//gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString" mode="keywords"/>
	  <xsl:apply-templates select="//gmd:abstract/gco:CharacterString" mode="abstract"/>
	  <xsl:apply-templates select="//gmd:purpose/gco:CharacterString" mode="purpose"/>
	  <xsl:apply-templates select="//gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL" mode="online"/>	
	  <xsl:apply-templates select="//gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString" mode="onlinetype"/>		  
	  <xsl:apply-templates select="//gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString" mode="organization"/>	
	  <xsl:apply-templates select="//gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer" mode="scale"/>  
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

	  
</xsl:stylesheet> 