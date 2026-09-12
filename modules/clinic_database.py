class ClinicDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClinicDatabase, cls).__new__(cls)
            cls._instance.appointments = {}
        return cls._instance

    def schedule_appointment(self, appointment):
        self.appointment[appointment.appointment_id] = appointment
        print(f"Appointment {appointment.appointment_id} scheduled for pet {appointment.pet_id} on {appointment.date}.")

    def view_appointment(self):
        return [
            f"ID: {appointment.appointment_id}, Pet ID: {appointment.pet_id}, Date: {appointment.date}, Status: {appointment.status}"
            for appointment in self.appointments.values()
        ]

    def cancel_appointment(self, appointment_id):
        if appointment_id in self.appointments:
            self.appointment[appointment_id].update_status("Cancelled")
            print(f"Appointment {appointment_id} has been cancelled.")

        else:
            print(f"Appointment {appointment_id} not found.")