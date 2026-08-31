#!/usr/bin/env python3
"""Optional zero-dependency validator for FrameCode VibeWork."""

from __future__ import annotations

import argparse
import unicodedata
import os
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from document_graph_fcvw import build_graph, render_catalog
from fcvw_cache import frontmatter as cache_frontmatter, read_text as cache_read_text
from frontmatter_fcvw import FrontmatterValue, parse_frontmatter, scalar, string_list
from knowledge_graph_fcvw import build_knowledge_graph
from plan_queue_fcvw import validate_plan_queues
from release_layout_fcvw import is_installed_release_layout

from urllib.parse import unquote


REQUIRED_PATHS = (
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "NOTICE",
    "tools/validate_fcvw.py",
    "tools/test_validate_fcvw.py",
    "tools/test_open_issues.py",
    "tools/test_plan_dependencies_and_knowledge.py",
    "tools/frontmatter_fcvw.py",
    "tools/document_graph_fcvw.py",
    "tools/knowledge_graph_fcvw.py",
    "tools/knowledge_sources_fcvw.py",
    "tools/plan_dependencies_fcvw.py",
    "tools/plan_queue_fcvw.py",
    "tools/build_context_index.py",
    "tools/retrieve_context.py",
    "tools/locale_fcvw.py",
    "tools/package_release_fcvw.py",
    "tools/release_layout_fcvw.py",
    "tools/fcvw_cache.py",
    "tools/role_manifest_fcvw.py",
    "tools/upgrade_fcvw.py",
    "FCVW/README.md",
    "FCVW/APP_RULES.md",
    "FCVW/DOCUMENT_GRAPH.md",
    "FCVW/Plans/pending/QUEUE.md",
    "FCVW/Plans/in_progress/QUEUE.md",
    "FCVW/FRAMEWORK_LOCK.md",
    "FCVW/OWNERSHIP.md",
    "FCVW/SCHEMAS.md",
    "FCVW/MIGRATIONS.md",
    "FCVW/PLANNING.md",
    "FCVW/CONTEXT_MAP.md",
    "FCVW/VERSIONING.md",
    "FCVW/RELEASE.md",
    "FCVW/MEMORY.md",
    "FCVW/AUTOMATION.md",
    "FCVW/REGRESSION_GUARDS.md",
    "FCVW/FILESYSTEM.md",
    "FCVW/governance/TEMPLATE_PLAN.md",
    "FCVW/governance/TEMPLATE_PLAN_COMPACT.md",
    "FCVW/governance/TEMPLATE_CI_WORKFLOW.md",
    "FCVW/governance/TEMPLATE_AUDIT.md",
    "FCVW/framework-releases/README.md",
    "FCVW/examples/minimal-change/README.md",
    "FCVW/skills/README.md",
    "FCVW/wiki/regressions/README.md",
    "FCVW/wiki/feedback/README.md",
    "FCVW/wiki/templates/TEMPLATE_FEEDBACK.md",
    "FCVW/wiki/templates/TEMPLATE_REGRESSION.md",
)

# A project rarely has every concern on day one. Without a third state the only
# way to pass `--profile instantiated` is to invent content for profiles the
# project does not use yet, so the validator would be measuring fiction.
INSTANTIATION_STATUSES = {"pending", "complete", "not_applicable"}
# Identity and scope always apply: a project always has a name and a boundary.
INSTANTIATION_REQUIRED_PROFILES = {"MANIFEST.md", "SCOPE.md"}
MINIMUM_INSTANTIATION_REASON = 40

PROJECT_PROFILES = (
    "BRIEFING.md",
    "DATA.md",
    "APP_RULES.md",
    "DESIGN.md",
    "ENVIRONMENT.md",
    "MANIFEST.md",
    "PERFORMANCE.md",
    "SCOPE.md",
    "SECURITY.md",
    "STACK.md",
    "WORKFLOW.md",
)

PLAN_FIELDS = (
    "id",
    "status",
    "priority",
    "risk",
    "created_at",
    "updated_at",
    "current_version",
    "expected_version",
    "owner",
    "context_files",
)

PLAN2_FIELDS = PLAN_FIELDS + ("regression_contract",)
COMPACT_PLAN_SCHEMA = "fcvw/plan-compact@1"
# A compact plan is the proportional form promised by PLANNING.md: identity,
# objective, affected files, validation and rollback. It is deliberately
# restricted so it can never absorb work that needs a regression contract.
COMPACT_PLAN_FIELDS = (
    "id",
    "status",
    "priority",
    "risk",
    "created_at",
    "updated_at",
    "owner",
    "context_files",
)
COMPACT_PLAN_SECTIONS = ("Objective", "Affected files", "Validation", "Rollback")
COMPACT_PLAN_PRIORITIES = {"P4", "P5"}
COMPACT_PLAN_RISKS = {"R1"}
PLAN_SCHEMAS = {"fcvw/plan@1", "fcvw/plan@2", COMPACT_PLAN_SCHEMA}
# Risk classes that may never waive the regression contract. REGRESSION_GUARDS.md
# and TESTS.md already say so in prose; this makes it machine-enforced.
REGRESSION_REQUIRED_RISKS = {"R3", "R4", "R5"}
SENSITIVE_CONTEXT_FILES = ("SECURITY.md", "DATA.md", "MIGRATIONS.md")
GENERIC_JUSTIFICATIONS = (
    "nao se aplica",
    "not applicable",
    "no aplica",
    "nicht zutreffend",
    "documentation only",
    "apenas documentacao",
    "solo documentacion",
    "nur dokumentation",
    "trivial",
    "sem impacto",
    "no impact",
)
MINIMUM_JUSTIFICATION = 40
INVISIBLE_CHARACTERS = {
    "\u200b": "zero-width space",
    "\u200c": "zero-width non-joiner",
    "\u200d": "zero-width joiner",
    "\u00a0": "non-breaking space",
    "\ufffd": "replacement character",
}
MANGLED_DASH = re.compile(r"(?<=\w)\s\?\s(?=\w)")
LANGUAGE_DISPLAY_FORMS = {
    "pt-BR": ("pt-br", "portuguese", "portugues", "brasil", "brazil"),
    "en-US": ("en-us", "english", "ingles", "united states"),
    "es": ("es", "spanish", "espanol", "castellano"),
    "de": ("de", "german", "deutsch", "alemao"),
}
PLAN_PRIORITIES = {f"P{index}" for index in range(1, 6)}
PLAN_RISKS = {f"R{index}" for index in range(1, 6)}
REGRESSION_CONTRACTS = {"required", "not_applicable"}
REGRESSION_MARKERS = (
    "### Existing behaviors that may be affected",
    "### Regression contracts consulted",
    "### Regression checks required",
    "### Regression evidence",
    "### Limitations and residual risk",
)
WIKI_TYPES = {
    "concept",
    "feedback",
    "decision",
    "pattern",
    "failure",
    "regression",
    "refactoring",
    "audit",
    "agent",
    "release",
    "session",
    "component",
    "prompt",
    "question",
    "synthesis",
    "source",
    "raw",
}
# Feedback about the framework itself is deliberately append-only and attributed.
# Two models may reach opposite conclusions about the same topic, and the value of
# the surface is that both survive; consolidating them would destroy the evidence
# the maintainer needs. This is the one wiki surface where updating a prior page
# is forbidden rather than preferred - see FCVW/wiki/agents/README.md for the
# opposite rule and why the difference is deliberate.
FEEDBACK_STATUSES = {"open", "accepted", "declined", "applied", "superseded"}
FEEDBACK_FIELDS = ("authored_by_model", "topic", "feedback_status")
FEEDBACK_SUGGESTION_TITLE = "Suggestion"
FEEDBACK_ASSESSMENT_TITLE = "Assessment of prior notes"

WIKI_STATUSES = {"draft", "in_validation", "validated", "obsolete", "superseded", "contradictory"}
WIKI_CONFIDENCE = {"low", "medium", "high"}
REGRESSION_TYPES = {
    "functional",
    "interface",
    "data",
    "visual",
    "security",
    "ai",
    "governance",
    "documentation",
    "performance",
    "operations",
}
REGRESSION_STATUSES = {"detected", "mitigated", "resolved", "accepted", "superseded"}
FORBIDDEN_ROOT_ENTRIES = ("FCVW - Exemplo retirado de aplicação real",)
CLEAN_ROOT_ENTRIES = {
    ".cursorrules",
    ".git",
    ".gitattributes",
    ".github",
    ".gitignore",
    ".obsidian",
    ".windsurfrules",
    "AGENTS.md",
    "FCVW",
    "LICENSE",
    "NOTICE",
    "README.md",
    "tools",
}

SKILL_FIELDS = (
    "schema",
    "name",
    "description",
    "version",
    "trigger_keywords",
    "session_types",
)

SKILL_BODY_HEADINGS = {
    "purpose": ("## purpose",),
    "use conditions": ("## use conditions", "## use when", "## activation triggers", "## profiles", "## modes"),
    "non-responsibilities": (
        "## non-responsibilities",
        "## boundaries",
        "## block conditions",
        "## hard rules",
        "## non-negotiable rules",
        "## forbidden patterns",
        "## do not use for",
    ),
    "inputs": ("## inputs", "## mandatory source of truth", "## scan order", "## audit order", "## inspect order"),
    "procedure": (
        "## procedure",
        "## workflow",
        "## execution checklist",
        "## safe improvement sequence",
        "## curation loop",
        "## cleanup sequence",
        "## checks",
        "## core directives",
        "## decision ladder",
        "## hard gates",
        "## hygiene scan",
        "## fixed cost mode",
        "## scan order",
        "## audit order",
        "## inspect order",
    ),
    "required output": ("## required output", "## output required"),
    "validation": ("## validation", "## validation and exit", "## exit criteria", "## metrics", "## creation gate", "## improvement gate", "## hard gates"),
    "exit criteria": ("## exit criteria", "## validation and exit", "## definition of done", "## post-release checklist"),
}

SKILL_BODY_TRANSLATIONS = {
    "purpose": ("## objetivo", "## proposito", "## zweck"),
    "use conditions": (
        "## activadores de activacion",
        "## aktivierungsausloser",
        "## condiciones de uso",
        "## condicoes de uso",
        "## gatilhos de ativacao",
        "## modi",
        "## modos",
        "## nutzungsbedingungen",
        "## perfiles",
        "## perfis",
        "## profile",
        "## usar cuando",
        "## use quando",
        "## verwenden sie wann",
        "## quando usar",
        "## wann verwenden",
    ),
    "non-responsibilities": (
        "## blockbedingungen",
        "## condiciones de bloqueo",
        "## condicoes de bloqueio",
        "## grenzen",
        "## harte regeln",
        "## keine verantwortung",
        "## limites",
        "## nao responsabilidades",
        "## nao use para",
        "## nicht verwenden fur",
        "## nicht-verantwortlichkeiten",
        "## no responsabilidades",
        "## no utilizar para",
        "## padroes proibidos",
        "## patrones prohibidos",
        "## reglas estrictas",
        "## reglas no negociables",
        "## regras nao negociaveis",
        "## regras rigidas",
        "## unverhandelbare regeln",
        "## verbotene muster",
    ),
    "inputs": (
        "## bestellung prufen",
        "## eingaben",
        "## entradas",
        "## fonte obrigatoria da verdade",
        "## fuente obligatoria de la verdad",
        "## inspeccionar orden",
        "## inspecionar pedido",
        "## obligatorische quelle der wahrheit",
        "## ordem de auditoria",
        "## ordem de digitalizacao",
        "## orden de auditoria",
        "## orden de escaneo",
        "## prufauftrag",
        "## scanreihenfolge",
    ),
    "procedure": (
        "## arbeitsablauf",
        "## aufraumsequenz",
        "## ausfuhrungscheckliste",
        "## bestellung prufen",
        "## bucle de curacion",
        "## cheques",
        "## ciclo de curadoria",
        "## entscheidungsleiter",
        "## escada de decisao",
        "## escalera de decision",
        "## escaneo de higiene",
        "## fixkostenmodus",
        "## flujo de trabajo",
        "## fluxo de trabalho",
        "## harte tore",
        "## hygiene-scan",
        "## inspeccionar orden",
        "## inspecionar pedido",
        "## kurationsschleife",
        "## lista de verificacao de execucao",
        "## lista de verificacion de ejecucion",
        "## modo de costo fijo",
        "## modo de custo fixo",
        "## ordem de auditoria",
        "## ordem de digitalizacao",
        "## orden de auditoria",
        "## orden de escaneo",
        "## portoes rigidos",
        "## procedimento",
        "## procedimiento",
        "## prufauftrag",
        "## puertas duras",
        "## scanreihenfolge",
        "## schecks",
        "## secuencia de limpieza",
        "## secuencia de mejora segura",
        "## sequencia de limpeza",
        "## sequencia de melhoria segura",
        "## sichere verbesserungssequenz",
        "## verificacao de higiene",
        "## verificacoes",
        "## vorgehensweise",
    ),
    "required output": (
        "## ausgabe erforderlich",
        "## erforderliche ausgabe",
        "## saida necessaria",
        "## salida requerida",
    ),
    "validation": (
        "## criterios de saida",
        "## criterios de salida",
        "## exit-kriterien",
        "## harte tore",
        "## metricas",
        "## metriken",
        "## portao de criacao",
        "## portao de melhoria",
        "## portoes rigidos",
        "## puerta de la creacion",
        "## puerta de mejora",
        "## puertas duras",
        "## schopfungstor",
        "## validacao",
        "## validacao e saida",
        "## validacion",
        "## validacion y salida",
        "## validierung",
        "## validierung und beenden",
        "## verbesserungstor",
    ),
    "exit criteria": (
        "## criterios de saida",
        "## criterios de salida",
        "## exit-kriterien",
        "## validacao e saida",
        "## validacion y salida",
        "## validierung und beenden",
    ),
}

LOCALIZED_TITLES = {
    "objective": {"objetivo", "ziel"},
    "affected files": {
        "arquivos afetados",
        "archivos afectados",
        "betroffene dateien",
        "affected files or boundaries",
        "arquivos ou limites afetados",
    },
    "validation": {"validacao", "validacion", "validierung", "validation plan", "plano de validacao"},
    "rollback": {"reversao", "reversion", "rueckabwicklung", "zuruckrollen"},
    "regression guardrails": {
        "protetores de regressao",
        "barandillas de regresion",
        "regressionsleitplanken",
    },
    "minimum regression evidence by risk": {
        "evidencia minima de regressao por risco",
        "evidencia minima de regresion por riesgo",
        "minimale regressionsnachweise nach risikoklasse",
    },
    "regression-prone events": {
        "eventos propensos a regressao",
        "eventos propensos a la regresion",
        "regressionsanfallige ereignisse",
    },
    "regression": {"regressao", "regresion"},
    "regression impact": {"impacto da regressao", "impacto de la regresion", "regressionsauswirkung"},
    "existing behaviors that may be affected": {
        "comportamentos existentes que podem ser afetados",
        "comportamientos existentes que pueden verse afectados",
        "bestehende verhaltensweisen, die moglicherweise betroffen sind",
    },
    "regression contracts consulted": {
        "contratos de regressao consultados",
        "contratos de regresion consultados",
        "regressionsvertrage konsultiert",
    },
    "regression checks required": {
        "verificacoes de regressao necessarias",
        "se requieren comprobaciones de regresion",
        "regressionsprufungen erforderlich",
    },
    "regression evidence": {"evidencia de regressao", "evidencia de regresion", "regressionsbeweise"},
    "justification": {"justificativa", "justificacion", "begrundung"},
    "summary": {"resumo", "resumen", "zusammenfassung"},
    "related framework plans": {
        "planos de estrutura relacionados",
        "planes marco relacionados",
        "verwandte rahmenplane",
    },
    "framework surfaces added": {
        "superficies de estrutura adicionadas",
        "se agregaron superficies de marco",
        "gerustflachen hinzugefugt",
    },
    "framework surfaces changed": {
        "superficies da estrutura alteradas",
        "las superficies del marco cambiaron",
        "gerustoberflachen geandert",
    },
    "framework surfaces removed": {
        "superficies da estrutura removidas",
        "superficies de estructura eliminadas",
        "gerustflachen entfernt",
    },
    "ownership and path changes": {
        "mudancas de propriedade e caminho",
        "cambios de propiedad y ruta",
        "eigentumer- und pfadanderungen",
    },
    "schema changes": {"mudancas de esquema", "cambios de esquema", "schemaanderungen"},
    "migration": {"migracao", "migracion"},
    "validation": {"validacao", "validacion", "validierung"},
    "language-variant parity and review evidence": {
        "paridade entre variantes de idioma e evidencias de revisao",
        "paridad de variantes linguisticas y evidencia de revision",
        "sprachvariantenparitat und uberprufungsnachweise",
    },
    "locale parity and language-review evidence": {
        "paridade de localidade e evidencias de revisao linguistica",
        "paridade de localidade e evidencias de revisao de idioma",
        "paridad regional y evidencia de revision linguistica",
        "paridad local y evidencia de revision de idioma",
        "gebietsschemaparitat und sprachprufungsnachweise",
        "lokale paritat und sprachuberprufungsnachweise",
    },
    "clean assets and package contents": {
        "limpe ativos e conteudo do pacote",
        "limpiar activos y contenido del paquete",
        "bereinigen sie assets und paketinhalte",
    },
    "checksums": {"somas de verificacao", "sumas de verificacion", "prufsummen"},
    "downstream preservation rules": {
        "regras de preservacao downstream",
        "reglas de preservacion posteriores",
        "nachgelagerte aufbewahrungsregeln",
    },
    "known gaps": {"lacunas conhecidas", "brechas conocidas", "bekannte lucken"},
    "rollback": {"reversao", "revertir"},
    "publication evidence": {
        "evidencia de publicacao",
        "prueba de publicacion",
        "veroffentlichungsnachweise",
    },
    "affected areas": {"areas afetadas", "areas afectadas", "betroffene gebiete"},
    "added": {"adicionado", "adicionados", "agregado", "agregados", "hinzugefugt"},
    "changed": {"alterado", "alterados", "cambiado", "cambiados", "geandert"},
    "fixed": {"corrigido", "corrigidos", "corregido", "corregidos", "behoben"},
    "removed": {"removido", "removidos", "eliminado", "eliminados", "entfernt"},
    "assets and package contents": {
        "ativos e conteudo do pacote",
        "activos y contenido del paquete",
        "assets und paketinhalte",
    },
    "security and data impact": {
        "impacto de seguranca e dados",
        "impacto en seguridad y datos",
        "sicherheits- und datenauswirkungen",
    },
    "post-release validation": {
        "validacao pos-release",
        "validacion posterior a la publicacion",
        "validierung nach der veroffentlichung",
    },
    "scope": {"escopo", "alcance", "geltungsbereich"},
    "authoritative sources": {"fontes autorizadas", "fuentes autorizadas", "massgebliche quellen"},
    "method": {"metodo", "methode"},
    "findings": {"achados", "hallazgos", "befunde"},
    "limitations and residual risk": {
        "limitacoes e risco residual",
        "limitaciones y riesgo residual",
        "einschrankungen und restrisiko",
    },
    "follow-up": {"acompanhamento", "seguimiento", "nachverfolgung"},
}

PROVIDER_TERMS = (
    "IsSkillFile",
    "view_file",
    "AlmogBaku",
    "Superpowers methodology",
    "Spartan AI Toolkit",
)
PLAN_ID = re.compile(r"^P[1-5]-R[1-5]-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")
PLACEHOLDER = re.compile(r"<[A-Za-z][^>\n]*>")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE = re.compile(r"`[^`]*`")
LOCAL_RELATIONSHIP_FIELDS = (
    "context_files",
    "sources",
    "related_plan",
    "related_release",
    "related",
    "depends_on",
    "supports",
    "contradicts",
    "implements",
    "derived_from",
    "invalidates",
    "supersedes",
    "superseded_by",
    "canonical_page",
    "source_path",
)
FRAMEWORK_RELEASE_FIELDS = (
    "version",
    "artifact_role",
    "owner",
    "upgrade_strategy",
    "record_scope",
    "date",
    "release_status",
    "release_type",
    "compatibility",
    "source_revision",
    "publication_revision",
    "release_languages",
    "related_plans",
)
FRAMEWORK_RELEASE_SECTIONS = (
    "Summary",
    "Related framework plans",
    "Framework surfaces added",
    "Framework surfaces changed",
    "Framework surfaces removed",
    "Ownership and path changes",
    "Schema changes",
    "Migration",
    "Validation",
    "Language-variant parity and review evidence",
    "Clean assets and package contents",
    "Checksums",
    "Downstream preservation rules",
    "Known gaps",
    "Rollback",
    "Publication evidence",
)
FRAMEWORK_RELEASE_SECTION_ALIASES = {
    "Language-variant parity and review evidence": ("Locale parity and language-review evidence",),
}
FRAMEWORK_RELEASE_LANGUAGES = {"pt-BR", "en-US", "es", "de"}


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class BaselineEntry:
    path: str
    rule: str
    message: str
    justification: str
    owner: str
    review_due: date


def read_text(path: Path) -> str:
    return cache_read_text(path)


def normalized_title(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFKD", value.casefold())
        if not unicodedata.combining(character)
    ).strip()


def title_aliases(title: str) -> set[str]:
    canonical = normalized_title(title)
    return {canonical, *LOCALIZED_TITLES.get(canonical, set())}


def has_localized_heading(text: str, level: int, title: str, *, include_fences: bool = False) -> bool:
    prefix = "#" * level + " "
    accepted = title_aliases(title)
    lines = enumerate(text.splitlines(), 1) if include_fences else outside_code_fences(text)
    return any(
        line.strip().startswith(prefix)
        and normalized_title(line.strip()[len(prefix) :]) in accepted
        for _, line in lines
    )


def frontmatter(text: str) -> dict[str, FrontmatterValue]:
    return parse_frontmatter(text).data


def frontmatter_of(path: Path) -> dict[str, FrontmatterValue]:
    """Frontmatter for one path, parsed at most once per run."""

    return cache_frontmatter(path)


def normalized_finding_path(value: str) -> str:
    return value.strip().replace("\\", "/").removeprefix("./")


def load_legacy_baseline(path: Path) -> tuple[list[BaselineEntry], list[Finding]]:
    """Load a time-bounded exact-match baseline from the documented Markdown format."""
    label = path.as_posix()
    if not path.is_file():
        return [], [Finding("baseline-config", label, "baseline file is missing")]

    text = read_text(path)
    metadata = frontmatter(text)
    errors: list[Finding] = []
    if scalar(metadata, "schema") != "fcvw/legacy-baseline@1":
        errors.append(Finding("baseline-config", label, "invalid or missing baseline schema"))
    for field in ("created_at", "review_due", "owner"):
        if not scalar(metadata, field):
            errors.append(Finding("baseline-config", label, f"missing baseline metadata: {field}"))

    for field in ("created_at", "review_due"):
        value = scalar(metadata, field)
        if not value:
            continue
        try:
            parsed = date.fromisoformat(value)
        except ValueError:
            errors.append(Finding("baseline-config", label, f"invalid ISO date in {field}: {value}"))
            continue
        if field == "review_due" and parsed < date.today():
            errors.append(Finding("baseline-expired", label, f"baseline review expired on {value}"))

    entries: list[BaselineEntry] = []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if not cells or cells[0] == "Exact path" or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if len(cells) != 6 or not any(cells):
            errors.append(Finding("baseline-config", label, f"invalid baseline row at line {number}"))
            continue
        exact_path, rule, message, justification, owner, review_due = cells
        if not all((exact_path, rule, message, justification, owner, review_due)):
            errors.append(Finding("baseline-config", label, f"incomplete baseline row at line {number}"))
            continue
        try:
            due = date.fromisoformat(review_due)
        except ValueError:
            errors.append(Finding("baseline-config", label, f"invalid row review date at line {number}: {review_due}"))
            continue
        if due < date.today():
            errors.append(Finding("baseline-expired", label, f"row review expired at line {number} on {review_due}"))
            continue
        entries.append(
            BaselineEntry(
                path=normalized_finding_path(exact_path),
                rule=rule,
                message=message,
                justification=justification,
                owner=owner,
                review_due=due,
            )
        )

    if not entries:
        errors.append(Finding("baseline-config", label, "baseline has no valid exact findings"))
    return entries, errors


def apply_legacy_baseline(
    findings: list[Finding], entries: list[BaselineEntry]
) -> tuple[list[Finding], list[Finding], list[Finding]]:
    """Return blocking findings, accepted exact matches, and stale baseline warnings."""
    entry_keys = {(entry.path, entry.rule, entry.message) for entry in entries}
    matched: set[tuple[str, str, str]] = set()
    blocking: list[Finding] = []
    accepted: list[Finding] = []
    for finding in findings:
        key = (normalized_finding_path(finding.path), finding.rule, finding.message)
        if (
            finding.severity == "error"
            and finding.rule not in {"baseline-config", "baseline-expired"}
            and key in entry_keys
        ):
            accepted.append(finding)
            matched.add(key)
        else:
            blocking.append(finding)
    stale = [
        Finding(
            "baseline-stale",
            entry.path,
            f"baseline entry no longer matches an active finding: [{entry.rule}] {entry.message}",
            severity="warning",
        )
        for entry in entries
        if (entry.path, entry.rule, entry.message) not in matched
    ]
    return blocking, accepted, stale


def outside_code_fences(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    marker = ""
    for number, line in enumerate(text.splitlines(), 1):
        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
            continue
        if not marker:
            lines.append((number, line))
    return lines


def markdown_files(root: Path, scope: set[str] | None = None) -> list[Path]:
    """Governed Markdown, optionally narrowed to a changed-path scope.

    Only rules whose verdict depends on a single file may be scoped. Anything
    that compares files with each other - identifier uniqueness, the document
    graph, the queues, release surfaces - keeps reading the whole tree, so a
    scoped run still fails when the repository as a whole is inconsistent.
    """

    paths = sorted((root / "FCVW").rglob("*.md"), key=lambda item: item.as_posix().lower())
    if scope is None:
        return paths
    return [path for path in paths if path.relative_to(root).as_posix() in scope]


AUTOMATION_SCHEMA = "fcvw/automation@1"
AUTOMATION_FIELDS = (
    "id",
    "kind",
    "status",
    "trigger",
    "preconditions",
    "actions",
    "evidence",
    "failure_policy",
    "rollback",
    "owner",
)
AUTOMATION_KINDS = {"hook", "watcher", "daemon", "governance_gate"}
AUTOMATION_STATUSES = {"draft", "active", "paused", "retired"}
AUTOMATION_SCENARIOS = {"1", "2", "3"}


def validate_automation(root: Path, findings: list[Finding], scope: set[str] | None = None) -> None:
    """Validate declared automation contracts.

    `fcvw/automation@1` was the only schema in SCHEMAS.md with required fields and
    no machine check at all, which meant a hook, watcher, daemon or gate could
    claim a lifecycle it never declared. Contracts are found by schema rather than
    by directory so a project can keep them wherever its documentation lives.
    """

    for path in markdown_files(root, scope):
        relative = path.relative_to(root).as_posix()
        if path.name.startswith("TEMPLATE_"):
            continue
        metadata = frontmatter_of(path)
        if scalar(metadata, "schema") != AUTOMATION_SCHEMA:
            continue
        for field in AUTOMATION_FIELDS:
            if field not in metadata:
                findings.append(Finding("automation-contract", relative, f"missing field: {field}"))
            elif not str(metadata[field]).strip():
                findings.append(Finding("automation-contract", relative, f"field must not be empty: {field}"))
        kind = scalar(metadata, "kind")
        if kind and kind not in AUTOMATION_KINDS:
            findings.append(
                Finding("automation-contract", relative, f"invalid kind: {kind!r}; expected one of {sorted(AUTOMATION_KINDS)}")
            )
        status = scalar(metadata, "status")
        if status and status not in AUTOMATION_STATUSES:
            findings.append(
                Finding("automation-contract", relative, f"invalid status: {status!r}; expected one of {sorted(AUTOMATION_STATUSES)}")
            )
        scenario = scalar(metadata, "scenario")
        if scenario and scenario not in AUTOMATION_SCENARIOS:
            findings.append(
                Finding("automation-contract", relative, f"invalid scenario: {scenario!r}; expected 1, 2, or 3")
            )
        # AUTOMATION.md: an executable contract needs named authority, because a
        # Markdown contract never proves that anything ran.
        if scenario in {"2", "3"} and not scalar(metadata, "authorized_by"):
            findings.append(
                Finding(
                    "automation-contract",
                    relative,
                    f"scenario {scenario} automation requires an explicit authorized_by",
                )
            )


def validate_character_integrity(root: Path, findings: list[Finding], scope: set[str] | None = None) -> None:
    """Catch invisible and transcoding-damaged characters in governed Markdown.

    Release variants are produced by transcoding and translation passes, which
    is exactly where em dashes decay into literal question marks and zero-width
    characters accumulate. Neither is visible in review, so only a machine check
    finds them.
    """

    for path in markdown_files(root, scope):
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        for character, label in INVISIBLE_CHARACTERS.items():
            count = text.count(character)
            if count:
                findings.append(
                    Finding(
                        "character-integrity",
                        relative,
                        f"{count} invisible or damaged character(s): {label} (U+{ord(character):04X})",
                    )
                )
        for line_number, line in outside_code_fences(text):
            if MANGLED_DASH.search(line):
                findings.append(
                    Finding(
                        "character-integrity",
                        relative,
                        f"line {line_number}: isolated '?' between words is a damaged dash or accent",
                    )
                )


def validate_language_review(root: Path, findings: list[Finding]) -> None:
    """Require the language-review record to name the language it declares.

    The record is the gate that authorises a language-specific release asset, so
    a body copied from another variant silently certifies the wrong language.
    """

    path = root / "FCVW" / "LANGUAGE_REVIEW.md"
    if not path.is_file():
        return
    relative = path.relative_to(root).as_posix()
    text = read_text(path)
    declared = scalar(frontmatter(text), "language")
    if declared not in LANGUAGE_DISPLAY_FORMS:
        findings.append(Finding("language-review", relative, f"unsupported declared language: {declared!r}"))
        return
    heading = next(
        (line[2:] for _, line in outside_code_fences(text) if line.startswith("# ")),
        "",
    )
    scope = level_two_section(text, "Scope") or ""
    body = normalized_title(heading + " " + scope)
    if not any(form in body for form in LANGUAGE_DISPLAY_FORMS[declared]):
        findings.append(
            Finding(
                "language-review",
                relative,
                f"title and scope must name the declared language {declared!r}",
            )
        )
    for other, forms in LANGUAGE_DISPLAY_FORMS.items():
        if other == declared:
            continue
        matched = [form for form in forms if len(form) > 3 and form in body]
        if matched:
            findings.append(
                Finding(
                    "language-review",
                    relative,
                    f"declares {declared!r} but title/scope describes {other!r} ({matched[0]!r})",
                )
            )


REPOSITORY_WIDE_RULES = {
    "required-path",
    "clean-root",
    "clean-contamination",
    "document-catalog-stale",
    "plan-queue",
    "queue",
    "version",
    "framework-release",
    "application-release",
    "language-review",
    "baseline-config",
    "reading-route",
    "skill-catalog",
    "duplicate-id",
}


def changed_markdown_since(root: Path, revision: str) -> tuple[set[str], Finding | None]:
    """List governed Markdown changed since a git revision.

    Scoping the report is about signal, not speed: repository-wide rules always
    run, so a scoped run still fails when the tree as a whole is inconsistent.
    """

    import subprocess

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", revision, "--", "*.md"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return set(), Finding("scope-config", str(root), f"--since could not run git: {error}")
    if result.returncode != 0:
        message = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "unknown git error"
        return set(), Finding("scope-config", revision, f"--since is not a usable git revision: {message}")
    return {normalized_finding_path(line) for line in result.stdout.splitlines() if line.strip()}, None


def validate_required(root: Path, findings: list[Finding]) -> None:
    installed = is_installed_release_layout(root)
    for relative in REQUIRED_PATHS:
        expected = relative
        if installed:
            if relative == "README.md":
                continue
            if relative in {"LICENSE", "NOTICE"} or relative.startswith("tools/"):
                expected = f"FCVW/{relative}"
        if not (root / expected).is_file():
            findings.append(Finding("required-path", expected, "required path is missing"))


def validate_canonical_metadata(root: Path, findings: list[Finding], scope: set[str] | None = None) -> None:
    for path in sorted((root / "FCVW").glob("*.md")):
        relative = path.relative_to(root).as_posix()
        if scope is not None and relative not in scope:
            continue
        metadata = frontmatter_of(path)
        for field in ("schema", "artifact_role", "owner", "upgrade_strategy"):
            if field not in metadata:
                findings.append(Finding("canonical-metadata", relative, f"missing field: {field}"))


def validate_markdown(root: Path, findings: list[Finding], scope: set[str] | None = None) -> None:
    for path in markdown_files(root, scope):
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        marker = ""
        for line in text.splitlines():
            fence = re.match(r"^\s*(`{3,}|~{3,})", line)
            if not fence:
                continue
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
        if marker:
            findings.append(Finding("markdown-fence", relative, f"unclosed Markdown fence: {marker}"))
        for line_number, line in outside_code_fences(text):
            code_ranges = [match.span() for match in INLINE_CODE.finditer(line)]
            for match in MARKDOWN_LINK.finditer(line):
                if any(start <= match.start() and match.end() <= end for start, end in code_ranges):
                    continue
                raw_target = match.group(1).strip()
                if raw_target.startswith("<") and ">" in raw_target:
                    target = raw_target[1:raw_target.find(">")]
                else:
                    target = raw_target.split(maxsplit=1)[0]
                target = target.split("#", 1)[0]
                if not target or target.startswith("#"):
                    continue
                target = unquote(target)
                if target.startswith("/") or re.match(r"^[A-Za-z]:[/\\]", target):
                    findings.append(
                        Finding(
                            "markdown-link-absolute",
                            relative,
                            f"line {line_number}: Markdown links must be source-relative: {target}",
                        )
                    )
                    continue
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue
                candidate = path.parent / target
                if not candidate.exists():
                    findings.append(
                        Finding("markdown-link", relative, f"line {line_number}: missing target: {target}")
                    )


def level_two_section(text: str, title: str) -> str | None:
    lines = text.splitlines()
    start: int | None = None
    body: list[str] = []
    marker = ""
    next_heading = re.compile(r"^##\s+")
    accepted = title_aliases(title)
    for index, line in enumerate(lines):
        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            current = fence.group(1)
            if not marker:
                marker = current
            elif current[0] == marker[0] and len(current) >= len(marker):
                marker = ""
            continue
        if not marker:
            if (
                start is None
                and line.strip().startswith("## ")
                and normalized_title(line.strip()[3:]) in accepted
            ):
                start = index + 1
                continue
            if start is not None and next_heading.match(line.strip()):
                return "\n".join(body).strip()
        if start is not None:
            body.append(line)
    if start is None:
        return None
    return "\n".join(body).strip()


def validate_plan_regression(
    relative: str,
    metadata: dict[str, FrontmatterValue],
    text: str,
    findings: list[Finding],
) -> None:
    if scalar(metadata, "schema") != "fcvw/plan@2":
        return
    contract = scalar(metadata, "regression_contract")
    if contract not in REGRESSION_CONTRACTS:
        findings.append(Finding("plan-regression", relative, f"invalid regression contract: {contract!r}"))
    section = level_two_section(text, "Regression impact")
    if section is None:
        findings.append(Finding("plan-regression", relative, "Regression impact section is missing"))
        return
    if not section or PLACEHOLDER.search(section):
        findings.append(Finding("plan-regression", relative, "Regression impact is empty or contains placeholders"))
    if contract == "required":
        for marker in REGRESSION_MARKERS:
            if not has_localized_heading(section, 3, marker.removeprefix("### ").strip()):
                findings.append(Finding("plan-regression", relative, f"missing regression marker: {marker}"))
    elif contract == "not_applicable":
        justification_labels = "|".join(re.escape(value) for value in title_aliases("Justification"))
        justification = re.search(rf"(?im)^(?:{justification_labels}):\s*(.+)$", normalized_title(section))
        reason = justification.group(1).strip() if justification else ""
        if len(reason) < MINIMUM_JUSTIFICATION:
            findings.append(
                Finding(
                    "plan-regression",
                    relative,
                    "not_applicable requires a specific Justification of at least "
                    f"{MINIMUM_JUSTIFICATION} characters",
                )
            )
        elif any(reason.startswith(generic) and len(reason) < 80 for generic in GENERIC_JUSTIFICATIONS):
            findings.append(
                Finding(
                    "plan-regression",
                    relative,
                    f"not_applicable Justification restates the waiver instead of arguing it: {reason[:60]!r}",
                )
            )
    if scalar(metadata, "status") == "completed" and re.search(r"\bpending\b", section, re.I):
        findings.append(Finding("plan-regression", relative, "completed plan has pending regression evidence"))
    rollback = level_two_section(text, "Rollback")
    if rollback is None:
        findings.append(Finding("plan-rollback", relative, "Rollback section is missing"))
    elif not rollback.strip() or PLACEHOLDER.search(rollback) or len(rollback.strip()) < 12:
        findings.append(
            Finding("plan-rollback", relative, "Rollback is empty, placeholder, or too short to be a procedure")
        )


def validate_plan_risk_binding(
    relative: str,
    metadata: dict[str, FrontmatterValue],
    findings: list[Finding],
) -> None:
    """Tie the regression contract to the declared risk and to sensitive surfaces.

    REGRESSION_GUARDS.md and TESTS.md already say that authentication, persisted
    data, public interfaces and destructive work are never low-risk. Without this
    check a plan could declare R5 and waive regression evidence in the same breath.
    """

    if scalar(metadata, "schema") != "fcvw/plan@2":
        return
    contract = scalar(metadata, "regression_contract")
    if contract != "not_applicable":
        return
    risk = scalar(metadata, "risk")
    if risk in REGRESSION_REQUIRED_RISKS:
        findings.append(
            Finding(
                "plan-risk-binding",
                relative,
                f"risk {risk} requires regression_contract: required",
            )
        )
    touched = [
        value
        for value in string_list(metadata, "context_files")
        if any(value.endswith(sensitive) for sensitive in SENSITIVE_CONTEXT_FILES)
    ]
    if touched:
        findings.append(
            Finding(
                "plan-risk-binding",
                relative,
                "a plan routed through a security, data, or migration contract "
                f"requires regression_contract: required ({touched[0]})",
            )
        )


def validate_compact_plan(
    relative: str,
    metadata: dict[str, FrontmatterValue],
    text: str,
    findings: list[Finding],
) -> None:
    """Keep the compact plan genuinely small and genuinely low-risk."""

    priority = scalar(metadata, "priority")
    risk = scalar(metadata, "risk")
    if priority not in COMPACT_PLAN_PRIORITIES:
        findings.append(
            Finding(
                "plan-compact",
                relative,
                f"a compact plan is limited to {sorted(COMPACT_PLAN_PRIORITIES)}; found {priority!r}",
            )
        )
    if risk not in COMPACT_PLAN_RISKS:
        findings.append(
            Finding(
                "plan-compact",
                relative,
                f"a compact plan is limited to {sorted(COMPACT_PLAN_RISKS)}; found {risk!r}",
            )
        )
    if "regression_contract" in metadata:
        findings.append(
            Finding(
                "plan-compact",
                relative,
                "a compact plan must not declare regression_contract; use fcvw/plan@2 instead",
            )
        )
    for title in COMPACT_PLAN_SECTIONS:
        if not has_localized_heading(text, 2, title):
            findings.append(Finding("plan-compact", relative, f"missing required section: {title}"))
    rollback = level_two_section(text, "Rollback")
    if rollback is not None and (not rollback.strip() or PLACEHOLDER.search(rollback)):
        findings.append(Finding("plan-rollback", relative, "Rollback is empty or contains placeholders"))


def validate_plans(root: Path, findings: list[Finding]) -> None:
    plans_root = root / "FCVW" / "Plans"
    seen: dict[str, str] = {}
    for state in ("pending", "in_progress", "completed", "discontinued"):
        for path in sorted((plans_root / state).glob("*.md")):
            if path.name in {"README.md", "QUEUE.md", "INDEX.md"}:
                continue
            relative = path.relative_to(root).as_posix()
            text = read_text(path)
            metadata = frontmatter(text)
            plan_id = scalar(metadata, "id")
            status = scalar(metadata, "status")
            schema = scalar(metadata, "schema")
            if schema not in PLAN_SCHEMAS:
                findings.append(Finding("plan-schema", relative, "plan must use a supported FCVW plan schema"))
            if schema == COMPACT_PLAN_SCHEMA:
                required_fields = COMPACT_PLAN_FIELDS
            elif schema == "fcvw/plan@2":
                required_fields = PLAN2_FIELDS
            else:
                required_fields = PLAN_FIELDS
            for field in required_fields:
                if field not in metadata:
                    findings.append(Finding("plan-schema", relative, f"missing field: {field}"))
            scalar_fields = (
                "id",
                "status",
                "priority",
                "risk",
                "created_at",
                "updated_at",
                "owner",
            )
            if schema != COMPACT_PLAN_SCHEMA:
                scalar_fields += ("current_version", "expected_version")
            if schema == "fcvw/plan@2":
                scalar_fields += ("regression_contract",)
            for field in scalar_fields:
                if field in metadata and not scalar(metadata, field).strip():
                    findings.append(Finding("plan-schema", relative, f"field must be a non-empty scalar: {field}"))
            if "context_files" in metadata:
                context_files = metadata["context_files"]
                if not isinstance(context_files, list) or not context_files:
                    findings.append(Finding("plan-schema", relative, "context_files must be a non-empty list"))
            if status != state:
                findings.append(Finding("plan-state", relative, f"status {status!r} != directory {state!r}"))
            if not PLAN_ID.fullmatch(plan_id):
                findings.append(Finding("plan-id", relative, f"invalid plan id: {plan_id!r}"))
            priority = scalar(metadata, "priority")
            risk = scalar(metadata, "risk")
            if priority not in PLAN_PRIORITIES:
                findings.append(Finding("plan-priority", relative, f"invalid priority: {priority!r}"))
            if risk not in PLAN_RISKS:
                findings.append(Finding("plan-risk", relative, f"invalid risk: {risk!r}"))
            identity = re.match(r"^(P[1-5])-(R[1-5])-", plan_id)
            if identity and priority and identity.group(1) != priority:
                findings.append(Finding("plan-priority", relative, "priority does not match the plan ID"))
            if identity and risk and identity.group(2) != risk:
                findings.append(Finding("plan-risk", relative, "risk does not match the plan ID"))
            if path.stem != plan_id:
                findings.append(Finding("plan-filename", relative, "filename must equal plan id"))
            if plan_id in seen:
                findings.append(Finding("duplicate-id", relative, f"plan id also used by {seen[plan_id]}"))
            seen[plan_id] = relative
            if schema == COMPACT_PLAN_SCHEMA:
                validate_compact_plan(relative, metadata, text, findings)
            else:
                validate_plan_risk_binding(relative, metadata, findings)
                validate_plan_regression(relative, metadata, text, findings)


def validate_skills(root: Path, findings: list[Finding]) -> None:
    skills_root = root / "FCVW" / "skills"
    catalog = read_text(skills_root / "README.md")
    seen: dict[str, str] = {}
    for path in sorted(skills_root.glob("*/SKILL.md")):
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter(text)
        for field in SKILL_FIELDS:
            if field not in metadata:
                findings.append(Finding("skill-metadata", relative, f"missing field: {field}"))
        if scalar(metadata, "schema") != "fcvw/skill@1":
            findings.append(Finding("skill-schema", relative, "skill must use fcvw/skill@1"))
        name = scalar(metadata, "name")
        if name != path.parent.name:
            findings.append(Finding("skill-name", relative, "skill name must match directory"))
        if name in seen:
            findings.append(Finding("duplicate-id", relative, f"skill name also used by {seen[name]}"))
        seen[name] = relative
        if name not in catalog:
            findings.append(Finding("skill-catalog", relative, "skill is missing from catalog"))
        for term in PROVIDER_TERMS:
            if term in text:
                findings.append(Finding("provider-neutrality", relative, f"provider-specific core term: {term}"))
        headings = tuple(normalized_title(line.strip()) for line in text.splitlines() if line.startswith("## "))
        for concept, accepted in SKILL_BODY_HEADINGS.items():
            markers = {
                normalized_title(marker)
                for marker in (*accepted, *SKILL_BODY_TRANSLATIONS.get(concept, ()))
            }
            if not any(any(heading.startswith(marker) for marker in markers) for heading in headings):
                findings.append(Finding("skill-contract", relative, f"missing body concept: {concept}"))


def declared_session_types(text: str) -> list[str]:
    return string_list(frontmatter(text), "session_types")


def validate_reading_routes(root: Path, findings: list[Finding]) -> None:
    context_path = root / "FCVW" / "CONTEXT_MAP.md"
    index_path = root / "FCVW" / "README.md"
    agents_path = root / "AGENTS.md"
    if not all(path.is_file() for path in (context_path, index_path, agents_path)):
        return
    context = read_text(context_path)
    fcvw_index = read_text(index_path)
    discoverability = "\n".join((read_text(agents_path), context, fcvw_index))
    for path in sorted((root / "FCVW").glob("*.md")):
        metadata = frontmatter_of(path)
        if scalar(metadata, "artifact_role") != "framework_policy":
            continue
        if path.name not in fcvw_index:
            findings.append(
                Finding(
                    "framework-index",
                    path.relative_to(root).as_posix(),
                    "framework policy is missing from the FCVW operational index",
                )
            )
        if path.name not in discoverability:
            findings.append(
                Finding(
                    "reading-route",
                    path.relative_to(root).as_posix(),
                    "framework policy is not discoverable from AGENTS.md, CONTEXT_MAP.md, or FCVW/README.md",
                )
            )
    for name in PROJECT_PROFILES:
        if (root / "FCVW" / name).is_file() and name not in fcvw_index:
            findings.append(
                Finding(
                    "framework-index",
                    f"FCVW/{name}",
                    "project profile is missing from the FCVW operational index",
                )
            )
    for path in sorted((root / "FCVW" / "skills").glob("*/SKILL.md")):
        relative = path.relative_to(root).as_posix()
        for session_type in declared_session_types(read_text(path)):
            if f"`{session_type}`" not in context:
                findings.append(
                    Finding(
                        "reading-route",
                        relative,
                        f"unmapped skill session type: {session_type}",
                    )
                )


def validate_feedback_notes(root: Path, findings: list[Finding]) -> None:
    """Keep framework feedback attributed, additive, and independently formed.

    Three properties matter and only these are machine-checkable. The note names
    the model that wrote it, so a later reader can weigh the source. It carries a
    lifecycle, so the surface does not grow without ever resolving. And when it
    responds to an earlier note it states its own suggestion *before* assessing
    that note, because a model that reads someone else's conclusion first tends
    to agree with it, and two independent readings are the entire point.
    """

    directory = root / "FCVW" / "wiki" / "feedback"
    if not directory.is_dir():
        return
    seen: dict[str, str] = {}
    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter_of(path)
        if scalar(metadata, "type") != "feedback":
            findings.append(Finding("feedback-note", relative, "feedback note must declare type: feedback"))
        for field in FEEDBACK_FIELDS:
            if not scalar(metadata, field).strip():
                findings.append(Finding("feedback-note", relative, f"missing or empty field: {field}"))
        status = scalar(metadata, "feedback_status")
        if status and status not in FEEDBACK_STATUSES:
            findings.append(
                Finding(
                    "feedback-note",
                    relative,
                    f"invalid feedback_status: {status!r}; expected one of {sorted(FEEDBACK_STATUSES)}",
                )
            )
        identity = scalar(metadata, "id").strip()
        if identity:
            if identity in seen:
                findings.append(Finding("duplicate-id", relative, f"feedback id also used by {seen[identity]}"))
            seen[identity] = relative
        # One note per model per topic keeps a disagreement readable; a second
        # note from the same model on the same topic belongs in that note.
        if not has_localized_heading(text, 2, FEEDBACK_SUGGESTION_TITLE):
            findings.append(
                Finding("feedback-note", relative, f"missing required section: {FEEDBACK_SUGGESTION_TITLE}")
            )
        prior = string_list(metadata, "related_feedback")
        if prior:
            if not has_localized_heading(text, 2, FEEDBACK_ASSESSMENT_TITLE):
                findings.append(
                    Finding(
                        "feedback-note",
                        relative,
                        "a note that cites related_feedback must assess it in "
                        f"'{FEEDBACK_ASSESSMENT_TITLE}'",
                    )
                )
            else:
                suggestion_at = _heading_position(text, FEEDBACK_SUGGESTION_TITLE)
                assessment_at = _heading_position(text, FEEDBACK_ASSESSMENT_TITLE)
                if suggestion_at is not None and assessment_at is not None and assessment_at < suggestion_at:
                    findings.append(
                        Finding(
                            "feedback-note",
                            relative,
                            "state your own suggestion before assessing prior notes, so the "
                            "assessment does not shape it",
                        )
                    )


def _heading_position(text: str, title: str) -> int | None:
    accepted = title_aliases(title)
    for number, line in outside_code_fences(text):
        stripped = line.strip()
        if stripped.startswith("## ") and normalized_title(stripped[3:]) in accepted:
            return number
    return None


def validate_wiki_ids(root: Path, findings: list[Finding]) -> None:
    wiki = root / "FCVW" / "wiki"
    seen: dict[str, str] = {}
    exempt = {"README.md", "index.md", "log.md", "metrics.md", "schema.md", "taxonomy.md"}
    for path in sorted(wiki.rglob("*.md")):
        if path.name in exempt or "templates" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        metadata = frontmatter_of(path)
        page_id = scalar(metadata, "id")
        if not page_id:
            findings.append(Finding("wiki-id", relative, "knowledge page is missing a unique id"))
            continue
        if page_id in seen:
            findings.append(Finding("duplicate-id", relative, f"wiki id also used by {seen[page_id]}"))
        seen[page_id] = relative
        schema = scalar(metadata, "schema")
        if schema == "fcvw/wiki@1":
            required_scalars = (
                "id",
                "artifact_role",
                "owner",
                "upgrade_strategy",
                "record_scope",
                "retrieval_scope",
                "title",
                "type",
                "status",
                "confidence",
                "created_at",
                "last_reviewed",
            )
            for field in required_scalars:
                if not scalar(metadata, field):
                    findings.append(Finding("wiki-schema", relative, f"missing or empty field: {field}"))
            for field in ("sources", "tags"):
                if not isinstance(metadata.get(field), list) or not string_list(metadata, field):
                    findings.append(Finding("wiki-schema", relative, f"{field} must be a non-empty list"))
            if "domain" in metadata and not isinstance(metadata.get("domain"), list):
                findings.append(Finding("wiki-schema", relative, "domain must be a first-level list"))
            if scalar(metadata, "artifact_role") != "record":
                findings.append(Finding("wiki-schema", relative, "artifact_role must be record"))
            if scalar(metadata, "upgrade_strategy") != "preserve":
                findings.append(Finding("wiki-schema", relative, "upgrade_strategy must be preserve"))
            if scalar(metadata, "record_scope") not in {"application", "framework"}:
                findings.append(Finding("wiki-schema", relative, "record_scope must be application or framework"))
            if scalar(metadata, "type") not in WIKI_TYPES:
                findings.append(Finding("wiki-schema", relative, f"invalid type: {scalar(metadata, 'type')!r}"))
            if scalar(metadata, "status") not in WIKI_STATUSES:
                findings.append(Finding("wiki-schema", relative, f"invalid status: {scalar(metadata, 'status')!r}"))
            if scalar(metadata, "confidence") not in WIKI_CONFIDENCE:
                findings.append(
                    Finding("wiki-schema", relative, f"invalid confidence: {scalar(metadata, 'confidence')!r}")
                )
        elif schema == "fcvw/regression@1":
            required_scalars = (
                "id",
                "artifact_role",
                "owner",
                "upgrade_strategy",
                "record_scope",
                "retrieval_scope",
                "title",
                "type",
                "severity",
                "status",
                "detected_at",
                "last_reviewed",
                "related_plan",
            )
            for field in required_scalars:
                if not scalar(metadata, field):
                    findings.append(Finding("regression-schema", relative, f"missing or empty field: {field}"))
            for field in ("sources", "tags"):
                if not isinstance(metadata.get(field), list) or not string_list(metadata, field):
                    findings.append(Finding("regression-schema", relative, f"{field} must be a non-empty list"))
            if scalar(metadata, "artifact_role") != "record":
                findings.append(Finding("regression-schema", relative, "artifact_role must be record"))
            if scalar(metadata, "upgrade_strategy") != "preserve":
                findings.append(Finding("regression-schema", relative, "upgrade_strategy must be preserve"))
            if scalar(metadata, "record_scope") not in {"application", "framework"}:
                findings.append(
                    Finding("regression-schema", relative, "record_scope must be application or framework")
                )
            if not re.fullmatch(r"REG-\d{8}-[a-z0-9-]+", page_id):
                findings.append(Finding("regression-schema", relative, f"invalid regression id: {page_id!r}"))
            if scalar(metadata, "type") not in REGRESSION_TYPES:
                findings.append(
                    Finding("regression-schema", relative, f"invalid type: {scalar(metadata, 'type')!r}")
                )
            if scalar(metadata, "severity") not in PLAN_RISKS:
                findings.append(
                    Finding("regression-schema", relative, f"invalid severity: {scalar(metadata, 'severity')!r}")
                )
            if scalar(metadata, "status") not in REGRESSION_STATUSES:
                findings.append(
                    Finding("regression-schema", relative, f"invalid status: {scalar(metadata, 'status')!r}")
                )
            related_plan = scalar(metadata, "related_plan")
            if related_plan and _find_plan_by_id(root, related_plan) is None:
                findings.append(
                    Finding("regression-schema", relative, f"related plan is missing or ambiguous: {related_plan}")
                )
        else:
            findings.append(Finding("wiki-schema", relative, f"unsupported knowledge schema: {schema!r}"))


def validate_audit_records(root: Path, findings: list[Finding]) -> None:
    audits = root / "FCVW" / "audits"
    seen_ids: dict[str, str] = {}
    for path in sorted(audits.glob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter(text)
        if scalar(metadata, "schema") != "fcvw/audit@1":
            findings.append(Finding("audit-schema", relative, "audit must use fcvw/audit@1"))
            continue
        for field in (
            "id",
            "artifact_role",
            "owner",
            "upgrade_strategy",
            "record_scope",
            "retrieval_scope",
            "status",
            "created_at",
            "last_reviewed",
        ):
            if not scalar(metadata, field):
                findings.append(Finding("audit-schema", relative, f"missing or empty field: {field}"))
        if not isinstance(metadata.get("sources"), list) or not string_list(metadata, "sources"):
            findings.append(Finding("audit-schema", relative, "sources must be a non-empty list"))
        if scalar(metadata, "artifact_role") != "record":
            findings.append(Finding("audit-schema", relative, "artifact_role must be record"))
        if scalar(metadata, "upgrade_strategy") != "preserve":
            findings.append(Finding("audit-schema", relative, "upgrade_strategy must be preserve"))
        audit_id = scalar(metadata, "id")
        if audit_id and not re.fullmatch(r"AUD-\d{8}-[a-z0-9-]+", audit_id):
            findings.append(Finding("audit-schema", relative, f"invalid audit id: {audit_id!r}"))
        if audit_id in seen_ids:
            findings.append(Finding("audit-schema", relative, f"audit id also used by {seen_ids[audit_id]}"))
        elif audit_id:
            seen_ids[audit_id] = relative
        if scalar(metadata, "record_scope") not in {"application", "framework"}:
            findings.append(Finding("audit-schema", relative, "record_scope must be application or framework"))
        if scalar(metadata, "status") not in {"draft", "completed", "blocked"}:
            findings.append(Finding("audit-schema", relative, f"invalid status: {scalar(metadata, 'status')!r}"))
        for section in (
            "Scope",
            "Authoritative sources",
            "Method",
            "Findings",
            "Validation",
            "Limitations and residual risk",
            "Follow-up",
        ):
            body = level_two_section(text, section)
            if body is None or not body.strip():
                findings.append(Finding("audit-schema", relative, f"missing or empty section: {section}"))


def validate_troubleshooting_records(root: Path, findings: list[Finding]) -> None:
    records = root / "FCVW" / "troubleshooting"
    seen_ids: dict[str, str] = {}
    for path in sorted(records.glob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter(text)
        schema = scalar(metadata, "schema")
        if not schema:
            continue
        if schema != "fcvw/troubleshooting@1":
            findings.append(
                Finding("troubleshooting-schema", relative, f"unsupported troubleshooting schema: {schema!r}")
            )
            continue
        required_scalars = (
            "id",
            "artifact_role",
            "owner",
            "upgrade_strategy",
            "record_scope",
            "retrieval_scope",
            "title",
            "type",
            "status",
            "confidence",
            "detected_at",
            "last_reviewed",
            "related_plan",
        )
        for field in required_scalars:
            if not scalar(metadata, field):
                findings.append(Finding("troubleshooting-schema", relative, f"missing or empty field: {field}"))
        for field in ("sources", "tags"):
            if not isinstance(metadata.get(field), list) or not string_list(metadata, field):
                findings.append(
                    Finding("troubleshooting-schema", relative, f"{field} must be a non-empty list")
                )
        record_id = scalar(metadata, "id")
        if record_id and not re.fullmatch(r"TRB-\d{8}-[a-z0-9-]+", record_id):
            findings.append(
                Finding("troubleshooting-schema", relative, f"invalid troubleshooting id: {record_id!r}")
            )
        if record_id in seen_ids:
            findings.append(
                Finding(
                    "troubleshooting-schema",
                    relative,
                    f"troubleshooting id also used by {seen_ids[record_id]}",
                )
            )
        elif record_id:
            seen_ids[record_id] = relative
        for field, expected in (
            ("artifact_role", "record"),
            ("upgrade_strategy", "preserve"),
            ("retrieval_scope", "search_only"),
            ("type", "failure"),
        ):
            if scalar(metadata, field) != expected:
                findings.append(Finding("troubleshooting-schema", relative, f"{field} must be {expected}"))
        if scalar(metadata, "record_scope") not in {"application", "framework"}:
            findings.append(
                Finding("troubleshooting-schema", relative, "record_scope must be application or framework")
            )
        if scalar(metadata, "status") not in {"draft", "in_validation", "validated", "obsolete"}:
            findings.append(
                Finding(
                    "troubleshooting-schema",
                    relative,
                    f"invalid status: {scalar(metadata, 'status')!r}",
                )
            )
        if scalar(metadata, "confidence") not in WIKI_CONFIDENCE:
            findings.append(
                Finding(
                    "troubleshooting-schema",
                    relative,
                    f"invalid confidence: {scalar(metadata, 'confidence')!r}",
                )
            )
        related_plan = scalar(metadata, "related_plan")
        if related_plan and not PLACEHOLDER.search(related_plan) and _find_plan_by_id(root, related_plan) is None:
            findings.append(
                Finding(
                    "troubleshooting-schema",
                    relative,
                    f"related plan is missing or ambiguous: {related_plan}",
                )
            )
        for section in (
            "1. Identification",
            "2. Symptom Description",
            "3. Hypotheses",
            "4. Root Cause",
            "5. Solution Applied",
            "6. Validation",
            "7. Prevention",
            "8. Wiki Promotion",
            "9. Status",
        ):
            body = level_two_section(text, section)
            if body is None or not body.strip() or PLACEHOLDER.search(body):
                findings.append(
                    Finding("troubleshooting-schema", relative, f"missing, empty, or unresolved section: {section}")
                )


def validate_profiles(root: Path, profile: str, findings: list[Finding]) -> None:
    for name in PROJECT_PROFILES:
        path = root / "FCVW" / name
        relative = path.relative_to(root).as_posix()
        if not path.is_file():
            findings.append(Finding("project-profile", relative, "project profile is missing"))
            continue
        text = read_text(path)
        metadata = frontmatter(text)
        if scalar(metadata, "artifact_role") != "project_profile":
            findings.append(Finding("ownership", relative, "profile must declare project_profile ownership"))
        status = scalar(metadata, "instantiation_status")
        if status and status not in INSTANTIATION_STATUSES:
            findings.append(
                Finding(
                    "instantiation",
                    relative,
                    f"invalid instantiation_status: {status!r}; expected one of "
                    f"{sorted(INSTANTIATION_STATUSES)}",
                )
            )
        if profile in {"instantiated", "strict", "incremental"}:
            if status == "not_applicable":
                if name in INSTANTIATION_REQUIRED_PROFILES:
                    findings.append(
                        Finding(
                            "instantiation",
                            relative,
                            "identity and scope profiles always apply and cannot be waived",
                        )
                    )
                    continue
                reason = scalar(metadata, "not_applicable_reason").strip()
                if len(reason) < MINIMUM_INSTANTIATION_REASON:
                    findings.append(
                        Finding(
                            "instantiation",
                            relative,
                            "not_applicable requires a not_applicable_reason of at least "
                            f"{MINIMUM_INSTANTIATION_REASON} characters",
                        )
                    )
                # A waived profile keeps its template placeholders on purpose:
                # the project is declaring that it does not use this concern yet.
                continue
            if status != "complete":
                findings.append(Finding("instantiation", relative, "profile is not complete"))
            if PLACEHOLDER.search(text):
                findings.append(Finding("placeholder", relative, "instantiated profile contains placeholders"))


def validate_clean_template(root: Path, findings: list[Finding]) -> None:
    fcvw = root / "FCVW"
    for name in FORBIDDEN_ROOT_ENTRIES:
        if (root / name).exists():
            findings.append(Finding("clean-contamination", name, "production-derived comparison fixture in project root"))
    for path in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        if path.name not in CLEAN_ROOT_ENTRIES and path.name not in FORBIDDEN_ROOT_ENTRIES:
            findings.append(
                Finding(
                    "clean-contamination",
                    path.name,
                    "unexpected root entry in clean framework package",
                )
            )
    for folder in ("audits", "briefings", "troubleshooting"):
        for path in (fcvw / folder).glob("*.md"):
            if path.name == "README.md":
                continue
            if scalar(frontmatter_of(path), "record_scope") != "framework":
                findings.append(
                    Finding(
                        "clean-contamination",
                        path.relative_to(root).as_posix(),
                        "non-framework record in clean baseline",
                    )
                )
    for path in (fcvw / "changelogs").rglob("*.md"):
        relative = path.relative_to(fcvw / "changelogs").as_posix()
        if relative != "unreleased/README.md":
            findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "application changelog in clean baseline"))
    for state in ("pending", "in_progress", "completed", "discontinued"):
        for path in (fcvw / "Plans" / state).glob("*.md"):
            if path.name in {"README.md", "QUEUE.md", "INDEX.md"}:
                continue
            metadata = frontmatter_of(path)
            if scalar(metadata, "record_scope") != "framework":
                findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "non-framework plan in clean baseline"))
    for path in (fcvw / "decisions").glob("*.md"):
        if path.name == "README.md":
            continue
        if scalar(frontmatter_of(path), "record_scope") != "framework":
            findings.append(Finding("clean-contamination", path.relative_to(root).as_posix(), "non-framework decision in clean baseline"))
    wiki_exempt = {"README.md", "index.md", "log.md", "metrics.md", "schema.md", "taxonomy.md"}
    for path in (fcvw / "wiki").rglob("*.md"):
        if path.name in wiki_exempt or "templates" in path.parts:
            continue
        if scalar(frontmatter_of(path), "record_scope") != "framework":
            findings.append(
                Finding(
                    "clean-contamination",
                    path.relative_to(root).as_posix(),
                    "non-framework knowledge record in clean baseline",
                )
            )
    forbidden_paths = ["FCVW/repository-open-graph-template.png"]
    if not is_installed_release_layout(root):
        forbidden_paths.append("FCVW/LICENSE")
    for forbidden in forbidden_paths:
        if (root / forbidden).exists():
            findings.append(Finding("clean-contamination", forbidden, "duplicate/application artifact in clean baseline"))


def validate_regression_surfaces(root: Path, findings: list[Finding]) -> None:
    required_content = {
        "AGENTS.md": "FCVW/REGRESSION_GUARDS.md",
        "FCVW/REGRESSION_GUARDS.md": "# Regression guardrails",
        "FCVW/PLANNING.md": "fcvw/plan@2",
        "FCVW/TESTS.md": "## Minimum regression evidence by risk",
        "FCVW/GOVERNANCE_GATES.md": "| Regression |",
        "FCVW/WATCHERS.md": "## Regression-prone events",
        "FCVW/SCHEMAS.md": "fcvw/regression@1",
        "FCVW/governance/TEMPLATE_PLAN.md": "## Regression impact",
        "FCVW/wiki/templates/TEMPLATE_REGRESSION.md": "fcvw/regression@1",
        "FCVW/examples/minimal-change/plan.md": "## Regression impact",
    }
    for relative, marker in required_content.items():
        path = root / relative
        if not path.is_file():
            continue
        text = read_text(path)
        present = marker in text
        heading_match = re.fullmatch(r"(#{1,6})\s+(.+)", marker)
        if heading_match:
            present = has_localized_heading(
                text,
                len(heading_match.group(1)),
                heading_match.group(2),
                include_fences=relative.startswith("FCVW/governance/TEMPLATE_"),
            )
        elif marker.startswith("| Regression |"):
            accepted = title_aliases("Regression")
            present = any(
                len(cells := [cell.strip() for cell in line.strip().strip("|").split("|")]) >= 1
                and normalized_title(cells[0]) in accepted
                for line in text.splitlines()
                if line.strip().startswith("|")
            )
        if not present:
            findings.append(Finding("regression-surface", relative, f"required marker is missing: {marker}"))


def _find_plan_by_id(root: Path, plan_id: str) -> Path | None:
    matches = list((root / "FCVW" / "Plans").glob(f"*/{plan_id}.md"))
    return matches[0] if len(matches) == 1 else None


def _validate_framework_release_record(root: Path, path: Path, findings: list[Finding]) -> str:
    relative = path.relative_to(root).as_posix()
    text = read_text(path)
    metadata = frontmatter(text)
    if scalar(metadata, "schema") != "fcvw/framework-release@1":
        findings.append(Finding("framework-release", relative, "invalid release schema"))
        return ""
    version = scalar(metadata, "version")
    status = scalar(metadata, "release_status")
    if path.stem != version:
        findings.append(Finding("framework-release", relative, "filename must match release version"))
    if status not in {"in_preparation", "ready", "published", "canceled"}:
        findings.append(Finding("framework-release", relative, "invalid release status"))
    current_record = scalar(metadata, "artifact_role") == "record"
    if status in {"in_preparation", "ready"} or current_record:
        for field in FRAMEWORK_RELEASE_FIELDS:
            value = metadata.get(field)
            if value is None or (isinstance(value, str) and not value.strip()) or (isinstance(value, list) and not value):
                findings.append(Finding("framework-release", relative, f"missing or empty release field: {field}"))
        if scalar(metadata, "release_type") not in {"patch", "minor", "major"}:
            findings.append(Finding("framework-release", relative, "invalid release_type"))
        if scalar(metadata, "compatibility") not in {"backward_compatible", "migration_required", "breaking"}:
            findings.append(Finding("framework-release", relative, "invalid compatibility"))
        if current_record:
            for field, expected in (
                ("owner", "framework"),
                ("upgrade_strategy", "preserve"),
                ("record_scope", "framework"),
            ):
                if scalar(metadata, field) != expected:
                    findings.append(Finding("framework-release", relative, f"{field} must be {expected}"))
        for section in FRAMEWORK_RELEASE_SECTIONS:
            accepted_sections = (section, *FRAMEWORK_RELEASE_SECTION_ALIASES.get(section, ()))
            body = next(
                (
                    candidate_body
                    for candidate in accepted_sections
                    if (candidate_body := level_two_section(text, candidate)) is not None
                ),
                None,
            )
            if body is None or not body.strip():
                findings.append(Finding("framework-release", relative, f"missing or empty section: {section}"))
    related_plans = string_list(metadata, "related_plans")
    for plan_id in related_plans:
        plan = _find_plan_by_id(root, plan_id)
        if plan is None:
            findings.append(Finding("framework-release", relative, f"related plan is missing or ambiguous: {plan_id}"))
            continue
        if status == "published" and scalar(frontmatter_of(plan), "status") != "completed":
            findings.append(Finding("framework-release", relative, f"published release has incomplete plan: {plan_id}"))
    if status in {"ready", "published"} and current_record:
        source_revision = scalar(metadata, "source_revision")
        if not re.fullmatch(r"[0-9a-fA-F]{40}", source_revision):
            findings.append(
                Finding("framework-release", relative, f"{status} release requires a 40-character source revision")
            )
    if status in {"in_preparation", "ready"} and current_record:
        if scalar(metadata, "publication_revision") != "UNPUBLISHED":
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    f"{status} release must keep publication_revision as UNPUBLISHED",
                )
            )
    if status == "published" and current_record:
        source_revision = scalar(metadata, "source_revision")
        publication_revision = scalar(metadata, "publication_revision")
        if not re.fullmatch(r"[0-9a-fA-F]{40}", publication_revision):
            findings.append(
                Finding("framework-release", relative, "published release requires a 40-character publication revision")
            )
        elif source_revision == publication_revision:
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "source_revision and publication_revision must identify different lifecycle commits",
                )
            )
        languages = set(string_list(metadata, "release_languages"))
        if languages != FRAMEWORK_RELEASE_LANGUAGES:
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "published language-specific release must contain pt-BR, en-US, es, and de assets",
                )
            )
        assets = level_two_section(text, "Clean assets and package contents") or ""
        expected_assets = {
            language: f"FrameCode-VibeWork-{version}-{language}.zip"
            for language in FRAMEWORK_RELEASE_LANGUAGES
        }
        missing_assets = [name for name in expected_assets.values() if name not in assets]
        if missing_assets:
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    f"published release is missing language assets: {', '.join(sorted(missing_assets))}",
                )
            )
        checksums = level_two_section(text, "Checksums") or ""
        asset_hashes: dict[str, str] = {}
        for language, asset_name in expected_assets.items():
            line = next((item for item in checksums.splitlines() if asset_name in item), "")
            match = re.search(r"\b[0-9a-fA-F]{64}\b", line)
            if match:
                asset_hashes[language] = match.group(0).lower()
        missing_checksums = sorted(FRAMEWORK_RELEASE_LANGUAGES - set(asset_hashes))
        if missing_checksums:
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "published release requires one SHA-256 checksum per language-specific asset; "
                    f"missing: {', '.join(missing_checksums)}",
                )
            )
        elif len(set(asset_hashes.values())) != len(asset_hashes):
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "language-specific assets must not reuse an identical SHA-256 checksum",
                )
            )
        publication = level_two_section(text, "Publication evidence") or ""
        if not re.search(r"https://github\.com/[^/\s]+/[^/\s]+/releases/tag/[^\s)]+", publication):
            findings.append(
                Finding(
                    "framework-release",
                    relative,
                    "published release requires a GitHub Release URL",
                )
            )
    return status


def validate_version(root: Path, findings: list[Finding]) -> None:
    lock_text = read_text(root / "FCVW" / "FRAMEWORK_LOCK.md")
    version = ""
    lock_state = ""
    for line in lock_text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2:
            continue
        value = cells[1].strip().strip("`")
        if not version and re.fullmatch(r"V\d+\.\d+\.\d+", value):
            version = value
        if not lock_state and value in {"ready", "published"}:
            lock_state = value
    if not version:
        findings.append(Finding("framework-version", "FCVW/FRAMEWORK_LOCK.md", "installed version not found"))
        return
    readme = root / ("FCVW/README.md" if is_installed_release_layout(root) else "README.md")
    if version not in read_text(readme):
        findings.append(
            Finding("framework-version", readme.relative_to(root).as_posix(), f"README does not reference {version}")
        )
    release_path = root / "FCVW" / "framework-releases" / f"{version}.md"
    if not release_path.is_file():
        findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "release record missing"))
    else:
        release_metadata = frontmatter_of(release_path)
        if scalar(release_metadata, "schema") != "fcvw/framework-release@1":
            findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "invalid release schema"))
        if scalar(release_metadata, "version") != version:
            findings.append(Finding("framework-release", release_path.relative_to(root).as_posix(), "version does not match framework lock"))
        release_status = scalar(release_metadata, "release_status")
        if lock_state not in {"ready", "published"}:
            findings.append(
                Finding(
                    "framework-version",
                    "FCVW/FRAMEWORK_LOCK.md",
                    "release state must be ready or published",
                )
            )
        if release_status != lock_state:
            findings.append(
                Finding(
                    "framework-release",
                    release_path.relative_to(root).as_posix(),
                    "framework lock state must match its release record",
                )
            )
    active_records: list[tuple[Path, str]] = []
    for candidate in sorted((root / "FCVW" / "framework-releases").glob("V*.md")):
        status = _validate_framework_release_record(root, candidate, findings)
        if status in {"in_preparation", "ready"}:
            active_records.append((candidate, status))
    if len(active_records) > 1:
        findings.append(
            Finding(
                "framework-release",
                "FCVW/framework-releases",
                f"multiple releases are active candidates: {', '.join(path.name for path, _ in active_records)}",
            )
        )
    ready_records = [path for path, status in active_records if status == "ready"]
    if ready_records and (lock_state != "ready" or ready_records[0].stem != version):
        findings.append(
            Finding(
                "framework-version",
                "FCVW/FRAMEWORK_LOCK.md",
                f"ready candidate {ready_records[0].stem} must be the ready framework lock",
            )
        )
    preparing_records = [path for path, status in active_records if status == "in_preparation"]
    if preparing_records and lock_state != "published":
        findings.append(
            Finding(
                "framework-version",
                "FCVW/FRAMEWORK_LOCK.md",
                "an in_preparation candidate requires the installed lock to remain published",
            )
        )
    if (root / "FCVW" / "changelogs" / f"{version}.md").exists():
        findings.append(Finding("version-namespace", f"FCVW/changelogs/{version}.md", "framework release in application namespace"))


def validate_application_releases(root: Path, findings: list[Finding]) -> None:
    changelogs = root / "FCVW" / "changelogs"
    for path in sorted(changelogs.rglob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        metadata = frontmatter(text)
        if scalar(metadata, "schema") != "fcvw/changelog@1":
            findings.append(Finding("application-release", relative, "invalid application release schema"))
            continue
        for field in ("version", "date", "release_status", "release_type"):
            if not scalar(metadata, field):
                findings.append(Finding("application-release", relative, f"missing or empty field: {field}"))
        if not isinstance(metadata.get("related_plans"), list) or not string_list(metadata, "related_plans"):
            findings.append(Finding("application-release", relative, "related_plans must be a non-empty list"))
        status = scalar(metadata, "release_status")
        if status not in {"unreleased", "in_preparation", "published", "canceled"}:
            findings.append(Finding("application-release", relative, f"invalid release_status: {status!r}"))
        if scalar(metadata, "release_type") not in {"patch", "minor", "major"}:
            findings.append(
                Finding("application-release", relative, f"invalid release_type: {scalar(metadata, 'release_type')!r}")
            )
        role = scalar(metadata, "artifact_role")
        if role == "record":
            for field in ("owner", "external_publication", "source_revision", "publication_revision"):
                if not scalar(metadata, field):
                    findings.append(Finding("application-release", relative, f"record field is required: {field}"))
            if scalar(metadata, "upgrade_strategy") != "preserve":
                findings.append(Finding("application-release", relative, "record upgrade_strategy must be preserve"))
            if scalar(metadata, "record_scope") != "application":
                findings.append(Finding("application-release", relative, "record_scope must be application"))
            if not isinstance(metadata.get("release_languages"), list) or not string_list(
                metadata,
                "release_languages",
            ):
                findings.append(Finding("application-release", relative, "release_languages must be a non-empty list"))
            source_revision = scalar(metadata, "source_revision")
            if source_revision and source_revision != "not_applicable" and not re.fullmatch(
                r"[0-9a-fA-F]{40}",
                source_revision,
            ):
                findings.append(
                    Finding(
                        "application-release",
                        relative,
                        "source_revision must be a 40-character revision or not_applicable",
                    )
                )
            publication_revision = scalar(metadata, "publication_revision")
            if publication_revision and publication_revision not in {"UNPUBLISHED", "not_applicable"} and not re.fullmatch(
                r"[0-9a-fA-F]{40}",
                publication_revision,
            ):
                findings.append(
                    Finding(
                        "application-release",
                        relative,
                        "publication_revision must be a 40-character revision, UNPUBLISHED, or not_applicable",
                    )
                )
        for section in ("Summary", "Validation", "Known gaps", "Rollback"):
            body = level_two_section(text, section)
            if body is None or not body.strip():
                findings.append(Finding("application-release", relative, f"missing or empty section: {section}"))
        if level_two_section(text, "Affected areas") is None and not any(
            level_two_section(text, section) is not None for section in ("Added", "Changed", "Fixed", "Removed")
        ):
            findings.append(
                Finding(
                    "application-release",
                    relative,
                    "release requires Affected areas or Added/Changed/Fixed/Removed sections",
                )
            )
        if role == "record":
            for section in (
                "Security and data impact",
                "Migration",
                "Assets and package contents",
                "Checksums",
                "Publication evidence",
                "Post-release validation",
            ):
                body = level_two_section(text, section)
                if body is None or not body.strip():
                    findings.append(
                        Finding("application-release", relative, f"missing or empty section: {section}")
                    )
        for plan_id in string_list(metadata, "related_plans"):
            plan = _find_plan_by_id(root, plan_id)
            if plan is None:
                findings.append(
                    Finding("application-release", relative, f"related plan is missing or ambiguous: {plan_id}")
                )
                continue
            if status == "published" and scalar(frontmatter_of(plan), "status") != "completed":
                findings.append(
                    Finding("application-release", relative, f"published release has incomplete plan: {plan_id}")
                )
        external = scalar(metadata, "external_publication")
        if external and external not in {"not_applicable", "pending", "published"}:
            findings.append(
                Finding("application-release", relative, f"invalid external_publication: {external!r}")
            )
        if external == "published":
            if not re.fullmatch(r"[0-9a-fA-F]{40}", scalar(metadata, "publication_revision")):
                findings.append(
                    Finding(
                        "application-release",
                        relative,
                        "externally published release requires a 40-character publication revision",
                    )
                )
            publication = level_two_section(text, "Publication evidence") or ""
            if not re.search(r"https?://[^\s)]+", publication):
                findings.append(
                    Finding("application-release", relative, "external publication requires an evidence URL")
                )


def _looks_like_local_relationship(field: str, value: str) -> bool:
    if field == "context_files":
        return True
    if re.match(r"^[a-z][a-z0-9+.-]*:", value, re.I):
        return False
    return (
        value.startswith((".", "/"))
        or "/" in value
        or "\\" in value
        or value.lower().endswith(".md")
    )


def _relationship_candidate(root: Path, source: Path, value: str) -> Path | None:
    target = unquote(value.strip().strip("<>")).split("#", 1)[0]
    if not target or PLACEHOLDER.search(target):
        return None
    target = target.replace("\\", "/")
    if target.startswith("/"):
        return root / target.lstrip("/")
    if target == "README.md" and is_installed_release_layout(root):
        return root / "FCVW" / "README.md"
    if target.startswith(("FCVW/", "AGENTS.md", "README.md")):
        return root / target
    return source.parent / target


def validate_frontmatter_documents(root: Path, findings: list[Finding]) -> None:
    roles = {"framework_policy", "framework_lock", "project_profile", "template", "record", "generated", "example"}
    strategies = {"replace", "replace_with_migration", "preserve", "regenerate", "merge"}
    retrieval_scopes = {"always", "routed", "search_only", "exact_only", "excluded_by_default"}
    authorities = {"canonical", "routed", "historical", "generated"}
    retrieval_priorities = {"high", "normal", "low"}
    paths = sorted(
        {*(root.glob("*.md")), *markdown_files(root)},
        key=lambda item: item.relative_to(root).as_posix().lower(),
    )
    for path in paths:
        relative = path.relative_to(root).as_posix()
        text = read_text(path)
        result = parse_frontmatter(text)
        for issue in result.issues:
            findings.append(Finding("frontmatter", relative, f"line {issue.line}: {issue.message}"))
        metadata = result.data
        if not metadata:
            continue
        role = scalar(metadata, "artifact_role")
        strategy = scalar(metadata, "upgrade_strategy")
        scope = scalar(metadata, "retrieval_scope")
        authority = scalar(metadata, "authority")
        retrieval_priority = scalar(metadata, "retrieval_priority")
        if role and role not in roles:
            findings.append(Finding("frontmatter-role", relative, f"invalid artifact_role: {role}"))
        if strategy and strategy not in strategies:
            findings.append(Finding("frontmatter-upgrade", relative, f"invalid upgrade_strategy: {strategy}"))
        if scope and scope not in retrieval_scopes:
            findings.append(Finding("frontmatter-retrieval", relative, f"invalid retrieval_scope: {scope}"))
        if authority and authority not in authorities:
            findings.append(Finding("frontmatter-retrieval", relative, f"invalid authority: {authority}"))
        expected_authority = {
            "framework_policy": "canonical",
            "framework_lock": "canonical",
            "project_profile": "routed",
            "record": "historical",
            "generated": "generated",
            "template": "generated",
            "example": "generated",
        }.get(role)
        if authority and expected_authority and authority != expected_authority:
            findings.append(
                Finding(
                    "frontmatter-retrieval",
                    relative,
                    f"{role} artifacts cannot elevate or change authority from {expected_authority}",
                )
            )
        if retrieval_priority and retrieval_priority not in retrieval_priorities:
            findings.append(
                Finding("frontmatter-retrieval", relative, f"invalid retrieval_priority: {retrieval_priority}")
            )
        if role in {"generated", "template", "example"} and scope and scope != "excluded_by_default":
            findings.append(
                Finding("frontmatter-retrieval", relative, f"{role} artifacts cannot elevate retrieval_scope")
            )
        if role == "generated" and strategy and strategy != "regenerate":
            findings.append(Finding("frontmatter-ownership", relative, "generated artifacts must use regenerate"))
        template_surface = path.name.upper().startswith("TEMPLATE_") or role in {"template", "example"} or any(
            part.lower() in {"templates", "examples"} for part in path.relative_to(root).parts
        )
        if template_surface:
            continue
        historical_legacy = (
            not role
            and "Plans" in path.relative_to(root).parts
            and any(state in path.relative_to(root).parts for state in ("completed", "discontinued"))
        )
        for field in (
            "created_at",
            "updated_at",
            "last_reviewed",
            "next_review",
            "ingested_at",
            "last_checked",
            "detected_at",
            "date",
        ):
            value = scalar(metadata, field)
            if value:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    findings.append(Finding("frontmatter-date", relative, f"invalid ISO date in {field}: {value}"))
        for field in LOCAL_RELATIONSHIP_FIELDS:
            if field not in metadata:
                continue
            raw_value = metadata[field]
            if field == "context_files" and not isinstance(raw_value, list):
                findings.append(Finding("frontmatter-list", relative, "context_files must be a first-level list"))
                continue
            values = string_list(metadata, field)
            normalized = [normalized_finding_path(item) for item in values]
            if not historical_legacy and len(normalized) != len(set(normalized)):
                findings.append(Finding("frontmatter-relationship", relative, f"{field} contains duplicates"))
            for target in dict.fromkeys(normalized):
                if not target or not _looks_like_local_relationship(field, target):
                    continue
                candidate = _relationship_candidate(root, path, target)
                if candidate is None:
                    continue
                try:
                    # `root` is resolved once in main(); frontmatter relationships
                    # are portable repository paths, so lexical normalisation is
                    # both correct and free of filesystem round trips.
                    resolved = Path(os.path.normpath(candidate))
                    resolved.relative_to(root)
                except (ValueError, OSError):
                    findings.append(
                        Finding("frontmatter-relationship", relative, f"{field} escapes repository root: {target}")
                    )
                    continue
                if not resolved.exists():
                    findings.append(
                        Finding("frontmatter-relationship", relative, f"{field} target is missing: {target}")
                    )


STALE_CATALOG_DERIVED_RULES = {"document-orphan", "document-unreachable"}


def validate_document_graph(root: Path, findings: list[Finding]) -> None:
    graph = build_graph(root)
    catalog = root / "FCVW" / "DOCUMENT_GRAPH.md"
    if catalog.is_file():
        actual_text = read_text(catalog)
        expected_text = render_catalog(root, catalog)
        actual_entries = tuple(
            sorted(
                (link.group(1), tuple(INLINE_CODE.findall(line)))
                for _, line in outside_code_fences(actual_text)
                for link in MARKDOWN_LINK.finditer(line)
            )
        )
        expected_entries = tuple(
            sorted(
                (link.group(1), tuple(INLINE_CODE.findall(line)))
                for _, line in outside_code_fences(expected_text)
                for link in MARKDOWN_LINK.finditer(line)
            )
        )
    else:
        actual_entries = ()
        expected_entries = ()
    stale = catalog.is_file() and actual_entries != expected_entries
    graph_findings = [
        Finding(item.rule, item.path, item.message, item.severity) for item in graph.findings
    ]
    if stale:
        # Orphan and reachability findings are derived from the generated
        # catalog, so a stale catalog reports every governed artifact twice.
        # One actionable finding replaces that noise; the derived rules are
        # re-evaluated for real once the catalog is regenerated.
        suppressed = sum(1 for item in graph_findings if item.rule in STALE_CATALOG_DERIVED_RULES)
        graph_findings = [item for item in graph_findings if item.rule not in STALE_CATALOG_DERIVED_RULES]
        detail = (
            f"; {suppressed} derived orphan/reachability finding(s) suppressed until it is regenerated"
            if suppressed
            else ""
        )
        findings.append(
            Finding(
                "document-catalog-stale",
                "FCVW/DOCUMENT_GRAPH.md",
                "generated catalog does not match the current Markdown filesystem"
                f"{detail}",
            )
        )
    findings.extend(graph_findings)


def validate_knowledge_graph(root: Path, findings: list[Finding]) -> None:
    graph = build_knowledge_graph(root)
    findings.extend(
        Finding(item.rule, item.path, item.message, item.severity)
        for item in graph.findings
    )


def validate_queues(root: Path, findings: list[Finding]) -> None:
    findings.extend(Finding(item.rule, item.path, item.message) for item in validate_plan_queues(root))


def validate_app_rules(root: Path, profile: str, findings: list[Finding]) -> None:
    path = root / "FCVW" / "APP_RULES.md"
    relative = "FCVW/APP_RULES.md"
    if not path.is_file():
        return
    text = read_text(path)
    metadata = frontmatter(text)
    if scalar(metadata, "schema") != "fcvw/app-rules@1":
        findings.append(Finding("app-rules-schema", relative, "invalid or missing APP_RULES schema"))
    if scalar(metadata, "artifact_role") != "project_profile":
        findings.append(Finding("app-rules-ownership", relative, "APP_RULES must be a project_profile"))
    instantiation_status = scalar(metadata, "instantiation_status")
    if instantiation_status not in INSTANTIATION_STATUSES:
        findings.append(
            Finding(
                "app-rules-status",
                relative,
                f"instantiation_status must be one of {sorted(INSTANTIATION_STATUSES)}",
            )
        )
    prose_lines = [line for _, line in outside_code_fences(text)]
    prose = "\n".join(prose_lines)
    matches = list(re.finditer(r"(?m)^##\s+(APP-RULE-\d{3,})\b[^\n]*$", prose))
    identifiers = [match.group(1) for match in matches]
    if len(identifiers) != len(set(identifiers)):
        findings.append(Finding("app-rules-id", relative, "APP_RULES contains duplicate rule IDs"))
    if profile in {"instantiated", "strict", "incremental"} and instantiation_status == "complete":
        if not identifiers:
            findings.append(Finding("app-rules-empty", relative, "completed APP_RULES has no application rules"))
        required_sections = (
            "Status",
            "Rule",
            "Affected components",
            "Rationale and expected behavior",
            "Exceptions",
            "Related records",
        )
        for index, match in enumerate(matches):
            rule_id = match.group(1)
            end = matches[index + 1].start() if index + 1 < len(matches) else len(prose)
            block = prose[match.end():end]
            sections = {
                title.lower(): body.strip()
                for title, body in re.findall(
                    r"(?ms)^###\s+([^\n]+)\n(.*?)(?=^###\s+|\Z)",
                    block,
                )
            }
            for section in required_sections:
                body = sections.get(section.lower(), "")
                if not body or PLACEHOLDER.search(body):
                    findings.append(
                        Finding("app-rules-contract", relative, f"{rule_id} has missing or empty section: {section}")
                    )
            status_body = sections.get("status", "").splitlines()
            status = status_body[0].strip().lower() if status_body else ""
            if status not in {"active", "deprecated", "superseded"}:
                findings.append(Finding("app-rules-contract", relative, f"{rule_id} has invalid status: {status!r}"))
            for section in ("affected components", "related records"):
                body = sections.get(section, "")
                if body and not MARKDOWN_LINK.search(body):
                    findings.append(
                        Finding("app-rules-contract", relative, f"{rule_id} section must contain a Markdown link: {section}")
                    )
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--profile",
        choices=("clean-template", "instantiated", "incremental", "strict"),
        default="clean-template",
    )
    parser.add_argument(
        "--baseline",
        help="legacy baseline Markdown file; valid only with --profile incremental",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="report format; json is intended for CI consumption",
    )
    parser.add_argument(
        "--fail-on",
        choices=("error", "warning", "never"),
        default="error",
        help="lowest severity that fails the run",
    )
    parser.add_argument(
        "--since",
        help=(
            "git revision; report per-file findings only for Markdown changed since it. "
            "Repository-wide rules are always reported."
        ),
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings: list[Finding] = []
    baseline_entries: list[BaselineEntry] = []
    accepted: list[Finding] = []

    if args.baseline and args.profile != "incremental":
        findings.append(
            Finding(
                "baseline-config",
                args.baseline,
                "--baseline is valid only with --profile incremental",
            )
        )
    elif args.baseline:
        baseline_path = Path(args.baseline)
        if not baseline_path.is_absolute():
            baseline_path = root / baseline_path
        baseline_entries, baseline_errors = load_legacy_baseline(baseline_path.resolve())
        findings.extend(baseline_errors)

    validate_required(root, findings)
    if not (root / "FCVW").is_dir():
        for finding in findings:
            print(f"ERROR [{finding.rule}] {finding.path}: {finding.message}")
        return 1

    scope: set[str] | None = None
    if args.since:
        changed, scope_error = changed_markdown_since(root, args.since)
        if scope_error is not None:
            findings.append(scope_error)
        else:
            scope = changed

    validate_markdown(root, findings, scope)
    validate_character_integrity(root, findings, scope)
    validate_automation(root, findings, scope)
    validate_language_review(root, findings)
    validate_frontmatter_documents(root, findings)
    validate_queues(root, findings)
    validate_document_graph(root, findings)
    validate_knowledge_graph(root, findings)
    validate_canonical_metadata(root, findings, scope)
    validate_plans(root, findings)
    validate_skills(root, findings)
    validate_reading_routes(root, findings)
    validate_wiki_ids(root, findings)
    validate_feedback_notes(root, findings)
    validate_audit_records(root, findings)
    validate_troubleshooting_records(root, findings)
    validate_profiles(root, args.profile, findings)
    validate_app_rules(root, args.profile, findings)
    validate_version(root, findings)
    validate_application_releases(root, findings)
    validate_regression_surfaces(root, findings)
    if args.profile == "clean-template":
        validate_clean_template(root, findings)

    if args.profile == "incremental" and baseline_entries:
        findings, accepted, stale = apply_legacy_baseline(findings, baseline_entries)
        findings.extend(stale)

    scoped_out = 0
    if scope is not None:
        kept = [
            item
            for item in findings
            if item.rule in REPOSITORY_WIDE_RULES or normalized_finding_path(item.path) in scope
        ]
        scoped_out = len(findings) - len(kept)
        findings = kept

    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]

    if args.format == "json":
        import json

        print(
            json.dumps(
                {
                    "profile": args.profile,
                    "errors": len(errors),
                    "warnings": len(warnings),
                    "findings": [
                        {
                            "rule": item.rule,
                            "path": item.path,
                            "message": item.message,
                            "severity": item.severity,
                        }
                        for item in findings
                    ],
                    "baseline": [
                        {"rule": item.rule, "path": item.path, "message": item.message}
                        for item in accepted
                    ],
                    "scoped_out": scoped_out,
                    "since": args.since,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for finding in accepted:
            print(f"BASELINE [{finding.rule}] {finding.path}: {finding.message}")
        for finding in findings:
            print(f"{finding.severity.upper()} [{finding.rule}] {finding.path}: {finding.message}")
        scope_note = f" scoped_out={scoped_out}" if args.since else ""
        print(
            f"FCVW validation: profile={args.profile} errors={len(errors)} "
            f"warnings={len(warnings)} findings={len(findings)} "
            f"baseline={len(accepted)}{scope_note}"
        )

    if args.fail_on == "never":
        return 0
    if args.fail_on == "warning":
        return 1 if findings else 0
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
