---
layout: post
title: "For VS code users: how to force a line width"
date: 2025-11-03
comments: true
---

I find using Github PRs a great way of reviewing writing as well as code. 
This
usually leads to a conversation about forcing a character length instead of the
visual line wrapping when using VS code. As I'm not a VS code user myself I am often
not able to show students who to do this.

Here is how to do this:

### Steps

1. **Install the Rewrap extension**
   - Open the Command Palette: `Cmd/Ctrl + Shift + P`
   - Type `Extensions: Install Extensions`
   - Search for **“Rewrap”** by *stkb* and install it

2. **Set your preferred column width**
   - Open Settings (`Cmd/Ctrl + ,`)
   - Search for: `Rewrap: Column`
   - Set a value such as `80`

3. **Use it manually**
   - Select the text (or place the cursor in a paragraph)
   - Run the command:
     ```
     Rewrap: Rewrap Comment / Text at Column
     ```
     (default shortcut: `Alt + Q`)

4. **Optional: Auto-format on save**
   - Add this to your `settings.json`:
     ```json
     "[markdown]": {
       "editor.defaultFormatter": "stkb.rewrap",
       "editor.formatOnSave": true
     }
     ```
   - Replace `[markdown]` with any other language block if needed, e.g.
     `[plaintext]`

### Notes

- `Rewrap` inserts **real line breaks** in the file.
- `editor.wordWrap` and `editor.rulers` only affect *visual appearance* — they
  do not modify the text itself.
