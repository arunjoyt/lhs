import frappe
import random

def get_context(context):
    context.user = frappe.session.user
    master_records = frappe.get_all("LHS Translation Master")
    translations = []
    for record in master_records:
        master_doc = frappe.get_doc("LHS Translation Master", record.name)
        translations.extend(master_doc.translations)
    # select a random sample of 10 translations
    if len(translations) > 10: 
        context.translations = random.sample(translations, 10)
    else:
        context.translations = translations
    # if caching is enabled, random sampling will not always work
    context.no_cache = 1
    return context

@frappe.whitelist()
def save_score(user, correct_answer_count, total_question_count):
    doc = frappe.new_doc("LHSUserScore")
    doc.user  = frappe.get_doc("User", user)
    print(doc.user)
    doc.correct_count = correct_answer_count
    doc.total_count = total_question_count
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return "Score saved successfully"
