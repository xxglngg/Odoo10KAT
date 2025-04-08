{
    'name': 'Booking Order Gilang 26022002',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage booking order, work order, and service team',
    'description': """
        Module for managing booking order, work order, and service team.
    """,
    'author': 'Gilang',
    'depends': ['sale', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sale_order_view.xml',
        'views/booking_order_view.xml',
        'views/work_order_view.xml',
        'views/service_team_view.xml',
        'reports/report_action.xml',
        'reports/template_report_work_order.xml',
        'wizard/wizard_cancel_work_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
