#!/usr/bin/env python3
"""Generate the PolicyC charts used by the portfolio article."""

from dataclasses import dataclass
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "static"

INK = "#2c2826"
MUTED = "#6b6763"
GRID = "#d4d1cb"
BACKGROUND = "#fcfcfb"
SAGE = "#cad2b9"
BLUE = "#c6d6e5"
CORAL = "#d7a18d"
GRAY = "#aaa6a0"
RUST = "#8f684e"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"


@dataclass(frozen=True)
class Study:
    version: str
    cases: int
    trial_slots: int
    complete_pairs: int
    planned_pairs: int
    web_searches: int
    cost: float
    input_reduction: float
    preservation: float
    wilson_low: float
    wilson_high: float
    baseline_passes: int
    billed_reduction: float
    uncached_reduction: float
    latency_change: float
    both_pass: int
    full_only: int
    compiler_only: int
    both_fail: int
    ungradable: int = 0


STUDIES = (
    Study("0.5", 50, 300, 129, 150, 0, 0.68807105, 98.23, 85.98, 78.15, 91.32, 107, 23.01, 67.80, -19.95, 92, 15, 9, 13),
    Study("0.6", 50, 300, 139, 150, 41, 1.03568580, 89.69, 86.49, 76.88, 92.49, 74, 24.50, 55.36, 0.39, 64, 10, 9, 53, 3),
    Study("0.7", 60, 360, 180, 180, 20, 0.93327915, 93.75, 79.75, 72.93, 85.21, 163, 12.14, 59.46, 14.63, 130, 33, 11, 6),
    Study("0.8", 60, 360, 163, 180, 16, 1.06527570, 94.76, 75.76, 67.79, 82.27, 132, 18.03, 66.00, -7.07, 100, 32, 11, 20),
    Study("0.9", 60, 360, 177, 180, 26, 1.17901190, 92.99, 75.91, 68.11, 82.30, 137, 17.21, 58.69, 13.36, 104, 33, 21, 19),
)

# Actual billed dollars per execution on each frozen audit's reported efficiency basis.
# Versions 0.5–0.7 use all planned executions; 0.8–0.9 use complete pairs.
BILLED_COST_PER_EXECUTION = {
    "0.5": (0.002591718667, 0.001995421667),
    "0.6": (0.003934319667, 0.002970252333),
    "0.7": (0.002760036944, 0.002424847222),
    "0.8": (0.002884990491, 0.002364964417),
    "0.9": (0.003426609040, 0.002836842655),
}

V09_EXTRACTION_READS = 60
V09_EXTRACTION_COST = 0.26783625

# Full policy versus itself on held-out v5: P(second sample passes | first sample passes), 177 ordered pairs, 13 of 60 cases split.
SELF_CONSISTENCY = 90.4

X_POSITIONS = (245, 450, 655, 860, 1065)


def text(x: float, y: float, value: str, **attrs: object) -> str:
    attributes = " ".join(f'{name.replace("_", "-")}="{escape(str(item))}"' for name, item in attrs.items())
    suffix = f" {attributes}" if attributes else ""
    return f'<text x="{x:g}" y="{y:g}"{suffix}>{escape(value)}</text>'


def line(x1: float, y1: float, x2: float, y2: float, **attrs: object) -> str:
    attributes = " ".join(f'{name.replace("_", "-")}="{item}"' for name, item in attrs.items())
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" {attributes} />'


def svg_document(width: int, height: int, title_value: str, description: str, body: list[str], defs: str = "") -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
            f'  <title id="title">{escape(title_value)}</title>',
            f'  <desc id="description">{escape(description)}</desc>',
            defs,
            f'  <rect width="{width}" height="{height}" fill="{BACKGROUND}" />',
            f'  <g font-family="{FONT}" fill="{INK}">',
            *(f"    {item}" for item in body),
            "  </g>",
            "</svg>",
            "",
        ]
    )


def write_svg(filename: str, width: int, height: int, title_value: str, description: str, body: list[str], defs: str = "") -> None:
    (STATIC / filename).write_text(svg_document(width, height, title_value, description, body, defs), encoding="utf-8")


def chart_frame(title_value: str, kicker: str, note: str) -> list[str]:
    return [
        f'<rect x="1" y="1" width="1128" height="760" fill="none" stroke="{INK}" stroke-width="1.5" />',
        text(40, 58, title_value, font_size=29, font_weight=650),
        text(1090, 58, kicker, text_anchor="end", fill=MUTED, font_size=22),
        text(1090, 105, note, text_anchor="end", fill=MUTED, font_size=18),
    ]

def add_direction_labels(body: list[str], *, more_is_better: bool, bottom_y: float = 590) -> None:
    top_label = "↑ More is better" if more_is_better else "↑ More is worse"
    bottom_label = "↓ Less is worse" if more_is_better else "↓ Less is better"
    body.extend(
        [
            text(1080, 142, top_label, text_anchor="end", fill=RUST, font_size=18, font_weight=600),
            text(1080, bottom_y, bottom_label, text_anchor="end", fill=RUST, font_size=18, font_weight=600),
        ]
    )


def chart_axes(
    y_min: float,
    y_max: float,
    ticks: tuple[float, ...],
    y_label: str,
    *,
    break_axis: bool = False,
    tick_prefix: str = "",
) -> tuple[list[str], object]:
    top = 165
    bottom = 600
    left = 155
    right = 1090

    def y_for(value: float) -> float:
        return bottom - ((value - y_min) / (y_max - y_min)) * (bottom - top)

    body: list[str] = []
    for tick in ticks:
        y = y_for(tick)
        body.append(line(left, y, right, y, stroke=GRID, stroke_width=1.5))
        label = f"{tick:+g}" if y_min < 0 < y_max and tick != 0 else f"{tick:g}"
        body.append(text(134, y + 8, f"{tick_prefix}{label.replace('-', '−')}", text_anchor="end", fill=MUTED, font_size=22))
    body.extend(
        [
            line(left, top, left, bottom, stroke=INK, stroke_width=2),
            line(left, bottom, right, bottom, stroke=INK, stroke_width=2),
            text(625, 731, "Compiler version", text_anchor="middle", font_size=24),
            text(52, 390, y_label, text_anchor="middle", font_size=24, transform="rotate(-90 52 390)"),
        ]
    )
    if break_axis:
        body.append(f'<path d="M146 620 l9 -8 l-9 -8 l9 -8" fill="none" stroke="{INK}" stroke-width="2" />')
    return body, y_for


def add_versions(body: list[str], *, cases: bool = False, baseline: bool = False) -> None:
    for x, study in zip(X_POSITIONS, STUDIES, strict=True):
        body.append(text(x, 646, study.version, text_anchor="middle", font_size=23, font_weight=650))
        if cases:
            body.append(text(x, 679, f"{study.cases} cases", text_anchor="middle", fill=MUTED, font_size=17))
        if baseline:
            body.append(text(x, 679, f"{study.baseline_passes} full passes", text_anchor="middle", fill=MUTED, font_size=16))


def input_chart() -> None:
    body = chart_frame("Input reduction", "Relative to full policy", "Different held-out set per version; sequence is descriptive")
    add_direction_labels(body, more_is_better=True)
    axes, y_for = chart_axes(85, 100, (100, 95, 90, 85), "Input reduction (%)", break_axis=True)
    body.extend(axes)
    points = [(x, y_for(study.input_reduction)) for x, study in zip(X_POSITIONS, STUDIES, strict=True)]
    body.append(f'<polyline points="{" ".join(f"{x},{y:.1f}" for x, y in points)}" fill="none" stroke="{INK}" stroke-width="3" />')
    offsets = (-28, 39, -28, -28, 39)
    for (x, y), study, offset in zip(points, STUDIES, offsets, strict=True):
        body.append(f'<circle cx="{x}" cy="{y:.1f}" r="12" fill="{SAGE}" stroke="{INK}" stroke-width="2" />')
        body.append(text(x, y + offset, f"{study.input_reduction:.2f}%", text_anchor="middle", font_size=21))
    add_versions(body, cases=True)
    description = "Mean actual input-token reduction relative to the full policy was " + ", ".join(
        f"{study.input_reduction:.2f} percent for compiler {study.version}" for study in STUDIES
    ) + ". Each version used a different held-out set, so the connected points show study sequence rather than controlled version-to-version gains. More reduction is better; less is worse."
    write_svg("policyc-input-reduction.svg", 1130, 762, "PolicyC input-token reduction across compiler versions", description, body)


def preservation_chart() -> None:
    body = chart_frame("Critical-obligation preservation", "Conditional rate", "Bars show trial-level Wilson 95% intervals")
    add_direction_labels(body, more_is_better=True)
    axes, y_for = chart_axes(65, 100, (100, 95, 90, 85, 80, 75, 70, 65), "Preservation (%)", break_axis=True)
    body.extend(axes)
    target_y = y_for(95)
    baseline_y = y_for(SELF_CONSISTENCY)
    body.extend(
        [
            line(155, target_y, 1090, target_y, stroke=RUST, stroke_width=2, stroke_dasharray="9 8"),
            text(1080, target_y - 12, "95% preregistered target", text_anchor="end", fill=RUST, font_size=19),
            line(155, baseline_y, 1090, baseline_y, stroke=INK, stroke_width=2, stroke_dasharray="3 7"),
            text(1080, baseline_y + 24, f"{SELF_CONSISTENCY:.1f}% full policy vs. itself (held-out v5)", text_anchor="end", fill=INK, font_size=19),
        ]
    )
    points = [(x, y_for(study.preservation)) for x, study in zip(X_POSITIONS, STUDIES, strict=True)]
    body.append(f'<polyline points="{" ".join(f"{x},{y:.1f}" for x, y in points)}" fill="none" stroke="{INK}" stroke-width="3" />')
    for (x, y), study in zip(points, STUDIES, strict=True):
        high = y_for(study.wilson_high)
        low = y_for(study.wilson_low)
        body.extend(
            [
                line(x, high, x, low, stroke=MUTED, stroke_width=2),
                line(x - 11, high, x + 11, high, stroke=MUTED, stroke_width=2),
                line(x - 11, low, x + 11, low, stroke=MUTED, stroke_width=2),
                f'<circle cx="{x}" cy="{y:.1f}" r="12" fill="{BLUE}" stroke="{INK}" stroke-width="2" />',
                text(x, y - 27, f"{study.preservation:.2f}%", text_anchor="middle", font_size=20),
            ]
        )
    add_versions(body, baseline=True)
    description = "Conditional critical-obligation preservation by compiler was " + "; ".join(
        f"{study.preservation:.2f} percent for {study.version}, with a trial-level Wilson 95 percent interval from {study.wilson_low:.2f} to {study.wilson_high:.2f} percent"
        for study in STUDIES
    ) + (
        f". Every result was below the 95 percent target. A second dashed line at {SELF_CONSISTENCY:.1f} percent marks how often one sample of the full policy "
        "reproduced another sample's pass on held-out v5, the reference's own self-consistency; it is a baseline, not a ceiling. "
        "The intervals are descriptive because samples are clustered by case, and every version used a different held-out set. More preservation is better; less is worse."
    )
    write_svg("policyc-preservation.svg", 1130, 762, "PolicyC conditional critical-obligation preservation across compiler versions", description, body)


def cost_chart() -> None:
    body = chart_frame("Execution-cost reduction", "Relative to full policy", "Paired runs only; 0.9 extraction reported separately")
    body[3] = text(40, 105, "Paired runs only; 0.9 extraction reported separately", fill=MUTED, font_size=18)
    body.extend(
        [
            f'<rect x="610" y="89" width="17" height="17" fill="{SAGE}" stroke="{INK}" stroke-width="1.5" />',
            text(640, 104, "Uncached-equivalent", font_size=20, font_weight=600),
            f'<rect x="880" y="89" width="17" height="17" fill="{BLUE}" stroke="{INK}" stroke-width="1.5" />',
            text(910, 104, "Actual billed", font_size=20, font_weight=600),
        ]
    )
    add_direction_labels(body, more_is_better=True)
    axes, y_for = chart_axes(0, 80, (80, 60, 40, 20, 0), "Cost reduction (%)")
    body.extend(axes)
    uncached = [(x, y_for(study.uncached_reduction)) for x, study in zip(X_POSITIONS, STUDIES, strict=True)]
    billed = [(x, y_for(study.billed_reduction)) for x, study in zip(X_POSITIONS, STUDIES, strict=True)]
    for points in (uncached, billed):
        body.append(f'<polyline points="{" ".join(f"{x},{y:.1f}" for x, y in points)}" fill="none" stroke="{INK}" stroke-width="3" />')
    for (x, y), study in zip(uncached, STUDIES, strict=True):
        body.append(f'<circle cx="{x}" cy="{y:.1f}" r="12" fill="{SAGE}" stroke="{INK}" stroke-width="2" />')
        body.append(text(x, y - 27, f"{study.uncached_reduction:.2f}%", text_anchor="middle", font_size=19))
    for (x, y), study in zip(billed, STUDIES, strict=True):
        body.append(f'<circle cx="{x}" cy="{y:.1f}" r="12" fill="{BLUE}" stroke="{INK}" stroke-width="2" />')
        body.append(text(x, y + 36, f"{study.billed_reduction:.2f}%", text_anchor="middle", font_size=19))
    add_versions(body)
    description = "Actual billed-cost reduction by compiler was " + ", ".join(
        f"{study.billed_reduction:.2f} percent for {study.version}" for study in STUDIES
    ) + ". Uncached-equivalent cost reduction was " + ", ".join(
        f"{study.uncached_reduction:.2f} percent for {study.version}" for study in STUDIES
    ) + (
        f". Compiler 0.9's {V09_EXTRACTION_READS} compile-time extractor calls cost "
        f"{V09_EXTRACTION_COST:.4f} dollars and are reported separately, not netted into these execution-study reductions. "
        "Its 17.21 percent billed comparison uses the same 177 complete pairs in both conditions. "
        "Every version used a different held-out set. More reduction is better; less is worse."
    )
    write_svg("policyc-cost-reduction.svg", 1130, 762, "PolicyC execution-cost reduction across compiler versions", description, body)


def billed_cost_chart() -> None:
    body = chart_frame(
        "Measured billed cost per execution",
        "Observed paired conditions",
        "Actual billed spend; tool fees included",
    )
    body.extend(
        [
            f'<rect x="40" y="89" width="17" height="17" fill="{GRAY}" stroke="{INK}" stroke-width="1.5" />',
            text(70, 104, "Full-policy billed", font_size=20, font_weight=600),
            f'<rect x="260" y="89" width="17" height="17" fill="{SAGE}" stroke="{INK}" stroke-width="1.5" />',
            text(290, 104, "Compiler-slice billed", font_size=20, font_weight=600),
        ]
    )
    add_direction_labels(body, more_is_better=False, bottom_y=625)
    axes, y_for = chart_axes(
        0,
        0.0045,
        (0.004, 0.003, 0.002, 0.001, 0),
        "Billed cost ($ / execution)",
        tick_prefix="$",
    )
    body.extend(axes)
    positions = (225, 425, 625, 825, 1025)
    bar_width = 48
    for x, study in zip(positions, STUDIES, strict=True):
        full_cost, compiled_cost = BILLED_COST_PER_EXECUTION[study.version]
        for left, value, color in (
            (x - 54, full_cost, GRAY),
            (x + 6, compiled_cost, SAGE),
        ):
            y = y_for(value)
            body.append(
                f'<rect x="{left}" y="{y:.1f}" width="{bar_width}" height="{600 - y:.1f}" '
                f'fill="{color}" stroke="{INK}" stroke-width="2" />'
            )
            body.append(text(left + bar_width / 2, y - 14, f"${value:.6f}", text_anchor="middle", font_size=15))
        body.extend(
            [
                text(x, 660, study.version, text_anchor="middle", font_size=22, font_weight=650),
                text(x, 691, f"−{study.billed_reduction:.2f}%", text_anchor="middle", fill=RUST, font_size=16, font_weight=600),
            ]
        )
    description = "Actual measured billed cost per execution for the full-policy and compiler-slice conditions was " + "; ".join(
        f"{full_cost:.6f} dollars and {compiled_cost:.6f} dollars for compiler {study.version}, {study.billed_reduction:.2f} percent lower"
        for study in STUDIES
        for full_cost, compiled_cost in (BILLED_COST_PER_EXECUTION[study.version],)
    ) + (
        ". Versions 0.5 through 0.7 use all planned executions. Version 0.8 uses the same 163 complete pairs in both conditions, and version 0.9 uses the same 177 complete pairs. "
        "Compiler 0.9's run total includes 179 issued full-policy calls and 180 issued compiler-slice calls; the unmatched calls are excluded from these normalized bars. "
        "Both series are observed spend, not forecasts. Less cost is better; more is worse."
    )
    write_svg(
        "policyc-billed-cost.svg",
        1130,
        762,
        "PolicyC measured billed cost per execution",
        description,
        body,
    )


def latency_chart() -> None:
    body = chart_frame("End-to-end latency change", "Relative to full policy", "Different held-out set per version; sequence is descriptive")
    add_direction_labels(body, more_is_better=False)
    axes, y_for = chart_axes(-25, 20, (20, 10, 0, -10, -20, -25), "Latency change (%)")
    body.extend(axes)
    zero_y = y_for(0)
    body.extend(
        [
            line(155, zero_y, 1090, zero_y, stroke=MUTED, stroke_width=2, stroke_dasharray="9 8"),
            text(1080, zero_y - 12, "same latency as full policy", text_anchor="end", fill=MUTED, font_size=18),
        ]
    )
    points = [(x, y_for(study.latency_change)) for x, study in zip(X_POSITIONS, STUDIES, strict=True)]
    body.append(f'<polyline points="{" ".join(f"{x},{y:.1f}" for x, y in points)}" fill="none" stroke="{INK}" stroke-width="3" />')
    offsets = (-28, 38, -28, 38, 38)
    for (x, y), study, offset in zip(points, STUDIES, offsets, strict=True):
        direction = "faster" if study.latency_change < 0 else "slower"
        body.append(f'<circle cx="{x}" cy="{y:.1f}" r="12" fill="{CORAL}" stroke="{INK}" stroke-width="2" />')
        body.append(text(x, y + offset, f"{abs(study.latency_change):.2f}% {direction}", text_anchor="middle", font_size=18))
    add_versions(body)
    description = "Relative to the full policy, " + ", ".join(
        f"compiler {study.version} was {abs(study.latency_change):.2f} percent {'faster' if study.latency_change < 0 else 'slower'}"
        for study in STUDIES
    ) + ". Each compiler used a different held-out set. Less latency change is better; more is worse."
    write_svg("policyc-latency.svg", 1130, 762, "PolicyC latency change across compiler versions", description, body)


def protocol_chart() -> None:
    body = [
        text(40, 58, "Five frozen held-out studies", font_size=29, font_weight=650),
        text(1090, 58, "New case set after every compiler", text_anchor="end", fill=MUTED, font_size=22),
        line(40, 112, 1090, 112, stroke=INK, stroke_width=1.5),
        text(55, 148, "Compiler", fill=MUTED, font_size=16, font_weight=600),
        text(145, 148, "Cases", fill=MUTED, font_size=16, font_weight=600),
        text(220, 148, "Trial slots", fill=MUTED, font_size=16, font_weight=600),
        text(340, 148, "Complete pairs", fill=MUTED, font_size=16, font_weight=600),
        text(515, 148, "Tool activity", fill=MUTED, font_size=16, font_weight=600),
        text(835, 137, "Full-policy", text_anchor="end", fill=MUTED, font_size=14, font_weight=600),
        text(835, 158, "billed / exec", text_anchor="end", fill=MUTED, font_size=14, font_weight=600),
        text(965, 137, "Compiler-slice", text_anchor="end", fill=MUTED, font_size=14, font_weight=600),
        text(965, 158, "billed / exec", text_anchor="end", fill=MUTED, font_size=14, font_weight=600),
        text(1090, 137, "All issued", text_anchor="end", fill=MUTED, font_size=14, font_weight=600),
        text(1090, 158, "run total", text_anchor="end", fill=MUTED, font_size=14, font_weight=600),
        line(40, 170, 1090, 170, stroke=GRID, stroke_width=1.5),
    ]
    centers = (215, 290, 365, 440, 515)
    separators = (245, 320, 395, 470, 545)
    for y, divider, study in zip(centers, separators, STUDIES, strict=True):
        activity = "No provider tools" if study.web_searches == 0 else f"{study.web_searches} web searches"
        full_cost, compiled_cost = BILLED_COST_PER_EXECUTION[study.version]
        body.extend(
            [
                text(55, y + 7, study.version, font_size=20, font_weight=650),
                text(145, y + 7, str(study.cases), font_size=19),
                text(220, y + 7, str(study.trial_slots), font_size=19),
                text(340, y + 7, f"{study.complete_pairs} / {study.planned_pairs}", font_size=19),
                text(515, y + 7, activity, font_size=18),
                text(835, y + 7, f"${full_cost:.6f}", text_anchor="end", font_size=17),
                text(965, y + 7, f"${compiled_cost:.6f}", text_anchor="end", font_size=17),
                text(1090, y + 7, f"${study.cost:.4f}", text_anchor="end", font_size=18),
                line(40, divider, 1090, divider, stroke=GRID, stroke_width=1.5),
            ]
        )
    body.extend(
        [
            f'<rect x="40" y="558" width="1050" height="170" fill="#f4f3ef" stroke="{GRID}" stroke-width="1.5" />',
            text(62, 584, "Compiler 0.6 denominator", font_size=17, font_weight=600),
            text(380, 584, "136 determinate pairs + 3 ungradable complete pairs", fill=MUTED, font_size=17),
            text(62, 614, "Compiler 0.9 dispatch", font_size=17, font_weight=600),
            text(380, 614, "179 full-policy + 180 compiler-slice calls; 359 of 360 issued", fill=MUTED, font_size=17),
            text(62, 644, "Compiler 0.9 frontend", font_size=17, font_weight=600),
            text(380, 644, f"{V09_EXTRACTION_READS} extractor calls · ${V09_EXTRACTION_COST:.4f}, reported separately", fill=MUTED, font_size=17),
            text(62, 674, "Per-execution basis", font_size=17, font_weight=600),
            text(380, 674, "0.5–0.7 all trials · 0.8: 163 pairs · 0.9: 177 pairs", fill=MUTED, font_size=17),
            text(62, 704, "Paired-execution total", font_size=17, font_weight=600),
            text(380, 704, "280 cases · 1,680 planned trial slots · 103 searches · $4.9013", fill=MUTED, font_size=17),
        ]
    )
    description = "; ".join(
        (
            f"Compiler {study.version} used {study.cases} cases, {study.trial_slots} planned trial slots, "
            f"{study.complete_pairs} of {study.planned_pairs} complete pairs, {study.web_searches} web searches, "
            f"{full_cost:.6f} dollars per full-policy billed execution, {compiled_cost:.6f} dollars per compiler-slice billed execution, "
            f"and {study.cost:.4f} dollars across all issued paired-study calls"
        )
        for study in STUDIES
        for full_cost, compiled_cost in (BILLED_COST_PER_EXECUTION[study.version],)
    ) + (
        f". Compiler 0.9 also used {V09_EXTRACTION_READS} compile-time extractor calls costing "
        f"{V09_EXTRACTION_COST:.4f} dollars, reported separately. Versions 0.5 through 0.7 use all planned executions for their per-execution costs; "
        "version 0.8 uses 163 complete pairs and version 0.9 uses 177 complete pairs. Compiler 0.9's run total contains 179 issued full-policy calls "
        "and 180 issued compiler-slice calls, while its normalized cost columns use equal 177-call denominators. Every version used a newly authored held-out set."
    )
    write_svg("policyc-study-protocol.svg", 1130, 760, "PolicyC frozen held-out paired-execution protocol by compiler version", description, body)


def paired_outcomes_chart() -> None:
    definitions = f'''  <defs>
    <pattern id="ungradable" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="8" height="8" fill="{BACKGROUND}" />
      <line x1="0" y1="0" x2="0" y2="8" stroke="#8b8782" stroke-width="2" />
    </pattern>
  </defs>'''
    body = [
        text(40, 58, "Strategy-blind paired outcomes", font_size=29, font_weight=650),
        text(1090, 58, "Primary semantic counts", text_anchor="end", fill=MUTED, font_size=22),
        text(40, 98, "Different held-out set per version; bar lengths are descriptive, not controlled comparisons.", fill=MUTED, font_size=18),
    ]
    legend = ((40, SAGE, "Both pass"), (210, CORAL, "Full policy only"), (435, BLUE, "Compiler only"), (635, GRAY, "Both fail"), (790, "url(#ungradable)", "Ungradable"))
    for x, color, label in legend:
        body.extend(
            [
                f'<rect x="{x}" y="128" width="17" height="17" fill="{color}" stroke="{INK}" />',
                text(x + 28, 143, label, font_size=18, font_weight=600),
            ]
        )
    plot_left = 190
    plot_right = 990
    scale = (plot_right - plot_left) / 180
    axis_bottom = 830
    for count in (0, 45, 90, 135, 180):
        x = plot_left + count * scale
        body.append(line(x, 185, x, axis_bottom, stroke=GRID, stroke_width=1.5))
        body.append(text(x, 868, f"{count}{' pairs' if count == 180 else ''}", text_anchor="middle", fill=MUTED, font_size=18))
    body.append(line(plot_left, axis_bottom, plot_right, axis_bottom, stroke=GRID, stroke_width=1.5))
    rows = (195, 320, 445, 570, 695)
    colors = (SAGE, CORAL, BLUE, GRAY)
    for y, study in zip(rows, STUDIES, strict=True):
        body.append(text(158, y + 30, study.version, text_anchor="end", font_size=22, font_weight=650))
        offset = plot_left
        for count, color in zip((study.both_pass, study.full_only, study.compiler_only, study.both_fail), colors, strict=True):
            width = count * scale
            body.append(f'<rect x="{offset:.1f}" y="{y}" width="{width:.1f}" height="46" fill="{color}" stroke="{INK}" stroke-width="1.5" />')
            offset += width
        if study.ungradable:
            width = study.ungradable * scale
            body.append(f'<rect x="{offset:.1f}" y="{y}" width="{width:.1f}" height="46" fill="url(#ungradable)" stroke="{INK}" stroke-width="1.5" />')
        determinate = study.both_pass + study.full_only + study.compiler_only + study.both_fail
        prefix = f"n={determinate}{' determinate' if study.ungradable else ''}"
        details = f"{prefix}: {study.both_pass} both pass · {study.full_only} full only · {study.compiler_only} compiler only · {study.both_fail} both fail"
        body.append(text(plot_left, y + 78, details, font_size=17))
        if study.ungradable:
            body.append(text(plot_left, y + 102, f"+ {study.ungradable} ungradable complete pairs", fill=MUTED, font_size=17))
    description = "Primary strategy-blind semantic paired outcomes. " + " ".join(
        f"Compiler {study.version} had {study.both_pass + study.full_only + study.compiler_only + study.both_fail} determinate pairs: {study.both_pass} both pass, {study.full_only} full policy only, {study.compiler_only} compiler only, and {study.both_fail} both fail" + (f", plus {study.ungradable} ungradable complete pairs." if study.ungradable else ".")
        for study in STUDIES
    ) + " Each compiler used a different held-out set."
    write_svg("policyc-paired-outcomes.svg", 1130, 900, "PolicyC strategy-blind paired outcomes across frozen studies", description, body, definitions)


def historical_pipeline() -> None:
    body = [
        text(40, 55, "How compilers 0.5–0.8 build Pₓ", font_size=29, font_weight=650),
        text(1090, 55, "Filter-first pipeline", text_anchor="end", fill=MUTED, font_size=22),
        line(100, 205, 1030, 205, stroke=INK, stroke_width=2),
    ]
    for x in (210, 447, 677, 907):
        body.append(f'<path d="M{x} 198 L{x + 10} 205 L{x} 212 Z" fill="{INK}" />')
    nodes = ((100, SAGE, 17), (335, BLUE, 14), (565, BLUE, 14), (795, BLUE, 14), (1030, SAGE, 17))
    for x, color, radius in nodes:
        body.append(f'<circle cx="{x}" cy="205" r="{radius}" fill="{color}" stroke="{INK}" stroke-width="2" />')
    labels = ((100, "Inputs"), (335, "Match and retain"), (565, "Dependency closure"), (795, "Specialize + emit"), (1030, "Pₓ"))
    for x, label in labels:
        body.append(text(x, 148, label, text_anchor="middle", font_size=20, font_weight=650))
    details = {
        100: ("Policy graph P", "Request x", "Context + tools"),
        335: ("Lexical intents", "Trigger fields", "Critical safeguards"),
        565: ("Requires edges", "Transitive nodes", "Stable ordering"),
        795: ("0.8: one regex predicate", "Model-visible rules", "Compact context"),
        1030: ("Active policy slice", "for this request"),
    }
    for x, lines in details.items():
        for index, value in enumerate(lines):
            body.append(text(x, 260 + index * 28, value, text_anchor="middle", fill=MUTED, font_size=16))
    body.extend(
        [
            line(40, 370, 1090, 370, stroke=GRID, stroke_width=1.5),
            text(40, 418, "Structural guarantee", font_size=20, font_weight=650),
            text(265, 418, "Every dependency declared in the graph is retained.", fill=MUTED, font_size=19),
            text(40, 466, "Remaining limitation", font_size=20, font_weight=650),
            text(265, 466, "Most state, limits, and precedence still live in matching and emitted prose.", fill=RUST, font_size=18),
        ]
    )
    write_svg(
        "policyc-compiler-pipeline.svg",
        1130,
        520,
        "PolicyC compilers 0.5 through 0.8 filter-first pipeline",
        "Compilers 0.5 through 0.8 take the policy graph, request, context, and tools; match and retain policies; close dependencies; then specialize and emit a compact slice. Compiler 0.8 adds one regular-expression predicate, but most request state, limits, and precedence still live in matching and emitted prose.",
        body,
    )


def box(body: list[str], x: int, y: int, width: int, height: int, fill: str, heading: str, lines: tuple[str, ...]) -> None:
    body.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="1.8" />')
    body.append(text(x + width / 2, y + 30, heading, text_anchor="middle", font_size=18, font_weight=650))
    for index, value in enumerate(lines):
        body.append(text(x + width / 2, y + 57 + index * 23, value, text_anchor="middle", fill=MUTED, font_size=15))


def arrow(body: list[str], x1: int, y1: int, x2: int, y2: int) -> None:
    body.append(line(x1, y1, x2, y2, stroke=INK, stroke_width=2))
    body.append(f'<path d="M{x2 - 10} {y2 - 7} L{x2} {y2} L{x2 - 10} {y2 + 7} Z" fill="{INK}" />')


def compiler_pipeline_v09() -> None:
    body = [
        text(40, 55, "How compiler 0.9 builds Pₓ", font_size=29, font_weight=650),
        text(1090, 55, "Typed IR + partial evaluation", text_anchor="end", fill=MUTED, font_size=22),
        text(40, 172, "Request", fill=MUTED, font_size=17, font_weight=600),
        text(40, 362, "Policy", fill=MUTED, font_size=17, font_weight=600),
    ]
    box(body, 115, 115, 140, 110, SAGE, "Inputs", ("Request x", "Context + tools"))
    box(body, 300, 102, 155, 135, BLUE, "Frontend", ("Model extractor:", "1 call / request", "or regex reader"))
    box(body, 505, 100, 185, 140, BLUE, "RequestState", ("Authorization · limit", "Fields · format", "Purpose · tools"))
    box(body, 115, 305, 140, 110, SAGE, "Policy graph P", ("44 nodes", "Six domains"))
    box(body, 300, 305, 155, 110, BLUE, "Select + close", ("Triggers", "Requires edges"))
    box(body, 505, 305, 185, 110, BLUE, "Selected nodes", ("Branches", "Obligations"))
    box(body, 755, 180, 170, 165, SAGE, "Partial evaluation", ("Choose branch", "Apply mask table", "Lower tools", "Record trace"))
    box(body, 960, 220, 100, 90, BLUE, "Printer", ("No policy", "decisions"))
    body.append(f'<circle cx="1095" cy="265" r="17" fill="{SAGE}" stroke="{INK}" stroke-width="2" />')
    body.append(text(1095, 211, "Pₓ", text_anchor="middle", font_size=20, font_weight=650))
    arrow(body, 255, 170, 300, 170)
    arrow(body, 455, 170, 505, 170)
    arrow(body, 255, 360, 300, 360)
    arrow(body, 455, 360, 505, 360)
    arrow(body, 690, 170, 755, 225)
    arrow(body, 690, 360, 755, 300)
    arrow(body, 925, 265, 960, 265)
    arrow(body, 1060, 265, 1078, 265)
    body.extend(
        [
            line(40, 455, 1090, 455, stroke=GRID, stroke_width=1.5),
            text(40, 500, "Typed boundary", font_size=19, font_weight=650),
            text(230, 500, "Held-out 0.9 used one model call per request, then persisted that state.", fill=MUTED, font_size=18),
            text(40, 545, "Semantic decisions", font_size=19, font_weight=650),
            text(230, 545, "Branches, obligation precedence, and tool lowering resolve before the printer.", fill=RUST, font_size=18),
        ]
    )
    write_svg(
        "policyc-compiler-pipeline-v09.svg",
        1130,
        580,
        "PolicyC compiler 0.9 typed intermediate representation pipeline",
        "Compiler 0.9 reads the request and context once through a frontend into a typed RequestState. For held-out v5, the extractor frontend makes one model call per request at compile time and persists the result before either execution condition runs. In parallel, the compiler selects policies and closes dependencies. Partial evaluation combines the state with selected nodes, chooses declared branches, applies the obligation-precedence table, lowers unavailable tools, and records the trace. A decision-free printer emits the compact policy slice.",
        body,
    )


# --- Polaris: the model-reader line (canaries 3-5) ------------------------------------------------


@dataclass(frozen=True)
class Arm:
    label: str
    passes: int
    unsafe: int
    reask: int
    kept: str


# Canary 3: 8 fresh cases, 2 samples, 16 trials per arm; kept = full-policy passes reproduced, paired by sample, of 6.
CANARY3_ARMS = (
    Arm("Compiler 0.10 slice", 2, 0, 8, "1/6"),
    Arm("Clause slice", 5, 2, 3, "2/6"),
    Arm("Full policy", 6, 3, 2, "2/6 vs. itself"),
    Arm("Model reader", 6, 0, 2, "4/6"),
)

# Canary 5 answer run (no reader): 8 fresh cases, 2 samples, 16 trials per arm; kept of the full policy's 5 passes; in-run full vs. itself 4/5.
CANARY5_ARMS = (
    Arm("Compiler 0.10 slice", 4, 0, 8, "4/5"),
    Arm("Clause slice", 4, 0, 7, "4/5"),
    Arm("Full policy", 5, 2, 0, "4/5 vs. itself"),
    Arm("Condition list", 3, 0, 4, "3/5"),
)


@dataclass(frozen=True)
class Reader:
    label: str
    contract: int
    cost: float
    latency: float
    reads: bool
    note: str


# Reader cost and median latency per case, from each run's report.json; "reads" = read the fresh confirmations correctly.
READERS = (
    Reader("mini, default", 1, 0.0059, 24.0, True, "canary 3: 3 of 4 confirmations read"),
    Reader("mini, default", 2, 0.0077, 30.6, True, "canary 5: every confirmed action read"),
    Reader("mini, minimal", 1, 0.0026, 11.2, False, "canary 4: 2 of 5, contradicts itself"),
    Reader("mini, minimal", 2, 0.0024, 10.0, False, "canary 5: \u201cyes\u201d on all 8, asks anyway"),
    Reader("nano, low", 2, 0.0009, 8.9, False, "canary 5: 3 of 8 readings invalid"),
    Reader("nano, low", 1, 0.00047, 5.3, False, "canary 4: \u201cproceed\u201d on the privileged send"),
    Reader("nano, minimal", 2, 0.0003, 3.4, False, "canary 5: noise"),
    Reader("nano, minimal", 1, 0.00014, 1.1, False, "canary 4: empty readings on 6 of 8"),
)

FULL_ANSWER_COST = 0.0046  # full-policy answer, mean per call, canary 3
READER_BREAK_EVEN = 0.001  # what the reader may cost for the pipeline to undercut the full policy


@dataclass(frozen=True)
class Canary:
    label: str
    cases: int
    arms: str
    calls: int
    cost: float
    tested: str
    outcome: str


CANARIES = (
    Canary("1", 4, "full · clause · compiler", 29, 0.0616, "Does the model apply a preserved condition?", "No: re-asked on the confirmed send"),
    Canary("2", 8, "+ evidence bare · apply", 80, 0.1639, "Does quoted evidence beside the rule help?", "Worse: evidence became a checklist"),
    Canary("3", 8, "+ model reader", 92, 0.4110, "Does a model reading the clauses read?", "Yes: 3 of 4 fresh confirmations, 0 unsafe"),
    Canary("4", 8, "3 cheaper readers, no answers", 24, 0.0260, "Can a cheaper reader keep the reading?", "No: all killed at the ledger gate"),
    Canary("5", 8, "4 readers · condition list", 96, 0.2450, "Does removing the search fix it?", "No: cheap readers still did not read"),
)


def panel_title(body: list[str], y: int, title_value: str, kicker: str) -> None:
    body.append(text(40, y, title_value, font_size=24, font_weight=650))
    body.append(text(1090, y, kicker, text_anchor="end", fill=MUTED, font_size=18))


def arms_panel(body: list[str], top: int, arms: tuple[Arm, ...], kept_heading: str) -> None:
    plot_top = top + 24
    plot_bottom = top + 264
    left = 150
    scale = (plot_bottom - plot_top) / 16

    def y_for(value: int) -> float:
        return plot_bottom - value * scale

    for tick in (0, 4, 8, 12, 16):
        y = y_for(tick)
        body.append(line(left, y, 1090, y, stroke=GRID, stroke_width=1.5))
        body.append(text(left - 16, y + 7, str(tick), text_anchor="end", fill=MUTED, font_size=18))
    body.append(line(left, plot_top, left, plot_bottom, stroke=INK, stroke_width=2))
    body.append(line(left, plot_bottom, 1090, plot_bottom, stroke=INK, stroke_width=2))
    body.append(text(58, (plot_top + plot_bottom) / 2, "Trials of 16", text_anchor="middle", font_size=19, transform=f"rotate(-90 58 {(plot_top + plot_bottom) / 2:g})"))
    group_width = (1090 - left) / len(arms)
    bar_width = 44
    for index, arm in enumerate(arms):
        center = left + group_width * (index + 0.5)
        for offset, (value, color) in enumerate(((arm.passes, SAGE), (arm.unsafe, CORAL), (arm.reask, GRAY))):
            x = center - 1.5 * bar_width - 6 + offset * (bar_width + 6)
            height = value * scale
            body.append(f'<rect x="{x:.1f}" y="{plot_bottom - height:.1f}" width="{bar_width}" height="{height:.1f}" fill="{color}" stroke="{INK}" stroke-width="1.5" />')
            body.append(text(x + bar_width / 2, plot_bottom - height - 8, str(value), text_anchor="middle", font_size=18))
        body.append(text(center, plot_bottom + 30, arm.label, text_anchor="middle", font_size=19, font_weight=650))
        body.append(text(center, plot_bottom + 56, f"{kept_heading} {arm.kept}", text_anchor="middle", fill=MUTED, font_size=16))


def canary_arms_chart() -> None:
    body = [
        text(40, 58, "Which prompt did what the policy says", font_size=29, font_weight=650),
        text(1090, 58, "Blind-graded canaries, 16 trials per arm", text_anchor="end", fill=MUTED, font_size=22),
        text(40, 98, "Eight fresh cases each, two samples, isolated author and grader, rubric locked before any output. Direction, not rate.", fill=MUTED, font_size=18),
    ]
    legend = ((40, SAGE, "All rubric items pass"), (330, CORAL, "Unsafe action"), (540, GRAY, "Redundant re-ask"))
    for x, color, label in legend:
        body.extend(
            [
                f'<rect x="{x}" y="128" width="17" height="17" fill="{color}" stroke="{INK}" />',
                text(x + 28, 143, label, font_size=18, font_weight=600),
            ]
        )
    panel_title(body, 200, "Canary 3: a model reads the clauses and writes directives", "Kept = full-policy passes reproduced, of 6")
    arms_panel(body, 210, CANARY3_ARMS, "kept")
    panel_title(body, 580, "Canary 5: conditions listed in the answer prompt, no reader", "Kept of 5 full passes; full vs. itself 4/5")
    arms_panel(body, 590, CANARY5_ARMS, "kept")
    body.append(text(40, 948, "Canary 5: three confirmed cases were blanked for every arm by a harness effect (lookup-first tool schemas; calls are recorded, not executed).", fill=MUTED, font_size=16))
    description = (
        "Canary 3, sixteen trials per arm: the compiler 0.10 slice passed 2 with 0 unsafe actions and 8 redundant re-asks and kept 1 of 6 full-policy passes; "
        "the clause slice passed 5 with 2 unsafe and 3 re-asks and kept 2 of 6; the full policy passed 6 with 3 unsafe and 2 re-asks and reproduced 2 of 6 of its own other sample's passes; "
        "the model reader passed 6 with 0 unsafe and 2 re-asks and kept 4 of 6. "
        "Canary 5 answer run without a reader: the compiler slice passed 4 with 0 unsafe and 8 re-asks and kept 4 of 5; the clause slice passed 4 with 0 unsafe and 7 re-asks and kept 4 of 5; "
        "the full policy passed 5 with 2 unsafe and 0 re-asks and reproduced 4 of 5 of its own; the condition list passed 3 with 0 unsafe and 4 re-asks and kept 3 of 5. "
        "Eight cases and two samples per canary; these are directions, not rates."
    )
    write_svg("policyc-canary-arms.svg", 1130, 970, "PolicyC canary 3 and canary 5 arm outcomes", description, body)


def reader_economics_chart() -> None:
    body = [
        text(40, 58, "What a reader costs, and whether it reads", font_size=29, font_weight=650),
        text(1090, 58, "Per request, gpt-5-mini / gpt-5-nano readers", text_anchor="end", fill=MUTED, font_size=22),
        text(40, 98, "Cost per case on a log scale. Only the two default-effort readers read the fresh confirmations; both cost more than the full-policy answer.", fill=MUTED, font_size=18),
    ]
    legend = ((40, SAGE, "Read the confirmations"), (330, GRAY, "Did not read"))
    for x, color, label in legend:
        body.extend(
            [
                f'<rect x="{x}" y="128" width="17" height="17" fill="{color}" stroke="{INK}" />',
                text(x + 28, 143, label, font_size=18, font_weight=600),
            ]
        )
    import math

    plot_left = 300
    plot_right = 860
    log_min = math.log10(0.0001)
    log_max = math.log10(0.01)

    def x_for(cost: float) -> float:
        return plot_left + (math.log10(cost) - log_min) / (log_max - log_min) * (plot_right - plot_left)

    top = 190
    row_height = 54
    bottom = top + row_height * len(READERS)
    for tick in (0.0001, 0.001, 0.01):
        x = x_for(tick)
        body.append(line(x, top - 10, x, bottom, stroke=GRID, stroke_width=1.5))
        body.append(text(x, bottom + 30, f"${tick:g}", text_anchor="middle", fill=MUTED, font_size=18))
    for value, label, color, dy in ((READER_BREAK_EVEN, "break-even reader budget", RUST, -18), (FULL_ANSWER_COST, "full-policy answer $0.0046", INK, -40)):
        x = x_for(value)
        body.append(line(x, top - 10, x, bottom, stroke=color, stroke_width=2, stroke_dasharray="9 8"))
        body.append(text(x, top + dy, label, text_anchor="middle", fill=color, font_size=17, font_weight=600))
    body.append(line(plot_left, bottom, plot_right, bottom, stroke=INK, stroke_width=2))
    body.append(text((plot_left + plot_right) / 2, bottom + 62, "Reader cost per case (log scale)", text_anchor="middle", font_size=20))
    for index, reader in enumerate(READERS):
        y = top + row_height * index
        width = x_for(reader.cost) - plot_left
        color = SAGE if reader.reads else GRAY
        body.append(f'<rect x="{plot_left}" y="{y + 10}" width="{width:.1f}" height="30" fill="{color}" stroke="{INK}" stroke-width="1.5" />')
        body.append(text(plot_left - 14, y + 31, f"{reader.label} · contract {reader.contract}", text_anchor="end", font_size=18, font_weight=600))
        body.append(text(plot_left + width + 12, y + 25, f"${reader.cost:.5f} · {reader.latency:g} s", font_size=17))
        body.append(text(plot_left + width + 12, y + 44, reader.note, fill=MUTED, font_size=14))
    body.append(text(40, bottom + 108, "Contract 1: the reader finds the request-dependent conditions in the clause slice.", fill=MUTED, font_size=16))
    body.append(text(40, bottom + 132, "Contract 2: the conditions are listed from a frozen source-first index and the reader answers each one once.", fill=MUTED, font_size=16))
    body.append(text(40, bottom + 156, "Break-even: the reader arm\u2019s answer already costs $0.0035 and 7.6 s against the full policy\u2019s $0.0046 and 8.0 s,", fill=MUTED, font_size=16))
    body.append(text(40, bottom + 180, "leaving about $0.001 and under a second for the read.", fill=MUTED, font_size=16))
    description = "Reader cost per case and median latency: " + "; ".join(
        f"{reader.label} under contract {reader.contract} cost {reader.cost:.5f} dollars and took {reader.latency:g} seconds and {'read' if reader.reads else 'did not read'} the fresh confirmations ({reader.note})"
        for reader in READERS
    ) + (
        f". The break-even reader budget is about {READER_BREAK_EVEN} dollars; the full-policy answer costs about {FULL_ANSWER_COST} dollars. "
        "Only the two default-effort gpt-5-mini readers read, and both cost more than the full-policy answer."
    )
    write_svg("policyc-reader-economics.svg", 1130, 830, "PolicyC reader cost per case against whether the reader read the request", description, body)


def canary_protocol_chart() -> None:
    body = [
        text(40, 58, "Five canaries", font_size=29, font_weight=650),
        text(1090, 58, "Small, isolated, blind-graded, kill conditions fixed first", text_anchor="end", fill=MUTED, font_size=22),
        line(40, 112, 1090, 112, stroke=INK, stroke_width=1.5),
        text(55, 148, "Canary", fill=MUTED, font_size=16, font_weight=600),
        text(140, 148, "Cases", fill=MUTED, font_size=16, font_weight=600),
        text(215, 148, "Arms", fill=MUTED, font_size=16, font_weight=600),
        text(505, 148, "Question", fill=MUTED, font_size=16, font_weight=600),
        text(890, 148, "Calls", text_anchor="end", fill=MUTED, font_size=16, font_weight=600),
        text(985, 148, "Cost", text_anchor="end", fill=MUTED, font_size=16, font_weight=600),
        line(40, 170, 1090, 170, stroke=GRID, stroke_width=1.5),
    ]
    y = 200
    for canary in CANARIES:
        body.extend(
            [
                text(55, y + 7, canary.label, font_size=20, font_weight=650),
                text(140, y + 7, str(canary.cases), font_size=19),
                text(215, y + 7, canary.arms, font_size=17),
                text(505, y + 7, canary.tested, font_size=17),
                text(890, y + 7, str(canary.calls), text_anchor="end", font_size=18),
                text(985, y + 7, f"${canary.cost:.4f}", text_anchor="end", font_size=18),
                text(505, y + 33, canary.outcome, fill=RUST, font_size=16),
                line(40, y + 52, 1090, y + 52, stroke=GRID, stroke_width=1.5),
            ]
        )
        y += 82
    body.extend(
        [
            f'<rect x="40" y="{y + 8}" width="1050" height="118" fill="#f4f3ef" stroke="{GRID}" stroke-width="1.5" />',
            text(62, y + 36, "Answer model", font_size=17, font_weight=600),
            text(300, y + 36, "gpt-5-mini-2025-08-07 in every arm; readers were gpt-5-mini or gpt-5-nano at a stated reasoning effort", fill=MUTED, font_size=17),
            text(62, y + 66, "Evidence class", font_size=17, font_weight=600),
            text(300, y + 66, "Development canaries: direction, not rate. Every case set is spent after one use.", fill=MUTED, font_size=17),
            text(62, y + 96, "Total", font_size=17, font_weight=600),
            text(300, y + 96, f"{sum(c.calls for c in CANARIES)} paid calls \u00b7 ${sum(c.cost for c in CANARIES):.3f}, plus the five held-out studies\u2019 $4.9013", fill=MUTED, font_size=17),
        ]
    )
    description = "; ".join(
        f"Canary {c.label} used {c.cases} cases and the arms {c.arms} over {c.calls} paid calls costing {c.cost:.4f} dollars to ask: {c.tested} Outcome: {c.outcome}"
        for c in CANARIES
    ) + ". Every canary used gpt-5-mini as the answer model, an isolated author, a rubric locked before any output, and, from canary 2 on, a separate isolated blind grader."
    write_svg("policyc-canary-protocol.svg", 1130, 760, "PolicyC canary protocol and outcomes", description, body)


def polaris_pipeline() -> None:
    body = [
        text(40, 55, "How Polaris builds P\u2093 + D\u2093", font_size=29, font_weight=650),
        text(1090, 55, "Verbatim slice + a model that reads it", text_anchor="end", fill=MUTED, font_size=22),
        text(40, 172, "Policy", fill=MUTED, font_size=17, font_weight=600),
        text(40, 362, "Request", fill=MUTED, font_size=17, font_weight=600),
    ]
    box(body, 115, 115, 150, 110, SAGE, "Source P", ("61 clauses, verbatim", "hash-checked"))
    box(body, 310, 102, 165, 135, BLUE, "Structural slice", ("Dedupe boilerplate", "Prune only on a", "declared fact"))
    box(body, 520, 100, 150, 140, BLUE, "P\u2093", ("~3,000 tokens", "Conditions kept", "conditional"))
    box(body, 115, 305, 150, 110, SAGE, "Request x", ("Context + tools",))
    box(body, 310, 305, 165, 110, BLUE, "Condition index", ("16 conditions", "frozen, source-first"))
    box(body, 715, 180, 180, 165, SAGE, "Semantic reader", ("One model call", "Reads P\u2093 + x", "Contract 1: finds", "Contract 2: answers list"))
    box(body, 940, 200, 120, 125, BLUE, "D\u2093", ("Directives only", "Verdicts stay", "in the artifact"))
    arrow(body, 265, 170, 310, 170)
    arrow(body, 475, 170, 520, 170)
    arrow(body, 670, 170, 715, 230)
    body.append(line(265, 360, 288, 360, stroke=INK, stroke_width=2))
    body.append(line(288, 360, 288, 445, stroke=INK, stroke_width=2))
    body.append(line(288, 445, 700, 445, stroke=INK, stroke_width=2))
    arrow(body, 700, 445, 780, 345)
    arrow(body, 475, 360, 715, 320)
    arrow(body, 895, 262, 940, 262)
    body.extend(
        [
            line(40, 455, 1090, 455, stroke=GRID, stroke_width=1.5),
            text(40, 500, "Answer call", font_size=19, font_weight=650),
            text(230, 500, "(P\u2093 + D\u2093, x) \u2192 y. No regex or request state anywhere on the request \u2192 directive path.", fill=MUTED, font_size=18),
            text(40, 545, "Degrades safely", font_size=19, font_weight=650),
            text(230, 545, "An empty reading renders the bare slice. The reader never manufactures a directive.", fill=RUST, font_size=18),
        ]
    )
    write_svg(
        "policyc-polaris-pipeline.svg",
        1130,
        580,
        "Polaris model-reader pipeline",
        "Polaris keeps the policy's original clauses: a hand-audited map of 61 clauses is deduplicated and pruned only on a structural fact the case declares, giving a verbatim slice of about three thousand tokens with every condition still conditional. A separate model call reads that slice and the request and writes request-specific directives; under contract 1 it finds the conditions itself, under contract 2 it answers each condition listed from a frozen source-first index exactly once. Only the directives are appended to the slice for the answer call. No regular expression or request state sits on the path from request to directive, and an empty reading renders the bare slice.",
        body,
    )


def validate_data() -> None:
    for study in STUDIES:
        determinate_pairs = study.both_pass + study.full_only + study.compiler_only + study.both_fail
        assert determinate_pairs + study.ungradable == study.complete_pairs
        assert study.both_pass + study.full_only == study.baseline_passes
        full_cost, compiled_cost = BILLED_COST_PER_EXECUTION[study.version]
        assert round((1 - (compiled_cost / full_cost)) * 100, 2) == study.billed_reduction
    assert sum(study.cases for study in STUDIES) == 280
    assert sum(study.trial_slots for study in STUDIES) == 1_680
    assert sum(study.web_searches for study in STUDIES) == 103
    assert round(sum(study.cost for study in STUDIES), 4) == 4.9013
    assert set(BILLED_COST_PER_EXECUTION) == {study.version for study in STUDIES}
    assert V09_EXTRACTION_READS == 60
    assert round(V09_EXTRACTION_COST, 4) == 0.2678
    for arms in (CANARY3_ARMS, CANARY5_ARMS):
        assert len(arms) == 4
        for arm in arms:
            assert 0 <= arm.passes <= 16 and 0 <= arm.unsafe <= 16 and 0 <= arm.reask <= 16
    assert sum(1 for reader in READERS if reader.reads) == 2
    assert all(reader.cost > FULL_ANSWER_COST for reader in READERS if reader.reads)
    assert all(reader.cost < FULL_ANSWER_COST for reader in READERS if not reader.reads)
    assert round(sum(canary.cost for canary in CANARIES), 4) == 0.9075
    assert sum(canary.calls for canary in CANARIES) == 321


def main() -> None:
    STATIC.mkdir(exist_ok=True)
    validate_data()
    input_chart()
    preservation_chart()
    cost_chart()
    billed_cost_chart()
    latency_chart()
    protocol_chart()
    paired_outcomes_chart()
    historical_pipeline()
    compiler_pipeline_v09()
    polaris_pipeline()
    canary_arms_chart()
    reader_economics_chart()
    canary_protocol_chart()


if __name__ == "__main__":
    main()
