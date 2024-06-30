from odoo import fields, models


class EmployeeDepartmentInherit(models.Model):
    _inherit = 'hr.department'

    department_groups = fields.Many2many("res.groups")