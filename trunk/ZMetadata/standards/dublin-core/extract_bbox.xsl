<xsl:stylesheet xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns" xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/" version = "1.0" >          
    <xsl:output method = "text" />          
    <xsl:template match = "/" >               
        <xsl:apply-templates select = "//dc:coverage" />          
    </xsl:template>
         
    <xsl:template match = "dc:coverage" >        
		<xsl:variable name="coverage" select="/simpledc/dc:coverage"/>
		<xsl:variable name="n" select="substring-after($coverage,'North ')"/>
		<xsl:variable name="north" select="substring-before($n,',')"/>
		<xsl:variable name="s" select="substring-after($coverage,'South ')"/>
		<xsl:variable name="south" select="substring-before($s,',')"/>
		<xsl:variable name="e" select="substring-after($coverage,'East ')"/>
		<xsl:variable name="east" select="substring-before($e,',')"/>
		<xsl:variable name="w" select="substring-after($coverage,'West ')"/>
		<xsl:variable name="west" select="substring-before($w,'. ')"/>
		
		<xsl:value-of select="$west"></xsl:value-of>
        	<xsl:text>|</xsl:text>
		<xsl:value-of select="$south"></xsl:value-of> 
        	<xsl:text>|</xsl:text>
		<xsl:value-of select="$east"></xsl:value-of> 
        	<xsl:text>|</xsl:text>
		<xsl:value-of select="$north"></xsl:value-of>
        
    </xsl:template>     
</xsl:stylesheet> 