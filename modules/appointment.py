#Appointment

class Appointment:
    def __init__(self, appointment_id, pet_id, date):
        self.appointment_id = appointment_id
        self.pet_id = pet_id
        self.date = date
        self.status = "Scheduled"

    def update_status(self, new_status):
        valid_statuses = ["Scheduled", "Completed", "Cancelled"]
        if new_status in valid_statuses:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status: {new_status}. Valid statuses are: {valid_statuses}")


