import json

def generate_iso27001_nfrm_html():
    """
    Generates an HTML file containing a formally compliant Mermaid diagram
    for the ISO 27001 / NFRM process, validated against the ISO/IEC 24744 metamodel.
    """

    # Revised tooltip data, compliant with the ISO 27001/NFRM context and
    # the formal ISO/IEC 24744 metamodel class mappings.
    tips = {
        'CO': {'de': 'Kontrollziel', 'en': 'Control Objective', 'de_def': 'Ein spezifisches, übergeordnetes Ziel zur Risikominderung, das durch Kontrollen erreicht werden soll.', 'en_def': 'A specific, high-level target for risk mitigation to be achieved by controls.', 'meta': 'GoalKind'},
        'RV': {'de': 'NFRM-Risikovektor', 'en': 'NFRM Risk Vector', 'de_def': 'Eine definierte Kategorie von nicht-finanziellen Risiken, die die Erreichung von Zielen gefährdet.', 'en_def': 'A defined category of non-financial risk that threatens the achievement of goals.', 'meta': 'RiskKind'},
        'CTRL': {'de': 'ISO 27002 Kontrolle', 'en': 'ISO 27002 Control', 'de_def': 'Eine spezifische Aktivität oder Maßnahme zur Minderung eines Risikos.', 'en_def': 'A specific activity or measure performed to mitigate a risk.', 'meta': 'WorkUnitKind'},
        'EVD': {'de': 'Operativer Nachweis', 'en': 'Operational Evidence', 'de_def': 'Ein konkretes Artefakt (z.B. ein Bericht, Logfile), das als Beweis dient.', 'en_def': 'A concrete artifact (e.g., a report, log file) that serves as proof.', 'meta': 'WorkProductKind'},
        'EVD_P': {'de': 'Beweis (Abstrakt)', 'en': 'Evidence (Abstract)', 'de_def': 'Das abstrakte Konzept des Beweises, das durch ein operatives Artefakt verkörpert wird.', 'en_def': 'The abstract concept of proof that is embodied by an operational artifact.', 'meta': 'EvidenceKind'},
        'ASSURE': {'de': 'Assurance-Aktivität', 'en': 'Assurance Activity', 'de_def': 'Eine unabhängige Überprüfung (z.B. RCSA, Audit) zur Verifizierung der Kontrollwirksamkeit.', 'en_def': 'An independent review (e.g., RCSA, Audit) to verify control effectiveness.', 'meta': 'WorkUnitKind'},
        'RR': {'de': 'Restrisiko', 'en': 'Residual Risk', 'de_def': 'Das verbleibende Risiko nach Anwendung von Kontrollen, bewertet durch die Assurance-Aktivität.', 'en_def': 'The risk remaining after controls are applied, evaluated by the assurance activity.', 'meta': 'Risk'},
        'SO': {'de': 'Sign-Off / Akzeptanz', 'en': 'Sign-Off / Acceptance', 'de_def': 'Die formale Entscheidung über das Restrisiko durch den Risikoverantwortlichen.', 'en_def': 'The formal decision on residual risk made by the risk owner.', 'meta': 'OutcomeKind'},
        'MON': {'de': 'ICT Incident Monitoring', 'en': 'ICT Incident Monitoring', 'de_def': 'Ein konsumierender Prozess, der Daten aus dem Kernprozess zur kontinuierlichen Überwachung nutzt.', 'en_def': 'A consuming process that uses data from the core process for continuous monitoring.', 'meta': 'Consuming Process'}
    }

    # Formally compliant Mermaid diagram definition, structured according to the
    # ISO 27005 risk management lifecycle and using ISO/IEC 24744 compliant relationships.
    diagram = r"""
graph TD
    %% ISO 27001 / NFRM Process View v9.0 - ISO/IEC 24744 Compliant

    %% === SUBGRAPH 1: GOVERNANCE & CONTEXT ESTABLISHMENT (ISO 27001: 4, 6.1.2) ===
    %% This section defines the "why" and the "what could go wrong".
    subgraph "1. Governance & Context"
        direction TB
        CO
        RV
        style RV fill:#fee2e2, stroke:#fca5a5,color:#991b1b
    end

    %% === SUBGRAPH 2: RISK TREATMENT & EXECUTION (ISO 27001: 6.1.3, 8.3) ===
    %% This section defines the "what we do about it".
    subgraph "2. Risk Treatment & Execution"
        direction TB
        CTRL
    end

    %% === SUBGRAPH 3: EVIDENCE & ASSURANCE (ISO 27001: 9.1, 9.2) ===
    %% This section defines the verification and assurance loop.
    subgraph "3. Evidence & Assurance"
        direction LR
        EVD
        EVD_P(("<br/><b>Evidence</b><br/>(Abstract Proof)<br/><<Metamodel: EvidenceKind>>"))
        style EVD_P fill:#fefce8, stroke:#fde047,color:#854d0e, stroke-dasharray: 5 5
        ASSURE
    end

    %% === SUBGRAPH 4: OUTCOME & DECISION (ISO 27001: 9.3, 10) ===
    %% This section defines the management decision and feedback.
    subgraph "4. Outcome & Decision"
        direction TB
        RR
        style RR fill:#fee2e2, stroke:#fca5a5,color:#991b1b
        SO
    end

    %% === SUBGRAPH 5: CONTINUOUS MONITORING (Consuming Process) ===
    subgraph "Continuous Monitoring (e.g., DORA)"
        MON
    end

    %% === DEFINE RELATIONSHIPS (The Formal "Golden Thread") ===
    %% These relationships use the formal verbs from the ISO/IEC 24744 metamodel extension.

    %% The core Risk-Goal relationship. Corrects the original model's flawed logic.
    %% As per [1], a RiskKind (Risk Vector) "affects" a GoalKind (Control Objective).
    RV -- "affects" --> CO

    %% The Risk Treatment relationship.
    %% As per [1], a WorkUnitKind (Control) "mitigates" a RiskKind (Risk Vector).
    CTRL -- "mitigates" --> RV

    %% The Evidence Generation chain. This separates the artifact from the abstract proof.
    %% A WorkUnitKind (Control) "produces" a WorkProductKind (Operational Evidence).
    CTRL -- "produces" --> EVD
    %% A WorkProductKind (Operational Evidence) "embodies" an EvidenceKind (Abstract Proof).
    EVD -- "embodies" --> EVD_P

    %% The Assurance loop.
    %% The abstract EvidenceKind "supports" the GoalKind, closing the primary loop.
    EVD_P -- "supports" --> CO
    %% An Assurance Activity (WorkUnitKind) "verifies" the tangible WorkProductKind.
    ASSURE -- "verifies" --> EVD
    %% The Assurance Activity also evaluates the Residual Risk.
    ASSURE -- "evaluates" --> RR
    %% The Residual Risk "informs" the final OutcomeKind (Sign-Off).
    RR -- "informs" --> SO

    %% Informational Feeds to the parallel Monitoring Process.
    EVD -.->|provides data to| MON
    SO -.->|may trigger| MON

    %% === STYLING DEFINITIONS ===
    classDef goal fill:#e0e7ff, stroke:#a5b4fc,color:#3730a3, stroke-width:2px;
    classDef risk fill:#fee2e2, stroke:#fca5a5,color:#991b1b,stroke-width:2px;
    classDef workunit fill:#d1fae5, stroke:#86efac,color:#14532d,stroke-width:2px;
    classDef evidence fill:#fefce8, stroke:#fde047,color:#854d0e,stroke-width:2px;
    classDef assurance fill:#f3e8ff, stroke:#d8b4fe,color:#6b21a8,stroke-width:2px;
    classDef outcome fill:#e9d5ff, stroke:#c084fc,color:#581c87,stroke-width:2px;
    classDef monitoring fill:#e2e8f0, stroke:#64748b,color:#1e293b,stroke-width:2px;

    %% Apply styles to nodes
    class CO goal;
    class RV,RR risk;
    class CTRL,ASSURE workunit;
    class EVD,EVD_P evidence;
    class SO outcome;
    class MON monitoring;
    """

    tips_js = json.dumps(tips, indent=4)

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ISO 27001 / NFRM Process View (Formally Compliant Model)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #f8fafc; }}
       .mermaid svg {{ max-width: 100%; height: auto; }}
       .header-title {{ background: linear-gradient(45deg, #0033A0, #0055C7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
       .legend-item {{ display: flex; align-items: center; gap:.75rem; font-size:.875rem; }}
       .legend-swatch {{ width: 1.2rem; height: 1.2rem; border-radius:.25rem; border: 1px solid; }}
       .note {{ background-color: #f0f5ff; border-left: 4px solid #0055c7; padding: 1rem; margin-bottom: 2rem; border-radius:.25rem; }}
    </style>
</head>
<body class="p-6 md:p-8">
    <div class="max-w-7xl mx-auto bg-white p-8 md:p-12 rounded-2xl shadow-lg border border-gray-200">
        <header class="mb-8 text-center border-b pb-6">
            <h1 class="text-4xl font-bold header-title">ISO 27001 / NFRM Process View (Compliant Model v9.0)</h1>
            <p class="text-gray-600 mt-3">"Golden Thread" visualization aligned with the ISO/IEC 24744 formal metamodel</p>
        </header>

        <div class="note">
            <h3 class="font-bold text-lg text-gray-800">Model Interpretation Guide</h3>
            <p class="text-gray-700 mt-2">
                This diagram illustrates the <strong>formally compliant process flow</strong> for Non-Financial Risk Management under ISO 27001. It establishes an auditable "golden thread" from a high-level Control Objective down to the Operational Evidence that supports it. Each node and relationship corresponds to the canonical ISO/IEC 24744 metamodel, ensuring logical integrity and traceability. The model demonstrates a closed-loop assurance case where risks are mitigated by controls, and the effectiveness of those controls is verified by evidence, which in turn supports the achievement of the initial objective.
            </p>
        </div>

        <section class="mb-8 p-4 bg-gray-50 rounded-lg">
            <h3 class="font-semibold text-lg text-gray-800 mb-4">Legend (Mapping to Formal Metamodel)</h3>
            <div class="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-x-6 gap-y-3 text-gray-700">
                <div class="legend-item"><span class="legend-swatch" style="background:#e0e7ff;border-color:#a5b4fc"></span><div><strong>GoalKind</strong></div></div>
                <div class="legend-item"><span class="legend-swatch" style="background:#fee2e2;border-color:#fca5a5"></span><div><strong>Risk / RiskKind</strong></div></div>
                <div class="legend-item"><span class="legend-swatch" style="background:#d1fae5;border-color:#86efac"></span><div><strong>WorkUnitKind</strong></div></div>
                <div class="legend-item"><span class="legend-swatch" style="background:#fefce8;border-color:#fde047"></span><div><strong>WorkProduct / Evidence</strong></div></div>
                <div class="legend-item"><span class="legend-swatch" style="background:#e9d5ff;border-color:#c084fc"></span><div><strong>OutcomeKind</strong></div></div>
                <div class="legend-item"><span class="legend-swatch" style="background:#e2e8f0;border-color:#64748b"></span><div><strong>Consuming Process</strong></div></div>
            </div>
        </section>

        <div class="bg-gray-50 p-4 rounded-xl overflow-auto" id="uml-container">
            <pre class="mermaid" id="uml-diagram"></pre>
        </div>

        <footer class="mt-8 text-center text-sm text-gray-500">
            Hover over nodes to see bilingual tooltips with definitions and metamodel types.
        </footer>
    </div>

    <script>
        const tips = {tips_js};
        const diagram = `{diagram}`.trim();

        document.addEventListener('DOMContentLoaded', async () => {{
            try {{
                mermaid.initialize({{ startOnLoad: false, securityLevel: 'strict' }});
                const umlDiagramElement = document.getElementById('uml-diagram');
                umlDiagramElement.textContent = diagram;
                // Corrected the line below to pass the element to mermaid.run()
                await mermaid.run({{ nodes: [umlDiagramElement] }});

                const container = document.getElementById('uml-container');
                for (const [id, t] of Object.entries(tips)) {{
                    const node = container.querySelector(`.node[data-id="${{id}}"]`);
                    if (node) {{
                        const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
                        let tooltipText = ` ${{t.de}}: ${{t.de_def}}\\n`;
                        tooltipText += `[EN] ${{t.en}}: ${{t.en_def}}\\n\\n`;
                        tooltipText += `[Metamodel: ${{t.meta}}]`;
                        title.textContent = tooltipText;
                        node.appendChild(title);
                    }} else {{
                        console.warn(`Could not find node with data-id: ${{id}} to attach tooltip.`);
                    }}
                }}
            }} catch (error) {{
                console.error('Mermaid rendering failed:', error);
                const target = document.getElementById('uml-container');
                if(target) {{
                    target.innerHTML = `<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">Error: Diagram could not be rendered. Check console for details.</div>`;
                }}
            }}
        }});
    </script>
</body>
</html>
    """
    return html_content

if __name__ == "__main__":
    html_output = generate_iso27001_nfrm_html()
    output_filename = "compliant_iso27001_nfrm_process_view_fixed.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"HTML file '{output_filename}' generated successfully.")