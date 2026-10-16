"""CloudOps 360 ticket manager (learning project)."""
import os
from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select


db = SQLAlchemy()


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=False, default="")
    priority = db.Column(db.String(10), nullable=False, default="medium")
    status = db.Column(db.String(15), nullable=False, default="open")

    def as_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description,
                "priority": self.priority, "status": self.status}


PAGE = """<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>CloudOps 360 — IT Tickets</title><style>body{font:16px system-ui;background:#f3f6fa;color:#17243b;margin:0}main{max-width:820px;margin:48px auto;padding:20px}h1{margin-bottom:4px}.card{background:white;padding:24px;border-radius:14px;margin:20px 0;box-shadow:0 3px 15px #dce3ed}input,textarea,select,button{font:inherit;padding:10px;margin:6px 0;width:100%;box-sizing:border-box}button{background:#2456cc;color:white;border:0;border-radius:8px;cursor:pointer}li{padding:12px;border-bottom:1px solid #eee}small{color:#526078}</style>
<main><h1>CloudOps 360</h1><small>IT Support Ticket Manager · Phase 2</small>
<section class='card'><h2>Raise a ticket</h2><form id='form'><input name='title' placeholder='Issue title' maxlength='120' required><textarea name='description' placeholder='Describe the issue'></textarea><select name='priority'><option>low</option><option selected>medium</option><option>high</option></select><button>Create ticket</button></form><p id='message' role='status'></p></section>
<section class='card'><h2>Support tickets</h2><ul id='tickets'></ul></section></main>
<script>
async function load(){const r=await fetch('/api/tickets');const t=await r.json();const ul=document.querySelector('#tickets');ul.replaceChildren();for(const x of t){const li=document.createElement('li');const b=document.createElement('b');b.textContent='#'+x.id+' '+x.title;li.append(b,document.createElement('br'));const s=document.createElement('small');s.textContent=x.priority+' · '+x.status+' · '+x.description;li.append(s);ul.append(li)}if(!t.length)ul.textContent='No tickets yet.'}
document.querySelector('#form').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.target);const r=await fetch('/api/tickets',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(f))});document.querySelector('#message').textContent=r.ok?'Ticket created!':'Could not create ticket';if(r.ok){e.target.reset();await load()}});load();
</script></html>"""


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///tickets.db"),
                      SQLALCHEMY_TRACK_MODIFICATIONS=False)
    if config:
        app.config.update(config)
    db.init_app(app)

    @app.get("/")
    def index():
        return render_template_string(PAGE)

    @app.get("/health")
    def health():
        try:
            db.session.execute(select(1)).scalar_one()
            return jsonify(status="healthy", database="connected"), 200
        except Exception:
            app.logger.exception("Database health check failed")
            return jsonify(status="unhealthy", database="unavailable"), 503

    @app.get("/api/tickets")
    def list_tickets():
        tickets = db.session.execute(select(Ticket).order_by(Ticket.id.desc())).scalars().all()
        return jsonify([ticket.as_dict() for ticket in tickets])

    @app.post("/api/tickets")
    def add_ticket():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="Expected JSON object"), 400
        title = data.get("title")
        description = data.get("description", "")
        priority = data.get("priority", "medium")
        if (not isinstance(title, str) or not title.strip() or len(title.strip()) > 120
                or not isinstance(description, str) or len(description) > 1000
                or priority not in ("low", "medium", "high")):
            return jsonify(error="Invalid title, description or priority"), 400
        ticket = Ticket(title=title.strip(), description=description, priority=priority)
        db.session.add(ticket)
        db.session.commit()
        return jsonify(ticket.as_dict()), 201

    @app.patch("/api/tickets/<int:ticket_id>")
    def update_ticket(ticket_id):
        ticket = db.session.get(Ticket, ticket_id)
        if ticket is None:
            return jsonify(error="Ticket not found"), 404
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or set(data) != {"status"} or data["status"] not in ("open", "in_progress", "resolved"):
            return jsonify(error="Valid status required"), 400
        ticket.status = data["status"]
        db.session.commit()
        return jsonify(ticket.as_dict())

    with app.app_context():
        db.create_all()  # Learning-only: use migrations for production systems.
    return app
