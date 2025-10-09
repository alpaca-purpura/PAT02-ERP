# Copyright 2025 PAT02-ERP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Field Service Sale Timesheet Bridge",
    "version": "18.0.1.0.0",
    "category": "Field Service",
    "summary": "Bridge module to connect Field Service with Sale Timesheet",
    "author": "PAT02-ERP",
    "website": "https://github.com/PAT02-ERP",
    "license": "AGPL-3",
    "depends": [
        "fieldservice_sale",
        "hr_timesheet",
        "patco_core",
    ],
    "data": [
        "views/timesheets_analysis_views.xml",
    ],
    "installable": True,
    "auto_install": True,
    "application": False,
}