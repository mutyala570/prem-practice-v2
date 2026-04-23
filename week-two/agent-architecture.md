# Week 2 — Agent Architecture Notes

## Topics Covered in This Document

1. [**The Corrected Agent Flow**](#1-the-corrected-agent-flow)
2. [**The Four Memory Types and How They Are Implemented**](#2-the-four-memory-types-and-how-they-are-implemented)
3. [**Function Calling / Tool Use at the API Level**](#3-function-calling--tool-use-at-the-api-level)
4. [**When to Choose RAG vs. Tools (Decision Framework)**](#4-when-to-choose-rag-vs-tools-decision-framework)

---

# 1. The Corrected Agent Flow

A modern AI agent is a system that takes a user's question, decides what to do with it, and returns an answer. The agent uses an LLM as its central reasoning engine, and routes each question through the right path — memory, tools, or RAG — depending on what the question needs. The complete flow has six steps.

## Step 1 — User Asks a Question

The user sends a question to the agent. This is the entry point into the system.

## Step 2 — LLM Reasoning Decides the Route

The question goes to the LLM, which uses **reasoning and planning** to decide the right path. In modern agent frameworks this routing is done directly by the LLM, typically through **function calling or tool use**, rather than by a separate intent classifier model. The LLM acts as the router, the policy, and the reasoning engine all at once. It looks at the question and decides whether to fetch from memory, call a tool, use RAG, or answer directly from its own knowledge.

## Step 3 — Memory Path (User-Specific Questions)

If the question depends on the user's context, the LLM reasoning picks the right memory store to read from. There are four memory stores, each serving a different purpose:

- **Short-term memory** — the current chat.
- **Semantic memory** — stable facts about the user.
- **Episodic memory** — past conversations and past events.
- **Procedural memory** — learned skills and workflows.

The full implementation of each store is covered in Section 2.

## Step 4 — Tool Path (Real-Time, External, or Action Data)

If the question needs real-time data, external information, calculation, or an action, the agent calls a **tool**. Tools include things like weather APIs, calculators, stock-price services, database queries, and write operations such as sending an email or creating a record. The mechanism that connects the LLM to tools is explained in Section 3.

## Step 5 — RAG Path (Document Retrieval)

If the question is about knowledge stored in a document corpus (manuals, policies, support articles, internal wiki), the agent uses the RAG pipeline:

```
embedding → vector db → retrieving → reranking → LLM
```

Older tutorials often show steps like NLP parsing and NER as explicit stages in this flow. In modern RAG, these steps are not used as separate stages — the embedding model handles tokenization internally, and natural-language understanding is implicit in the LLM and embedding model. NER is still sometimes used, but only as an optional step for metadata filtering.

## Step 6 — LLM Generates the Response, Agent Returns It

Once the relevant context is gathered — from memory, tools, or RAG — the LLM **generates** the final answer using that context. The agent then returns the generated answer to the user. It is important to note that the LLM *generates* the answer; it does not *choose* between options. The choosing is done earlier by the reranker (in the RAG path) or by the tool result (in the tool path). The LLM's job at this stage is synthesis, not selection.

---

# 2. The Four Memory Types and How They Are Implemented

The four memory types in an agent are borrowed from cognitive architecture: short-term, semantic, episodic, and procedural. Each type stores a different kind of information and is implemented differently in real systems.

## 2.1 Short-Term Memory

Short-term memory holds the **current conversation** — the last N messages exchanged between the user and the agent. It gives the agent immediate context for follow-up questions and pronoun resolution (for example, understanding "it" in "make it shorter").

**Typical implementation:** a session cache in Redis, an in-process memory object, or a conversation buffer. The raw messages are simply re-sent to the LLM in every turn as part of the prompt.

**Key constraint:** short-term memory is bounded by the LLM's context window. Once the conversation grows too long, older messages are either dropped or summarized into a compact form.

## 2.2 Semantic Memory

Semantic memory holds **stable facts about the user** — name, language, timezone, role, preferences, and any profile information that does not change often. This memory gives the agent a persistent understanding of who the user is across sessions.

**Typical implementation:** a structured database such as Postgres or MongoDB, storing key-value pairs or JSON documents. Sometimes a vector database is used instead, if semantic retrieval by meaning is needed (for example, "find facts related to the user's work preferences").

**Example record:**

```json
{
  "user_id": "123",
  "language": "en",
  "timezone": "IST",
  "role": "developer"
}
```

## 2.3 Episodic Memory

Episodic memory holds **past conversations and past events** — what the user asked last week, what the agent explained two sessions ago, what happened in the previous transaction. This memory lets the agent stay coherent across long time spans.

**Typical implementation:** a vector database with timestamps, so that past episodes can be retrieved both **semantically** (by meaning) and **temporally** (by time). Long conversations are often summarized before being stored, so that the stored "episode" is a compact, meaningful record rather than a raw transcript.

**Example episode:** *"Last week, the user asked about vanilla RAG and I explained the embedding → vector DB → retrieval → reranking → LLM pipeline."*

## 2.4 Procedural Memory

Procedural memory holds **skills and workflows** — how to do things. It represents the agent's reusable capabilities: how to send an email, how to create a ticket, how to book a meeting.

**Typical implementation:** in practice, procedural memory is stored as **prompt templates, code snippets, or tool definitions**. In most modern agent frameworks, the set of registered tools (with their schemas and system prompts) effectively *is* the agent's procedural memory.

**Example:** a `send_email` tool with a defined schema is procedural memory for the skill of sending an email.

## 2.5 Summary Table

| Memory Type | Typical Storage                  | What's Stored                |
| ----------- | -------------------------------- | ---------------------------- |
| Short-term  | Session cache / in-memory        | Recent messages              |
| Semantic    | Structured DB (or vector DB)     | User facts and preferences   |
| Episodic    | Vector DB with timestamps        | Past chats and events        |
| Procedural  | Tool registry / prompt templates | Skills and workflows         |

---

# 3. Function Calling / Tool Use at the API Level

Function calling (also called tool use) is the mechanism that lets an LLM interact with external systems such as APIs, databases, and calculators. It is supported natively by modern LLM APIs — Anthropic Claude, OpenAI GPT, and Google Gemini all provide function calling interfaces. Frameworks like LangChain and LangGraph wrap these into a common abstraction.

## 3.1 The Six-Step Flow

The interaction between the LLM and a tool follows six clear steps.

### Step 1 — Define Tools as Structured Schemas

You register each tool with a name, a description, and a parameter schema. The LLM reads these definitions and uses them to decide when a tool is appropriate.

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "parameters": {
    "location": "string"
  }
}
```

### Step 2 — Send the User's Message + Tool Definitions to the LLM

When a request comes in, you send the user's message along with the full list of available tool definitions to the LLM.

### Step 3 — The LLM Decides: Answer Directly or Call a Tool

The LLM reads the message and decides whether to answer from its own knowledge or to request a tool call. If it decides to call a tool, it returns a structured JSON response indicating the tool name and the arguments.

```json
{
  "tool_call": {
    "name": "get_weather",
    "arguments": { "location": "Hyderabad" }
  }
}
```

### Step 4 — Your Application Executes the Tool

Your code receives the tool call request and actually runs the corresponding function — calling the weather API, running the calculation, querying the database, whatever the tool does. The LLM does not execute the tool itself; it only requests that your code execute it.

### Step 5 — Send the Tool's Result Back to the LLM

Once the tool returns a result, you send that result back to the LLM in a follow-up call so the model can use it.

```
Tool result: { "temp": "32°C", "condition": "sunny" }
```

### Step 6 — The LLM Generates the Final Response

With the tool's output now in its context, the LLM produces a natural-language answer for the user. For example: *"The weather in Hyderabad is 32°C and sunny today."*

## 3.2 The Key Mental Model

**The LLM does not actually call the API itself.** It only *decides* which tool to use and *what arguments* to pass. Your application does the real execution. This separation is what makes tool use safe — you control exactly which tools exist and when they are allowed to run.

## 3.3 Supported Platforms

- **Anthropic Claude** — tool use
- **OpenAI GPT** — function calling
- **Google Gemini** — function calling
- **LangChain / LangGraph** — a common interface that wraps all of the above

---

# 4. When to Choose RAG vs. Tools (Decision Framework)

A common question in agent design is whether a given piece of information should come from RAG or from a tool. The answer depends on **where the information lives** and **how it changes**, not on whether it is inside the model's training data.

## 4.1 Use RAG When…

RAG is the right choice when the information lives in **documents you control**, is **relatively stable**, and can be **indexed ahead of time**. Typical examples include product manuals, policy documents, internal wikis, and support articles. RAG works well because the corpus can be split into chunks, embedded, and stored in a vector database once — and then retrieved quickly at query time.

## 4.2 Use Tools When…

Tools are the right choice when the information is **real-time** or **dynamic**, lives in a **live system** (database, CRM, SaaS API), requires **computation** (calculators, conversions), or when the agent needs to **perform an action** such as sending an email, creating a record, or booking a meeting. Tools give the agent access to the outside world and the ability to act, not just read.

## 4.3 Worked Examples

| User Question                                     | Path                  | Why                                              |
| ------------------------------------------------- | --------------------- | ------------------------------------------------ |
| *"What's our refund policy?"*                     | **RAG**               | Lives in policy docs; stable.                    |
| *"What's my order status?"*                       | **Tool**              | Lives in order DB; real-time.                    |
| *"What's the weather today?"*                     | **Tool**              | Real-time external data.                         |
| *"How do I configure feature X?"*                 | **RAG**               | Product docs; stable.                            |
| *"Create an invoice for customer Y"*              | **Tool**              | Action — writes to DB.                           |
| *"What did I discuss with support last week?"*    | **Memory (episodic)** | Past conversations; not docs or live data.       |
| *"Explain vanilla RAG"*                           | **LLM only**          | Already in the model's training.                 |
| *"What's the gold price now?"*                    | **Tool**              | Real-time external data.                         |

## 4.4 Gray Zones (When Paths Combine)

Not every question falls cleanly into one path. Some questions require **multiple paths combined**. For example, *"Summarize last quarter's sales"* needs a **Tool** call to fetch the sales data from the database, plus **LLM reasoning** to produce the summary. *"How does our return process compare to Amazon's?"* might need **RAG** (for your own return policy docs) and a **Tool** (for a live lookup of Amazon's policy, if that API is available). In modern agents, the LLM's reasoning decides which paths to use — and it can use more than one in a single turn.

## 4.5 Quick Rule of Thumb

A simple heuristic to decide the path:

- **Static document information?** → RAG
- **Live, dynamic, or action-based?** → Tool
- **User-specific context?** → Memory
- **General knowledge the model already has?** → Plain LLM

This rule covers the majority of cases and is a good starting point when designing agent behavior.

---

## Final Summary

A modern AI agent is built on four pillars: **LLM reasoning** for routing, **memory** for user context, **tools** for real-time and action data, and **RAG** for document knowledge. The LLM does not call tools directly; it requests them through function calling, and the application executes them. Memory is split into short-term, semantic, episodic, and procedural stores, each with its own implementation pattern. RAG and tools are chosen based on where the information lives and how often it changes — not based on whether it is in training data. Together, these pieces form a complete and practical agent architecture.
