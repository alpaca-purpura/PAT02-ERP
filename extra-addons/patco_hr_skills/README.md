# PATCO HR Skills - Gestión de Habilidades Técnicas HORECA

## Descripción

`patco_hr_skills` es el módulo especializado en la gestión integral de habilidades técnicas dentro del ecosistema PATCO. Proporciona un sistema completo para definir, evaluar y gestionar las competencias técnicas específicas del sector HORECA (Hoteles, Restaurantes y Cafeterías), con integración directa al módulo `fieldservice_skill` de OCA para la asignación optimizada de técnicos.

## Funcionalidades Principales

### 1. Gestión de Habilidades Técnicas HORECA
- **Modelo base**: Extensión e integración con `fieldservice_skill`
- **Propósito**: Definir competencias específicas para equipos y servicios HORECA
- **Integración**: Conexión directa con asignación de técnicos en FSM

#### Habilidades Técnicas Típicas:
- **Refrigeración Comercial**: Mantenimiento de cámaras, vitrinas, congeladores
- **Cocina Industrial**: Hornos, freidoras, planchas, equipos de cocción
- **Ventilación HVAC**: Campanas extractoras, sistemas de climatización
- **Lavado Industrial**: Lavavajillas, sistemas de limpieza automatizados
- **Sistemas Eléctricos**: Instalaciones eléctricas especializadas HORECA
- **Fontanería Especializada**: Sistemas de agua caliente, vapor, drenajes
- **Equipos de Bar**: Máquinas de café, dispensadores, equipos de bebidas
- **Panificación**: Hornos de pan, amasadoras, equipos de panadería

### 2. Integración con Field Service Management
- **Modelo integrado**: `fieldservice_skill` (OCA)
- **Funcionalidad**: Asignación automática basada en habilidades requeridas
- **Optimización**: Matching técnico-servicio según competencias
- **Escalamiento**: Asignación por niveles de experiencia

### 3. Matriz de Competencias por Equipo
- **Vinculación**: Habilidades requeridas por tipo de equipo
- **Niveles**: Básico, Intermedio, Avanzado, Especialista
- **Certificaciones**: Registro de certificaciones técnicas
- **Experiencia**: Seguimiento de horas de experiencia por habilidad

### 4. Gestión de Recursos Humanos
- **Modelo extendido**: `hr.employee` (implícito)
- **Funcionalidad**: Perfil de habilidades por técnico
- **Evaluación**: Sistema de evaluación de competencias
- **Desarrollo**: Planes de capacitación y mejora

## Estructura de Archivos

```
patco_hr_skills/
├── __init__.py
├── __manifest__.py
├── security/
│   └── ir.model.access.csv          # Permisos de acceso
├── static/
│   └── description/
│       └── icon.png                 # Icono del módulo
└── README.md
```

**Nota**: El módulo actualmente tiene una estructura mínima con archivos de vistas y datos comentados en el manifiesto, indicando que está en fase de desarrollo o configuración inicial.

## Dependencias

### Módulos Odoo Core:
- `hr`: Gestión de recursos humanos base
- `base`: Funcionalidades básicas del sistema

### Módulos OCA (Integración):
- `fieldservice_skill`: Sistema de habilidades para servicios de campo
- `hr_skill`: Gestión avanzada de habilidades (si está disponible)

### Módulos PATCO:
- `patco_core`: Funcionalidades centrales y naturalezas de servicio
- `patco_customer_equipment`: Vinculación de habilidades con tipos de equipo

## Funcionalidades Técnicas (Planificadas)

### 1. Definición de Habilidades HORECA
```python
# Ejemplo de estructura de habilidades
skills_horeca = {
    'refrigeration': {
        'name': 'Refrigeración Comercial',
        'category': 'Equipos de Frío',
        'levels': ['Básico', 'Intermedio', 'Avanzado', 'Especialista'],
        'equipment_types': ['Cámaras frigoríficas', 'Vitrinas', 'Congeladores']
    },
    'industrial_cooking': {
        'name': 'Cocina Industrial',
        'category': 'Equipos de Cocción',
        'levels': ['Básico', 'Intermedio', 'Avanzado', 'Especialista'],
        'equipment_types': ['Hornos', 'Freidoras', 'Planchas', 'Parrillas']
    }
}
```

### 2. Asignación Automática de Técnicos
```python
# Lógica de asignación basada en habilidades
def assign_technician_by_skills(self, fsm_order):
    required_skills = fsm_order.equipment_id.required_skills
    available_technicians = self.env['hr.employee'].search([
        ('is_technician', '=', True),
        ('skill_ids.skill_id', 'in', required_skills.ids),
        ('available', '=', True)
    ])
    
    # Ordenar por nivel de competencia y experiencia
    best_match = available_technicians.sorted(
        key=lambda t: t.get_skill_level(required_skills)
    )
    
    return best_match[0] if best_match else False
```

### 3. Evaluación de Competencias
```python
# Sistema de evaluación de habilidades
def evaluate_technician_skill(self, technician, skill, level):
    evaluation = self.env['hr.skill.evaluation'].create({
        'employee_id': technician.id,
        'skill_id': skill.id,
        'level': level,
        'evaluation_date': fields.Date.today(),
        'evaluator_id': self.env.user.id,
    })
    
    # Actualizar perfil del técnico
    technician.update_skill_profile(skill, level)
    
    return evaluation
```

## Casos de Uso Principales

### 1. Configuración de Habilidades por Equipo
```python
# Definir habilidades requeridas para un tipo de equipo
equipment_category = self.env['maintenance.equipment.category'].search([
    ('name', '=', 'Freidoras Industriales')
])

required_skills = [
    ('industrial_cooking', 'Intermedio'),
    ('electrical_systems', 'Básico'),
    ('safety_protocols', 'Avanzado')
]

equipment_category.required_skill_ids = [(6, 0, skill_ids)]
```

### 2. Asignación Automática en Órdenes FSM
```python
# Asignación basada en habilidades al crear orden de servicio
fsm_order = self.env['fsm.order'].create({
    'name': 'Mantenimiento Freidora Industrial',
    'equipment_id': equipment.id,
    'location_id': customer.id,
})

# El sistema asigna automáticamente el técnico más competente
best_technician = fsm_order.auto_assign_technician()
fsm_order.person_id = best_technician.id
```

### 3. Evaluación Post-Servicio
```python
# Evaluación de desempeño después del servicio
def complete_service_evaluation(self, fsm_order):
    technician = fsm_order.person_id
    skills_used = fsm_order.equipment_id.required_skills
    
    for skill in skills_used:
        # Incrementar experiencia
        technician.add_skill_experience(skill, fsm_order.duration)
        
        # Evaluación de calidad del servicio
        if fsm_order.customer_rating >= 4:
            technician.improve_skill_level(skill)
```

## Integración con Otros Módulos PATCO

### Con `patco_core`:
- **Naturalezas de Servicio**: Habilidades específicas por tipo de servicio
- **Líneas Analíticas**: Registro de tiempo por habilidad desarrollada
- **Clasificación**: Servicios categorizados por complejidad técnica

### Con `patco_customer_equipment`:
- **Equipos Especializados**: Habilidades requeridas por tipo de equipo
- **Historial de Servicios**: Seguimiento de técnicos por equipo
- **Especialización**: Desarrollo de expertise en equipos específicos

### Con `fieldservice` (OCA):
- **Asignación Inteligente**: Matching automático técnico-servicio
- **Optimización de Rutas**: Considerando habilidades y ubicación
- **Escalamiento**: Reasignación por falta de competencias

## Flujos de Trabajo

### 1. Onboarding de Técnicos
1. **Evaluación Inicial**: Identificación de habilidades actuales
2. **Perfil de Competencias**: Creación del perfil técnico
3. **Asignación de Nivel**: Clasificación por experiencia
4. **Plan de Desarrollo**: Identificación de áreas de mejora
5. **Certificación**: Registro de certificaciones técnicas

### 2. Asignación de Servicios
1. **Análisis de Requerimientos**: Identificación de habilidades necesarias
2. **Búsqueda de Técnicos**: Filtrado por competencias disponibles
3. **Evaluación de Candidatos**: Ranking por nivel y experiencia
4. **Asignación Óptima**: Selección del mejor candidato
5. **Confirmación**: Validación de disponibilidad y asignación

### 3. Desarrollo de Competencias
1. **Evaluación Continua**: Seguimiento de desempeño en servicios
2. **Identificación de Brechas**: Análisis de competencias faltantes
3. **Plan de Capacitación**: Diseño de programa de desarrollo
4. **Ejecución**: Implementación de capacitaciones
5. **Certificación**: Validación de nuevas competencias

## Métricas y KPIs

### Por Técnico:
- **Nivel de Competencias**: Promedio por área técnica
- **Especialización**: Áreas de mayor expertise
- **Desarrollo**: Progreso en habilidades a lo largo del tiempo
- **Utilización**: Porcentaje de servicios asignados vs. disponibilidad

### Por Habilidad:
- **Demanda**: Frecuencia de requerimiento en servicios
- **Disponibilidad**: Número de técnicos competentes
- **Brecha**: Diferencia entre demanda y disponibilidad
- **Desarrollo**: Técnicos en proceso de capacitación

### Operacionales:
- **Efectividad de Asignación**: Servicios completados exitosamente
- **Tiempo de Asignación**: Rapidez en encontrar técnico competente
- **Satisfacción del Cliente**: Rating por nivel de competencia del técnico
- **Desarrollo de Talento**: Progresión de técnicos en competencias

## Configuración y Personalización

### Configuración Inicial:
1. **Catálogo de Habilidades**: Definir competencias específicas HORECA
2. **Niveles de Competencia**: Establecer escalas de evaluación
3. **Matriz Equipo-Habilidad**: Vincular equipos con competencias requeridas
4. **Perfiles de Técnicos**: Evaluar y registrar habilidades actuales

### Personalización Avanzada:
- **Habilidades Específicas**: Competencias únicas del cliente
- **Criterios de Evaluación**: Métricas personalizadas de competencia
- **Algoritmos de Asignación**: Lógica específica de matching
- **Reportes Customizados**: Análisis según necesidades del negocio

## Beneficios del Módulo

### Operacionales:
1. **Asignación Optimizada**: Técnico correcto para cada servicio
2. **Reducción de Errores**: Competencias adecuadas para cada tarea
3. **Eficiencia**: Menor tiempo de resolución por mayor expertise
4. **Calidad**: Mejor resultado por especialización técnica

### Estratégicos:
1. **Desarrollo de Talento**: Crecimiento sistemático de competencias
2. **Planificación de RRHH**: Identificación de necesidades de contratación
3. **Ventaja Competitiva**: Equipo técnico altamente especializado
4. **Satisfacción del Cliente**: Servicio de mayor calidad técnica

## Casos de Uso según Documento Funcional

### Matriz de Competencias (Configuración Inicial):
- Definición de habilidades técnicas por área HORECA
- Evaluación inicial de técnicos existentes
- Creación de perfiles de competencia
- Establecimiento de planes de desarrollo

### Asignación de Técnicos (Macro-proceso 2):
- Matching automático basado en habilidades requeridas
- Consideración de nivel de experiencia necesario
- Optimización por disponibilidad y ubicación
- Escalamiento por falta de competencias

### Desarrollo Continuo (Macro-proceso 4):
- Evaluación post-servicio de desempeño
- Identificación de brechas de competencias
- Planificación de capacitaciones específicas
- Seguimiento de progreso en habilidades

## Estado Actual del Módulo

### Implementación:
- **Estructura Base**: Manifiesto y configuración inicial completados
- **Dependencias**: Integración con `hr` y `fieldservice_skill` definida
- **Desarrollo Pendiente**: Vistas y datos comentados en manifiesto
- **Funcionalidades**: En fase de desarrollo o configuración

### Próximos Pasos:
1. **Desarrollo de Modelos**: Implementación de extensiones específicas
2. **Creación de Vistas**: Interfaces para gestión de habilidades
3. **Datos Iniciales**: Catálogo base de habilidades HORECA
4. **Integración FSM**: Conexión completa con asignación de servicios

## Integración con fieldservice_skill (OCA)

### Funcionalidades Heredadas:
- **Modelo de Habilidades**: Base para competencias técnicas
- **Asignación por Skills**: Lógica de matching técnico-servicio
- **Niveles de Competencia**: Sistema de evaluación escalable
- **Reportes**: Análisis de habilidades y asignaciones

### Extensiones PATCO:
- **Habilidades HORECA**: Competencias específicas del sector
- **Evaluación Continua**: Sistema de mejora basado en servicios
- **Certificaciones**: Registro de certificaciones técnicas
- **Desarrollo de Carrera**: Planes de crecimiento profesional

## Mantenimiento y Soporte

### Tareas de Mantenimiento:
- **Actualización de Habilidades**: Incorporación de nuevas competencias
- **Evaluación de Técnicos**: Revisión periódica de niveles
- **Optimización de Asignaciones**: Ajuste de algoritmos de matching
- **Análisis de Brechas**: Identificación de necesidades de capacitación

### Monitoreo:
- **Efectividad de Asignaciones**: Seguimiento de éxito en servicios
- **Desarrollo de Competencias**: Progreso de técnicos en habilidades
- **Demanda vs. Oferta**: Balance entre necesidades y disponibilidad
- **Satisfacción**: Impacto de competencias en calidad de servicio

---

**PATCO HR Skills** - Gestión inteligente de competencias técnicas HORECA