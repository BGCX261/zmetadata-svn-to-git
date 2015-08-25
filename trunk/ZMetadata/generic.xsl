<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
   <xsl:output method="html" indent="yes" />

<!-- entry point -->
   <xsl:template match="/">
      <html>
      	<style>
      		div.element{border:thin solid #CCCCCC;background-color:#FFFFCC}
      		div.attribute{font-style: italic; border:thin solid green; background-color:#CCCC99}
      		
      		span.element{font-weight:bold;}
      		span.attribute{font-style: italic;background-color:#CCCC99}
      		
      	</style>
         <body>
            <xsl:call-template name="element" />
         </body>
      </html>
   </xsl:template>

   <xsl:template name="element">
      <div>
         <xsl:for-each select="/descendant-or-self::*">
         <!--<xsl:for-each select="/metadata/descendant-or-self::*"> -->
            
            <xsl:variable name = "A" ><xsl:value-of select="count(ancestor::*) * 20" /></xsl:variable>  
            <xsl:variable name = "B" ><xsl:value-of select="count(ancestor::*) * 40" /></xsl:variable>  
            <div class="element" style="position:relative;left:{$A}px;">
               <span>
                  <span class="element"><xsl:value-of select="local-name()"/></span>  <span style="margin-left:30px;"><xsl:value-of select="text()" /></span> 
               </span>              

               <xsl:for-each select="@*">
                  <div class="attribute" style="position:relative;left:{$B}px;">
                     <span>
                       <span class="attribute"><xsl:value-of select="name()"/></span> <span class="attribute" style="margin-left:30px;"><xsl:value-of select="."/></span>
                     </span>                     
                  </div>
               </xsl:for-each>            
            </div>
            
         </xsl:for-each>
      </div>
   </xsl:template>

   <xsl:template name="attribute">
      <p>attribute</p>
   </xsl:template>
</xsl:stylesheet>

