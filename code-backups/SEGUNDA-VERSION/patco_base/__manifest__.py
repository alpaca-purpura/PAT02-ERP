# -*- coding: utf-8 -*-
{
    'name': 'PATCO Base',
    'version': '18.0.1.0.0',
    'category': 'Services/Field Service',
    'summary': 'PATCO Base Module - Core functionalities and base models',
    'description': """
        PATCO Base Module
        =================
        
        This module provides the base functionalities for the PATCO system:
        
        * Service Area classification
        * Service Complexity levels
        * Service Nature types
        * Service Order Classification (Helpdesk & FSM)
        * Maintenance Equipment Category extensions
        * Security groups and permissions
        * Product categories for maintenance services
        * Master configurations and base models
        
        This is the foundation module that other PATCO modules depend on.
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.pe',
    'license': 'LGPL-3',
    'depends': [
        # Odoo Core
        'base',
        'product',
        'mail',
        'contacts',
        'stock',
        'sale',
        'purchase',
        'account',
        'hr',
        'project',
        'maintenance',
        
        # OCA Dependencies
        'fieldservice',
        'fieldservice_stock',
        'hr_timesheet',
        'partner_firstname',
        'base_location',
        'base_location_geonames_import',
        'web_widget_x2many_2d_matrix',

        #MODULOS OCA
        'agreement',
        'agreement_sale',
        # partner-contact This modules allows you to click on a button and open the full Contact form from a Company form.	
        'partner_contact_access_link',
        'maintenance',
        # reporting-engine This module provides a basic report class to generate xlsx report.	
        'report_xlsx',
        # web This module adds responsiveness to web backend.	
        'web_responsive',
        'web_favicon',
        'web_company_color',
        'web_quick_start_screen',
        'web_dialog_size',
        # web This module allows you to refresh the list of records in any view.
        'web_refresher',
        # web This module allows you to use the AND condition on the search bar. Example: Search for “John.” Do another search with “Smith” and click on the “Shift” key on your keyboard. The condition applied will be “John” AND “Smith.”
        'web_search_with_and',
        # web This module enables selecting a range of records using the shift key.
        # 'web_listview_range_select',  # Comentado temporalmente - módulo no disponible
        # mail This module modifies the feature of emails to remove the Odoo branding, specifically the "Powered by Odoo"
        'mail_debrand',
        # server-brand This module removes links to Odoo in emails
        'disable_odoo_online',
        #  server-tool This module allows you to do a more flexible search and allows you to add specific fields to the name search. Example: You have a partner named “John Mr. Brown”, and if you type “John Brown”, it will find it. Or you have custom product field, if you search by the custom code in the product name, it will find it.
        'base_name_search_improved',
    ],
    'data': [
        'security/patco_security_groups.xml',
        'security/patco_record_rules.xml',
        'security/ir.model.access.csv',

        # Data
        'data/patco_general_data.xml',
        'data/patco_service_area_data.xml',
        'data/patco_service_complexity_data.xml',
        'data/patco_service_nature_data.xml',
        
        # Views
        'views/patco_menus.xml',
        'views/patco_service_area_views.xml',
        'views/patco_service_complexity_views.xml',
        'views/patco_service_nature_views.xml',
        # 'views/patco_base_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'external_dependencies': {
        'python': [],
    },
}