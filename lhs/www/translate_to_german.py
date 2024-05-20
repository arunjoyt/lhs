import frappe
import random
from datetime import datetime

def get_context(context):
    context.user = frappe.session.user
    questions_per_page = frappe.get_doc("LHS Settings").questions_per_page
    master_records = frappe.get_all("LHS Translation Master")
    translations = []
    for record in master_records:
        master_doc = frappe.get_doc("LHS Translation Master", record.name)
        translations.extend(master_doc.translations)
    # select a random sample of translations
    if len(translations) > questions_per_page: 
        context.translations = random.sample(translations, questions_per_page)
    else:
        context.translations = translations
    # if caching is enabled, random sampling will not always work
    
    # get score of logged in user from LHSScore
    if (context.user != 'Guest'):
        scores = frappe.get_list(
            "LHSScore",
            filters={"user_name": context.user},
            fields=['submit_date',"correct_count","total_count"]
            )
        context.scores = scores

    context.no_cache = 1
    return context

@frappe.whitelist()
def save_score(user, correct_answer_count, total_question_count):
    doc = frappe.new_doc("LHSScore")
    doc.user_name  = user
    doc.correct_count = correct_answer_count
    doc.total_count = total_question_count
    doc.submit_date = datetime.now()
    doc.insert(ignore_permissions=True)
    return "Score saved successfully"
