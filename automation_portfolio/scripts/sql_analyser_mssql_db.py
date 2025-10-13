import os
import pyodbc
import argparse
from fpdf import FPDF
from graphviz import Digraph
from datetime import datetime

# ────── CLI Arguments ──────
parser = argparse.ArgumentParser(description="Analyze MSSQL database schema directly.")
parser.add_argument("--server", required=True, help="SQL Server instance name")
parser.add_argument("--database", required=True, help="Database name")
parser.add_argument("--trusted", action="store_true", help="Use Windows authentication")
parser.add_argument("--username", help="SQL Server username (if not using Windows auth)")
parser.add_argument("--password", help="SQL Server password (if not using Windows auth)")
parser.add_argument("--output", default="./output", help="Path to output folder")
args = parser.parse_args()

output_folder = args.output
os.makedirs(output_folder, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_pdf = os.path.join(output_folder, f"mssql_analysis_{timestamp}.pdf")
output_erd = os.path.join(output_folder, f"erd_{timestamp}")

# ────── Database Connection ──────
if args.trusted:
    conn_str = f'DRIVER={{SQL Server}};SERVER={args.server};DATABASE={args.database};Trusted_Connection=yes;'
else:
    conn_str = f'DRIVER={{SQL Server}};SERVER={args.server};DATABASE={args.database};UID={args.username};PWD={args.password}'

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# ────── Get Schema Info ──────
tables = {}
relationships = []
views = {}

# Get all tables and their columns
print("\nGathering table information...")
cursor.execute("""
    SELECT 
        SCHEMA_NAME(t.schema_id) as schema_name,
        t.name as table_name,
        c.name as column_name,
        tp.name as data_type,
        c.max_length,
        c.precision,
        c.scale,
        c.is_nullable,
        c.is_computed
    FROM sys.tables t
    INNER JOIN sys.columns c ON t.object_id = c.object_id
    INNER JOIN sys.types tp ON c.user_type_id = tp.user_type_id
    ORDER BY schema_name, table_name, c.column_id
""")

for row in cursor.fetchall():
    schema_name = row.schema_name
    table_name = row.table_name
    full_name = f"{schema_name}.{table_name}"
    
    if full_name not in tables:
        print(f"\nFound table: {full_name}")
        tables[full_name] = {"columns": [], "pks": [], "fks": []}
    
    if not row.is_computed:  # Skip computed columns
        # Format type with size/precision/scale if needed
        type_name = row.data_type
        if row.data_type in ('varchar', 'nvarchar', 'char', 'nchar'):
            size = row.max_length
            if row.data_type.startswith('n'):
                size = size // 2  # Unicode types
            if size == -1:
                size = 'max'
            type_name = f"{type_name}({size})"
        elif row.data_type in ('decimal', 'numeric'):
            type_name = f"{type_name}({row.precision},{row.scale})"
        
        print(f"  Column: {row.column_name} ({type_name})")
        tables[full_name]["columns"].append((row.column_name, type_name))

# Get primary keys
print("\nGathering primary key information...")
cursor.execute("""
    SELECT 
        SCHEMA_NAME(t.schema_id) as schema_name,
        t.name as table_name,
        c.name as column_name
    FROM sys.tables t
    INNER JOIN sys.indexes i ON t.object_id = i.object_id
    INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
    INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
    WHERE i.is_primary_key = 1
    ORDER BY schema_name, table_name, ic.key_ordinal
""")

for row in cursor.fetchall():
    full_name = f"{row.schema_name}.{row.table_name}"
    if full_name in tables:
        print(f"PK found for {full_name}: {row.column_name}")
        tables[full_name]["pks"].append(row.column_name)

# Get foreign keys
print("\nGathering foreign key information...")
cursor.execute("""
    SELECT
        SCHEMA_NAME(fk_tab.schema_id) as fk_schema_name,
        fk_tab.name as fk_table_name,
        fk_col.name as fk_column_name,
        SCHEMA_NAME(pk_tab.schema_id) as pk_schema_name,
        pk_tab.name as pk_table_name,
        pk_col.name as pk_column_name
    FROM sys.foreign_keys fk
    INNER JOIN sys.tables fk_tab ON fk.parent_object_id = fk_tab.object_id
    INNER JOIN sys.tables pk_tab ON fk.referenced_object_id = pk_tab.object_id
    INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
    INNER JOIN sys.columns fk_col ON fkc.parent_object_id = fk_col.object_id AND fkc.parent_column_id = fk_col.column_id
    INNER JOIN sys.columns pk_col ON fkc.referenced_object_id = pk_col.object_id AND fkc.referenced_column_id = pk_col.column_id
    ORDER BY fk_schema_name, fk_table_name, fk_col.column_id
""")

for row in cursor.fetchall():
    fk_full_name = f"{row.fk_schema_name}.{row.fk_table_name}"
    pk_full_name = f"{row.pk_schema_name}.{row.pk_table_name}"
    if fk_full_name in tables:
        print(f"FK found: {fk_full_name}.{row.fk_column_name} -> {pk_full_name}.{row.pk_column_name}")
        tables[fk_full_name]["fks"].append((row.fk_column_name, pk_full_name, row.pk_column_name))
        relationships.append((fk_full_name, pk_full_name))

# Get views
print("\nGathering view information...")
cursor.execute("""
    SELECT 
        SCHEMA_NAME(v.schema_id) as schema_name,
        v.name as view_name,
        OBJECT_DEFINITION(v.object_id) as view_definition
    FROM sys.views v
    ORDER BY schema_name, view_name
""")

for row in cursor.fetchall():
    full_name = f"{row.schema_name}.{row.view_name}"
    print(f"Found view: {full_name}")
    views[full_name] = row.view_definition

# ────── Table purpose detection ──────
def table_purpose(name):
    """Detect table purpose by analyzing its structure and relationships"""
    table_data = tables.get(name)
    if not table_data:
        return "Unknown purpose (table data not found)"

    # Get column names and analysis data
    columns = [col[0].lower() for col in table_data["columns"]]
    column_count = len(table_data["columns"])
    pk_count = len(table_data["pks"])
    fk_count = len(table_data["fks"])
    
    # Count relationships
    incoming = sum(1 for r in relationships if r[1] == name)  # Tables referencing this one
    outgoing = sum(1 for r in relationships if r[0] == name)  # Tables this one references
    
    # Detect temporal/audit patterns
    temporal_columns = ['created_at', 'modified_at', 'created_by', 'modified_by', 
                       'created_date', 'modified_date', 'timestamp', 'date_added']
    has_temporal = any(col for col in columns if any(t in col for t in temporal_columns))
    has_audit = any(col for col in columns if 'version' in col or 'action' in col or 'type' in col)
    
    # Detect lookup/reference tables
    if column_count <= 3 and pk_count == 1 and incoming > 2:
        return f"Lookup/reference table (referenced by {incoming} tables)"
    
    # Detect junction/mapping tables
    if fk_count >= 2 and column_count <= (fk_count + 2):
        return f"Junction/mapping table ({fk_count} relationships)"
    
    # Detect audit/history tables
    if has_temporal and has_audit:
        return "Audit/history tracking table"
    
    # Detect master/primary entity tables
    if incoming > outgoing and column_count > 5 and pk_count == 1:
        return f"Master entity table (referenced by {incoming} tables)"
    
    # Detect configuration tables
    config_indicators = ['setting', 'config', 'parameter', 'option', 'preference']
    if any(col for col in columns if any(ind in col for ind in config_indicators)):
        return "Configuration/settings table"
    
    # Detect transaction/fact tables
    transaction_indicators = ['amount', 'quantity', 'total', 'balance', 'price', 
                            'cost', 'payment', 'transaction']
    if has_temporal and any(col for col in columns if any(ind in col for ind in transaction_indicators)):
        return "Transaction/fact table"
    
    # Detect status tracking tables
    status_indicators = ['status', 'state', 'condition', 'phase', 'stage']
    if any(col for col in columns if any(ind in col for ind in status_indicators)):
        return "Status tracking table"
    
    # Detect hierarchy/tree structures
    if any(fk[1] == name for fk in table_data["fks"]):  # Self-referencing
        return "Hierarchical/tree structure table"
        
    # If no specific pattern is detected
    if incoming == 0 and outgoing > 0:
        return "Child/detail table"
    elif incoming > 0 and outgoing == 0:
        return "Parent/header table"
    else:
        return "General purpose or domain-specific table"

# ────── Generate ERD ──────
print("\nGenerating ERD diagram...")
dot = Digraph(comment="MSSQL ERD", format="png")
for t in tables:
    dot.node(t)
for rel in relationships:
    dot.edge(rel[0], rel[1])
dot.render(output_erd, cleanup=True)

# ────── PDF Report ──────
print("\nGenerating PDF report...")
class PDF(FPDF):

    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'MSSQL Database Schema Analysis', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(220, 220, 250)
        self.cell(0, 8, title, ln=True, fill=True)
        self.ln(2)

    def section_body(self, text):
        self.set_font('Arial', '', 10)
        text = text.replace('—', '-')  # Replace em dash with regular hyphen
        self.multi_cell(0, 5, text)
        self.ln()

pdf = PDF()
pdf.add_page()

pdf.section_title("1. Overview")
pdf.section_body(f"Database: {args.server}.{args.database}\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

pdf.section_title("2. Tables & Assumptions")
if tables:
    for name, data in tables.items():
        text = f"Table: {name}\nPurpose: {table_purpose(name)}\nColumns: {', '.join([c[0] for c in data['columns']])}\nPrimary Keys: {', '.join(data['pks'])}\nForeign Keys: {', '.join([f'{fk[0]} -> {fk[1]}.{fk[2]}' for fk in data['fks']])}\n"
        pdf.section_body(text)
else:
    pdf.section_body("No tables detected.")

pdf.section_title("3. Views")
if views:
    for v in views:
        pdf.section_body(f"{v} - likely a reporting or simplified query layer.")
else:
    pdf.section_body("No views detected.")

pdf.section_title("4. Relationships Overview")
if relationships:
    rels = "\n".join([f"{src} -> {dst}" for src, dst in relationships])
    pdf.section_body(rels)
else:
    pdf.section_body("No relationships detected.")

pdf.section_title("5. Entity-Relationship Diagram")
pdf.image(output_erd + ".png", w=180)

# Add glossary section
pdf.add_page()
pdf.section_title("6. Glossary of Terms")
glossary = {
    "Lookup/reference table": 
        "A small table that contains a list of valid values or codes and their descriptions. "
        "For example, a table of country codes and their full names, or a list of product categories. "
        "These tables are frequently referenced by other tables to ensure data consistency.",

    "Junction/mapping table": 
        "A table that connects two or more other tables, typically used to represent many-to-many relationships. "
        "For example, a table linking students to courses they're enrolled in, where each student can take multiple courses "
        "and each course can have multiple students.",

    "Audit/history tracking table": 
        "A table that keeps a record of changes made to data over time. It typically includes timestamps, "
        "user information, and details about what was changed. This helps maintain a historical record "
        "of data modifications for compliance and troubleshooting.",

    "Master entity table": 
        "A primary table that contains the core information about a main business entity. "
        "For example, a Customer table containing basic customer information that other tables "
        "reference for customer-related data. These tables are central to the database structure.",

    "Configuration/settings table": 
        "A table storing system or application settings, parameters, or preferences. "
        "These might include user preferences, system configuration values, or application parameters "
        "that control how the system behaves.",

    "Transaction/fact table": 
        "A table that records business events or transactions, typically including dates, amounts, "
        "and quantities. Examples include sales transactions, financial records, or inventory movements. "
        "These tables often grow larger over time as new transactions are recorded.",

    "Status tracking table": 
        "A table that monitors the current state or condition of entities in the system. "
        "It might track order statuses, project phases, or approval stages, helping to manage "
        "workflows and business processes.",

    "Hierarchical/tree structure table": 
        "A table that represents hierarchical relationships within itself, like an organizational chart "
        "where employees report to other employees, or a category system where categories can have subcategories.",

    "Child/detail table": 
        "A table that depends on or provides additional information for records in another table. "
        "For example, order details providing line items for a main order record. These tables "
        "typically reference their parent tables.",

    "Parent/header table": 
        "A main table that other tables reference and depend on. It typically contains the primary "
        "information that detail records elaborate on. For example, an order header table containing "
        "basic order information, with details stored in related tables.",

    "General purpose or domain-specific table": 
        "A table that serves a specific business need but doesn't follow a common structural pattern. "
        "These tables are customized for particular business requirements and may combine various "
        "characteristics of other table types."
}

for term, definition in glossary.items():
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 6, term, ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, definition)
    pdf.ln(5)

pdf.output(output_pdf)
print(f"\n✅ Report generated: {output_pdf}")
