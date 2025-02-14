# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PmsSesCommunication(models.Model):
    _name = "pms.ses.communication"
    _description = "SES Communication"
    _order = "create_date desc"

    reservation_id = fields.Many2one(
        string="Reservation",
        help="Reservation related to this communication",
        index=True,
        required=True,
        comodel_name="pms.reservation",
    )
    pms_property_id = fields.Many2one(
        comodel_name="pms.property",
        string="Property",
        help="Property related to this communication",
        related="reservation_id.pms_property_id",
        index=True,
        store=True,
    )
    room_id = fields.Many2one(
        comodel_name="pms.room",
        string="Room",
        help="Room related to this communication",
        related="reservation_id.preferred_room_id",
        index=True,
        store=True,
    )
    batch_id = fields.Char(
        string="Batch ID",
        default=False,
    )
    communication_id = fields.Char(
        string="Communication ID",
        help="ID of the communication",
        default=False,
    )
    operation = fields.Selection(
        string="Operation",
        help="Operation of the communication",
        selection=[("A", "New communication"), ("B", "Delete communication")],
        required=True,
    )
    entity = fields.Selection(
        string="Entity",
        help="Entity of the communication",
        selection=[("RH", "Reservation"), ("PV", "Traveller report")],
        required=True,
    )
    communication_time = fields.Datetime(
        string="Communication time",
        help="Date and time of the communication",
    )
    query_status_time = fields.Datetime(
        string="Query status time",
        help="Date and time of the last state query",
    )
    state = fields.Selection(
        string="State",
        help="State of the communication",
        default="to_send",
        required=True,
        selection=[
            ("incomplete", "Incomplete checkin data"),
            ("to_send", "Pending Notification"),
            ("to_process", "Pending Processing"),
            ("error_sending", "Error Sending"),
            ("error_processing", "Error Processing"),
            ("processed", "Processed"),
        ],
    )
    sending_result = fields.Text(
        string="Sending Result",
        help="Notification sending result",
    )
    processing_result = fields.Text(
        string="Processing Result",
        help="Notification processing result",
    )
    communication_xml = fields.Text(
        string="XML Com.",
        help="XML content communication",
    )
    communication_soap = fields.Text(
        string="SOAP Com.",
        help="SOAP content communication",
    )
    response_communication_soap = fields.Text(
        string="SOAP Resp. Com.",
        help="SOAP response communication",
    )

    query_status_xml = fields.Text(
        string="XML Query Status",
        help="XML query status content communication",
    )
    query_status_soap = fields.Text(
        string="SOAP Query Status",
        help="SOAP query status content communication",
    )
    response_query_status_soap = fields.Text(
        string="SOAP Resp. Status",
        help="SOAP response status query",
    )

    def force_send_communication(self):
        for record in self:
            self.env["traveller.report.wizard"].ses_send_communications(
                entity=record.entity,
                pms_ses_communication_id=record.id,
            )
