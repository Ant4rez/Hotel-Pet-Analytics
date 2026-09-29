"""
diagram_kit: small toolkit to draw clean, accurate cloud architecture diagrams
as SVG + high-resolution PNG, using the official AWS icons shipped inside the
`diagrams` Python package (no Graphviz layout: you place every element).

Install:  pip install diagrams pillow cairosvg
Usage:    see references/example_alphagen.py
"""
from __future__ import annotations
import base64, glob, io, os, platform, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageFont

# ---------------------------------------------------------------- resources
def resources_dir() -> Path:
    """Folder with the icon PNGs bundled by the `diagrams` package."""
    import diagrams
    p = Path(diagrams.__file__).resolve().parent.parent / "resources"
    if not p.exists():
        raise FileNotFoundError(f"diagrams resources not found at {p}. Run: pip install diagrams")
    return p

# Friendly aliases -> path under resources/. Use find_icons() for anything else.
ICONS = {
    "eventbridge": "aws/integration/eventbridge.png",
    "eventbridge-scheduler": "aws/integration/eventbridge-scheduler.png",
    "sqs": "aws/integration/simple-queue-service-sqs.png",
    "sns": "aws/integration/simple-notification-service-sns.png",
    "step-functions": "aws/integration/step-functions.png",
    "lambda": "aws/compute/lambda.png",
    "ecr": "aws/compute/ec2-container-registry.png",
    "ec2": "aws/compute/ec2.png",
    "ecs": "aws/compute/elastic-container-service.png",
    "fargate": "aws/compute/fargate.png",
    "bedrock": "aws/ml/bedrock.png",
    "sagemaker": "aws/ml/sagemaker.png",
    "s3": "aws/storage/simple-storage-service-s3.png",
    "dynamodb": "aws/database/dynamodb.png",
    "rds": "aws/database/rds.png",
    "aurora": "aws/database/aurora.png",
    "redshift": "aws/database/redshift.png",
    "elasticache": "aws/database/elasticache.png",
    "ses": "aws/engagement/simple-email-service-ses.png",
    "apigw": "aws/network/api-gateway.png",
    "cloudfront": "aws/network/cloudfront.png",
    "vpc": "aws/network/vpc.png",
    "cloudwatch": "aws/management/cloudwatch.png",
    "cloudformation": "aws/management/cloudformation.png",
    "ssm": "aws/management/systems-manager.png",
    "iam": "aws/security/identity-and-access-management-iam.png",
    "secrets-manager": "aws/security/secrets-manager.png",
    "cognito": "aws/security/cognito.png",
    "glue": "aws/analytics/glue.png",
    "athena": "aws/analytics/athena.png",
    "kinesis": "aws/analytics/kinesis.png",
    "quicksight": "aws/analytics/quicksight.png",
    "internet": "aws/general/internet-alt1.png",
    "user": "aws/general/user.png",
    "users": "aws/general/users.png",
    "client": "aws/general/client.png",
    "python": "programming/language/python.png",
    "docker": "onprem/container/docker.png",
    "airflow": "onprem/workflow/airflow.png",
    "postgresql": "onprem/database/postgresql.png",
    "mysql": "onprem/database/mysql.png",
    "oracle": "onprem/database/oracle.png",
    "spark": "onprem/analytics/spark.png",
    "databricks": "onprem/analytics/databricks.png",
    "powerbi": "onprem/analytics/powerbi.png",
    "github": "onprem/vcs/github.png",
}

def find_icons(pattern: str) -> list[str]:
    """Search icon files by substring, e.g. find_icons('glue')."""
    root = resources_dir()
    return sorted(str(Path(p).relative_to(root)).replace("\\", "/")
                  for p in glob.glob(str(root / "**" / "*.png"), recursive=True)
                  if pattern.lower() in Path(p).name.lower())

def icon_path(key: str) -> Path:
    rel = ICONS.get(key, key)
    p = resources_dir() / rel
    if not p.exists():
        hits = find_icons(Path(key).stem.split("/")[-1])
        raise FileNotFoundError(f"icon '{key}' not found ({p}). Similar: {hits[:8]}")
    return p

_B64: dict[str, str] = {}
def icon_b64(key_or_path: str) -> str:
    if key_or_path not in _B64:
        p = Path(key_or_path) if os.path.exists(key_or_path) else icon_path(key_or_path)
        im = Image.open(p).convert("RGBA").resize((256, 256), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "PNG")
        _B64[key_or_path] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    return _B64[key_or_path]

# ---------------------------------------------------------------- fonts
def find_font() -> tuple[str, str, str]:
    """Return (family, regular_ttf, bold_ttf). Prefers Carlito/Calibri, falls back to DejaVu/Arial."""
    candidates = [
        ("Carlito", "Carlito-Regular.ttf", "Carlito-Bold.ttf"),
        ("Calibri", "calibri.ttf", "calibrib.ttf"),
        ("DejaVu Sans", "DejaVuSans.ttf", "DejaVuSans-Bold.ttf"),
        ("Arial", "arial.ttf", "arialbd.ttf"),
    ]
    dirs = ["/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts"),
            os.path.expanduser("~/Library/Fonts"), "/Library/Fonts", "/System/Library/Fonts",
            r"C:\Windows\Fonts", os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts")]
    files = {}
    for d in dirs:
        if os.path.isdir(d):
            for p in glob.glob(os.path.join(d, "**", "*.ttf"), recursive=True):
                files.setdefault(os.path.basename(p).lower(), p)
    for fam, reg, bold in candidates:
        r, b = files.get(reg.lower()), files.get(bold.lower())
        if r and b:
            return fam, r, b
    raise FileNotFoundError("No suitable TTF font found (install Carlito: fonts-crosextra-carlito)")

# ---------------------------------------------------------------- palette (AWS categories)
PALETTE = {
    "dark": "#232F3E", "gray": "#545B64", "light": "#879196", "border": "#D5DBDB",
    "compute": "#D45B07", "storage": "#3F8624", "database": "#3334B9", "integration": "#E7157B",
    "management": "#E7157B", "security": "#DD344C", "ml": "#01A88D", "network": "#8C4FFF",
    "engagement": "#3334B9", "analytics": "#8C4FFF", "external": "#232F3E",
}

def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- canvas
class Diagram:
    """Absolute-coordinate SVG canvas. All sizes are in px at 1x (default 1920 wide)."""

    def __init__(self, width=1920, height=1080, background="#FFFFFF"):
        self.W, self.H, self.bg = width, height, background
        self.family, self._fr, self._fb = find_font()
        self.out: list[str] = []
        self.warnings: list[str] = []
        self._markers: set[str] = set()
        self.boxes: list[tuple[str, float, float, float, float]] = []  # for overlap checks

    # ---- measuring
    def text_width(self, s: str, size: float, bold=False) -> float:
        return ImageFont.truetype(self._fb if bold else self._fr, int(round(size))).getlength(s) * (size / int(round(size)))

    # ---- primitives
    def text(self, x, y, s, size=12, color=PALETTE["gray"], bold=False, anchor="middle", maxw=None, italic=False):
        if maxw and self.text_width(s, size, bold) > maxw:
            self.warnings.append(f"TEXT OVERFLOW: {s!r} is {self.text_width(s, size, bold):.0f}px > {maxw:.0f}px")
        fw = ' font-weight="bold"' if bold else ""
        fi = ' font-style="italic"' if italic else ""
        self.out.append(f'<text x="{x}" y="{y}" font-family="{self.family}" font-size="{size}" '
                        f'fill="{color}" text-anchor="{anchor}"{fw}{fi}>{_esc(s)}</text>')

    def rect(self, x, y, w, h, fill="#FFFFFF", stroke=PALETTE["border"], sw=1, rx=10, dash=None, shadow=False, opacity=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        f = ' filter="url(#sh)"' if shadow else ""
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                        f'fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"{d}{f}/>')

    def circle(self, cx, cy, r, fill="#FFFFFF", stroke="none"):
        self.out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}"/>')

    def icon(self, key, x, y, size):
        self.out.append(f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="{icon_b64(key)}"/>')

    # ---- composites
    def card(self, cx, y, w, icon, title, lines=(), color=PALETTE["dark"], icon_size=46, h=None,
             shadow=True, fill="#FFFFFF", name=None):
        """Service card centered at cx. Returns (x, y, w, h)."""
        lines = [l for l in lines]
        h = h or (icon_size + 34 + 16 * len(lines) + 10)
        x = cx - w / 2
        self.rect(x, y, w, h, fill=fill, shadow=shadow)
        self.icon(icon, cx - icon_size / 2, y + 12, icon_size)
        self.text(cx, y + icon_size + 30, title, 15, color, True, maxw=w - 12)
        for i, l in enumerate(lines):
            if l:
                self.text(cx, y + icon_size + 48 + 16 * i, l, 12, PALETTE["gray"], maxw=w - 12)
        self.boxes.append((name or title, x, y, w, h))
        return (x, y, w, h)

    def external(self, cx, y, w, icon, title, lines=(), icon_size=40, name=None):
        """Card for things outside the cloud boundary (users, SaaS, data sources)."""
        return self.card(cx, y, w, icon, title, lines, PALETTE["dark"], icon_size, shadow=False, fill="#F7F8F8", name=name)

    def group(self, x, y, w, h, label, color, fill, dash="6 4"):
        """Dashed logical group (pipeline, API, IaC...)."""
        self.rect(x, y, w, h, fill=fill, stroke=color, sw=1.4, rx=12, dash=dash)
        self.text(x + 16, y + 22, label, 14, color, True, anchor="start")
        return (x, y, w, h)

    def cloud_boundary(self, x, y, w, h, label="AWS Cloud"):
        self.rect(x, y, w, h, fill="#FFFFFF", stroke=PALETTE["dark"], sw=1.6, rx=14)
        tw = self.text_width(label, 14, True) + 36
        self.rect(x, y, tw, 30, fill=PALETTE["dark"], stroke=PALETTE["dark"], rx=8)
        self.text(x + tw / 2, y + 20, label, 14, "#FFFFFF", True)
        return (x, y, w, h)

    def stage_row(self, x0, y, stages, width=194, gap=11, height=168):
        """Numbered step cards in a row. stages = [(num, title, color, [lines])].
        Returns {title: (center_x, bottom_y)} to anchor arrows."""
        anchors = {}
        for i, (n, t, col, ls) in enumerate(stages):
            x = x0 + i * (width + gap)
            self.rect(x, y, width, height, fill="#FFFFFF", stroke=col, sw=1.3, rx=10)
            self.rect(x, y, width, 34, fill=col, stroke=col, rx=10)
            self.rect(x, y + 20, width, 14, fill=col, stroke=col, rx=0)
            self.circle(x + 20, y + 17, 11)
            self.text(x + 20, y + 22, str(n), 14, col, True)
            self.text(x + 38, y + 23, t, 16, "#FFFFFF", True, anchor="start", maxw=width - 44)
            for j, l in enumerate(ls):
                if l:
                    self.text(x + 12, y + 58 + j * 20, l, 12.5, PALETTE["gray"], anchor="start", maxw=width - 18)
            anchors[t] = (x + width / 2, y + height)
        return anchors

    def arrow(self, points, color=PALETTE["gray"], width=1.8, dash=None, head=True,
              label=None, label_at=None, label_anchor="start", label_color=None):
        """Orthogonal polyline through `points`. Put label_at in empty space, never on a border."""
        d = "M " + " L ".join(f"{a},{b}" for a, b in points)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#a{color.lstrip("#")})"' if head else ""
        self.out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
                        f'stroke-linejoin="round"{da}{mk}/>')
        if head:
            self._markers.add(color)
        if label:
            lx, ly = label_at
            wbox = self.text_width(label, 12) + 10
            bx = lx - 5 if label_anchor == "start" else (lx - wbox / 2 if label_anchor == "middle" else lx - wbox + 5)
            self.out.append(f'<rect x="{bx}" y="{ly - 12}" width="{wbox}" height="17" rx="4" fill="#FFFFFF" fill-opacity="0.92"/>')
            self.text(lx, ly, label, 12, label_color or color, anchor=label_anchor)

    def legend(self, x, y, items=(("data flow", PALETTE["gray"], None), ("logs", PALETTE["light"], "6 4"),
                                  ("deployment", "#E7157B", "3 3"))):
        for lab, col, dash in items:
            self.arrow([(x, y - 4), (x + 34, y - 4)], col, dash=dash)
            self.text(x + 42, y, lab, 13, PALETTE["gray"], anchor="start")
            x += 42 + self.text_width(lab, 13) + 30

    def header(self, title, subtitle="", caption="", chip=None, x=60):
        self.text(x, 62, title, 40, PALETTE["dark"], True, anchor="start")
        if subtitle:
            self.text(x + self.text_width(title, 40, True) + 18, 62, subtitle, 22, PALETTE["gray"], anchor="start")
        if caption:
            self.text(x, 94, caption, 15, PALETTE["light"], anchor="start")
        if chip:
            cw = self.text_width(chip, 14, True) + 28
            self.rect(self.W - 60 - cw, 40, cw, 34, fill="#FFF3E6", stroke="#ED7100", rx=17)
            self.text(self.W - 60 - cw / 2, 62, chip, 14, "#D45B07", True)

    def stats_box(self, x, y, w, title, line):
        self.rect(x, y, w, 62, fill="#F2F3F3", stroke="#F2F3F3", rx=10)
        self.text(x + 20, y + 26, title, 15, PALETTE["dark"], True, anchor="start")
        self.text(x + 20, y + 48, line, 14, PALETTE["gray"], anchor="start", maxw=w - 40)

    # ---- checks
    def check_overlaps(self, pad=4):
        """Warn when two registered cards overlap (cards only, not groups/arrows)."""
        b = self.boxes
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                n1, x1, y1, w1, h1 = b[i]; n2, x2, y2, w2, h2 = b[j]
                if x1 < x2 + w2 + pad and x2 < x1 + w1 + pad and y1 < y2 + h2 + pad and y2 < y1 + h1 + pad:
                    self.warnings.append(f"CARD OVERLAP: {n1} x {n2}")
        for n, x, y, w, h in b:
            if x < 0 or y < 0 or x + w > self.W or y + h > self.H:
                self.warnings.append(f"OUT OF CANVAS: {n}")

    # ---- output
    def svg(self) -> str:
        defs = ('<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="130%">'
                '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.10"/></filter>')
        for c in sorted(self._markers):
            defs += (f'<marker id="a{c.lstrip("#")}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                     f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
        defs += "</defs>"
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}">'
                f'<rect width="100%" height="100%" fill="{self.bg}"/>{defs}' + "\n".join(self.out) + "</svg>")

    def save(self, path_png: str, scale=2, save_svg=True) -> list[str]:
        """Render PNG at `scale`x (2 = 3840 px wide for a 1920 canvas). Returns warnings."""
        import cairosvg
        self.check_overlaps()
        svg = self.svg()
        if save_svg:
            Path(path_png).with_suffix(".svg").write_text(svg, encoding="utf-8")
        cairosvg.svg2png(bytestring=svg.encode(), write_to=path_png,
                         output_width=self.W * scale, output_height=self.H * scale)
        return self.warnings

def crop(path_png: str, box: tuple[int, int, int, int], out: str, scale=2):
    """Save a zoomed crop (box in 1x canvas coordinates) for visual review."""
    im = Image.open(path_png)
    x0, y0, x1, y1 = (v * scale for v in box)
    im.crop((x0, y0, x1, y1)).save(out)
    return out
