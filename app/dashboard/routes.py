from app.dashboard import dashboard_bp
from flask import render_template, request, jsonify


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.html")
    elif request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data received"}), 400

            # Process the data and redirect to the Dash app
            return jsonify(
                {
                    "success": True,
                    "redirect_url": "/dashboard/viz/",  # Redirect to Dash app URL
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
