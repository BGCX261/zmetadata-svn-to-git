<xsl:stylesheet xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns" xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/" version = "1.0" >          
    <xsl:output method = "text" />   
           
    <xsl:template match = "/" >                     
      <xsl:apply-templates select="//dc:title" mode="title"/>
	  <xsl:apply-templates select="//dc:date" mode="date"/>
	  <xsl:apply-templates select="//dc:subject" mode="keywords"/>
	  <xsl:apply-templates select="//dc:description" mode="abstract"/>	  
	  <xsl:apply-templates select="//dc:publisher" mode="organization"/>
	  <xsl:apply-templates select="//dc:language" mode="language"/>	  
	  <xsl:apply-templates select="//dc:creator" mode="owner"/>online=<xsl:apply-templates select="//rdf:Description/@rdf:about" mode="online"/>|</xsl:template>
	
	<xsl:template match="*" mode="owner">
		<xsl:text>owner=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template> 
	
	
	<xsl:template match="*" mode="language">
		<xsl:text>language=</xsl:text>
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

	<xsl:template match="*" mode="organization">
		<xsl:text>organization=</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template>  
	
	<xsl:template match="*" mode="online">
		<xsl:text>online</xsl:text>
		<xsl:value-of select="."></xsl:value-of>
		<xsl:text>|</xsl:text>
	</xsl:template>  
	  
</xsl:stylesheet> 