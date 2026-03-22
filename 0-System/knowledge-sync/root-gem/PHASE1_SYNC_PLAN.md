# PHASE 1 EXECUTION PLAN & MEMORY HANDOVER (AI-to-AI)

**To: Gemini Agent on Victory & Surface**
**From: Gemini Agent on U22 (Local)**
**Date: 2026-03-20**

## Context & Background Memory
I am the Gemini Agent running on the U22 environment. I have just completed deep structural repairs and preparations. Here is the critical context you need to inherit:
1. **Network Connectivity**: I have fixed the RDP Firewall isolation on Victory (`172.16.2.97`) and opened port 3389 to any IP (so the hiwifi router can proxy to it). I also fixed the strict `administrators_authorized_keys` ACLs on Windows OpenSSH.
2. **WSL SSH**: Direct SSH to Windows lands in Session 0, making WSL inaccessible directly. The optimal path is to use Git Bash as the default Windows OpenSSH shell. (Which I've recommended to the user).
3. **Repository State**: 
   - `aihub-mycc` on U22 had a severely corrupted `.git/HEAD` and broken blob hashes. It must be abandoned.
   - `aihub` (Monorepo) on U22 has local uncommitted changes (intranet-hub.html, voice_test.mp3, etc.).
   - `mycc` on CC server has extensive uncommitted changes (feishu/dingtalk v2 bots).
4. **Scnet/Nim Claude Error**: I just hotfixed the local `free-claude-code` and `mycc` environments on U22 to fallback to `nvidia_nim` because the `scnet` upstream was injecting `<think>` tags that broke the Claude CLI streaming parser ("Interrupted" bug).

## Your Mission: Execute Phase 1 (Data Rescue & Base Setup)

As the resident Gemini on **Victory** (Windows - Data Center) and **Surface** (Ubuntu - Edge Node), you are to carry out the following:

### Task for Victory (Data Center)
1. **Target Directory**: The `aihub` project on Victory is located at `D:\python\aihub` (NOT the C: drive). All operations must be directed here.
2. **Initialize the Private Lab Repo**: Since Victory is the 24/7 stable node with high capacity, create a bare Git repository to act as the central "Lab Repo" for all sensitive `aihub` and `mycc` full-data configurations.
3. **Receive U22's Code**: Guide the user to push the cleaned-up `aihub` from U22 directly to this new Victory Lab Repo.
4. **WeChat Bot Prep**: Setup the scaffolding for the WeChat integration. Keep in mind Victory will *not* use Clash VPN continuously, so all API routing must be stable domestic (e.g., Qwen/SCNET) or proxied through CC.

### Task for Surface (Edge Node)
1. **Repository Sync**: Clone the new Victory Lab Repo.
2. **Network Operations**: Surface is a clean XUbuntu environment, so it can safely keep Clash open. It should handle "radical" network deployments. (Check Clash startup scripts).
3. **Lobster & Qwen Verification**: Ensure the local Qwen model and Lobster voice services are stable and properly exposed via the intranet for U22/Victory to call as fallbacks. 

## ⚠️ Transferred Experience & Known Pitfalls
I have resolved several critical blockers. Do not repeat these mistakes:
1. **Windows OpenSSH ACLs**: If you configure SSH keys on Windows, `C:\ProgramData\ssh\administrators_authorized_keys` must ONLY have `SYSTEM` and `Administrators` permissions. NO inherited `Authenticated Users` allowed, or it falls back to password.
2. **Windows Session 0 Isolation**: Executing WSL directly from a background SSH session to Windows will fail (LxssManager cannot find the GUI session). Advise using Git Bash as the DefaultShell or running a native OpenSSH inside WSL itself.
3. **Cross-Platform Scripting (PowerShell)**: When pushing `.ps1` scripts from Linux to Windows via SSH/SCP, use **pure ASCII/English** text. UTF-8 Chinese characters will be mangled by Windows' default local encoding, causing syntax parser errors (e.g., swallowing quotation marks).
4. **Git Corruption**: If a `.git` repo reports `fatal: bad object HEAD` with missing blobs, the hash tree is broken (likely from power loss or bad sync). Do not try to commit; move the files to a newly initialized repo.
5. **Scnet / Nim Proxy Crash**: Scnet injects `<think>` tags that break streaming parsers in terminals. If Claude Code throws "Interrupted", fallback the API priority to `nvidia_nim` or `unicloud` immediately.


## Execution Directives
- **Do not mix** the minimalist `aihub` architecture with the deep `.claude/skills` directory tree of `mycc`.
- **MyCC Upstream**: Ensure the CC server's `mycc` tracks `vickioo/mycc` as `origin` and `Aster110/mycc` as `upstream`.
- When you initialize, parse this document, understand your role, and begin executing your specific device tasks. Prompt the user for approval before running destructive git commands.

---
*End of Handover.*
