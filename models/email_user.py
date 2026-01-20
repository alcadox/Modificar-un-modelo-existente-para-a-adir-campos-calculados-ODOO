from odoo import models, fields, api

class EmailUser(models.Model):
    _name = "email.user"
    _description = "Usuario de correo electrónico"

    name = fields.Char(string="Nombre completo", required=True)

    # añadido compos necesarios como primer apellido, segundo apellido
    surname = fields.Char(string="Apellido", required=True)
    surname2 = fields.Char(string="Segundo apellido")

    # añadido campo  fecha de nacimiento y edad
    fecha_nacimiento = fields.Date("Fecha de nacimiento")
    edad = fields.Integer(string="Edad", compute="_calcula_edad", store=True, readonly=True)

    # añadido campo  mayor de edad
    mayor_edad = fields.Boolean(string="Mayor de edad", compute="_calcula_mayor_edad", store=True, readonly=True)

    email = fields.Char(string="Dirección de correo", required=True)
    # añadido campo  correo corporativo
    correo_corporativo = fields.Char(string="Correo corporativo", default=False, compute="_calcula_correo_corporativo", store=True, readonly=True)

    password = fields.Char(string="Contraseña", required=True)
    quota = fields.Integer(string="Cuota (MB)", default=1024)
    active = fields.Boolean(string="Activo", default=True)

    domain = fields.Char(string="Dominio", default="midominio.com")
    forwarding = fields.Char(string="Reenvío a")
    notes = fields.Text(string="Notas")

    # método para calcular la edad
    @api.depends("fecha_nacimiento")
    def _calcula_edad(self):
        # puede que nos llegue mas de un registro por eso esta definido el bucle for
        for registro in self:
            # si existe fecha_nacimiento le calculo la edad
            if registro.fecha_nacimiento:
                from datetime import date # importamos date

                # calculamos la edad
                hoy = date.today()
                fecha_cumpleanos = registro.fecha_nacimiento
                # como calcula la edad: restamos años y ajustamos si no ha cumplido este año
                anos = hoy.year - fecha_cumpleanos.year - ((hoy.month, hoy.day) < (fecha_cumpleanos.month, fecha_cumpleanos.day))
                registro.edad = anos

            else:
                registro.edad = 0

    # método para calcular si es mayor de edad
    @api.depends("edad")
    def _calcula_mayor_edad(self):
        # puede que nos llegue mas de un registro por eso esta definido el bucle for
        for registro in self:
            # si la edad es mayor o igual a 18
            if registro.edad >= 18:
                registro.mayor_edad = True
            else:
                registro.mayor_edad = False

    # método para calcular el correo corporativo InicalNombre+Apellido1+Apellido2@empresa.es
    @api.depends("name", "surname", "surname2", "domain")
    def _calcula_correo_corporativo(self):
        # puede que nos llegue mas de un registro por eso esta definido el bucle for
        for registro in self:
            # construimos el correo corporativo
            nombre_partes = registro.name.split(" ")
            if len(nombre_partes) > 0:
                primer_nombre = nombre_partes[0]
            else:
                primer_nombre = ""

            correo = primer_nombre.lower() + "." + registro.surname.lower()
            if registro.surname2:
                correo += "." + registro.surname2.lower()
            correo += "@" + registro.domain.lower()

            registro.correo_corporativo = correo