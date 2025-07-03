# Copyright (c) 2025, faizan and contributors
# For license information, please see license.txt
# airplane_ticket.py

import frappe
from frappe.model.document import Document

class AirplaneTicket(Document):
	def validate(self):
		self.remove_duplicate_add_ons()
		self.calculate_total_amount()

	def remove_duplicate_add_ons(self):
		seen = set()
		unique_add_ons = []
		for row in self.add_ons:
			if row.item not in seen:
				seen.add(row.item)
				unique_add_ons.append(row)
		self.set("add_ons", unique_add_ons)

	def calculate_total_amount(self):
		total_addon_amount = sum(addon.item_amount for addon in self.add_ons)
		self.total_amount = (self.flight_price or 0) + total_addon_amount

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("Only tickets with status 'Boarded' can be submitted.")
