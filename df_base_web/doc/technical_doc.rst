============================================
Documentación Técnica del Módulo df_base_web
============================================

El módulo df_base_web está creado para resolver los problemas y necesidades referentes al desarrollo en OpenERP con openobject, específicamente los relacionados con las funcionalidades necesarias en los widgets que existen actualmente en OpenERP.

A continuación se irán detallando las funcionalidades que están contenidas en el modulo y su forma de utilización a través de ejemplos que puedan ilustrar el uso que puede tener cada funcionalidad. Se analizaran las funcionalidades añadidas por cada widget


openerp.web.form.Field
----------------------
Funcionalidad Agregada:
Posibilidad de especificar que se desea que el valor de este campo se envie aún cuando este readOnly mediante la opción rosend

Modo de uso:
Se especifica en la definición del campo para la vista form un atributo options el cual contendrá como valor un diccionario con la llave rosend con uno de estos volores como true:  "1", "true", "yes", "y", 1 o true cualquier otro valor es tomado como false. 

Ejemplo:

    <field name="name" options='{"rosend": "1"}'/>

Funcionalidad Agregada:
Posibilidad de especificar el mensaje de error cuando el campo no es valido mediante la opción invalidMsg

Modo de uso:
Se especifica en la definición del campo para la vista form un atributo options el cual contendrá como valor un diccionario con la llave invalidMsg y valor el mensaje de error. El mensaje es concatenado con el nombre del campo.

Ejemplo:

    <field name="name" options='{"invalidMsg": "es incorrecto"}'/>

openerp.web.form.FieldDatetime
----------------------
Funcionalidad Agregada:
Posibilidad de especificar la validacion para un rango de fechas y especificar cualquier propiedad disponible en el widget. Para tener
referencia de estás propiedades y funcionalidades se puede dirigir a la ayuda de jQuery relacionada con este widget.

Modo de uso:
Para validar se especifica en la definición del campo para la vista form un atributo options el cual contendrá como valor un diccionario con la llave "greaterThan" y en el valor,
el nombre del campo con el que se desea comparar o una fecha en el formato "yyyy-MM-dd" o "0" para comparar con la fecha actual, en este caso se valida que el valor entrado en el campo sea mayor que el del especificado
si a demas se especifica la llave "ge" con un valor verdadero (ejm:"1", "true", "yes", "y", 1 o true) se valida que el campo pueda ser mayor o igual y con la llave "lessThan" se valida que el valor sea menor y si se especifica "le" se valida que el valor sea menor o igual. 
Si no se especifica un mensaje con la llave invalidMsg mostrara un mensaje por defecto segun el caso.

Para configurar el widget especificar dentro del atributo options, otro elemento de ese diccionario llamado ui_settings y ahí
definir cualquiera de las propiedades existentes en jQuery. 

Ejemplo:

    <field name="date_start"/>
	<field name="date_end" options='{"greaterThan": "date_start", "ui_settings":{"showWeek":"false"}}'/>
ó
	<field name="date_start" options='{"lessThan": "date_end", "ui_settings":{"changeYear":"false"}}'/>
	<field name="date_end"/>
ó
	<field name="date_start" options='{"ui_settings":{"showButtonPanel":"false","changeYear":"false"}}'/>
	<field name="date" options='{"lessThan": "date_end", "greaterThan": "date_start"}'/>
	<field name="date_end"/>
ó
    <field name="date_start" options='{"lessThan": "0", "le": "1"}'/>
	<field name="date_end" options='{"greaterThan": "date_start", "ge": "1"}'/>
ó
	<field name="date_start" options='{"greaterThan": "1950-01-01"}'/>
	<field name="date_end" options='{"lessThan": "0", "le": "1"}'/>/>
	
openerp.web.form.FieldBinaryFile
--------------------------------
Funcionalidad Agregada:
Posibilidad de definir que tipos de archivos van a ser válidos para su selección.

Modo de uso:
Se especifica en la definición del campo para la vista form un atributo options el cual contendrá como valor un diccionario 
con la llave fileType y asociado a esta una cadena que contenga el content type que define el tipo de archivo que será aceptado.
En caso de de especificar más de uno se debe hacer separados por comas.Para un mejor conocimiento de los tipos de archivo remitirse a
http://www.iana.org/assignments/media-types 


Ejemplo:

    <field name="csv_file" options='{"fileType": "text/csv"}'/>
ó
	<field name="csv_and_msword_file" options='{"fileType": "text/csv,application/msword"}'/>
    

openerp.web.form.FieldChar
--------------------------

De este widget heredan unos cuantos widgets en OpenERP, es el utilizado para el tipo de fields char aunque como los demás heredan de este, los cambios que se especifiquen aquí sirven para los demás widgets

Widgets que heredan de openerp.web.form.FieldChar(pueden haber otros):
    - openerp.web.form.FieldID
    - openerp.web.form.FieldEmail
    - openerp.web.form.FieldUrl
    - openerp.web.form.FieldFloat

Funcionalidad Agregada:
Validación adicional del campo mediante una expresión regular de JavaScript especificada desde el xml la vista.

Modo de uso:
Se especifica en la definición del campo para la vista form un atributo options el cual contendrá como valor un diccionario con la llave regex y asociado a esta una cadena que contenga la expresión regular de JavaScript a validarse en el campo. 

Ejemplo:

    <field name="name" options='{"regex": "[0-9]"}'/>
    
Esto pudiera ser la base para establecer validaciones por defecto en los demás widgets que heredan de openerp.web.form.FieldChar para luego por cada uno no tener que especificar la expresión regular correspondiente.


openerp.web.form.FieldEmail
---------------------------
Funcionalidad Agregada:
Validación por defecto de la sintaxis de correo electrónico


openerp.web.form.FieldSelection
-------------------------------
Este widget se utiliza para mostrar un select de html básico de acuerdo a lo especificado en el fields selection de la clase. El inconveniente que tiene este widget es la imposibilidad en OpenERP que hay de especificarle un domain o un conjunto de valores como resultado de un on_change. 

Funcionalidad Agregada:
Posibilidad de especificar un domain para cada valor del campo de forma que si la condicion del domain se evalua a verdadero se deshabilita esa opcion de seleccion

Modo de uso:
	Se debe especificar para el campo un options modifiers con los valores del campo y asociados a cada uno de ellos un domain 

Ejemplo:

.. code-block:: xml
	<field name="context_lang" options='{"modifiers": {"en_US": [["user_email", "=", "axel.mendoza@cmw.desoft.cu"]], "es_ES": [["active", "=", false]]}}'/>

openerp.web.ListView y openerp.web.FormView
-------------------------------------------
Este Widget es el que se ve como una grid, aunque se especifique como tree en la definicion de la vista no es el mismo Widget que el TreeView que se utiliza para mostrar arboles y que se especifica de igual forma como tree en la vista.

Funcionalidad Agregada:
Posibilidad de especificar las opciones de la vista desde el xml de la misma. Esto sin base_web y esta extensión no se puede lograr actualmente en openerp debido a que no existe una forma en la cual se puedan comunicar las opciones de los widgets de vista a diferencia de los widgets para campos de formulario y demás.

Modo de uso:
Se especifica en la definición del tag tree o form de la vista un atributo options el cual contendrá como valor un diccionario con las llaves correspondientes a las opciones y sus valores que queremos establecer para esta vista. 

Opciones que se pueden establecer:
(tomado del codigo fuente en view_list.js)
    // records can be selected one by one
        'selectable': true,
      // list rows can be deleted
        'deletable': true,
      // whether the column headers should be displayed
        'header': true,
      // display addition button, with that label
        'addable': _lt("Create"),
      // whether the list view can be sorted, note that once a view has been
      // sorted it can not be reordered anymore
        'sortable': true,
      // whether the view rows can be reordered (via vertical drag & drop)
        'reorderable': true,
      // display an edit icon linking to form view
        'isClarkGable': true
(encontradas que se utilizan en el codigo, pueden existir otras debido a la herencia de widgets)
    limit
    editable
    sidebar
    sidebar_id

Ejemplo:

    <field name="arch" type="xml">
        <tree string="Actividades" options='{"deletable": false, "addable": null, “sidebar”: false}'>
            <field name="name"/>
            <field name="description"/>
            <field name="valor"/>
        </tree>
    </field>
    
Funcionalidad Agregada:
Se adicionaron botones de accion en la parte superior de la tabla, tomandose las acciones definidas para el modelo que son visibles en el panel lateral.
Modo de uso:
Defina acciones de la forma estandar en OpenERP y estas seran visibles como botones en la toolbar de la lista a continuación de los botones Create y/o Delete.


openerp.web.PageView
--------------------
Funcionalidad Agregada:
Se elimino por defecto que saliera el boton de accion para duplicar, se creo una opcion para mostrarlo.
Modo de uso:
Se puede lograr mostrar el boton de accion para duplicar mediante la opcion duplicate con valor true a la definicion del form en xml
Ejemplo:
   
    <field name="arch" type="xml">
        <form string="Title" options='{"duplicate": true}'>
           <field name="name"/> 
           <field name="category"/>
           <field name="description"/> 
        </form>
    </field>

custom_actions
--------------
Se adiciono la posibilidad de especificar botones de accion que se mostraran en el ListView para ejecutar una accion definida en un modelo
Ejemplo:

    <field name="arch" type="xml">
        <tree string="Title" options='{"custom_actions": [{"model": "res.partner", "method": "create", "args": [], "label": "Create a Partner"}]}'>
           <field name="name"/> 
           <field name="category"/>
           <field name="description"/> 
        </tree>
    </field>
    

cancel_action
-------------
Se adicionó la posibilidad de llamar a una función cuando es accionado el botón cancelar del formulario.
Ejemplo:

    <field name="arch" type="xml">
        <form string="Title" options='{"cancel_action": {"model": "res.partner", "method": "create", "args": []}}'>
           <field name="name"/> 
           <field name="category"/>
           <field name="description"/> 
        </form>
    </field>
     
options modifiers
-----------------
Se adiciono la posibilidad de especificar modificadores de opciones las cuales funcionan en base a domains y que permiten alterar las opciones de la vista en base a los valores de los campos.
En el widget FormView funciona con todas las opciones disponibles de las vistas.
En el widget ListView funciona con todas las opciones disponibles de las filas, es decir se varian y aplican las opciones por registro.

Ejemplo:

    <field name="arch" type="xml">
        <tree string="Title" options='{"modifiers": { "isClarkGable": [["state", "not in", ["draft", "pending", "approval"] ]] } }'>
           <field name="name"/> 
           <field name="category"/>
           <field name="state"/> 
        </tree>
    </field>

Ejemplo:
    <field name="arch" type="xml">
        <form string="Title"  options='{"modifiers": {"action_buttons": [["name", "=", "9"]]}}'>
            <field name="name"/> 
            <field name="category"/>
            <field name="state"/>
        </form>
    </field>


openerp.web.search.ReferenceField
---------------------------------
Este widget no existe en OpenERP y sera creado para posibilitar incluir campos de tipo reference en vistas search para realizar búsquedas.


openerp.web.form.WidgetButton
-----------------------------
Este widget es utilizado para mostrar un botón que ejecute una acción.
Opcionalmente es posible especificar una imagen a través del atributo icon. La imagen especificada debe encontrarse en la dirección /web/static/src/img/icons/ 

Funcionalidad Agregada:
Se adicionó un nuevo atributo (icon_src) que permite especificar el módulo de OpenERP que contiene la imagen, dando la posibilidad a cada módulo de contener las imágenes que necesite.
  
Ejemplo:

    <button name="button_cancel" string="Cancel" icon="close" icon_src="df_base_web"/>

Esto permite buscar la imagen en la dirección /df_base_web/static/src/img/icons/.


SearchView.filter
-----------------
Este widget es utilizado para mostrar en las vistas de búsqueda un botón que permite buscar o agrupar por una columna determinada.
Es posible especificar una imagen a través del atributo icon. la imagen especificada debe encontrarse en la dirección /web/static/src/img/icons/ 

Funcionalidad Agregada:
Se adicionó un nuevo atributo (icon_src) que permite especificar el módulo de OpenERP que contiene la imagen, dando la posibilidad a cada módulo de contener las imágenes que necesite.

Ejemplo:

    <filter name="closed" icon="close"  icon_src="df_base_web" string="Closed" domain="[('state','=','closed')]" help="Closed Document"/>

Esto permite buscar la imagen en la dirección /df_base_web/static/src/img/icons/.


openerp.web.form.Many2ManyListView
----------------------------------
Funcionalidad Agregada:
- Se le adicionaron chequeos de permisos para controlar que no se puedan crear elementos usando el widget de acuerdo a la configuracion de seguridad del usuario para el modelo en cuestión.
- Se adiciono la opción nocreate para controlar que no se puedan crear elementos usando el widget para este campo aun cuando el chequeo de permisos permita hacerlo.

Ejemplo:

     <field name="category_ids" widget="many2many" options='{"nocreate": true}'/>


openerp.web.form.Many2ManyListView, openerp.web.form.FieldMany2Many, openerp.web.form.FieldOne2Many, openerp.web.form.FieldMany2One
-----------------------------------------------------------------------------------------------------------------------------------
Funcionalidad Agregada:
- Se le adicionaron chequeos de permisos para controlar que no se puedan crear elementos usando el widget de acuerdo a la configuracion de seguridad del usuario para el modelo en cuestión.
- Se adiciono la opción nocreate para controlar que no se puedan crear elementos usando el widget para este campo aun cuando el chequeo de permisos permita hacerlo.
    Ejemplo:
        <field name="category_ids" widget="many2many" options='{"nocreate": true}'/>

- Se adicionaron las opciones list_view_options y form_view_options para controlar un poco las opciones de las vistas list y form que son utilizadas en el add del widget many2many
    - Las opciones que se pueden especificar son:
        - para list_view_options y form_view_options:
            - view_id: aqui se puede especificar el nombre completo de la vista incluyendo el nombre del modulo en el que fue declarada
                Ejemplo:
                    <field name="bank_ids" nolabel="1" options='{"list_view_options": {"view_id": "df_contract.df_partner_bank_tree_view"}}'/>
                    
        - para list_view_options:
            - domain: se utiliza para aplicar un domain a la vista ListView de seleccion, el valor de este campo es un domain en forma de cadena de texto
                Ejemplo: 
                    <field name="bank_ids" options='{"list_view_options":{"domain": "[[\"code\",\"!=\",code],[\"partner_id\",\"=\",partner_id], [\"nature\",\"=\",context.get(\"nature\",\" \")], [\"type\", \"in\",context.get(\"dom_t\",False)], [\"state\", \"in\",context.get(\"dom_s\",False) ]] " } }'/>
                    
            - context: se utiliza para especificar el context a utilizar en la vista ListView de seleccion
- Para el FieldMany2One existen tambien las opciones nosearch y noopen ademas de nocreate, las cuales deshabilitan los botones del menu contextual relativas a estas opciones.

openerp.web.form.FieldReference
-------------------------------
Funcionalidad Agregada:
- Se adiciono la opción model_domains para permitir especificar domains para el many2one del campo reference en dependencia del modelo que esta seleccionado.
    Ejemplo:
        <field name="received_by" options='{"model_domains": {"res.users": [["id", "=", "1"]], "res.partner": [["id", "=", "2"]]}}' />
- Se adiciono la opción model_options para permitir especificar options para el many2one del campo reference en dependencia del modelo que esta seleccionado.
    Ejemplo:
        <field name="received_by" options='{"model_options": {"res.users": {"nocreate": true}}}' />


moficadores de opciones en las vistas
-------------------------------------
        <record model="ir.ui.view" id="view_contract_proform_supplement_contract_tree">
            <field name="name">df.contract.tree</field>
            <field name="model">df.contract</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <tree string="contract"
                    colors="red:state=='pending';grey:state in ('cancel', 'done', 'proform');blue:one_month_after_date"
                    options='{"modifiers": { "isClarkGable": [["state", "not in", ["draft", "pending", "approval"] ]] } }'>
                    
                    <field name="number" string="Number" />
                    <field name="partner_id" />
                    <field name="parent_id"/>
                    <field name="type" invisible="1"/>
                    <field name="filing_date" />
                    <field name="current_date" />
                    <field name="validity_date_progress" widget="progressbar" />
                    <field name="import_amount" />
                    <field name="state" />

                    <field name="one_month_after_date"  invisible="1"/>

                </tree>
            </field>
        </record>
        
options como resultado del on_change
------------------------------------
En el codigo Python se pueden retornar opciones para los campos como parte de un onchange de la forma:
    Ejemplo:
        return {'options':{
            'caja_id': {
                nocreate: true
            },
            'banco_id': {
                nocreate: false
            }
        }}

parametros extra como entrada al on_change
------------------------------------------
En las vistas XML se puede enviar como parametros al onchange cualquier valor que posea el campo como objeto en el dom usando la notacion de '.', esto posibilita enviar argumentos tales como las opciones del campo:
    Ejemplo: 
        on_product_change(product_ids, context, product_ids.options)
            o
        on_product_change(product_ids, context, product_ids.dirty)
            o
        on_product_change(product_ids, context, product_ids.widget_parent.options)
        
ir.ui.menu, ir.ui.menu.hider
------------------------------------
Funcionalidad agregada:
- Se adiciona la posibilidad de ocultar entradas de menú. Las entradas de menú afectadas, lo estarán solamente mientras que exista el objeto que las ocultas,
por lo que el cambio es reversible.
Modo de uso:
- Se declara un objeto de tipo ir.ui.menu.hider cuyo atributo hidden_items es un listado con los menuitem a ocultar.
Ejemplo:

	<record id="menu_sales_hide" model="ir.ui.menu.hider">
		<field name="hidden_items" eval="[(6, 0, [ref('crm.menu_crm_case_opp'), ref('crm.menu_crm_case_categ0_act_leads')])]" />
	</record>

record readonly en el Form
--------------------------
implementada la opcion readonly para bloquear la edicion de un registro en un formulario y cambiar automaticamente a la vista Page. Se puede especificar de 2 formas como todas las opciones de los widgets:
1- La primera es con un valor fijo de la forma:
	<form string="Municipalities" options='{"readonly": true}'>

2- La segunda es mediante el uso de los modificadores de opciones los cuales tienen en cuenta que se cumpla una condicion especificada mediante un domain de la forma:
	<form string="Municipalities" options='{"modifiers": {"readonly": [["state", "=", "done"]]}}'>

focus de un page en el notebook
-------------------------------
Funcionalidad Agregada:
Posibilidad de establecerle el focus a una pestaña específica de un notebook es decir que salga seleccionada por defecto.

Modo de uso:
Se especifica en la definición del campo para la vista form un atributo default_focus que contenga el valor True o un dominio. 

Ejemplo:

    <page options='{"default_focus": true}'> 
ó
	<page options='{"modifiers": {"default_focus": [["state","=","open"]]}}'>  
	
Opciones para ocultar los botones de la vista search
----------------------------------------------------
A las vistas search se le pueden especificar las opciones:
searchable: para que no salga el boton de buscar
clearable: para que no salga el boton de limpiar
filterable: para que no salgan los filtros

Ejemplo:
	<search string="Search Sale Orders" options='{"searchable": false, "clearable": false, "filterable": false}'>
	

Mostrar acciones de menú lateral derecho según vistas XML
---------------------------------------------------------

**Funcionalidad Agregada:** Posibilidad de restringir las acciones(definidas para un modelo) que
aparecen en el menú lateral derecho(MLD) de acuerdo a vistas definidas en un mismo modelo.

**Caso ejemplo donde se hace necesario emplear esta funcionalidad:**
En el módulo *crm* se tiene el recurso *crm.lead*. Entre unos de sus usos 
en el módulo, este se emplea para representar conceptos como *Iniciativas* 
y *Oportunidades*. En el caso de *Iniciativas* (en la vista listado) se requiere mostrar en el MLD la 
funcionalidad: *Convertir a Oportunidad*

Sin emplear la funcionalidad que aquí se presenta, ocurre un efecto no 
deseado y es que aparece la opción *Convertir a Oportunidad* en la 
vista de listado de *Oportunidades*. Esto ocurre debido a que tanto una 
*Iniciativa* como una *Oportunidad* pertenecen al mismo modelo: *crm.lead*.

**Modo de uso:**
Se declara en un XML compatible con OpenERP una instancia del objeto de tipo *ir.values.filter* 
donde se debe espeficar los parámetros *ir_values_id* y 
*ir_ui_view_id*, ambos requeridos. *ir_values_id* representa el 
identificador de la propia acción definida 
en el MLD (dígase acción que llama a ventana, acción que llama a 
reporte, acción que llama a wizard) mientras que *ir_ui_view_id* es el 
identificador de la vista en la cual se quiere que aparezca la acción 
especificada en *ir_values_id*. 

**Ejemplo:**

Porción de código tomada de OpenERP v6.1, módulo *crm*.    

Ubicación: crm/crm_lead_view.xml	 
 
 .. code-block:: xml

	<record model="ir.ui.view" id="crm_case_tree_view_leads">
		...
		<field name="model">crm.lead</field>
		<field name="type">tree</field>
		...
	</record>


Ubicación: crm/wizard/crm_lead_to_opportunity_view.xml	   

 .. code-block:: xml
 
	<act_window id="action_crm_send_mass_convert"
         multi="True"
         key2="client_action_multi" name="Convert opportunities"
         res_model="crm.lead2opportunity.partner.mass" src_model="crm.lead"
         view_mode="form" target="new" view_type="form"
         context='{"mass_convert" : True}'
         view_id="view_crm_lead2opportunity_partner_mass"/> 

De acuerdo a la situación de negocio y funcionalidad descritas anteriormente tendríamos:

 .. code-block:: xml
 
	<record model="ir.values.filter" id="restrict_action_crm">
   	  <field name= "ir_values_id"  
		search="[('value','=','ir.actions.act_window,'+str(action_crm_send_mass_convert)),
		('model','=','crm.lead'),('key2', '=', 'client_action_multi')]"/>
	  <field name="ir_ui_view_id" ref="crm_case_tree_view_leads"/>
	</record>
	

Nota: El parámetro *key2* representa el tipo de entrada (Acciones, 
Enlaces, Reportes) en el MLD. Entre los valores que puede tomar *key2* 
se encuentran:
- *client_action_multi* (entrada Acciones) - Use este valor cuando defina 
una acción(utilizando el tag <act_window>) que llame a un wizard.
- *client_action_relate* (entrada Enlaces) - Use este valor cuando 
defina una acción(utilizando el tag <act_window>) que llame a vistas 
formulario, listado,etc definidas para modelos persistentes.
- *client_print_multi* (entrada Reportes) -  Use este valor cuando defina 
una acción utilizando el tag <report>.

**Observaciones:**

- Notar que el hecho de especificar que una acción tiene asociada una vista (la vista en la que se va a mostrar) significa que la acción solo se verá para esa vista. Si se requiere que la acción esté disponible para varias vistas de un mismo modelo se deberán definir por cada vista una instancia tipo *ir.values.filter*.
 
- No especificar ninguna instancia de tipo *ir.values.filter* implica que cada acción definida en un modelo en particular estará disponible para todas las vistas de dicho modelo.

- Tener en cuenta que en la declaración de la instancia de tipo "ir.values.filter" se deben hacer referencias a vistas y a acciones que ya hayan sido creadas. Tener en cuenta el orden de importación de los ficheros XML.


Traducir el nombre de los ficheros de reportes
----------------------------------------------
Se debe especificar una traducción en el .po para traducir el nombre del fichero pdf que se genera al ejecutar una acción de reporte.

#. module: <modulo>
#: model:ir.actions.report.xml,report_name:<modulo>.<id del acción de reporte>
msgid "report_name value"
msgstr "valor de report_name"

**Ejemplo:**
#. module: df_maintenance
#: model:ir.actions.report.xml,report_name:df_maintenance.report_maintenance_order
msgid "Maintenance_Work_Order"
msgstr "Orden_Trabajo_Mantenimiento"

Cambiar color de fondo o de letra a un field del form
------------------------------------------
Para que un field tome un color de fondo o de letra distinto del original se puede especificar un domain por color en los options modifiers de la siguiente forma:
    
   <field name="state" options='{"rosend": "1","modifiers": {"color":{"green": [["budget_availability", "&#62;", 0]], "red": [["budget_availability", "&#60;&#61;", 0]]}}} />
            o
   <field name="state" options='{"rosend": "1","modifiers": {"background-color":{"green": [["budget_availability", "&#62;", 0]], "red": [["budget_availability", "&#60;&#61;", 0]]}}} />
Se utilizará como color el primer domain que resulte verdadero
nota: los simbolos > , >= hay que escaparlos y poner el codigo html sino da error en la definicion de la vista, el ejemplo los usa pero no es que sean requeridos para el mismo, puede ser cualquier domain 

