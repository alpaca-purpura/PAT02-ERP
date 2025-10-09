# FLUJO FUNCIONAL

## ARBOL DE ACCESO

(0)Conversaciones
└── Lista de conversaciones

(0)Administración
├── (1) Empleados (hr.employee)
│   ├── (2)Departamentos (action id: hr.hr_department_kanban_action)
│   │   ├── Listados 
│   │   │    ├──Search: [nombre: hr.department.search, id:hr.view_department_filter]
│   │   │    └──Kanban: [nombre: hr.department.kanban, id: hr.hr_department_view_kanban]
│   │   └── Formulario
│   │       └──[nombre: hr.department.form, id: hr.view_department_form]
│   │
│   ├── (2)Empleados (action: hr.open_view_employee_list_my, tipo_accion: ir.actions.act_window)
│   │   ├── Listados (todos aparecen como botones en el menú)
│   │   │    ├── Search: [nombre: hr.employee.search, id:view_employee_filter,
│   │   │    │           domain: "['|', ('work_email', 'ilike', self), ('name', 'ilike', self)]"]
│   │   │    ├── Kanban: [nombre: hr.employee.kanban, id: hr.hr_kanban_view_employees]
│   │   │    ├── List: [nombre: hr.employee.list, id: hr.view_employee_tree]
│   │   │    ├── Actividad: [nombre: hr.employee.activity, id: hr.hr_employee_view_activity, modelo: hr.employee.kanban]
│   │   │    └── Organigrama: [nombre: hr.employee.view.hierarchy, id: hr_org_chart.hr_employee_hierarchy_view]
│   │   └── Formulario
│   │       └──[nombre: hr.employee.form, id: hr.view_employee_form]
│   │           └── Botón Iniciar Plan (*Ocultar*)
│   │           └── Pestaña "Curriculum" (*Ocultar*) (la agrega id: hr_skills.hr_employee_view_form name: hr.employee.view.form.inherit.resume)
│   │
│   ├── (2)Usuarios
│   │   └──
│   │
│   ├── (2)Matriz de Habilidades (nombre: Habilidades de Empleados, action: patco_skills_mgmt.action_hr_employee_skill_employee)
│   │   └── List [nombre: hr.employee.skill.list,  id: patco_skills_mgmt.view_hr_employee_skill_list, edit: bottom]
│   │
│   ├── (2)Tipos de Habilidades [action id: patco_skills_mgmt.action_hr_skill_type, objeto: hr.skill.type]
│   │   ├── Form [nombre: hr.skill.type.form, id: hr_skills.hr_employee_skill_type_view_form]
│   │   └── List [nombre: hr.skill.type.list, id: patco_skills.hr_skill_type_view_tree]
│   │
│   └── (2)Niveles de Habilidades [action id: patco_skills_mgmt.action_hr_skill_level, objeto: hr.skill.level]
│       └── List [nombre: hr.skill.level.list, id: hr_skills.employee_skill_level_view_tree, editable: bottom]
│
├── (1)Clientes
│   ├── (2)Clientes (res.partner)
│   │
│   ├── (2)Contactos ()
│   │      
│   ├── (2)Ubicaciones (res.loaction)
│   │   
│   ├── (2)Acuerdos (sale.agreement)  (sale.order)
│   │   
│   └──
│
├── (1) Facturación y Cobranza/
│   ├── (2)Cotizaciones 
│   ├── (2)Órdenes de Venta
│   ├── (2)Facturación
│   ├── (2)Cobranza
│   └── (2)Pagos
│
└── (1) Configuración/
    ├── (2)Ajustes (muestra la ventana de ajustes pero únicamente la sección de empleados. view general: base.res_config_settings_view_form)
    ├── (2*)Empleado
    │   ├── (2)Ubicaciones de trabajo
    │   ├── (2)Horarios de trabajo
    │   ├── (2)Motivos de salida
    │   ├── (2)Tipos de habilidad
    │   ├── (2)Etiquetas
    │   ├── (2)Tipos de lineas (Curriculum)
    │   ├── (2)Puestos de trabajo (*Data pre-cargada*)
    │   ├── (2)Plan de actividad (*Eliminar*)    
    │   └── (2)Tipos de empleo (*Data pre-cargada*)
    │    
    ├── (2*)Clientes
    │   ├── (2)    
    │   └── (2)
    └── (2*)Facturación y Cobranza
        ├── (2)    
        └── (2)

(0)Servicio Técnico/
├── (1)Activos y Manuales
│   ├── (2)Activos de Clientes [action id: patco_equipment.action_maintenance_equipment_patco, 
│   │   │                   ref: maintenance.equipment.search.patco, contexto: {'search_default_active_equipment': 1}]
│   │   ├── List [nombre: maintenance.equipment.list.patco, id: patco_equipment.view_maintenance_equipment_list_patco]
│   │   └── Form [nombre: maintenance.equipment.form.patco, id: patco_equipment.view_maintenance_equipment_form_patco]
│   │   
│   └── (2)Manuales y Checklists [action id: patco_equipment.action_maintenance_equipment_category_patco, 
│       │                       objeto:maintenance.equipment.category]
│       ├── List [nombre: maintenance.equipment.category.list.inherit, 
│       │                    id: patco_equipment.view_list_maintenance_equipment_category_inherit, Vista heredada: equipment.category.list]
│       └── Form [nombre: maintenance.equipment.category.form.patco, id: patco_equipment.view_form_maintenance_equipment_category_new]
│
├── (1)Órdenes de Servicio
│   ├── (2) Mis Ordenes [action id: patco_fsm.action_fsm_order_patco, contexto: {'search_default_my_orders': 1,'search_default_open': 1}]
│   │   ├── List [nombre: fsm.order.list.patco, id: patco_fsm.fsm_order_list_view_patco]
│   │   └── Form [nombre: fsm.order.form.patco, id: patco_fsm.fsm_order_form_view_patco, modelo fsm.order] 
│   │             Asignación técnico-activo: patco_fsm.view_fsm_order_asset_technician_list
│   │
│   └── (2)
│       ├── 
│       └──
│
└── (1)Tickets
    ├── (2)
    │   ├──    
    │   └──
    └── (2)
        ├──    
        └──

(0)Configuración IA/
├── (1)Conversaciones
│   ├── (2)Todas las conversaciones
│   │   ├── 
│   │   └──
│   └──
│       ├── 
│       └──
├── (1)Base de Conocimiento
│   ├── (2)Documentos RAG
│   │   ├── 
│   │   └──
│   └── (2)Pendientes de Indexación
│       ├── 
│       └──
└── (1)Configuración
        ├── Estadísticas IA
        └── Estadísticas RAG

(0)Gerencia/
├── (1)Reporte de Habilidades (nombre: Habilidades del empleado, id: hr_skills.hr_employee_skill_report_action) 
└── (1)Tableros/ 
    ├── (2)Tableros (Action |nombre:Tableros, id:spreadsheet_dashboard.ir_actions_dashboard_action, etiqueta: action_spreadsheet_dashboard) 
    └── (2)Configuración (Action | nombre: Tableros, id: spreadsheet_dashboard.spreadsheet_dashboard_action_configuration_dashboards)
        └── Search (nombre: , id: )
        └── List (nombre: spreadsheet.dashboard.group.view.list, id: spreadsheet_dashboard.spreadsheet_dashboard_container_view_list)
        └── Form (nombre: spreadsheet.dashboard.group.view.form, id: spreadsheet_dashboard.spreadsheet_dashboard_container_view_form)
