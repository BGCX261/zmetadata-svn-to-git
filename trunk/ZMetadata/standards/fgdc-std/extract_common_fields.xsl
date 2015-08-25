<xsl:stylesheet xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/" version = "1.0" >          
    <xsl:output method = "text" />   
           
    <xsl:template match = "/" >               
      <xsl:apply-templates select="//citeinfo/title" mode="title"/>
	  <xsl:apply-templates select="//citeinfo/pubdate" mode="date"/>
	  <xsl:apply-templates select="//keywords/theme/themekt" mode="keywords"/>
	  <xsl:apply-templates select="//descript/abstract" mode="abstract"/>
	  <xsl:apply-templates select="//descript/purpose" mode="purpose"/>
	  <xsl:apply-templates select="//citation/citeinfo/onlink" mode="online"/>	
	  <xsl:apply-templates select="//citeinfo/pubinfo/publish" mode="organization"/>
    <xsl:apply-templates select="//dataIdInfo/dataLang/languageCode/@value" mode="language"/>
    <xsl:apply-templates select="//ptcontac/cntinfo/cntperp/cntper/text()" mode="owner"/>	
    </xsl:template>
    
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

	  
</xsl:stylesheet> 