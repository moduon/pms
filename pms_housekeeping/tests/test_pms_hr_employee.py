from odoo.exceptions import ValidationError
from .common import TestPms


class TestPmsHrEmployee(TestPms):
    def setUp(self):
        super().setUp()

    def test_employee_pre_assigned_room_inconsistent(self):
        # ARRANGE

        self.pms_property2 = self.env["pms.property"].create(
            {
                "name": "Property 2",
                "company_id": self.company1.id,
                "default_pricelist_id": self.pricelist1.id,
            }
        )
        self.room2 = self.env["pms.room"].create(
            {
                "name": "Room 202",
                "pms_property_id": self.pms_property2.id,
                "room_type_id": self.room_type1.id,
            }
        )

        # ACT & ASSERT
        with self.assertRaises(
            ValidationError, msg="The room should belong to the employee's property."
        ):
            self.hr_employee = self.env["hr.employee"].create(
                {
                    "name": "Test Employee",
                    "company_id": self.company1.id,
                    "job_id": self.env.ref("pms_housekeeping.housekeeping_job_id").id,
                    "property_ids": [(6, 0, [self.pms_property1.id])],
                    "pre_assigned_room_ids": [(6, 0, [self.room2.id])],
                }
            )

    def test_employee_pre_assigned_room_consistent_with_property(self):
        # ARRANGE
        self.hr_employee = self.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "company_id": self.company1.id,
                "job_id": self.env.ref("pms_housekeeping.housekeeping_job_id").id,
                "property_ids": [(6, 0, [self.pms_property1.id])],
            }
        )

        # ACT
        self.hr_employee.pre_assigned_room_ids = [(6, 0, [self.room1.id])]

        # ASSERT
        self.assertTrue(
            self.hr_employee.pre_assigned_room_ids, "Pre assigned room is not consistent with property"
        )

    def test_employee_pre_assigned_room_consistent_without_properties(self):
        # ARRANGE
        self.hr_employee = self.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "company_id": self.company1.id,
                "job_id": self.env.ref("pms_housekeeping.housekeeping_job_id").id,
            }
        )

        # ACT
        self.hr_employee.pre_assigned_room_ids = [(6, 0, [self.room1.id])]

        # ASSERT
        self.assertTrue(
            self.hr_employee.pre_assigned_room_ids, "Pre assigned room is not consistent without properties"
        )

    def test_not_pre_assigned_room_no_housekeeper_employee(self):
        # ARRANGE
        self.hr_employee = self.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "company_id": self.company1.id,
                "job_id": self.env.ref("hr.job_trainee").id,
            }
        )

        # ACT & ASSERT
        with self.assertRaises(
            ValidationError, msg="The job position should be Housekeeper."
        ):
            self.hr_employee.pre_assigned_room_ids = [(6, 0, [self.room1.id])]