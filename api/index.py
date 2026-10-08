from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape

queue = []
next_id = 1
total_added = 0
total_treated = 0

labels = {1: "Critical", 2: "Serious", 3: "Moderate", 4: "Stable"}
classes = {1: "critical", 2: "serious", 3: "moderate", 4: "stable"}

CSS = """
body{margin:0;font-family:Arial,sans-serif;background:lightblue;color:black}
.container{width:92%;max-width:1100px;margin:25px auto}
.header{background:darkblue;color:white;padding:22px;border-radius:10px}
.header h1{margin:0 0 8px}
.card{background:white;padding:18px;margin-top:15px;border-radius:10px}
h2{color:darkblue}
input,select{padding:10px;margin:5px;border:1px solid gray;border-radius:5px}
button{padding:10px 16px;margin:5px;border:0;border-radius:5px;background:darkblue;color:white;cursor:pointer}
button.orange{background:orange} button.gray{background:gray}
table{width:100%;border-collapse:collapse}
th{background:darkblue;color:white}
th,td{padding:10px;border:1px solid lightgray;text-align:left}
.critical{color:red;font-weight:bold}.serious{color:orange;font-weight:bold}
.moderate{color:darkblue;font-weight:bold}.stable{color:green;font-weight:bold}
.stats{display:flex;gap:15px;flex-wrap:wrap}
.stat{background:lightgray;padding:15px 25px;border-radius:8px}
"""

def sort_queue():
    queue.sort(key=lambda p: (p["priority"], p["id"]))

def add_patient(name, age, priority, condition):
    global next_id, total_added
    queue.append({
        "id": next_id, "name": name, "age": age,
        "priority": int(priority), "condition": condition
    })
    next_id += 1
    total_added += 1
    sort_queue()

def treat_patient():
    global total_treated
    if queue:
        patient = queue.pop(0)
        total_treated += 1
        return patient
    return None

def load_demo():
    global queue
    queue.clear()
    for patient in [
        ("Arun",52,3,"Fever"),
        ("Meena",64,1,"Chest pain"),
        ("Rahul",28,4,"Minor injury"),
        ("Priya",45,2,"Breathing difficulty"),
        ("Kumar",70,1,"Severe bleeding")
    ]:
        add_patient(*patient)

load_demo()

def page(message=""):
    sort_queue()
    rows = ""
    for i,p in enumerate(queue,1):
        rows += f"""
        <tr>
          <td>{i}</td>
          <td>{escape(str(p["name"]))}</td>
          <td>{p["age"]}</td>
          <td>P{p["priority"]}</td>
          <td class="{classes[p["priority"]]}">{labels[p["priority"]]}</td>
          <td>{escape(str(p["condition"]))}</td>
        </tr>"""

    if queue:
        p = queue[0]
        next_html = f"""
        <p><b>Name:</b> {escape(str(p["name"]))}</p>
        <p><b>Age:</b> {p["age"]}</p>
        <p><b>Condition:</b> {escape(str(p["condition"]))}</p>
        <p><b>Priority:</b> P{p["priority"]} - {labels[p["priority"]]}</p>
        """
    else:
        next_html = "<p>No patient waiting.</p>"

    notice = f'<div class="card"><b>{escape(message)}</b></div>' if message else ""

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hospital Emergency Queue</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>Hospital Emergency Queue</h1>
<div>Priority Queue — Critical patients are treated first</div>
</div>
{notice}
<div class="card">
<h2>Add Patient</h2>
<form method="POST" action="/add">
<input name="name" placeholder="Patient Name" required>
<input name="age" type="number" min="0" max="120" placeholder="Age" required>
<select name="priority">
<option value="1">1 - Critical</option>
<option value="2">2 - Serious</option>
<option value="3" selected>3 - Moderate</option>
<option value="4">4 - Stable</option>
</select>
<input name="condition" placeholder="Condition" required>
<button type="submit">Add Patient</button>
</form>
<form method="POST" action="/demo" style="display:inline">
<button class="orange" type="submit">Load Demo Patients</button>
</form>
<form method="POST" action="/clear" style="display:inline">
<button class="gray" type="submit">Clear All</button>
</form>
</div>

<div class="card">
<h2>Priority Queue</h2>
<table>
<tr><th>Position</th><th>Patient</th><th>Age</th><th>Priority</th><th>Emergency Level</th><th>Condition</th></tr>
{rows if rows else '<tr><td colspan="6">No patients in queue.</td></tr>'}
</table>
</div>

<div class="card">
<h2>Next Patient</h2>
{next_html}
<form method="POST" action="/treat">
<button type="submit">Treat Next Patient</button>
</form>
</div>

<div class="card">
<h2>Statistics</h2>
<div class="stats">
<div class="stat"><b>Total Added</b><br>{total_added}</div>
<div class="stat"><b>Treated</b><br>{total_treated}</div>
<div class="stat"><b>Waiting</b><br>{len(queue)}</div>
</div>
</div>

<div class="card">
<b>Data Structure:</b> Priority Queue
&nbsp; | &nbsp; <b>Algorithm:</b> Priority Ordering
&nbsp; | &nbsp; <b>JavaScript:</b> None
</div>
</div>
</body>
</html>"""

class handler(BaseHTTPRequestHandler):
    def _send(self, body, content_type="text/html; charset=utf-8", status=200):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(page())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode("utf-8"))

        if self.path == "/add":
            name = form.get("name", [""])[0].strip()
            condition = form.get("condition", [""])[0].strip()
            try:
                age = int(form.get("age", ["0"])[0])
                priority = int(form.get("priority", ["3"])[0])
                if not name or not condition or not 0 <= age <= 120:
                    raise ValueError
                add_patient(name, age, priority, condition)
                self._send(page("INSERT: Patient added successfully."))
            except ValueError:
                self._send(page("Invalid patient details."), status=400)

        elif self.path == "/treat":
            patient = treat_patient()
            msg = f"DELETE: {patient['name']} has been treated." if patient else "Queue is empty."
            self._send(page(msg))

        elif self.path == "/clear":
            queue.clear()
            self._send(page("Queue cleared successfully."))

        elif self.path == "/demo":
            load_demo()
            self._send(page("Demo patients loaded successfully."))

        else:
            self._send(page())

    def log_message(self, format, *args):
        return
