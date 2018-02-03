<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
<!-- ==================================================================
     Definir cantidad de rompimientos 
 ====================================================================== -->
<xsl:variable name="mode_break">
     <xsl:value-of select="0"/>
 </xsl:variable>
 
 <xsl:variable name="header_span">
     <xsl:value-of select="0"/>
 </xsl:variable>
 
 <!-- ==================================================================
    Definir cantidad de campos agrupados
 ====================================================================== -->
<xsl:key name="key1"  match="model" use="concat(generate-id(model), campo1,'+',campo2)"/>
 <!-- ==================================================================
    Definir variable para rompimientos (hasta 4)
 ====================================================================== -->
<xsl:key name="keyH1"  match="model" use="concat(generate-id(model), campo1)"/>
<xsl:key name="keyH2"  match="model" use="concat(generate-id(model), campo1,'+',campo2)"/>
<xsl:key name="keyH3"  match="model" use="concat(generate-id(model), campo1,'+',campo2,'+',campo3)"/>
<xsl:key name="keyH4"  match="model" use="concat(generate-id(model), campo1,'+',campo2,'+',campo3,'+',campo4)"/>
<xsl:template match="/">
     <xsl:apply-templates select="models"/>
</xsl:template>
<xsl:template match="models">
    <document>
         <template pageSize="(595,842)"
             showBoundary="0"                          
             author="Desoft SA" allowSplitting="20"> 
             <pageTemplate id="template_page"> 
                 <frame id="first_frame" x1="57.6" y1="57.6" width="499.0" height="726.8"/>
    <xsl:call-template name="corporate_header"/>        
             </pageTemplate>
           </template>
            <stylesheet> 
                  <blockTableStyle id="Standard_Outline"><blockAlignment value="LEFT"/><blockValign value="TOP"/>
                  </blockTableStyle>
        
       <blockTableStyle id="tablePageHeader">
       
       <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="1.0"/>
       <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="1.0"/>
       
       </blockTableStyle>
       
       <blockTableStyle id="tablePageDetails">
       
       <lineStyle kind="LINEBELOW" colorName="#C0C0C0" start="0,0" stop="-1,-1" thickness="0.2"/>
       
       </blockTableStyle>
       
       <blockTableStyle id="tablePageTotals">
       
       <lineStyle kind="LINEABOVE" colorName="#000000" start="0,0" stop="-1,-1" thickness="1.0"/>
       <lineStyle kind="LINEBELOW" colorName="#000000" start="0,0" stop="-1,-1" thickness="1.0"/>
       
       </blockTableStyle>
       
                <initialize>
                   <paraStyle name="all" alignment="justify"/>
                </initialize>
           
                   <paraStyle name="titleReport" fontName="Helvetica-Bold" fontSize="14" textColor="#000000" alignment="CENTER"/>
           
                   <paraStyle name="pNumber" fontName="Helvetica" fontSize="9" textColor="#000000" alignment="RIGHT"/>
           
                   <paraStyle name="pString" fontName="Helvetica" fontSize="9" textColor="#000000" alignment="LEFT"/>
           
                   <paraStyle name="pTotalNumber" fontName="Helvetica-Bold" fontSize="9" textColor="#000000" alignment="RIGHT"/>
           
                   <paraStyle name="pTotalString" fontName="Helvetica-Bold" fontSize="9" textColor="#000000" alignment="LEFT"/>
           
                   <paraStyle name="pHeader" fontName="Helvetica-Bold" fontSize="10" textColor="#000000"/>
           
                   <paraStyle name="pHeaderR" fontName="Helvetica-Bold" fontSize="10" textColor="#000000" alignment="RIGHT"/>
           
                   <paraStyle name="pDetails" fontName="Helvetica" fontSize="9" textColor="#000000"/>
           
                   <paraStyle name="pCenter" fontName="Helvetica-Bold" fontSize="9" textColor="#000000" alignment="CENTER"/>
           
                   <paraStyle name="pGroup1" fontName="Helvetica-Bold" fontSize="11" textColor="#000000" leftIndent="1in"/>
           
                   <paraStyle name="pGroup2" fontName="Times-Bold" fontSize="11" textColor="#000000" leftIndent="3in"/>
           
                   <paraStyle name="pGroup3" fontName="Times-Bold" fontSize="11" textColor="#000000" leftIndent="5in"/>
           
                   <paraStyle name="pGroup4" fontName="Times-Bold" fontSize="11" textColor="#000000" leftIndent="5in"/>
        
             </stylesheet>
        
        <story>
        <!-- ==================================================================
                                 MODO LIST
              mode_report = 1 ==> Datos primarios sin agrupamientos
              mode_report = 2 ==> Agrupados sin datos primarios
              mode_report = 3 ==> Agrupados con datos primarios
             ====================================================================== -->
                
        <xsl:variable name="mode_report">
          <xsl:value-of select="1"/>
        </xsl:variable> 
        <para  style="titleReport">Contratos</para>
        <spacer length="15"/>
        <pto>
           <xsl:choose>
                <xsl:when test="$header_span=0">
                       <xsl:call-template name="head_column"/> 
                         <pto_header>
                            <para  style="titleReport">Contratos</para>
                             <spacer length="15"/>
                            <xsl:call-template name="head_column"/>
                            </pto_header>
                        
                </xsl:when>                
                <xsl:when test="$header_span=1">
                       <xsl:call-template name="head_column_span"/>
                         <pto_header>
                            <para  style="titleReport">Contratos</para>
                             <spacer length="15"/>
                            <xsl:call-template name="head_column"/>
                            </pto_header>
                                     
                </xsl:when>     
          </xsl:choose>
         <spacer length="2"/>         
         <xsl:choose>
                <xsl:when test="$mode_report=1">
                    <xsl:call-template name="primary_data"></xsl:call-template>           
                   </xsl:when> 
                <xsl:when test="$mode_report=2">
                    <xsl:call-template name="grouping_no_detail"></xsl:call-template>           
                </xsl:when>     
                <xsl:when test="$mode_report=3">
                    <xsl:call-template name="grouping_detail"></xsl:call-template>           
                   </xsl:when> 
          </xsl:choose>
      </pto>          
    </story>
    </document>
</xsl:template>

<!-- ==================================================================
   PLANTILLA nueva AGRUPADOS SIN DATOS PRIMARIOS MODE LIST = 2
 ====================================================================== --> 
<xsl:template name="grouping_no_detail">
    <blockTable style="tablePageDetails" colWidths="80,80" >
        <xsl:call-template name="breaks_grouping_no_detail"></xsl:call-template>                    
    </blockTable>            
    
</xsl:template>


<!-- ==================================================================
   PLANTILLA DE ENCABEZADO 
 ====================================================================== -->
<xsl:template name="head_column">
    <blockTable  style="tablePageHeader" colWidths="80,80" >
         <tr>
              <td><para style="pHeaderR">Fecha Contratacion</para></td>
        <td><para style="pHeaderR">Fecha de Vencimiento</para></td>
        
         </tr>        
         </blockTable>   
   </xsl:template>
   
<!-- ==================================================================
   PLANTILLA DE ENCABEZADO 
 ====================================================================== -->
<xsl:template name="head_column_span">
    <blockTable  style="tablePageHeader" colWidths="80,80" >
          <tr>
        <td><para style="pTotalString">Fecha Contratacion</para></td>
                 <td><para style="pTotalString">Fecha de Vencimiento</para></td>
                 </tr>
               
    </blockTable>   
 </xsl:template>
 <!-- ==================================================================
   PLANTILLA PARA CONTADOR TOTAL 
 ====================================================================== -->
<xsl:template name="records_muenchian">
       <xsl:for-each select="model[generate-id() = generate-id(key('key1', concat(generate-id(model),  campo1,'+',campo2))[1]) ]">   
            <xsl:if test="position()=last()">
                   <xsl:value-of select="position()"/>
            </xsl:if>
       </xsl:for-each>
   </xsl:template>
 <!-- ==================================================================
   PLANTILLA PARA MINIMO 
 ====================================================================== -->
    <xsl:template name="minimun">
        <xsl:param name="pSequence"/>
        <xsl:for-each select="$pSequence">
            <xsl:sort select="." data-type="number" order="ascending"/>
            <xsl:if test="position()=1">
                <xsl:value-of select="format-number(., '#.00')"/>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
 <!-- ==================================================================
   PLANTILLA PARA MAXIMO 
 ====================================================================== -->
    <xsl:template name="maximun">
        <xsl:param name="pSequence"/>
        <xsl:for-each select="$pSequence">
            <xsl:sort select="." data-type="number" order="descending"/>
            <xsl:if test="position()=1">
                <xsl:value-of select="format-number(., '#.00')"/>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
<!-- ==================================================================
   PLANTILLA PARA DATOS PRIMARIOS MODE LIST = 1 
 ====================================================================== -->
    <xsl:template name="primary_data"> 
         <blockTable style="tablePageDetails" colWidths="80,80" >
               <xsl:call-template name="breaks_primary_data"></xsl:call-template>                    
        </blockTable>        
        
    </xsl:template>  
 <!-- ==================================================================
   PLANTILLA PARA AGRUPAMIENTOS CON DETALLES
 ====================================================================== -->
  <xsl:template name="grouping_detail">
 <blockTable style="tablePageDetails" colWidths="80,80" >
         <xsl:for-each select="model[generate-id() = generate-id(key('key1', concat(generate-id(model),  campo1,'+',campo2))[1]) ]">
         <xsl:sort/>   
         <xsl:variable name="vkeyGroup" select="key('key1', concat(generate-id(model),  campo1,'+',campo2))"/>
         <xsl:call-template name="detailswithparam">             
                <xsl:with-param name="llave" select="$vkeyGroup"/>                
         </xsl:call-template>         
         <tr>
             <td></td>
        <td></td>
        
         </tr>        
        </xsl:for-each>        
        </blockTable>
        
</xsl:template>
 <!-- ==================================================================
   PLANTILLA PARA FILTRAR POR LLAVES
 ====================================================================== -->
<xsl:template name="detailswithparam">                          
    <xsl:param name="llave"/>
    <xsl:for-each select="$llave">            
           <tr>
           <td><para style="pNumber"><xsl:call-template name="formato_fecha"><xsl:with-param name="valor" select="campo1"/><xsl:with-param name="formato" select="itemsDate/numberDate"/></xsl:call-template></para></td>
            <td><para style="pNumber"><xsl:call-template name="formato_fecha"><xsl:with-param name="valor" select="campo2"/><xsl:with-param name="formato" select="itemsDate/numberDate"/></xsl:call-template></para></td>
            
           </tr>
    </xsl:for-each>
</xsl:template>
 <!-- ==================================================================
   PLANTILLA PARA CONTAR DETALLES
 ====================================================================== -->
<xsl:template name="records_count">
       <xsl:for-each select="model">   
            <xsl:if test="position()=last()">
                   <xsl:value-of select="position()"/>
            </xsl:if>
       </xsl:for-each>
</xsl:template>
 <!-- ==================================================================
   PLANTILLA PARA HEADER CORPORATIVO
 ====================================================================== -->
<xsl:template name="corporate_header">
    <xsl:variable name="h_full_left">                                                   
      <xsl:value-of select="//models/corporate-header/corporation/name"/>
      <xsl:value-of select="' '"/>                                            
    </xsl:variable>
    <xsl:variable name="h_full_right">                                                   
         <xsl:value-of select="//models/corporate-header/corporation/rml_header1"/>                      
    </xsl:variable>      
    <pageGraphics> 
        <image file="addons/base/res/res_company_logo.png"  x="1.3cm" y="28.0013302295cm" height="40" />      
        <setFont name="DejaVu Sans" size="8"/><fill color="black"/> <stroke color="black"/> 
        <lines>57.6 798.8 537.4 798.8</lines> 
        <drawString      x="57.6" y="788.8"> <xsl:value-of select="$h_full_left"></xsl:value-of></drawString> 
        <drawRightString x="537.4"  y="788.8"> <xsl:value-of select="$h_full_right"></xsl:value-of>- Pag: <pageNumber/>/<pageCount/></drawRightString> 
    </pageGraphics>
</xsl:template> 
<!-- ==================================================================
   PLANTILLA PARA CAMPOS SELECCTION
 ====================================================================== -->
 

<!-- ==================================================================
   PLANTILLA PARA CAMPOS FECHAS
 ====================================================================== -->
 <xsl:template name="formato_fecha">                          

   <xsl:param name="valor"/>
   <xsl:param name="formato"/>
       <xsl:choose>    
           <xsl:when test="string-length($valor)=0"><xsl:value-of select="$valor"></xsl:value-of></xsl:when>
           <xsl:when test="string-length($valor) &gt; 0">
               <xsl:choose>    
                <xsl:when test="$formato=1"><xsl:value-of select="concat(substring($valor,1,3),'-',substring($valor,6,2),'-',substring($valor,9,2))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=2"><xsl:value-of select="concat(substring($valor,1,4),'/',substring($valor,6,2),'/',substring($valor,9,2))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=3"><xsl:value-of select="concat(substring($valor,9,2),'-',substring($valor,6,2),'-',substring($valor,1,4))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=4"><xsl:value-of select="concat(substring($valor,9,2),'/',substring($valor,6,2),'/',substring($valor,1,4))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=5"><xsl:value-of select="concat(substring($valor,6,2),'-',substring($valor,9,2),'-',substring($valor,1,4))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=6"><xsl:value-of select="concat(substring($valor,6,2),'/',substring($valor,9,2),'/',substring($valor,1,4))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=11"><xsl:value-of select="concat(substring($valor,3,2),'-',substring($valor,6,2),'-',substring($valor,9,2))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=21"><xsl:value-of select="concat(substring($valor,3,2),'/',substring($valor,6,2),'/',substring($valor,9,2))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=31"><xsl:value-of select="concat(substring($valor,9,2),'-',substring($valor,6,2),'-',substring($valor,3,2))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=41"><xsl:value-of select="concat(substring($valor,9,2),'/',substring($valor,6,2),'/',substring($valor,3,2))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=51"><xsl:value-of select="concat(substring($valor,6,2),'-',substring($valor,9,2),'-',substring($valor,3,2))"></xsl:value-of></xsl:when>
                <xsl:when test="$formato=61"><xsl:value-of select="concat(substring($valor,6,2),'/',substring($valor,9,2),'/',substring($valor,3,2))"></xsl:value-of></xsl:when>
                <xsl:otherwise><xsl:value-of select="concat(substring($valor,9,2),'/',substring($valor,6,2),'/',substring($valor,3,2))"></xsl:value-of></xsl:otherwise>
             </xsl:choose>
           </xsl:when> 
       </xsl:choose>
 </xsl:template>
<!-- ==================================================================
   PLANTILLA PARA RESUMIR
 ====================================================================== -->
<xsl:template name="totalresumen">
   
</xsl:template> 
 <!-- ==================================================================
      PLANTILLA PARA DATOS PRIMARIOS CON Y SIN ROMPIMIENTOS
  ====================================================================== -->
<xsl:template name="breaks_primary_data">
            <xsl:choose>
                <!-- No hay rompimientos -->
                
                <xsl:when test="$mode_break=0">
                    <xsl:for-each select="model">
                       <xsl:sort/> 
                       <tr>
                         <td><para style="pNumber"><xsl:call-template name="formato_fecha"><xsl:with-param name="valor" select="campo1"/><xsl:with-param name="formato" select="itemsDate/numberDate"/></xsl:call-template></para></td>
            <td><para style="pNumber"><xsl:call-template name="formato_fecha"><xsl:with-param name="valor" select="campo2"/><xsl:with-param name="formato" select="itemsDate/numberDate"/></xsl:call-template></para></td>
            
                       </tr>
                   </xsl:for-each>
                </xsl:when> 
                
                <!-- Romper por primera columna -->
                
                <xsl:when test="$mode_break=1">
                
                         <xsl:for-each select="model[generate-id()=generate-id(key('keyH1', campo1)[1])]">
                             <xsl:sort/> 
                             <xsl:variable name="vkeyGroup" select="key('keyH1', campo1)"/>
                              <xsl:call-template name="HeaderBreak"> 
                                  <xsl:with-param name="llave" select="$vkeyGroup"/> 
                                  <xsl:with-param name="nivel" select="1"/> 
                              </xsl:call-template>  
                              <xsl:call-template name="DetailsBreak"> 
                                  <xsl:with-param name="llave" select="$vkeyGroup"/>                                   
                              </xsl:call-template>  
                         </xsl:for-each>                        
                        
                </xsl:when> 
                
                <!-- Romper por primera y segunda columna -->
                
                <xsl:when test="$mode_break=2">

                     <xsl:for-each select="model[generate-id() = generate-id(key('keyH1', concat(generate-id(model),campo1))[1])]">
                     <xsl:sort/>                     
                             <xsl:variable name="vkeyGroup1" select="key('keyH1',campo1)" />
                              <xsl:call-template name="HeaderBreak"> 
                                 <xsl:with-param name="llave" select="$vkeyGroup1"/>
                                 <xsl:with-param name="nivel" select="1"/>
                              </xsl:call-template>  
                             <xsl:for-each select="$vkeyGroup1[generate-id()=generate-id(key('keyH2', concat(generate-id(model),   campo1,'+',campo2))[1])]">
                                   <xsl:variable name="vkeyGroup2" select="key('keyH2', concat(generate-id(model),  campo1,'+',campo2))"/>
                                   <xsl:call-template name="HeaderBreak">
                                       <xsl:with-param name="llave" select="$vkeyGroup2"/>
                                       <xsl:with-param name="nivel" select="2"/>
                                   </xsl:call-template>  
                                    <xsl:call-template name="DetailsBreak"> 
                                    <xsl:with-param name="llave" select="$vkeyGroup2"/>                                   
                                    </xsl:call-template>  
                             </xsl:for-each>
                     </xsl:for-each>
                </xsl:when> 
                
                <!-- Romper por primera , segunda y 3era columna -->
                
                <xsl:when test="$mode_break=3">

                     <xsl:for-each select="model[generate-id() = generate-id(key('keyH1', concat(generate-id(model),campo1))[1])]">
                     <xsl:sort/>                     
                             <xsl:variable name="vkeyGroup1" select="key('keyH1',campo1)" />
                              <xsl:call-template name="HeaderBreak"> 
                                 <xsl:with-param name="llave" select="$vkeyGroup1"/>
                                 <xsl:with-param name="nivel" select="1"/>
                              </xsl:call-template>  
                             <xsl:for-each select="$vkeyGroup1[generate-id()=generate-id(key('keyH2', concat(generate-id(model),   campo1,'+',campo2))[1])]">
                                   <xsl:variable name="vkeyGroup2" select="key('keyH2', concat(generate-id(model),  campo1,'+',campo2))"/>
                                   <xsl:call-template name="HeaderBreak">
                                       <xsl:with-param name="llave" select="$vkeyGroup2"/>
                                       <xsl:with-param name="nivel" select="2"/>
                                   </xsl:call-template>  
                                   <xsl:for-each select="$vkeyGroup2[generate-id()=generate-id(key('keyH3', concat(generate-id(model),   campo1,'+',campo2,'+',campo3 ))[1])]">
                                         <xsl:variable name="vkeyGroup3" select="key('keyH3', concat(generate-id(model),  campo1,'+',campo2,'+',campo3))"/>                                   
                                         <xsl:call-template name="HeaderBreak">
                                         <xsl:with-param name="llave" select="$vkeyGroup3"/>
                                         <xsl:with-param name="nivel" select="3"/>
                                         </xsl:call-template>  
                                         <xsl:call-template name="DetailsBreak"> 
                                         <xsl:with-param name="llave" select="$vkeyGroup3"/>                                   
                                         </xsl:call-template>  
                                    </xsl:for-each>                                                                      
                             </xsl:for-each>
                     </xsl:for-each>
                </xsl:when> 
           </xsl:choose>
</xsl:template> 
 <!-- ==================================================================
 PLANTILLA PARA MOSTRAR LOS ENCABEZADOS DEL ROMPIMIENTO hasta 3 niveles
 ====================================================================== -->
 <xsl:template name="HeaderBreak">                          
    <xsl:param name="llave"/> 
    <xsl:param name="nivel"/> 
    <xsl:for-each select="$llave">            
       <xsl:if test="position()=1">    
             <xsl:choose>
                 <xsl:when test="$nivel=1">
                        <xsl:variable name="valueCampo">
                            <xsl:choose>
                               <xsl:when test="string-length(campo1) &gt; 0"><xsl:value-of select="campo1"></xsl:value-of></xsl:when>
                               <xsl:otherwise>Sin definir</xsl:otherwise>
                           </xsl:choose>    
                        </xsl:variable>
                        <tr>      
                           <td><para style="pTotalString"><xsl:value-of select="$valueCampo"></xsl:value-of></para></td><xsl:call-template name="EmptyTable"> <xsl:with-param name="td" select="1"/></xsl:call-template>
                        </tr> 
                 </xsl:when> 
             <xsl:when test="$nivel=2">
                        <xsl:variable name="valueCampo">
                            <xsl:choose>
                               <xsl:when test="string-length(campo2) &gt; 0"><xsl:value-of select="campo2"></xsl:value-of></xsl:when>
                               <xsl:otherwise>Sin definir</xsl:otherwise>
                           </xsl:choose>    
                        </xsl:variable>
                        <tr>
                          <td></td><td><para style="pTotalString"><xsl:value-of select="$valueCampo"></xsl:value-of></para></td><xsl:call-template name="EmptyTable"> <xsl:with-param name="td" select="0"/></xsl:call-template>
                        </tr>
             </xsl:when> 
             
             <xsl:when test="$nivel=3">
                        <xsl:variable name="valueCampo">
                            <xsl:choose>
                               <xsl:when test="string-length(campo3) &gt; 0"><xsl:value-of select="campo3"></xsl:value-of></xsl:when>
                               <xsl:otherwise>Sin definir</xsl:otherwise>
                           </xsl:choose>    
                        </xsl:variable>
                        <tr>      
                          <td></td><td></td><td><para style="pTotalString"><xsl:value-of select="$valueCampo"></xsl:value-of></para></td><xsl:call-template name="EmptyTable"> <xsl:with-param name="td" select="-1"/></xsl:call-template>
                        </tr>
             </xsl:when> 
         </xsl:choose>
      </xsl:if>        
  </xsl:for-each>                
 </xsl:template> 
    <!-- ==================================================================
    PLANTILLA PARA MOSTRAR RESTO DE LOS DETALLES SEGUN NIVEL DE ROMPIMIENTO
    ====================================================================== -->
    <xsl:template name="DetailsBreak">
        <xsl:param name="llave"/>                          
        <xsl:for-each select="$llave">            
           <xsl:choose>
               <xsl:when test="$mode_break=1">
                    <tr>
                       <td></td>
            <td><para style="pNumber"><xsl:call-template name="formato_fecha"><xsl:with-param name="valor" select="campo2"/><xsl:with-param name="formato" select="itemsDate/numberDate"/></xsl:call-template></para></td>
            
                    </tr>
               </xsl:when> 
               <xsl:when test="$mode_break=2">
                    <tr>
                       <td></td><td></td>
            
                   </tr>
               </xsl:when> 
               <xsl:when test="$mode_break=3">
                    <tr>
                       ********
            
                    </tr>
               </xsl:when>
          </xsl:choose>                
        </xsl:for-each>
    </xsl:template>
    <!--==================================================================
     PLANTILLA PARA MOSTRAR RESTO DE TD VACIAS SEGUN PARAMETRO 
    ====================================================================== -->
    <xsl:template name="EmptyTable">                          
       <xsl:param name="td"/>
       <xsl:if test="$td=1"> <td></td> </xsl:if>         
       <xsl:if test="$td=2"> <td></td> <td></td> </xsl:if>         
       <xsl:if test="$td=3"> <td></td> <td></td> <td></td> </xsl:if>         
       <xsl:if test="$td=4"> <td></td> <td></td> <td></td> <td></td> </xsl:if>         
       <xsl:if test="$td=5"> <td></td> <td></td> <td></td> <td></td> <td></td> </xsl:if>         
       <xsl:if test="$td=6"> <td></td> <td></td> <td></td>  <td></td> <td></td> <td></td> </xsl:if>             
       <xsl:if test="$td=7"> <td></td> <td></td> <td></td> <td></td>  <td></td> <td></td> <td></td> </xsl:if>
       <xsl:if test="$td=8"> <td></td> <td></td> <td></td> <td></td> <td></td><td></td> <td></td> <td></td> </xsl:if>
       <xsl:if test="$td=9"> <td></td> <td></td> <td></td> <td></td> <td></td><td></td> <td></td> <td></td> <td></td></xsl:if>
       <xsl:if test="$td=10"><td></td> <td></td> <td></td> <td></td> <td></td><td></td> <td></td> <td></td> <td></td><td></td></xsl:if>
       <xsl:if test="$td=11"><td></td> <td></td> <td></td> <td></td> <td></td><td></td> <td></td> <td></td> <td></td><td></td><td></td></xsl:if>
       <xsl:if test="$td=12"><td></td> <td></td> <td></td> <td></td> <td></td><td></td> <td></td> <td></td> <td></td><td></td><td></td><td></td></xsl:if>
       <xsl:if test="$td=13"><td></td> <td></td> <td></td> <td></td> <td></td><td></td> <td></td> <td></td> <td></td><td></td><td></td><td></td><td></td></xsl:if>                               
    </xsl:template>
    <!-- ==================================================================
     PLANTILLA PARA DATOS AGRUPADOS SIN/ROMPIMIENTOS
 ====================================================================== --> 
    <xsl:template name="breaks_grouping_no_detail">
            <xsl:choose>
            
                <!-- No hay rompimientos -->
                
                <xsl:when test="$mode_break=0">
                         <xsl:for-each select="model[generate-id() = generate-id(key('key1', concat(generate-id(model), campo1,'+',campo2))[1])]">
                         <xsl:sort/>   
                         <xsl:variable name="vkeyGroup" select="key('key1', concat(generate-id(model),  campo1,'+',campo2))"/>
                         <tr>
                            <td><para style="pNumber"><xsl:call-template name="formato_fecha"><xsl:with-param name="valor" select="campo1"/><xsl:with-param name="formato" select="itemsDate/numberDate"/></xsl:call-template></para></td>
            <td><para style="pNumber"><xsl:call-template name="formato_fecha"><xsl:with-param name="valor" select="campo2"/><xsl:with-param name="formato" select="itemsDate/numberDate"/></xsl:call-template></para></td>
            
                         </tr>        
                         </xsl:for-each>        
               </xsl:when>
                
                <!-- Romper por primera columna -->
                
                <xsl:when test="$mode_break=1">
                         <xsl:for-each select="model[generate-id()=generate-id(key('keyH1', campo1)[1])]">
                             <xsl:sort/>
                             
      <xsl:variable name="vkeyGroup1"  select="key('keyH1', campo1)"/>
         <xsl:call-template name="HeaderBreak"> 
            <xsl:with-param name="llave" select="$vkeyGroup1"/>
            <xsl:with-param name="nivel" select="1"/> 
         </xsl:call-template>
     
                              <xsl:for-each select="$vkeyGroup1[generate-id() = generate-id(key('key1', concat(generate-id(model), campo1,'+',campo2))[1])]">
                              <xsl:sort/>   
                              <xsl:variable name="vkeyGroup2" select="key('key1', concat(generate-id(model), campo1,'+',campo2))"/>
                              <tr>
                                <td></td>
            <td><para style="pNumber"><xsl:call-template name="formato_fecha"><xsl:with-param name="valor" select="campo2"/><xsl:with-param name="formato" select="itemsDate/numberDate"/></xsl:call-template></para></td>
             
                              </tr>        
                              </xsl:for-each>                                 
                        </xsl:for-each>                            
                </xsl:when>
                
                <!-- Rompen por 1 y 2 columnas -->
                
                <xsl:when test="$mode_break=2">
                
                    <xsl:for-each select="model[generate-id() = generate-id(key('keyH1', concat(generate-id(model),campo1))[1])]">
                        <xsl:sort/>
                             
      <xsl:variable name="vkeyGroup1"  select="key('keyH1', campo1)"/>
         <xsl:call-template name="HeaderBreak"> 
            <xsl:with-param name="llave" select="$vkeyGroup1"/>
            <xsl:with-param name="nivel" select="1"/> 
         </xsl:call-template>
                     
                             <xsl:for-each select="$vkeyGroup1[generate-id() = generate-id(key('keyH2', concat(generate-id(model), campo1,'+',campo2))[1])]">
                                   <xsl:sort/>
                                   
      <xsl:variable name="vkeyGroup2" select="key('keyH2', concat(generate-id(model),  campo1,'+',campo2))"/>  
      <xsl:call-template name="HeaderBreak">
         <xsl:with-param name="llave" select="$vkeyGroup2"/>
         <xsl:with-param name="nivel" select="2"/>
      </xsl:call-template>
    
                                   <xsl:for-each select="$vkeyGroup2[generate-id() = generate-id(key('key1', concat(generate-id(model), campo1,'+',campo2))[1]) ]">                                                                
                                       <xsl:sort/>   
                                       <xsl:variable name="vkeyGroup3" select="key('key1', concat(generate-id(model), campo1,'+',campo2))"/>
                                       <tr>
                                          <td></td><td></td>
            
                                       </tr>        
                                   </xsl:for-each>                                 
                             </xsl:for-each>
                    </xsl:for-each>
                     
                </xsl:when>
                
                <!-- Rompen por 1, 2 y 3 columnas -->
                
                <xsl:when test="$mode_break=3">

                     <xsl:for-each select="model[generate-id() = generate-id(key('keyH1', concat(generate-id(model),campo1))[1])]">
                         <xsl:sort/>
                             
      <xsl:variable name="vkeyGroup1"  select="key('keyH1', campo1)"/>
         <xsl:call-template name="HeaderBreak"> 
            <xsl:with-param name="llave" select="$vkeyGroup1"/>
            <xsl:with-param name="nivel" select="1"/> 
         </xsl:call-template>
                         
                             <xsl:for-each select="$vkeyGroup1[generate-id() = generate-id(key('keyH2', concat(generate-id(model), campo1,'+',campo2))[1])]">
                                   
      <xsl:variable name="vkeyGroup2" select="key('keyH2', concat(generate-id(model),  campo1,'+',campo2))"/>  
      <xsl:call-template name="HeaderBreak">
         <xsl:with-param name="llave" select="$vkeyGroup2"/>
         <xsl:with-param name="nivel" select="2"/>
      </xsl:call-template>
    
                                   <xsl:for-each select="$vkeyGroup2[generate-id() = generate-id(key('keyH3', concat(generate-id(model), campo1,'+',campo2,'+',campo3))[1])]">
                                      
      <xsl:variable name="vkeyGroup3" select="key('keyH3', concat(generate-id(model),  campo1,'+',campo2 ,'+',campo3))"/>
      <xsl:call-template name="HeaderBreak">
         <xsl:with-param name="llave" select="$vkeyGroup3"/>
         <xsl:with-param name="nivel" select="3"/>
      </xsl:call-template>
    
                                      <xsl:for-each select="$vkeyGroup3[generate-id() = generate-id(key('key1', concat(generate-id(model), campo1,'+',campo2))[1]) ]">                                                                
                                          <xsl:sort/>   
                                          <xsl:variable name="vkeyGroup4" select="key('key1', concat(generate-id(model), campo1,'+',campo2))"/>
                                          <tr>
                                             ********
            
                                          </tr>        
                                     </xsl:for-each>                                   
                                   </xsl:for-each>                                 
                             </xsl:for-each>
                     </xsl:for-each>
                     
                </xsl:when> 
           </xsl:choose>
</xsl:template>  
    </xsl:stylesheet> 