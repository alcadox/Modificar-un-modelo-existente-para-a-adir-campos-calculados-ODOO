from odoo import models, fields

class EmailUser(models.Model):
    _name = "email.user"
    _description = "Usuario de correo electrónico"

    name = fields.Char(string="Nombre completo", required=True)
    email = fields.Char(string="Dirección de correo", required=True)
    password = fields.Char(string="Contraseña", required=True)
    quota = fields.Integer(string="Cuota (MB)", default=1024)
    active = fields.Boolean(string="Activo", default=True)

    domain = fields.Char(string="Dominio", default="midominio.com")
    forwarding = fields.Char(string="Reenvío a")
    notes = fields.Text(string="Notas")
