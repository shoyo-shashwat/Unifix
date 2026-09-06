# UNIFIX logo brief — prompt for an AI model

Two versions below. **Prompt A** is for a reasoning model (ChatGPT, Claude) that
will think through concepts and hand back SVG. **Prompt B** is the stripped-down
version for an image generator (DALL·E, Midjourney, GPT image).

Use A if you want options you can actually ship. Use B if you want to look at
pictures first.

---

## Prompt A — for a reasoning model (returns SVG)

> You are a brand designer. Design a logo mark for the product described below.
> Give me **three distinct concepts**, each as clean flat SVG code plus one
> sentence explaining what it means. No lettering in any of them.
>
> **The product**
> UNIFIX is a campus grievance and infrastructure platform for GL Bajaj
> Institute of Technology & Management in Greater Noida, India. Staff photograph
> something broken at a specific place on campus — a dead ceiling fan in AB2, a
> leaking tap in the hostel block, a failed lab socket — and file it in about
> fifteen seconds. The report is auto-classified, routed to the right unit
> (Electrical, Plumbing, Civil, IT), tracked through a fixed set of statuses,
> verified by an administrator, and closed. Every step is logged and visible.
>
> **Who sees it**
> College staff aged roughly 25–60 on Android phones, with mixed comfort using
> apps. Also senior administrators and the institute's leadership. This is an
> internal accountability tool, not a consumer social product, so it has to look
> institutional and credible rather than playful or startup-ish.
>
> **What the mark must visualise**
> The promise is not "report problems" — anyone can complain. The promise is
> that a reported problem **comes back closed**. Follow-through is the whole
> product. Nothing sits in a drawer.
>
> Build the mark from one or more of these ideas, but find your own form for
> them:
> - **A specific place.** Every issue happens somewhere real and nameable.
> - **Closure.** Something completed, verified, signed off — a loop that returns
>   to its start, a circuit that connects, a state that resolves.
> - **Transparency.** The outcome is visible to everyone, not buried. Negative
>   space is a good tool for this.
> - **One campus.** The "UNI" in the name — many buildings, departments and
>   trades acting as a single system.
>
> **Tone**
> Civic infrastructure. Municipal utility, public works, signage. Calm,
> trustworthy, permanent. Confident rather than clever.
>
> **Hard constraints**
> - Flat vector. One continuous idea, not an assembly of parts.
> - Must read at **16 px** as a favicon.
> - Must work in **a single colour**, and knocked out in white on navy.
> - Compact, roughly square silhouette — it has to sit inside the middle of a
>   printed QR code at about 15 mm across and still be recognisable.
> - Transparent background. No text, letters or wordmark.
>
> **Palette**
> - `#0E2F5C` navy — primary, structure, trust
> - `#12885A` green — resolution, a closed issue
> - `#1E5FBF` blue — an issue in progress
> The mark must survive being reduced to navy alone.
>
> **Do not use**
> Gradients, 3D, bevels, gloss, drop shadows, swooshes, globes, gears, speech
> bubbles, generic person icons, wrenches or hammers (too literally "repair"),
> a clipart checkmark inside a circle, or any lettering. Nothing so detailed it
> dies at small size.

---

## Prompt B — for an image generator

> Flat vector logo mark, no text, for a campus infrastructure repair-tracking
> app used by college staff in India. The idea: a problem reported at a specific
> place always comes back resolved — follow-through and visible closure.
> Minimal geometric symbol combining a sense of place with a sense of
> completion, using negative space. Institutional and civic, like public-works
> signage — calm and permanent, not playful. Solid deep navy #0E2F5C on a
> transparent background, single colour, no gradients, no shadows, no 3D, no
> lettering. Bold simple silhouette that stays legible at 16 pixels. Centred,
> compact, roughly square.

---

## Two notes before you paste it

**The existing direction.** The mark already in this folder is a map pin with a
checkmark cut clean through its centre — place, plus closure, plus transparency,
in one shape. If you want genuinely different options, add to the prompt: *"Do
not propose a map pin with a checkmark; that direction is already taken."* If
you want variations on it instead, say so explicitly.

**Image generators cannot do text.** Ask only for the symbol. Set the word
UNIFIX yourself afterwards, or reuse the drawn wordmark in
`unifix-logo-horizontal.svg`.
