# 🔐 **SISTEMA DE PERMISOS PATCO**

## 📋 **RESUMEN EJECUTIVO**

El sistema PATCO implementa un modelo de permisos jerárquico basado en **4 roles principales** que mapean directamente a los roles de negocio de la empresa. Cada rol tiene permisos específicos diseñados para maximizar la seguridad y eficiencia operativa.

---

## 🎯 **ROLES Y PERMISOS**

### **1. 🔧 TÉCNICO** (`group_patco_technician`)
**Filosofía**: "Solo lo que necesito para hacer mi trabajo"

#### **Permisos por Módulo:**
- **✅ Field Service Orders**: Leer/Escribir **solo órdenes asignadas a él**
- **✅ Maintenance Equipment**: Crear nuevos activos, Leer/Escribir activos de sus órdenes
- **✅ Agreement**: Solo lectura de acuerdos relacionados con sus órdenes
- **✅ Stock/Inventory**: Ver/consumir stock de **su furgoneta únicamente**
- **✅ HR**: Solo lectura de su propio perfil
- **✅ AI Agent**: Acceso completo para interactuar con el bot
- **❌ Helpdesk**: Sin acceso (no gestiona tickets)
- **❌ Accounting**: Sin acceso
- **❌ User Management**: Sin acceso

#### **Restricciones de Datos (ir.rule):**
```xml
<!-- Solo órdenes asignadas -->
[('person_id.user_id', '=', user.id)]

<!-- Solo activos de sus órdenes o creados por él -->
['|', ('fsm_order_ids.person_id.user_id', '=', user.id), ('create_uid', '=', user.id)]

<!-- Solo stock de su furgoneta -->
[('location_id.x_technician_id.user_id', '=', user.id)]
```

---

### **2. 👨‍💼 JEFE DE OPERACIONES** (`group_patco_operations_manager`)
**Filosofía**: "Control total operativo, sin facturación"

#### **Permisos por Módulo:**
- **✅ Field Service**: Acceso completo (crear, asignar, cerrar órdenes)
- **✅ Helpdesk**: Acceso completo (crear, gestionar tickets)
- **✅ Maintenance Equipment**: Acceso completo (gestión de activos)
- **✅ Agreement**: Acceso completo (contratos y acuerdos)
- **✅ Stock/Inventory**: Acceso completo (gestión de inventario)
- **✅ HR**: Crear técnicos, asignar habilidades
- **✅ Sales**: Crear cotizaciones y órdenes de venta
- **✅ AI Agent**: Gestión completa del RAG y conocimiento
- **✅ Users**: Crear/gestionar usuarios técnicos
- **❌ Accounting**: **Sin acceso a facturación**

#### **Restricciones Específicas:**
```xml
<!-- Bloqueo total a facturas -->
[('id', '=', 0)]  # Para account.move

<!-- Bloqueo total a pagos -->
[('id', '=', 0)]  # Para account.payment
```

---

### **3. 📊 ADMINISTRATIVO** (`group_patco_administrative`)
**Filosofía**: "Acceso total excepto administración de sistema"

#### **Permisos por Módulo:**
- **✅ Todos los módulos**: Acceso completo
- **✅ Accounting**: Facturación y cobranza completa
- **✅ Users**: Crear todos los tipos de usuario **excepto Administradores**
- **✅ Configuration**: Configuraciones operativas (no técnicas del sistema)

#### **Herencia de Permisos:**
- Hereda todos los permisos del **Jefe de Operaciones**
- Añade permisos de **Facturación** y **Gestión Administrativa**

---

### **4. 👑 GERENTE GENERAL** (`group_patco_administrator`)
**Filosofía**: "Superusuario sin restricciones"

#### **Permisos por Módulo:**
- **✅ TODO**: Acceso completo sin excepciones
- **✅ Users**: Crear cualquier tipo de usuario
- **✅ System**: Configuraciones técnicas y de sistema
- **✅ Database**: Acceso a configuraciones de base de datos

#### **Herencia de Permisos:**
- Hereda todos los permisos del **Administrativo**
- Añade permisos de **Sistema** (`base.group_system`)

---

## 🏗️ **ARQUITECTURA TÉCNICA**

### **Jerarquía de Grupos**
```
Técnico
  ↓ (hereda)
Jefe de Operaciones
  ↓ (hereda)
Administrativo
  ↓ (hereda)
Gerente General
```

### **Integración con Módulos OCA**
El sistema se integra automáticamente con grupos nativos de Odoo y OCA:

```xml
<!-- Field Service -->
fieldservice.group_fsm_user → group_patco_technician
fieldservice.group_fsm_manager → group_patco_operations_manager

<!-- Helpdesk -->
helpdesk_mgmt.group_helpdesk_user → group_patco_operations_manager

<!-- Maintenance -->
maintenance.group_equipment_manager → group_patco_operations_manager

<!-- Agreement -->
agreement.group_agreement_user → group_patco_operations_manager
```

---

## 📁 **ARCHIVOS DE CONFIGURACIÓN**

### **Grupos de Seguridad**
- **Archivo**: `patco_base/security/patco_security_groups.xml`
- **Función**: Define los 4 roles principales y sus relaciones

### **Permisos de Acceso a Modelos**
- **Archivos**: `*/security/ir.model.access.csv` (en cada módulo)
- **Función**: Define permisos CRUD por modelo y grupo

### **Reglas de Registro**
- **Archivo**: `patco_base/security/patco_record_rules.xml`
- **Función**: Implementa restricciones de datos a nivel de fila

---

## 🔍 **MATRIZ DE PERMISOS DETALLADA**

| Módulo/Funcionalidad | Técnico | Jefe Ops | Administrativo | Gerente |
|---------------------|---------|----------|----------------|---------|
| **FSM Orders** | Solo asignadas | Completo | Completo | Completo |
| **Equipment** | Crear/Ver propios | Completo | Completo | Completo |
| **Helpdesk** | ❌ | Completo | Completo | Completo |
| **Agreements** | Solo lectura | Completo | Completo | Completo |
| **Stock** | Solo su furgoneta | Completo | Completo | Completo |
| **Sales** | ❌ | Cotizaciones | Completo | Completo |
| **Accounting** | ❌ | ❌ | Completo | Completo |
| **HR** | Solo su perfil | Gestión técnicos | Completo | Completo |
| **Users** | ❌ | Solo técnicos | Todos excepto Admin | Completo |
| **System Config** | ❌ | ❌ | ❌ | Completo |

---

## 🛡️ **SEGURIDAD Y RESTRICCIONES**

### **Restricciones por Técnico**
1. **Órdenes de Servicio**: Solo ve órdenes donde `person_id.user_id = user.id`
2. **Activos**: Solo ve activos de sus órdenes o creados por él
3. **Stock**: Solo ve ubicaciones donde `x_technician_id.user_id = user.id`
4. **Acuerdos**: Solo ve acuerdos relacionados con sus órdenes
5. **Empleados**: Solo ve su propio perfil

### **Restricciones por Jefe de Operaciones**
1. **Facturas**: Dominio `[('id', '=', 0)]` - Sin acceso
2. **Pagos**: Dominio `[('id', '=', 0)]` - Sin acceso
3. **Usuarios**: No puede crear administradores

### **Sin Restricciones**
- **Administrativo**: Acceso completo excepto configuración de sistema
- **Gerente General**: Sin restricciones

---

## 🚀 **IMPLEMENTACIÓN Y MANTENIMIENTO**

### **Agregar Nuevo Usuario**
1. Ir a **Configuración > Usuarios y Empresas > Usuarios**
2. Crear usuario y asignar **uno** de los 4 grupos PATCO
3. El sistema aplicará automáticamente todos los permisos heredados

### **Modificar Permisos**
1. **Grupos**: Editar `patco_security_groups.xml`
2. **Modelos**: Editar `ir.model.access.csv` del módulo correspondiente
3. **Datos**: Editar `patco_record_rules.xml`
4. Actualizar módulo: `docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_suite --stop-after-init`

### **Debugging de Permisos**
1. **Activar modo desarrollador**
2. **Configuración > Técnico > Seguridad > Reglas de Registro**
3. **Configuración > Técnico > Seguridad > Permisos de Acceso**

---

## ⚠️ **CONSIDERACIONES IMPORTANTES**

### **Buenas Prácticas**
1. **Un solo grupo por usuario**: Asignar solo un grupo PATCO principal
2. **Herencia automática**: Los permisos se heredan automáticamente
3. **Pruebas**: Siempre probar con usuarios de cada rol antes de producción
4. **Documentación**: Mantener este documento actualizado con cambios

### **Limitaciones**
1. **Técnicos**: No pueden ver datos de otros técnicos
2. **Jefe Ops**: No puede acceder a información financiera
3. **Administrativo**: No puede modificar configuración de sistema
4. **Cambios**: Requieren actualización de módulo para aplicarse

### **Seguridad**
1. **Reglas de registro**: Se evalúan en tiempo real
2. **Permisos de modelo**: Se verifican en cada operación CRUD
3. **Herencia**: Los permisos se acumulan, no se sobrescriben
4. **Auditoría**: Todos los cambios quedan registrados en logs

---

## 📞 **SOPORTE Y CONTACTO**

Para modificaciones o consultas sobre el sistema de permisos:
1. **Revisar este documento** primero
2. **Probar en entorno de desarrollo** antes de producción
3. **Documentar cambios** en este archivo
4. **Actualizar módulos** según procedimiento estándar

---

*Última actualización: Enero 2025*
*Versión del sistema: Odoo 18 Community*
*Módulos PATCO: v18.0.1.0.0*