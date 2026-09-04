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
    body.extend(
        [
            line(155, target_y, 1090, target_y, stroke=RUST, stroke_width=2, stroke_dasharray="9 8"),
            text(1080, target_y - 12, "95% target", text_anchor="end", fill=RUST, font_size=19),
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
    ) + ". Every result was below the 95 percent target. The intervals are descriptive because samples are clustered by case, and every version used a different held-out set. More preservation is better; less is worse."
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
        "Every version used a different held-out set. More reduction is better; less is worse."
    )
    write_svg("policyc-cost-reduction.svg", 1130, 762, "PolicyC execution-cost reduction across compiler versions", description, body)


def billed_cost_chart() -> None:
    body = chart_frame(
        "Measured billed cost per execution",
        "Full policy vs compiled slice",
        "Actual spend; tool fees included",
    )
    body.extend(
        [
            f'<rect x="40" y="89" width="17" height="17" fill="{GRAY}" stroke="{INK}" stroke-width="1.5" />',
            text(70, 104, "Full policy", font_size=20, font_weight=600),
            f'<rect x="205" y="89" width="17" height="17" fill="{SAGE}" stroke="{INK}" stroke-width="1.5" />',
            text(235, 104, "Compiled slice", font_size=20, font_weight=600),
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
    description = "Actual measured billed cost per execution for the full policy and compiled slice was " + "; ".join(
        f"{full_cost:.6f} dollars and {compiled_cost:.6f} dollars for compiler {study.version}, a {study.billed_reduction:.2f} percent reduction"
        for study in STUDIES
        for full_cost, compiled_cost in (BILLED_COST_PER_EXECUTION[study.version],)
    ) + (
        ". Versions 0.5 through 0.7 use all planned executions; versions 0.8 and 0.9 use complete pairs, matching each frozen audit's reported efficiency basis. "
        "Both series are measured spend, not forecasts. Less cost is better; more is worse."
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
        text(835, 148, "Full / exec", text_anchor="end", fill=MUTED, font_size=16, font_weight=600),
        text(965, 148, "Compiled / exec", text_anchor="end", fill=MUTED, font_size=16, font_weight=600),
        text(1090, 148, "Run total", text_anchor="end", fill=MUTED, font_size=16, font_weight=600),
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
            text(380, 614, "359 of 360 calls issued; one stopped at the call ceiling", fill=MUTED, font_size=17),
            text(62, 644, "Compiler 0.9 frontend", font_size=17, font_weight=600),
            text(380, 644, f"{V09_EXTRACTION_READS} extractor calls · ${V09_EXTRACTION_COST:.4f}, reported separately", fill=MUTED, font_size=17),
            text(62, 674, "Per-execution costs", font_size=17, font_weight=600),
            text(380, 674, "Actual billed spend · each frozen audit's reported basis", fill=MUTED, font_size=17),
            text(62, 704, "Paired-execution total", font_size=17, font_weight=600),
            text(380, 704, "280 cases · 1,680 planned trial slots · 103 searches · $4.9013", fill=MUTED, font_size=17),
        ]
    )
    description = "; ".join(
        (
            f"Compiler {study.version} used {study.cases} cases, {study.trial_slots} planned trial slots, "
            f"{study.complete_pairs} of {study.planned_pairs} complete pairs, {study.web_searches} web searches, "
            f"{full_cost:.6f} dollars per full-policy execution, {compiled_cost:.6f} dollars per compiled execution, "
            f"and {study.cost:.4f} dollars across all issued paired-study calls"
        )
        for study in STUDIES
        for full_cost, compiled_cost in (BILLED_COST_PER_EXECUTION[study.version],)
    ) + (
        f". Compiler 0.9 also used {V09_EXTRACTION_READS} compile-time extractor calls costing "
        f"{V09_EXTRACTION_COST:.4f} dollars, reported separately. Per-execution costs follow each frozen audit's reported efficiency basis. "
        "Every version used a newly authored held-out set."
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


if __name__ == "__main__":
    main()
