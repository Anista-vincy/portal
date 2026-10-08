from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from html import escape

HOST = "127.0.0.1"
PORT = 5000

queue = []
next_id = 1
total_added = 0
total_treated = 0

labels = {1: "Critical", 2: "Serious", 3: "Moderate", 4: "Stable"}
classes = {1: "critical", 2: "serious", 3: "moderate", 4: "stable"}

def sort_queue():
    queue.sort(key=lambda p: (p["priority"], p["id"]))

def add_patient(name, age, priority, condition):
    global next_id, total_added
    queue.append({
        "id": next_id,
        "name": name,
        "age": age,
        "priority": int(priority),
        "condition": condition
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
    demo = [
        ("Arun", 52, 3, "Fever"),
        ("Meena", 64, 1, "Chest pain"),
        ("Rahul", 28, 4, "Minor injury"),
        ("Priya", 45, 2, "Breathing difficulty"),
        ("Kumar", 70, 1, "Severe bleeding")
    ]
    for patient in demo:
        add_patient(*patient)

def page(message="", operation="Waiting for an operation..."):
    sort_queue()
    queue_html = ""

    for i, p in enumerate(queue):
        next_class = " next-card" if i == 0 else ""
        queue_html += f"""
        <div class="patient{next_class}">
            <div class="number">#{i + 1}</div>
            <div>
                <div class="pname">{escape(str(p["name"]))}</div>
                <div class="detail">Age {escape(str(p["age"]))} • {escape(str(p["condition"]))}</div>
            </div>
            <div class="priority {classes[p["priority"]]}">
                P{p["priority"]}<br>{labels[p["priority"]]}
            </div>
        </div>
        """

    if queue:
        empty_style = "display:none;"
        p = queue[0]
        next_html = f"""
        <strong>{escape(str(p["name"]))}</strong>
        <small>Age {escape(str(p["age"]))} • {escape(str(p["condition"]))} • Priority {labels[p["priority"]]}</small>
        """
    else:
        empty_style = ""
        next_html = "No patient waiting"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hospital Emergency Queue Visualizer</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="app">
<header>
  <div>
    <h1>Hospital Emergency Queue</h1>
    <p>Visualize how a Priority Queue manages emergency patients</p>
  </div>
  <span class="badge">Data Structures Project</span>
</header>

<main>
<section class="panel form-panel">
  <h2>Add Patient</h2>
  <form method="POST" action="/add">
    <div class="form-grid">
      <div><label>Patient Name</label>
        <input name="name" placeholder="Enter name" required></div>
      <div><label>Age</label>
        <input name="age" type="number" min="0" max="120" placeholder="Age" required></div>
      <div><label>Emergency Level</label>
        <select name="priority">
          <option value="1">1 - Critical</option>
          <option value="2">2 - Serious</option>
          <option value="3" selected>3 - Moderate</option>
          <option value="4">4 - Stable</option>
        </select>
      </div>
      <div><label>Condition</label>
        <input name="condition" placeholder="e.g. Chest pain" required></div>
    </div>
    <div class="actions">
      <button class="primary" type="submit">+ Add Patient</button>
    </div>
  </form>

  <div class="actions">
    <form method="POST" action="/demo">
      <button type="submit">Load Demo Patients</button>
    </form>
    <form method="POST" action="/clear">
      <button class="secondary" type="submit">Clear All</button>
    </form>
  </div>
  <p class="message">{escape(message)}</p>
</section>

<section class="layout">
  <section class="panel queue-panel">
    <div class="title-row">
      <div><h2>Priority Queue</h2>
      <p>Patients are automatically arranged by emergency level.</p></div>
      <div class="queue-info"><b>{len(queue)}</b> patients</div>
    </div>

    <div class="priority-guide">
      <span><b>1</b> Critical</span>
      <span><b>2</b> Serious</span>
      <span><b>3</b> Moderate</span>
      <span><b>4</b> Stable</span>
    </div>

    <div class="queue">{queue_html}</div>
    <div class="empty" style="{empty_style}">No patients in the queue.</div>
  </section>

  <aside>
    <section class="panel">
      <h2>Next Patient</h2>
      <div class="next">{next_html}</div>
      <form method="POST" action="/treat">
        <button class="primary full" type="submit">Treat Next Patient</button>
      </form>
    </section>

    <section class="panel">
      <h2>Queue Operations</h2>
      <div class="operation">{escape(operation)}</div>
      <div class="ops">
        <div><strong>Insert</strong><small>Patient enters queue</small></div>
        <div><strong>Priority</strong><small>Critical patients move ahead</small></div>
        <div><strong>Delete</strong><small>Treat removes highest priority</small></div>
      </div>
    </section>

    <section class="panel stats">
      <h2>Statistics</h2>
      <div>
        <p>Total Added <b>{total_added}</b></p>
        <p>Treated <b>{total_treated}</b></p>
        <p>Waiting <b>{len(queue)}</b></p>
      </div>
    </section>
  </aside>
</section>
</main>
<footer>Hospital Emergency Queue Visualizer - Priority Queue - Python</footer>
</div>
</body>
</html>"""

CSS = """
*{box-sizing:border-box}
body{margin:0;background:linear-gradient(135deg,#eef2ff,#fff7ef);font-family:Arial,Helvetica,sans-serif;color:#172033}
.app{max-width:1250px;margin:auto;padding:22px}
header{background:#6579be;color:#fff;border-radius:18px;padding:24px 28px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 12px 28px #6579be33}
header h1{margin:0 0 6px;font-size:29px} header p{margin:0;opacity:.9}.badge{background:#0e1733;padding:10px 15px;border-radius:30px;font-weight:bold;font-size:13px}
main{margin-top:18px}.panel{background:#fff;border:1px solid #dce1ec;border-radius:16px;padding:19px;box-shadow:0 8px 22px #18234a12}
h2{margin:0 0 6px;font-size:19px}.form-panel>h2{margin-bottom:15px}.form-grid{display:grid;grid-template-columns:1.1fr .6fr 1fr 1.4fr;gap:12px}
label{display:block;color:#697386;font-size:12px;font-weight:bold;margin-bottom:6px}
input,select{width:100%;height:42px;border:1px solid #ccd3e1;border-radius:9px;padding:0 12px;font-size:14px;background:#fff}
.actions{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap}form{margin:0}
button{height:42px;border:1px solid #ccd3e1;border-radius:9px;padding:0 15px;background:#fff;color:#0e1733;font-weight:bold;cursor:pointer}
.primary{background:#0e1733;color:#fff;border-color:#0e1733}.secondary{background:#f5f6fa}
.message{min-height:16px;margin:8px 0 0;color:#d46d00;font-size:12px}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 350px;gap:18px;margin-top:18px}.layout aside{display:flex;flex-direction:column;gap:18px}
.title-row{display:flex;justify-content:space-between;align-items:flex-start}.title-row p{margin:0;color:#697386;font-size:13px}.queue-info{background:#eef2ff;padding:8px 11px;border-radius:9px;font-size:12px}.queue-info b{font-size:18px}
.priority-guide{display:flex;gap:8px;flex-wrap:wrap;margin:15px 0}.priority-guide span{background:#f6f7fa;border:1px solid #e2e5ed;border-radius:8px;padding:7px 9px;font-size:11px}.priority-guide b{background:#0e1733;color:#fff;border-radius:50%;padding:3px 6px;margin-right:3px}
.queue{display:flex;flex-direction:column;gap:9px}.patient{display:grid;grid-template-columns:52px 1fr auto;gap:12px;align-items:center;padding:13px;border:1px solid #e0e4ed;border-radius:11px;background:#fbfcff}.patient.next-card{border:2px solid #f98603;background:#fffaf3}
.number{width:42px;height:42px;border-radius:10px;background:#eef2ff;display:grid;place-items:center;font-weight:bold;color:#6579be}.pname{font-weight:bold}.detail{font-size:12px;color:#697386;margin-top:4px}.priority{padding:7px 9px;border-radius:8px;font-size:11px;font-weight:bold;background:#f0f1f5;text-align:center}.critical{background:#ffe1d7}.serious{background:#ffeecf}.moderate{background:#eef2ff}.stable{background:#e7f5ec}
.empty{text-align:center;color:#8a93a5;padding:45px 10px;border:1px dashed #d6dce8;border-radius:11px}
.next{min-height:82px;background:#f7f8fc;border-radius:10px;padding:13px;margin:12px 0}.next strong{font-size:16px}.next small{display:block;color:#697386;margin-top:6px}.full{width:100%}
.operation{background:#f3f5fa;border-radius:10px;padding:12px;font-family:monospace;font-size:12px;min-height:48px;display:flex;align-items:center}.ops{margin-top:12px;display:grid;gap:8px}.ops div{display:flex;justify-content:space-between;border-bottom:1px solid #edf0f5;padding-bottom:8px}.ops small{color:#697386}.stats p{display:flex;justify-content:space-between;border-bottom:1px solid #edf0f5;padding-bottom:8px;font-size:13px}.stats p:last-child{border:0}.stats b{font-family:monospace}
footer{text-align:center;color:#7d8799;font-size:12px;padding:18px}
@media(max-width:850px){.form-grid{grid-template-columns:1fr 1fr}.layout{grid-template-columns:1fr}}
@media(max-width:550px){.app{padding:10px}header{padding:18px}header h1{font-size:22px}.badge{display:none}.form-grid{grid-template-columns:1fr}.patient{grid-template-columns:45px 1fr}.priority{grid-column:2}}
"""

class Handler(BaseHTTPRequestHandler):
    def send_html(self, content, status=200):
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/style.css":
            data = CSS.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif self.path == "/" or self.path.startswith("/?"):
            self.send_html(page())
        else:
            self.send_html(page("Page not found."), 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)

        if self.path == "/add":
            name = data.get("name", [""])[0].strip()
            age = data.get("age", [""])[0].strip()
            priority = data.get("priority", ["3"])[0]
            condition = data.get("condition", [""])[0].strip()

            if not name or not age or not condition:
                self.send_html(page("Please enter name, age and condition."))
                return

            try:
                age_num = int(age)
                priority_num = int(priority)
            except ValueError:
                self.send_html(page("Please enter valid values."))
                return

            if age_num < 0 or age_num > 120:
                self.send_html(page("Enter a valid age."))
                return

            add_patient(name, age_num, priority_num, condition)
            self.send_html(page(
                f"Patient {name} added successfully.",
                f"INSERT -> {name} (Priority {priority_num}) -> Queue reordered"
            ))

        elif self.path == "/treat":
            patient = treat_patient()
            if patient:
                self.send_html(page(
                    operation=f"DELETE -> {patient['name']} treated and removed from front of Priority Queue"
                ))
            else:
                self.send_html(page(operation="DELETE -> Queue is empty"))

        elif self.path == "/clear":
            queue.clear()
            self.send_html(page(operation="CLEAR -> Queue emptied"))

        elif self.path == "/demo":
            load_demo()
            self.send_html(page(
                "Demo patients loaded.",
                "INSERT -> Demo patients added and queue reordered"
            ))
        else:
            self.send_html(page("Page not found."), 404)

if __name__ == "__main__":
    print("=" * 60)
    print("Hospital Emergency Queue Visualizer - Python")
    print("No JavaScript / No Flask / No extra packages")
    print(f"Open http://{HOST}:{PORT} in your browser")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)
    HTTPServer((HOST, PORT), Handler).serve_forever()