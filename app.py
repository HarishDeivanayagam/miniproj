from flask import Flask, render_template, request, redirect, Response
from services.extract_amazon_leads import extract_from_amazon
from services.score_amazon_leads import score_from_amazon
from services.extract_linkedin_lead import extract_from_linkedin

linkedin_leads = []

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def generate_leads():
    form_data = request.form
    if form_data.get('source') == "linkedin":
        lead_info = extract_from_linkedin(form_data.get("task"),form_data.get("url"),form_data.get("context"), form_data.get("search"))
        if lead_info != None:
            linkedin_leads.append(lead_info)
            return render_template("linkedin.html", leads=linkedin_leads)
        else:
            return render_template("scorelinkedin.html", data=False)
    elif form_data.get('source') == "amazon":
        leads = extract_from_amazon(form_data.get('url'))
        return Response(leads, mimetype="text/json", headers={"Content-Disposition":"attachment;filename=" + form_data.get('task')  + ".json"})
    else:
        return "SITE NOT FOUND"

@app.route("/amazon", methods=["GET"])
def score_amazon():
    return render_template('scoring.html')

@app.route("/amazon",methods=["POST"])
def post_score():
    results = score_from_amazon(request.form['json'])
    return results

@app.route("/linkedin")
def get_all_linkedin():
    return render_template("linkedin.html", leads=linkedin_leads)

if __name__ == "__main__":
    app.run(debug=True)
