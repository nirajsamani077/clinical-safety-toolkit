"""Builds the Word and Excel downloads for each template from src/data/templates.json.

Run from the project root:  python3 scripts/make_downloads.py
Writes public/downloads/<slug>.(docx|xlsx) and <slug>-oakfield-example.(docx|xlsx).
Needs: pip install python-docx openpyxl
"""
import json
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'src/data/templates.json').read_text())
OUT = ROOT / 'public/downloads'
OUT.mkdir(parents=True, exist_ok=True)
RISK = DATA['risk']
NAVY, TEAL, GREY = '032C47', '057092', '4B6577'
TONE = {1: 'DFF0D2', 2: 'DFF0D2', 3: 'FDE9B3', 4: 'F6C9C3', 5: 'F6C9C3'}
FOOT = ('From the Clinical Safety Toolkit for General Practice by Dr Niraj Samani. Written for the toolkit; '
        'free to copy and adapt. Not legal advice. Your Clinical Safety Officer signs off your practice\'s own documents.')
DRAFT = 'DRAFT for review by a Clinical Safety Officer. Adapt it to your practice before use.'


def cellval(c, example):
    if isinstance(c, list):
        return c[1] if example else c[0]
    return c


# ---------- Word ----------
def shade(cell, hex_colour):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_colour)
    tcPr.append(shd)


def head_row(table, cols):
    for i, c in enumerate(cols):
        cell = table.rows[0].cells[i]
        cell.text = ''
        r = cell.paragraphs[0].add_run(c)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        shade(cell, NAVY)


def para(doc, text, italic=False, colour=None, size=None, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic, r.bold = italic, bold
    if colour:
        r.font.color.rgb = RGBColor.from_string(colour)
    if size:
        r.font.size = Pt(size)
    return p


def word(t, example):
    doc = Document()
    st = doc.styles['Normal']
    st.font.name = 'Arial'
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2)
        s.top_margin = s.bottom_margin = Cm(1.8)
        fp = s.footer.paragraphs[0]
        fr = fp.add_run(FOOT)
        fr.font.size = Pt(8)
        fr.font.color.rgb = RGBColor.from_string(GREY)
    para(doc, DRAFT, bold=True, colour='8A5A00', size=9)
    para(doc, f"{t['formal']}  ·  {t['stage']} stage", colour=TEAL, size=9, bold=True)
    h = doc.add_heading(t['title'], 0)
    for r in h.runs:
        r.font.color.rgb = RGBColor.from_string(NAVY)
    if example:
        para(doc, 'Oakfield Surgery (a made-up practice). Example only.', bold=True, colour='920570')
    for label, key in (('What it\'s for', 'purpose'), ('Who', 'who'), ('When', 'when')):
        p = doc.add_paragraph()
        r = p.add_run(label + ': ')
        r.bold = True
        p.add_run(t[key])
    for b in t['blocks']:
        k = b['t']
        if k == 'h':
            hh = doc.add_heading(b['x'], 1)
            for r in hh.runs:
                r.font.color.rgb = RGBColor.from_string(NAVY)
        elif k == 'p':
            doc.add_paragraph(b['x'])
        elif k == 'g':
            para(doc, b['x'], italic=True, colour=GREY)
        elif k == 'list':
            for x in b['x']:
                doc.add_paragraph(x, style='List Bullet')
        elif k == 'fields':
            tb = doc.add_table(rows=len(b['rows']), cols=2)
            tb.style = 'Table Grid'
            for i, (l, ex) in enumerate(b['rows']):
                c0 = tb.rows[i].cells[0]
                c0.text = ''
                c0.paragraphs[0].add_run(l).bold = True
                shade(c0, 'EEF4F7')
                tb.rows[i].cells[1].text = ex if example else ''
            doc.add_paragraph()
        elif k == 'area':
            tb = doc.add_table(rows=1, cols=1)
            tb.style = 'Table Grid'
            c = tb.rows[0].cells[0]
            c.text = ''
            r = c.paragraphs[0].add_run(b['label'])
            r.bold = True
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor.from_string(GREY)
            c.add_paragraph(b['ex'] if example else '')
            if not example:
                c.add_paragraph('')
                c.add_paragraph('')
            doc.add_paragraph()
        elif k == 'sign':
            cols = ['Role', 'Name', 'Signature', 'Date']
            tb = doc.add_table(rows=1 + len(b['rows']), cols=4)
            tb.style = 'Table Grid'
            head_row(tb, cols)
            for i, r in enumerate(b['rows'], 1):
                tb.rows[i].cells[0].text = r
                tb.rows[i].height = Cm(1.2)
        elif k == 'grid':
            tb = doc.add_table(rows=6, cols=6)
            tb.style = 'Table Grid'
            tb.alignment = WD_TABLE_ALIGNMENT.CENTER
            head_row(tb, ['Likelihood / Severity'] + RISK['severity'])
            for i, row in enumerate(RISK['grid'], 1):
                tb.rows[i].cells[0].text = RISK['likelihood'][i - 1]
                for j, v in enumerate(row, 1):
                    c = tb.rows[i].cells[j]
                    c.text = str(v)
                    shade(c, TONE[v])
            doc.add_paragraph()
        elif k == 'table':
            rows = [list(r) for r in b.get('fixed', [])] + [[cellval(c, example) for c in r] for r in b.get('rows', [])]
            rows += [[''] * len(b['cols']) for _ in range(b.get('blank', 0))]
            tb = doc.add_table(rows=1 + len(rows), cols=len(b['cols']))
            tb.style = 'Table Grid'
            head_row(tb, b['cols'])
            for i, r in enumerate(rows, 1):
                for j, v in enumerate(r):
                    tb.rows[i].cells[j].text = str(v)
                if not any(r):
                    tb.rows[i].height = Cm(0.8)
            doc.add_paragraph()
    name = t['slug'] + ('-oakfield-example' if example else '') + '.docx'
    doc.save(OUT / name)


# ---------- Excel ----------
thin = Side(style='thin', color='CFDBE3')
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def excel(t, example):
    wb = Workbook()
    ws = wb.active
    ws.title = t['title'][:31]
    cols = t['cols']
    ncol = len(cols)
    ws.cell(row=1, column=1, value=f"{t['title']}  ·  {DRAFT}").font = Font(bold=True, color='8A5A00')
    for j, c in enumerate(cols, 1):
        h = ws.cell(row=2, column=j, value=c['n'])
        h.font = Font(bold=True, color='FFFFFF')
        h.fill = PatternFill('solid', fgColor=NAVY)
        h.alignment = Alignment(wrap_text=True, vertical='top')
        h.border = BORDER
        g = ws.cell(row=3, column=j, value=c['g'] + (f" ({' / '.join(c['v'])})" if isinstance(c.get('v'), list) else ''))
        g.font = Font(italic=True, color=GREY, size=9)
        g.fill = PatternFill('solid', fgColor='EEF4F7')
        g.alignment = Alignment(wrap_text=True, vertical='top')
        g.border = BORDER
        ws.column_dimensions[get_column_letter(j)].width = c['w']
    first = 4
    data_rows = t['ex'] if example else []
    total = len(data_rows) + t.get('blank', 20)
    last = first + total - 1
    for i in range(total):
        r = first + i
        vals = data_rows[i] if i < len(data_rows) else [''] * ncol
        for j, c in enumerate(cols, 1):
            cell = ws.cell(row=r, column=j)
            if c.get('f'):
                a, b2 = (int(x) + 1 for x in c['f'].split(','))
                la, lb = get_column_letter(a), get_column_letter(b2)
                cell.value = (f'=IF(OR({la}{r}="",{lb}{r}=""),"",INDEX(Grid!$B$2:$F$6,'
                              f'MATCH({la}{r},Grid!$A$2:$A$6,0),MATCH({lb}{r},Grid!$B$1:$F$1,0)))')
                cell.alignment = Alignment(horizontal='center', vertical='top')
                cell.font = Font(bold=True)
            else:
                cell.value = vals[j - 1] or None
                cell.alignment = Alignment(wrap_text=True, vertical='top')
            cell.border = BORDER
    # Drop-down lists
    for j, c in enumerate(cols, 1):
        v = c.get('v')
        if not v:
            continue
        col = get_column_letter(j)
        if v == 'L':
            dv = DataValidation(type='list', formula1='=Grid!$A$2:$A$6', allow_blank=True)
        elif v == 'S':
            dv = DataValidation(type='list', formula1='=Grid!$B$1:$F$1', allow_blank=True)
        else:
            dv = DataValidation(type='list', formula1='"' + ','.join(v) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f'{col}{first}:{col}{last}')
    # Colour the risk scores
    for j, c in enumerate(cols, 1):
        if c.get('f'):
            rng = f'{get_column_letter(j)}{first}:{get_column_letter(j)}{last}'
            ws.conditional_formatting.add(rng, CellIsRule(operator='between', formula=['1', '2'], fill=PatternFill('solid', fgColor=TONE[1])))
            ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['3'], fill=PatternFill('solid', fgColor=TONE[3])))
            ws.conditional_formatting.add(rng, CellIsRule(operator='between', formula=['4', '5'], fill=PatternFill('solid', fgColor=TONE[4])))
    ws.freeze_panes = 'B4'
    ws.row_dimensions[2].height = 32
    ws.row_dimensions[3].height = 30
    # Risk grid sheet (always included: the hazard log formulas use it)
    if t.get('risk'):
        g = wb.create_sheet('Grid')
        g['A1'] = 'Likelihood / Severity'
        g['A1'].font = Font(bold=True)
        for j, s in enumerate(RISK['severity'], 2):
            c = g.cell(row=1, column=j, value=s)
            c.font = Font(bold=True, color='FFFFFF')
            c.fill = PatternFill('solid', fgColor=NAVY)
            g.column_dimensions[get_column_letter(j)].width = 14
        g.column_dimensions['A'].width = 22
        for i, row in enumerate(RISK['grid'], 2):
            g.cell(row=i, column=1, value=RISK['likelihood'][i - 2]).font = Font(bold=True)
            for j, v in enumerate(row, 2):
                c = g.cell(row=i, column=j, value=v)
                c.fill = PatternFill('solid', fgColor=TONE[v])
                c.alignment = Alignment(horizontal='center')
                c.border = BORDER
        for i, (k, m) in enumerate(RISK['meaning'].items(), 8):
            g.cell(row=i, column=1, value=f'{k}: {m}')
    # About sheet
    a = wb.create_sheet('About')
    a.column_dimensions['A'].width = 18
    a.column_dimensions['B'].width = 90
    rows = [('Template', t['title']), ('Standard', t['formal']), ("What it's for", t['purpose']), ('Who', t['who']),
            ('When', t['when']), ('Status', DRAFT), ('Source', FOOT)]
    if example:
        rows.insert(1, ('Example', 'Filled in for Oakfield Surgery, a made-up practice.'))
    for i, (k, v) in enumerate(rows, 1):
        a.cell(row=i, column=1, value=k).font = Font(bold=True)
        a.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True)
    name = t['slug'] + ('-oakfield-example' if example else '') + '.xlsx'
    wb.save(OUT / name)


for t in DATA['templates']:
    for ex in (False, True):
        (excel if t['kind'] == 'sheet' else word)(t, ex)
print('Wrote', len(list(OUT.iterdir())), 'files to', OUT)
