#!/usr/bin/env python3
"""Regenerate the GUARD Framework figures into docs/figures/.

Requires: matplotlib. Run from the repo root:
    python3 docs/generate_figures.py

The figures are documentation assets. They are not required to install or run
the skill (SKILL.md + references/ are self-contained); they illustrate the
full playbook in docs/GUARD-Framework.md.
"""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

INK, FAINT, PANEL, EDGE = "#1F2937", "#6B7280", "#F8FAFC", "#D1D5DB"
ACCENT, GILT = "#0E7C86", "#AD8A45"
GREEN, AMBER, RED = "#2F7D4F", "#B45309", "#B3352B"

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)


def box(ax, x, y, w, h, title, sub, fc="white", ec=EDGE, tc=INK, tfs=11, sfs=8.2, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.025",
                                fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center", fontsize=tfs, color=tc, fontweight="bold")
    ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=sfs, color=FAINT, linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.6, style="-|>", ms=14, conn="arc3,rad=0"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, connectionstyle=conn))


def fig1():
    years = ["2020", "2021", "2022", "2023", "2024"]
    vals = [0.70, 0.48, 0.45, 1.80, 6.66]
    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=160)
    fig.patch.set_facecolor("white")
    ax.bar(years, vals, color=ACCENT, width=0.62)
    ax.set_title("Commits Containing a Duplicated Code Block, by Year (%)",
                 fontsize=12, fontweight="bold", color=INK)
    ax.set_xlabel("Year code was authored", color=FAINT)
    ax.set_ylabel("% of commits with a duplicated block", color=FAINT)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.12, f"{v:.2f}", ha="center", fontsize=9, color=INK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=FAINT)
    ax.set_ylim(0, 7.4)
    fig.text(0.5, 0.01, "GitClear analysis of 211M changed lines; median duplicated block ~ 10 lines",
             ha="center", fontsize=8, color=FAINT)
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(f"{OUT}/fig1-duplication-surge.png", bbox_inches="tight", facecolor="white")
    plt.close()


def fig2():
    phases = [
        ("PHASE 0\nBASELINE LOCK", "behavior snapshot\nmetrics baseline\nrollback point"),
        ("PHASE 1\nDEEP SCAN", "static tooling\n+ LLM semantic\npass (dual-track)"),
        ("PHASE 2\nEVIDENCE TRIAGE", "confidence score\nfalse-positive\nfilter - risk tier"),
        ("PHASE 3\nUSER WIZARD", "scope, appetite,\nconstraints -\nuser decides"),
        ("PHASE 4\nPLAN SYNTHESIS", "ordered task cards\nverify cmds +\nrollback per task"),
        ("PHASE 5\nGUARDED\nEXECUTION", "one task -> verify\n-> atomic commit\nor auto-revert"),
    ]
    W, H, Y0, GAP, x0 = 1.78, 1.55, 1.75, 0.28, 0.35
    fig, ax = plt.subplots(figsize=(13.2, 5.0), dpi=160)
    ax.set_xlim(0, 13.2); ax.set_ylim(0.55, 4.35); ax.axis("off")
    fig.patch.set_facecolor("white")
    for i, (t, s) in enumerate(phases):
        x = x0 + i * (W + GAP)
        box(ax, x, Y0, W, H, t, s, tfs=10, sfs=8.0)
        if i < len(phases) - 1:
            arrow(ax, x + W + 0.02, Y0 + H / 2, x + W + GAP - 0.02, Y0 + H / 2, lw=1.5)
    for gx, label in [(x0 + 2 * (W + GAP) - GAP / 2, "GATE A - user approves findings"),
                      (x0 + 4 * (W + GAP) - GAP / 2, "GATE B - user approves plan")]:
        ax.scatter([gx], [Y0 + H + 0.33], marker="D", s=240, color=GILT, zorder=5)
        ax.text(gx, Y0 + H + 0.33, "U", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
        ax.text(gx + 0.42, Y0 + H + 0.33, label, ha="left", va="center", fontsize=8.2, color=GILT, fontweight="bold")
    vx = x0 + 5 * (W + GAP); loop_y = 0.62
    box(ax, vx - 0.1, loop_y, W + 0.2, 0.78, "VERIFY & CLOSE-OUT",
        "equivalence proof - metrics delta - report", fc=PANEL, tfs=8.8, sfs=7.4)
    arrow(ax, vx + W / 2, Y0 - 0.02, vx + W / 2, loop_y + 0.78 + 0.02, color=ACCENT, lw=1.6)
    mid_x = x0 + 3 * (W + GAP) + W / 2
    arrow(ax, vx - 0.14, loop_y + 0.39, mid_x + 0.05, loop_y + 0.39, color=FAINT, lw=1.1, style="-")
    arrow(ax, mid_x, loop_y + 0.39, mid_x, Y0 - 0.02, color=FAINT, lw=1.1)
    ax.text((vx + mid_x) / 2, loop_y + 0.52, "mismatch -> re-triage / adjust scope (never force-fit)",
            fontsize=7.6, color=FAINT, ha="center")
    ax.text(0.35, 4.08, "The GUARD Framework - one-way pipeline, two user gates, one verification loop",
            fontsize=13, fontweight="bold", color=INK)
    ax.text(0.35, 3.72, "Ground truth -> Uncover -> Arbitrate -> Roadmap -> Deliver.   <> = mandatory user decision point",
            fontsize=9, color=FAINT)
    plt.savefig(f"{OUT}/fig2-guard-pipeline.png", bbox_inches="tight", facecolor="white")
    plt.close()


def fig3():
    cols = ["STRONG SAFETY NET\ncharacterization tests +\ngolden master at touch point",
            "PARTIAL SAFETY NET\nsome unit tests /\ntype checks only",
            "NO SAFETY NET\nnothing verifies\nbehavior here"]
    rows = [("DATA / EXTERNAL CONTRACT\nschema, API payloads, DB", ["T3", "T3", "T3"]),
            ("CROSS-MODULE\npublic API, shared utils", ["T2", "T3", "T3"]),
            ("MODULE-INTERNAL\ncomponents, services", ["T1", "T2", "T3"]),
            ("PURE / LEAF\nprivate functions, format", ["T0", "T1", "T2"])]
    TIER = {"T0": (GREEN, "auto-approvable"), "T1": (ACCENT, "standard verify"),
            "T2": (AMBER, "elevated - GM + diff review"), "T3": (RED, "critical - flag + staged + sign-off")}
    gx, gy, cw, ch = 3.15, 0.85, 2.28, 1.02
    fig, ax = plt.subplots(figsize=(10.6, 7.2), dpi=160)
    ax.set_xlim(0, 10.6); ax.set_ylim(0, 7.2); ax.axis("off")
    fig.patch.set_facecolor("white")
    for j, c in enumerate(cols):
        ax.text(gx + j * cw + cw / 2, gy + 4 * ch + 0.55, c, ha="center", va="center",
                fontsize=7.8, color=INK, fontweight="bold", linespacing=1.3)
    for i, (rl, tiers) in enumerate(rows):
        ry = gy + (3 - i) * ch
        ax.text(gx - 0.18, ry + ch / 2, rl, ha="right", va="center", fontsize=7.8, color=INK,
                fontweight="bold", linespacing=1.3)
        for j, t in enumerate(tiers):
            color, desc = TIER[t]
            ax.add_patch(FancyBboxPatch((gx + j * cw + 0.05, ry + 0.06), cw - 0.1, ch - 0.12,
                                        boxstyle="round,pad=0.008,rounding_size=0.03", fc=color, ec="none", alpha=0.92))
            ax.text(gx + j * cw + cw / 2, ry + ch * 0.60, t, ha="center", va="center", fontsize=13,
                    color="white", fontweight="bold")
            ax.text(gx + j * cw + cw / 2, ry + ch * 0.26, desc, ha="center", va="center", fontsize=6.6, color="white")
    ax.text(gx + 1.5 * cw, gy + 4 * ch + 1.42, "VERIFICATION STRENGTH AT THE TOUCH POINT ->",
            ha="center", fontsize=9.5, color=FAINT, fontweight="bold")
    ax.text(0.5, gy + 2 * ch, "BLAST RADIUS  ->", rotation=90, va="center", fontsize=9.5, color=FAINT, fontweight="bold")
    ax.text(0.4, 6.85, "Protocol Tier Matrix - every finding is routed to a change protocol, not a hunch",
            fontsize=12.5, fontweight="bold", color=INK)
    ax.text(0.4, 6.48, "Tier is decided by (what could break) x (what would catch it). Data-touching changes are always T3.",
            fontsize=8.8, color=FAINT)
    plt.savefig(f"{OUT}/fig3-risk-tier-matrix.png", bbox_inches="tight", facecolor="white")
    plt.close()


def fig4():
    Ww, Wh, row1_y, row2_y, xs = 3.55, 1.28, 4.05, 1.85, [0.45, 4.62, 8.79]
    wiz_top = [("W1 - TRIGGER", "Why this run, why now?\nroutine hygiene - pre-release\nhardening - perf pain - post-incident"),
               ("W2 - SCOPE", "What may be touched?\nwhole repo - named modules -\nhotspot list only (churn x complexity)"),
               ("W3 - APPETITE", "Change profile?\nConservative (T0-T1) - Balanced\n(+T2) - Accelerated (+T3 w/ sign-off)")]
    wiz_bot = [("W4 - SAFETY NET", "What proves behavior today?\ntests+GM - tests only - nothing\n-> nothing = Phase 0 work FIRST"),
               ("W5 - AUTONOMY", "Where are the brakes?\napprove every task - every batch -\nplan-only + final report"),
               ("W6 - DELIVERY", "How do changes land?\nPR per task - PR per phase -\nsingle integration branch")]
    fig, ax = plt.subplots(figsize=(12.6, 6.4), dpi=160)
    ax.set_xlim(0, 12.6); ax.set_ylim(0, 6.4); ax.axis("off")
    fig.patch.set_facecolor("white")
    for i, (t, s) in enumerate(wiz_top):
        box(ax, xs[i], row1_y, Ww, Wh, t, s, tfs=10, sfs=7.8)
        if i < 2:
            arrow(ax, xs[i] + Ww + 0.03, row1_y + Wh / 2, xs[i + 1] - 0.03, row1_y + Wh / 2, lw=1.5)
    arrow(ax, xs[2] + Ww / 2, row1_y - 0.03, xs[2] + Ww / 2, row2_y + Wh + 0.03, lw=1.5)
    for i, (t, s) in enumerate(wiz_bot):
        x = xs[2 - i]
        box(ax, x, row2_y, Ww, Wh, t, s, tfs=10, sfs=7.8,
            fc=("#FDF6EC" if t.startswith("W4") else "white"), ec=(GILT if t.startswith("W4") else EDGE))
    for xf, xt in [(xs[2], xs[1]), (xs[1], xs[0])]:
        arrow(ax, xf - 0.03, row2_y + Wh / 2, xt + Ww + 0.03, row2_y + Wh / 2, lw=1.5)
    ax.text(xs[2] + Ww / 2, row2_y - 0.28, "hard rule: no safety net => characterize before any change (Feathers)",
            ha="center", fontsize=7.8, color=GILT, fontweight="bold")
    out_y = 0.28
    box(ax, 3.1, out_y, 6.4, 0.92, "OUTPUT - PLAN CONFIGURATION  ->  GATE B",
        "selections compile into guard-config.json + PLAN.md the agent executes", fc=PANEL, tfs=10.5, sfs=8)
    arrow(ax, xs[0] + Ww / 2, row2_y - 0.03, xs[0] + Ww / 2, out_y + 0.92 + 0.02, lw=1.5, conn="arc3,rad=-0.25")
    ax.text(0.45, 6.05, "The User Wizard - six decisions that turn analysis into a user-owned execution plan",
            fontsize=12.5, fontweight="bold", color=INK)
    ax.text(0.45, 5.68, "The agent asks; the user decides. Every answer maps to concrete guard-rails in the generated plan.",
            fontsize=8.8, color=FAINT)
    plt.savefig(f"{OUT}/fig4-wizard-flow.png", bbox_inches="tight", facecolor="white")
    plt.close()


def fig5():
    fig, ax = plt.subplots(figsize=(12.6, 5.6), dpi=160)
    ax.set_xlim(0, 12.6); ax.set_ylim(0, 5.6); ax.axis("off")
    fig.patch.set_facecolor("white")
    cx, cy = 3.0, 2.75
    nodes = ["suite", "review", "gate", "monitor"]
    pos = {}
    for i, n in enumerate(nodes):
        ang = math.pi / 2 - i * (2 * math.pi / len(nodes))
        pos[n] = (cx + 1.55 * math.cos(ang), cy + 1.35 * math.sin(ang))
    for n in nodes:
        x, y = pos[n]
        ax.add_patch(FancyBboxPatch((x - 0.62, y - 0.34), 1.24, 0.68,
                                    boxstyle="round,pad=0.01,rounding_size=0.04", fc="white", ec=RED, lw=1.4))
        ax.text(x, y, n, ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
    for i in range(len(nodes)):
        a = pos[nodes[i]]; b = pos[nodes[(i + 1) % len(nodes)]]
        arrow(ax, a[0], a[1], b[0], b[1], color=RED, lw=1.3, conn="arc3,rad=-0.28", ms=11)
    ax.text(cx, cy, "internally\nconsistent,\ntouches nothing", ha="center", va="center", fontsize=9, color=RED, style="italic")
    ax.text(cx, 5.15, "CIRCULAR - every loop watches another loop", ha="center", fontsize=10.5, color=RED, fontweight="bold")
    ax.text(cx, 0.55, '"truthful about itself, worthless as evidence"', ha="center", fontsize=8.5, color=FAINT)
    ax.plot([6.3, 6.3], [0.7, 5.0], color=EDGE, lw=1, ls="--")
    rx = 9.45
    chain = [("DIFF", "code change"), ("SUITE", "executes it"), ("GATE", "commands exit 0")]
    yy = 3.55
    for i, (n, sub) in enumerate(chain):
        x = 7.0 + i * 2.05
        box(ax, x, yy, 1.8, 0.95, n, sub, tfs=10, sfs=7.6)
        if i < 2:
            arrow(ax, x + 1.82, yy + 0.47, x + 2.03, yy + 0.47, lw=1.4)
    ax_x = 7.0 + 2 * 2.05
    box(ax, ax_x, 1.35, 1.8, 0.95, "ANCHOR", "the world, measured\ndirectly", fc="#FBF3E4", ec=GILT, tc=GILT, tfs=10, sfs=7.6, lw=1.6)
    arrow(ax, ax_x + 0.9, yy - 0.02, ax_x + 0.9, 1.35 + 0.95 + 0.02, color=GILT, lw=1.8)
    ax.text(ax_x + 0.9, 0.95, "deploy alias serves new SHA - runtime mode live -\nendpoint binds a port - named test goes RED on revert",
            ha="center", fontsize=7.6, color=FAINT)
    ax.text(rx, 5.15, "ANCHORED - a claim terminates at the world", ha="center", fontsize=10.5, color=GREEN, fontweight="bold")
    ax.text(rx, 0.55, "three verdicts: ANCHORED - UNANCHORED - UNKNOWN (blocks)", ha="center", fontsize=8.5, color=GILT, fontweight="bold")
    plt.savefig(f"{OUT}/fig5-anchors.png", bbox_inches="tight", facecolor="white")
    plt.close()


def fig6():
    rungs = [("V0 - CLAIM", "the agent asserts it", "trust nothing - a claim is not evidence", RED, 0.16),
             ("V1 - RAN", "the command executed and exited 0", "necessary, not sufficient - green != safe", AMBER, 0.30),
             ("V2 - PRESENT & NON-EMPTY", "the check's subject exists and is non-trivial", "guards 'satisfiable by absence'", "#7A6C2F", 0.46),
             ("V3 - FALSIFICATION-SURVIVOR", "tried hard to disprove the claim; failed", "required for every NEGATIVE claim", ACCENT, 0.62),
             ("V4 - MUTATION-PROVEN", "revert/break the code -> the NAMED test goes RED", "proves the net catches this change", GREEN, 0.80),
             ("V5 - ANCHORED", "a measurement from the world, not a report about one", "the only verdict that closes a T2/T3 change", GILT, 1.0)]
    base_x, top_y, rung_h = 0.5, 4.7, 0.66
    fig, ax = plt.subplots(figsize=(12.4, 6.2), dpi=160)
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 6.2); ax.axis("off")
    fig.patch.set_facecolor("white")
    for i, (t, sub, note, color, strength) in enumerate(rungs):
        y = top_y - i * (rung_h + 0.08)
        ax.add_patch(FancyBboxPatch((base_x, y), 5.6, rung_h, boxstyle="round,pad=0.008,rounding_size=0.03",
                                    fc=color, ec="none", alpha=0.94))
        ax.text(base_x + 0.22, y + rung_h * 0.62, t, ha="left", va="center", fontsize=10.5, color="white", fontweight="bold")
        ax.text(base_x + 0.22, y + rung_h * 0.26, sub, ha="left", va="center", fontsize=7.7, color="white")
        ax.text(base_x + 5.85, y + rung_h / 2, note, ha="left", va="center", fontsize=8.2, color=INK)
        ax.add_patch(FancyBboxPatch((11.0, y + 0.06), 1.15, rung_h - 0.12, boxstyle="round,pad=0.004,rounding_size=0.02",
                                    fc=PANEL, ec=EDGE, lw=0.8))
        ax.add_patch(FancyBboxPatch((11.0, y + 0.06), 1.15 * strength, rung_h - 0.12,
                                    boxstyle="round,pad=0.004,rounding_size=0.02", fc=color, ec="none", alpha=0.85))
    arrow(ax, base_x - 0.18, 0.7, base_x - 0.18, 5.35, lw=1.6, ms=15)
    ax.text(base_x - 0.4, 3.0, "INCREASING STRENGTH OF PROOF", rotation=90, va="center", fontsize=9, color=FAINT, fontweight="bold")
    ax.text(0.5, 5.85, "The Verification Ladder - match the rung to the tier, never settle for V1 on a risky claim",
            fontsize=12.5, fontweight="bold", color=INK)
    ax.text(0.5, 5.5, "GUARD v2 routing: T0 needs V2 - T1 needs V3 - T2 needs V4 - T3 needs V5.  \"The suite is green\" lives at V1.",
            fontsize=8.8, color=FAINT)
    plt.savefig(f"{OUT}/fig6-verification-ladder.png", bbox_inches="tight", facecolor="white")
    plt.close()


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print("Wrote 6 figures to", OUT)
