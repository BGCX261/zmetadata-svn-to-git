<xsl:stylesheet 
		xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" 
		xmlns:gco="http://www.isotc211.org/2005/gco"
		xmlns:gmd="http://www.isotc211.org/2005/gmd" 
		xmlns:fn="http://www.w3.org/2005/xpath-functions"
		version = "1.0" >          
    <xsl:output method = "text" />   

    <xsl:template match = "/" >               
      <xsl:apply-templates select="//dataset/title" mode="title"/>
	  <xsl:apply-templates select="//dataset/pubDate" mode="date"/>
	  <xsl:apply-templates select="//keywordSet/keyword" mode="keywords"/>
	  <xsl:apply-templates select="//dataset/abstract/para | //abstract/section/para" mode="abstract"/>	  
	  <xsl:apply-templates select="//distribution/online/url" mode="online"/>	
	  <xsl:apply-templates select="//publisher/organizationName" mode="organization"/>	
	  <xsl:apply-templates select="//dataset/language" mode="language"/>	
	  <xsl:apply-templates select="/" mode="owner"/>
      <xsl:apply-templates select="/" mode="secondowner"/>
    </xsl:template>

	<xsl:template match="*" mode="owner">
		<xsl:text>owner=</xsl:text>
		<xsl:value-of select="//dataset[1]/contact[1]/individualName[1]/salutation[1]/text()"></xsl:value-of>
		<xsl:text> </xsl:text>
		<xsl:value-of select="//dataset[1]/contact[1]/individualName[1]/givenName[1]/text()"></xsl:value-of>
		<xsl:text> </xsl:text>
		<xsl:value-of select="//dataset[1]/contact[1]/individualName[1]/surName[1]/text()"></xsl:value-of>
		
		<xsl:text>|</xsl:text>
	</xsl:template> 	
		
	<xsl:template match="*" mode="secondowner">
		<xsl:text>secondowner=</xsl:text>
		<xsl:value-of select="//dataset[1]/contact[1]/organizationName[1]/text()"></xsl:value-of>
		
		<xsl:text>|</xsl:text>
	</xsl:template> 	
		
    
	<xsl:template match="*" mode="language">
		<xsl:text>language=</xsl:text>
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