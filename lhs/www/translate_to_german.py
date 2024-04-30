import frappe

def get_context(context):
    master_records = frappe.get_all("LHS Translation Master")
    context.translations = []
    for record in master_records:
        master_doc = frappe.get_doc("LHS Translation Master", record.name)
        context.translations.extend(master_doc.translations)
    return context
