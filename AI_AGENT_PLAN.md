# 45-Day AI Engineer Plan

**Dates:** Oct 27 → Dec 10, 2026
**Time:** about 2–3 hours a day (AI learning) + 30 min DSA
**Stack:** Python, Gemini (`google-genai`), ChromaDB, FastAPI, Docker
**Goal:** Get good at Gen AI, agentic AI and RAG, be interview-ready for AI Engineer / GenAI roles, and finish with a **fully deployed personal AI agent**.

Slipping a few days is fine: move the dates, but don't skip topics. Weeks 3 (RAG) and 4 (Evals) matter most.

---

## How we work

1. Claude teaches one concept, starting with a real-world analogy.
2. You write a **small exercise** (5–15 lines). Claude reviews it but doesn't write the solution unless you're stuck.
3. Add the next piece only after the current one works.
4. Write 3 lines in `LEARNINGS.md`: what you learned, what surprised you, what broke.
5. Push to GitHub every day.
6. **Move on only when you pass the "explain it" test:** you can explain the topic out loud in 2 minutes, without notes.

### Every topic is learned in 3 layers

| Layer | Question | Example (temperature) |
|---|---|---|
| **What** | What is it? | A setting that controls randomness |
| **How** | How does it work inside? | It rescales the probabilities of the next token before one is picked |
| **Why / when** | When do you use it, and what are the trade-offs? | Low for code and extraction, higher for brainstorming; 0 is still not fully deterministic |

Interviewers test the **How** and **Why** layers. Tutorials usually stop at **What**.

### Daily and weekly habits (for interview readiness)

- **Every day: 30 min of DSA**, separate from AI learning. 1 easy/medium LeetCode problem. Order: arrays → strings → hashmaps → two pointers → sliding window → stacks → linked lists → trees.
- **Every Sunday: interview drill.** Answer 3 conceptual questions on the week's topic + 1 AI system design question, out loud.

---

## Week 1 (Days 1–7): Gen AI foundations

*Goal: understand what an LLM actually does and control its output.*
Already done: basic calls (`LLM1.py`) and retries (`LLMRetry.py`), so review those quickly and go deep on the rest.

| Day | Topic | Exercise |
|---|---|---|
| 1 | How LLMs work: tokens, next-token prediction, context window | Count tokens for 3 prompts with `client.models.count_tokens` |
| 2 | Temperature, top-p, max tokens | Ask the same question at temp 0, 0.7 and 1.5 and compare |
| 3 | Prompt engineering: system prompts, few-shot, roles | Make the bot answer only as a "strict Python tutor" |
| 4 | Structured output: JSON + Pydantic schemas | Pull `{name, skills, years}` out of a resume paragraph |
| 5 | Streaming responses | Print the reply word by word |
| 6 | Errors, retries, timeouts, cost (review `LLMRetry.py`) | Add a cost-per-request print |
| 7 | 🏁 Milestone + Sunday drill | — |

**🏁 Milestone 1:** A CLI chatbot with conversation memory, a system persona, streaming output, and a `/extract` command that returns validated Pydantic JSON.

**Interview questions:** Why do outputs vary even at temperature 0? What happens when the context window is full? How do you get reliable JSON from an LLM?

---

## Week 2 (Days 8–14): Tool calling and the agent loop

*Goal: turn a chatbot into an agent that acts.*

| Day | Topic | Exercise |
|---|---|---|
| 8 | What makes something an "agent": LLM + tools + loop | Draw the loop on paper |
| 9 | Function declarations in Gemini | Declare one tool: `get_time()` |
| 10 | Dispatching: running the tool the model picks | Map tool names to Python functions with a dict |
| 11 | The agent loop: send the result back, repeat until a final answer | Loop with `max_steps=5` |
| 12 | Multiple tools + real APIs | Add a weather API + calculator |
| 13 | Tool errors and bad arguments | The tool raises → the agent recovers and retries |
| 14 | 🏁 Milestone + Sunday drill | — |

**🏁 Milestone 2:** A "Daily Assistant" agent with 3+ tools (weather, calculator, save/read notes to a file) that chains them on its own. Example: *"What's the weather in Delhi? Save it to my notes."*

**Interview questions:** Does the model run the tool itself? Why does every agent step cost more than the one before? What happens without a max-steps limit?

---

## Week 3 (Days 15–21): RAG (Retrieval-Augmented Generation)

*Goal: let the AI answer from your own data, with sources.*

| Day | Topic | Exercise |
|---|---|---|
| 15 | Why RAG: hallucination, knowledge cutoff, private data | Ask Gemini about your own notes and watch it fail |
| 16 | Embeddings: text becomes a vector | Embed 5 sentences and print vector length |
| 17 | Cosine similarity **from scratch** | Find the most similar sentence using plain Python math |
| 18 | Chunking strategies (size, overlap) | Split a long text file into overlapping chunks |
| 19 | Vector DB: ChromaDB | Store chunks and query the top 3 |
| 20 | Full pipeline: retrieve → augment prompt → generate + citations | Answer with `[source: file, chunk #]` |
| 21 | 🏁 Milestone + Sunday drill | — |

**🏁 Milestone 3:** "Chat with my PDFs": load a folder of PDFs and ask questions. Answers cite their sources and say "I don't know" when nothing relevant comes back.

**Interview questions:** Why can vector search miss an exact name or error code (hybrid search)? How does chunk size affect answers? RAG vs long context vs fine-tuning: when to use which?

---

## Week 4 (Days 22–28): Agentic patterns, memory and evals

*Goal: smarter agents, and proof that they work.*

| Day | Topic | Exercise |
|---|---|---|
| 22 | ReAct pattern (Reason + Act) | Make the agent print its "thought" before each action |
| 23 | Routing + planning | The agent writes a plan, then carries it out step by step |
| 24 | Reflection / self-critique | The agent checks its own answer before replying |
| 25 | Agentic RAG: retrieval as a *tool* | The agent decides: search docs, use tools, or just answer |
| 26 | Memory: short-term (history trimming) vs long-term (stored facts) | Remember the user's name across restarts |
| 27 | **Evals:** test sets, LLM-as-judge, retrieval hit rate | Write 10 Q&A pairs and score your RAG automatically |
| 28 | 🏁 Milestone + Sunday drill | — |

**🏁 Milestone 4:** An agentic RAG assistant with long-term memory, plus an `evals.py` that prints a score (e.g. "8/10 correct, retrieval hit rate 90%").

**Interview questions:** When is a fixed workflow better than an agent? How do you evaluate output that changes on every run? How do you know your LLM judge is trustworthy?

**System design practice starts this week:** e.g. "Design a customer-support RAG bot for 1M documents."

---

## Week 5 (Days 29–35): Production skills

*Goal: get it out of the terminal and into a real backend.*

| Day | Topic | Exercise |
|---|---|---|
| 29 | FastAPI basics (+ Python `async`/`await`) | A `/chat` POST endpoint |
| 30 | Wrap the agent in an API + sessions | Chat history per `session_id` |
| 31 | Streaming over HTTP (SSE) | Stream the agent's reply to the browser |
| 32 | Guardrails: prompt injection, input/output checks | Block "ignore previous instructions" attacks |
| 33 | Logging, tracing, cost tracking | Log every tool call + tokens used |
| 34 | MCP + frameworks overview (LangGraph): what they solve | Rebuild your loop in LangGraph and compare it to your own |
| 35 | 🏁 Milestone + **pick your capstone** + Sunday drill | — |

**🏁 Milestone 5:** Your agent runs as a FastAPI service with sessions, streaming, logs and basic guardrails.

**Interview questions:** What is prompt injection and why is there no complete fix? How would you cut an agent's cost without hurting quality? What does a framework hide from you?

---

## Week 6 (Days 36–42): Capstone build

*Goal: put everything together in one project you own.*

Capstone ideas (all use RAG + tools + memory):
1. **Study Buddy Agent:** upload notes/PDFs → it answers questions, makes quizzes, tracks weak topics and builds revision plans.
2. **Job Hunt Agent:** reads your resume + job descriptions → scores fit, rewrites bullets, drafts cover letters, tracks applications.
3. **Personal Knowledge Agent:** your notes, bookmarks and docs in one place → search, summarize and remind.

| Day | Work |
|---|---|
| 36 | Design: features, tools, data flow diagram |
| 37–38 | Core agent + tools |
| 39 | RAG over your data |
| 40 | Memory + guardrails |
| 41 | Simple frontend (Streamlit or plain HTML) |
| 42 | Evals for the capstone + fix failures |

The capstone must have: tools, an agent loop, RAG, memory, evals with numbers, guardrails, cost tracking, and a deployment.

---

## Days 43–45: Deploy, showcase and interview prep 🚀

| Day | Work |
|---|---|
| 43 | Dockerize the app, use env variables for secrets |
| 44 | Deploy to **Render** or **Google Cloud Run** (free tier), live public URL |
| 45 | README with an architecture diagram, 2-min demo video, LinkedIn post, ML basics revision, **full mock interview with Claude** |

**🏁 Final milestone:** A live, deployed AI agent with a URL, GitHub repo, eval results and demo video.

---

## Interview gaps this plan also covers

| Gap | Why it matters | Where it's covered |
|---|---|---|
| DSA / coding rounds | Most product companies have an online assessment + coding round | 30 min every day |
| System design | "Design a RAG system for 1M documents" is a common question | Sunday drills from Week 4, capstone design on Day 36 |
| Python depth | async, generators, decorators, OOP | Picked up along the way, especially in Week 5 |
| ML basics | Overfitting, train/test split, fine-tuning vs RAG | Day 45 revision |
| Explaining under pressure | Knowing something ≠ explaining it in an interview | Sunday drills + Day 45 mock interview |

---

## Progress tracker

- [ ] Week 1: Gen AI foundations (Milestone 1: CLI chatbot)
- [ ] Week 2: Tool calling + agent loop (Milestone 2: Daily Assistant)
- [ ] Week 3: RAG (Milestone 3: Chat with my PDFs)
- [ ] Week 4: Agentic patterns, memory, evals (Milestone 4: agentic RAG + `evals.py`)
- [ ] Week 5: Production (Milestone 5: FastAPI agent service)
- [ ] Week 6: Capstone build
- [ ] Days 43–45: Deploy + showcase + mock interview

---

## Reading list

- Anthropic: **"Building effective agents"** (Weeks 2 and 4)
- Anthropic: **"Writing effective tools for agents"** (Week 2)
- Anthropic: **"Effective context engineering for AI agents"** (Week 4)
- Hamel Husain's blog posts on evals (Week 4)
- **OWASP Top 10 for LLM Applications** (Week 5)
- Simon Willison's posts on prompt injection (Week 5)
- modelcontextprotocol.io (Week 5)

---

## Folder layout

```
python-practice/
├── AI_AGENT_PLAN.md       ← this file
├── LEARNINGS.md           ← 3 lines after every session
├── week1_genai_basics/
├── week2_tools_agents/
├── week3_rag/
├── week4_patterns_evals/
├── week5_production/
├── dsa/                   ← daily LeetCode solutions
└── capstone/
```



https://x.com/techyoutbe/status/2114267779083981044?s=20
