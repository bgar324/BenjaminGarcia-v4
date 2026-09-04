# Benjamin Garcia Portfolio

Personal portfolio for Benjamin Garcia, written in plain HTML and CSS and deployed on Vercel.

Live site: [bentgarcia.com](https://bentgarcia.com)

## Overview

This repository contains a deliberately minimal, static portfolio with five public routes:

- `/` - introduction, experience, selected work, about, and contact links
- `/projects` - a chronological collection of projects with live-site and source links
- `/blog/annie` - a case study about building Annie, a personal iMessage assistant
- `/blog/policyc` - a case study about testing request-specific policy compilation
- `/blog/logit` - a case study about designing a workout logger that gets out of the way

The interface uses a single-column charcoal layout, a conventional system-font scale, and underline-to-fill link interactions. There is no JavaScript, build step, framework, theme toggle, navigation shell, or UI state to maintain.

## Highlights

- Plain HTML and CSS with zero JavaScript and zero dependencies
- Responsive single-column layout for desktop and mobile
- Accessible keyboard focus states and reduced-motion handling
- Immediate content rendering with no entrance animation or font download
- Canonical metadata, structured data, sitemap, robots, and web manifest
- Native system font stack with standard 400, 500, and 600 weights
- Resume and PolicyC paper served as public PDF assets

## Project Structure

```text
index.html            Home page
projects/index.html   Complete project collection
blog/annie/index.html   Blog article about Annie
blog/policyc/index.html Blog article about PolicyC
blog/logit/index.html  Blog article about Logit
404.html              Custom 404 page
styles.css            Layout, typography, and interaction styles
scripts/generate-policyc-charts.py   Regenerates the PolicyC SVG figures
static/favicon.svg
static/annie-imessage-conversation.webp
static/annie-deepseek-usage.webp
static/logit-workout.webp
static/logit-workout-square.webp
static/logit-iterations.png
static/logit-logged-today.svg
static/policyc-input-reduction.svg
static/policyc-preservation.svg
static/policyc-cost-reduction.svg
static/policyc-billed-cost.svg
static/policyc-latency.svg
static/policyc-compiler-pipeline.svg
static/policyc-compiler-pipeline-v09.svg
static/policyc-study-protocol.svg
static/policyc-paired-outcomes.svg
manifest.webmanifest
sitemap.xml
robots.txt
policyc.pdf
resume.pdf
vercel.json           Buildless deploy overrides, clean URLs, cache headers
```

`vercel.json` pins `framework`, `buildCommand`, `installCommand`, and
`outputDirectory` to `null`. The Vercel project predates this rewrite and still
carries the old Astro framework preset, so those keys are what force a buildless
static deploy. Removing them makes Vercel fall back to the preset and the
deployment fails with no `package.json` to build.

## Local Development

No install or build step. Serve the directory with any static file server:

```bash
python3 -m http.server 8000
```

Open [localhost:8000](http://localhost:8000).

## Editing Content

- Update homepage structure and copy in `index.html`.
- Update the project collection in `projects/index.html`.
- Update global visual styling and motion in `styles.css`.
- Add portfolio articles under `blog/<slug>/index.html` and their images under `static/`.
- Run `python3 scripts/generate-policyc-charts.py` after changing PolicyC study data or figure copy.
- Replace `resume.pdf` or `policyc.pdf` to publish newer document versions at the same URLs.

No environment variables are required.
