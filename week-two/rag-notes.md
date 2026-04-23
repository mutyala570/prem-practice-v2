# Week 2 — RAG Learning Notes

## Topics Covered in This Document

1. [**Why RAG is Needed**](#1-why-rag-is-needed)
2. [**RAG Scenarios**](#2-rag-scenarios)
3. [**Vanilla RAG**](#3-vanilla-rag)
4. [**Reranker (Cross Encoder)**](#4-reranker-cross-encoder)

---

# 1. Why RAG is Needed

Retrieval-Augmented Generation (RAG) is a technique that gives a Large Language Model (LLM) access to external information at the time of answering a question. Although LLMs are powerful, they have several built-in limitations. RAG is needed to address those limitations. The main reasons are explained below.

## Knowledge Cutoff Limitations

Every LLM is trained on data collected up to a specific date, called its training cutoff. After that date, the model has no awareness of new events, new documents, or updated facts. This means the model cannot answer questions about recent developments on its own. RAG solves this by retrieving fresh information from external sources at query time and handing it to the model.

## Privacy and Compliance

Organizations often need to work with sensitive data such as customer records, internal policies, or proprietary research. This data should not be part of a publicly trained model's weights. RAG keeps such information inside retrieval systems that the organization owns and controls. The LLM reads from these systems only when needed, so the sensitive data never becomes part of the model itself. This makes privacy and compliance much easier to manage.

## Reducing Hallucinations

A hallucination is when a model produces an answer that sounds correct but is actually wrong. Because RAG grounds the model's response in specific retrieved documents, the output can be traced back to its source. This reduces fabricated answers and also makes it possible to cite the original passages, giving users a way to verify the information.

## Domain-Specific Accuracy

General-purpose LLMs are trained on broad internet data, so they have wide but shallow coverage. They often struggle with specialized fields such as medicine, law, or a company's internal processes. RAG allows the model to reach into curated, domain-specific knowledge bases (technical manuals, legal archives, product documents) and use them as the source of truth.

## Handling Long-Tail Entities

LLMs perform well on popular topics because those topics appear frequently in training data. For rare entities — an obscure assistant professor, a small regional company, an uncommon medication — the model's knowledge is weak and unreliable. RAG fills this gap by retrieving targeted documents about those rare entities whenever they are needed.

---

# 2. RAG Scenarios

RAG is not limited to one use case. It is applied in several common scenarios depending on what kind of information the system needs to bring in. The three main scenarios are described below.

## Retrieving External Knowledge

This is the most common scenario. When a question goes beyond what the LLM already knows — because the information is recent, specialized, or private — the system retrieves relevant documents from an external knowledge base and provides them to the model as supporting context. This plugs the knowledge gap of the LLM.

## Retrieving Context History

In long-running conversations, it is not practical to keep every past message inside the prompt because of context window limits and cost. Instead, RAG stores earlier parts of the conversation in a retrievable form. When the current conversation refers back to an older topic, the system fetches only the relevant history. This allows the assistant to stay coherent over hours, days, or weeks.

## Retrieving In-Context Training Examples

LLMs can learn new tasks directly from examples placed inside the prompt. This is called in-context learning. For a new or unusual task, RAG dynamically retrieves the most relevant examples from a stored pool and adds them to the prompt. This helps the model understand the task without any retraining. This scenario connects directly to the prompting strategies below.

### Prompting Strategies: Zero-shot, One-shot, Few-shot

These strategies describe *how many examples* are provided to the LLM. They are not RAG by themselves, but the few-shot strategy becomes powerful when combined with RAG.

**Zero-shot** — The model is given only the instruction, without any examples. It relies entirely on what it already knows. Example: *"Classify this review as positive or negative: 'The food was amazing.'"*

**One-shot** — The model is given a single worked example before the real task. This helps it understand the expected format. Example: *"Review: 'Terrible service.' → Negative. Now classify: 'The food was amazing.'"*

**Few-shot** — The model is given several examples (usually two to five) before the real task. This is useful for tasks with subtle patterns or strict output formatting.

**Dynamic Few-shot (RAG-powered)** — Instead of hard-coding examples in the prompt, the system retrieves the most relevant examples for each incoming query from a larger pool. The model sees examples that match the specific situation, which significantly improves accuracy on varied tasks.

| Technique        | Uses RAG?                                       |
| ---------------- | ----------------------------------------------- |
| Zero-shot        | No — no examples retrieved                      |
| Static few-shot  | No — examples hardcoded in prompt               |
| Dynamic few-shot | **Yes** — RAG retrieves best examples per query |

### Dynamic Few-shot vs. Prompt Chain

Dynamic few-shot and prompt chaining are sometimes confused, but they are different patterns.

**Dynamic few-shot** is about *what goes into one prompt*. The system retrieves relevant examples, injects them into a single prompt, and makes one LLM call.

**Prompt chain** is about *how a task is split across multiple prompts*. The system makes several sequential LLM calls, where the output of one call becomes the input of the next.

The two can also be combined — a step inside a prompt chain can itself use dynamic few-shot retrieval.

---

# 3. Vanilla RAG

Vanilla RAG is the simplest, baseline version of Retrieval-Augmented Generation. It contains no advanced optimizations and serves as the foundation that every more sophisticated RAG system extends. Understanding vanilla RAG is essential because all improvements are built on top of its basic pipeline.

## The Vanilla RAG Pipeline

The pipeline consists of two parallel flows that converge at a step called *Context Engineering / Augment*, and the result is finally passed to the LLM to generate the response.

```
        ┌─────────┐       ┌──────────┐
Data →  │ Chunks  │  →    │ Vector   │
        └─────────┘       │  Store   │
                          └──────────┘
                               │
                               ▼
Query  →  Retriever  →  Retrieved Chunks  →  Context Engineering (Augment)  →  LLM  →  Generated Response
```

The user's query is passed directly into the Augment step. At the same time, the retriever uses the query to search the vector store and produces a set of relevant chunks, which also flow into the Augment step. Augmentation combines both into a single prompt, which is then sent to the LLM to produce the final response.

## Indexing Stage

Before any queries can be answered, the source documents must be prepared. This is done once, ahead of time. Each document is split into smaller chunks that are semantically coherent. Every chunk is passed through an embedding model, which converts it into a numerical vector that represents its meaning. These vectors are stored in a specialized vector database such as Pinecone, Chroma, or FAISS, which supports fast similarity search.

## Retrieval Stage

When a user submits a query, the system converts the query into an embedding using the same model that was used during indexing. The retriever searches the vector database for the top-k most similar chunks, usually ranked by cosine similarity. The result is a small set of document snippets that are most relevant to the question.

### Top-k in Retrieval

The term **top-k** refers to the number of most-similar chunks that the retriever returns. The letter *k* is a parameter chosen by the system designer, commonly 3, 5, or 10. "Top" means the chunks with the highest similarity scores.

For example, if the vector database contains 10,000 chunks and a user asks *"What's the refund policy?"* with *k = 3*, the database returns the three chunks with the highest similarity scores. Only those three are sent forward into the augmentation step.

Choosing the right value of *k* is a trade-off between recall and noise:

| k value           | Trade-off                                                    |
| ----------------- | ------------------------------------------------------------ |
| **Small** (1–3)   | Precise, less noise, but may miss information. Cheaper.     |
| **Medium** (5–10) | Balanced; common default.                                    |
| **Large** (20+)   | Higher recall but noisy and expensive; can confuse the LLM. |

Most vanilla RAG systems start at *k = 3 to 5* and tune from there. Sending all chunks is impractical because of context window limits, higher cost, slower responses, and the "lost in the middle" problem where the model overlooks important information buried in too much content.

## Context Engineering / Augment Stage

This stage is the bridge between retrieval and generation. The retrieved chunks and the original query are combined into a single, well-structured prompt. The prompt usually has clear section headers such as *Context* and *Question*, along with explicit instructions on how the model should use the context. The quality of this step directly affects how grounded and accurate the final answer will be.

A typical augmented prompt looks like this:

```
Context:
{retrieved_chunk_1}
{retrieved_chunk_2}
{retrieved_chunk_3}

Question: {user_query}

Answer using only the context above.
```

### Why Context and Question Are Sent Together

The retrieved context and the user's question are always sent in one combined prompt, not as separate messages. The reason is how LLMs fundamentally work.

An LLM is **stateless** — each API call is independent. The model has no memory of previous calls. If the context were sent in one call and the question in another, the model would have already forgotten the context by the time the question arrived. Everything the model needs must be inside a single prompt.

The **context** acts as the knowledge source — the "open book" the model reads from. Without it, the model would fall back on its training data, which may be outdated or wrong for the specific case.

The **question** acts as the instruction — it tells the model what to extract, summarize, or reason about using the given context.

Together, they form a complete request: *"Using this context, answer this question."* Neither part is useful on its own.

## Generation Stage

The augmented prompt is sent to the LLM. The LLM reads the context, interprets the question, and produces the final response. Because the relevant information is already present in the prompt, the answer is grounded in the retrieved material rather than relying only on the model's internal memory.

## Why Chunking Matters

Chunking is one of the most important design decisions in a RAG system, for three reasons.

First, chunks must be **semantically coherent**. A good chunk contains a complete idea or section so that it still makes sense when retrieved on its own.

Second, **LLMs have a fixed input window**. Regardless of document size, only a limited number of tokens fit into one prompt. Chunking breaks long documents into manageable pieces that fit within this limit.

Third, **chunking enables precise retrieval**. Instead of fetching an entire document when only one paragraph is relevant, the system fetches just the matching pieces. This avoids clutter in the context and lets the model focus on what is actually useful.

## Limitations of Vanilla RAG

Vanilla RAG is a strong starting point but has known weaknesses. Retrieval quality is fragile — if the retriever fetches the wrong chunks, the answer will be wrong regardless of how capable the LLM is. Naive fixed-size chunking often cuts across sentence or paragraph boundaries, destroying meaning. The retrieval step is single-shot, meaning the system cannot refine its query or re-rank results. Multi-hop questions that need information from multiple documents are not handled well. And when too many irrelevant chunks are included, the LLM can become confused rather than better informed.

## What Comes After Vanilla RAG

More advanced RAG systems improve on these limitations with techniques such as **query rewriting** and HyDE (Hypothetical Document Embeddings) to reformulate the query before retrieval; **re-ranking** to sort candidates more accurately using a second model; **hybrid search** to combine vector similarity with keyword methods like BM25; **multi-hop or agentic RAG** for iterative retrieval across reasoning steps; and **better chunking strategies** based on semantic boundaries or document structure.

---

# 4. Reranker (Cross Encoder)

A **Reranker** is an advanced component in a RAG pipeline that runs **after** the initial retrieval step. Its job is to re-score the candidate chunks returned by the retriever and pick out the truly most relevant ones before they are sent to the LLM. The key property of a reranker is that it is **very slow but more accurate** than the initial retriever.

## Pros and Cons of Vector Similarity — The Need for Reranking

Before looking at how a reranker works, it is important to understand *why* reranking is needed at all. In Vanilla RAG, retrieval is done using **vector similarity** (cosine similarity or dot product between query and chunk embeddings). This approach has clear strengths but also real weaknesses, and those weaknesses are what motivate adding a reranker on top.

### The Good (Why Vector Similarity Works Well)

Vector similarity is the backbone of modern retrieval because it is **fast and practical at scale**. Comparing vectors is just a dot product, which can be computed extremely quickly — making it efficient enough to search over millions of documents in real time. It also naturally handles documents of different lengths, since each document is reduced to a fixed-size vector regardless of how long the original text is. On top of that, the approach is well-established and supported by a mature ecosystem of vector databases such as **FAISS, Chroma, Qdrant, and Weaviate**, which makes it easy to adopt in production systems.

### The Bad (Where Vector Similarity Falls Short)

Despite its speed, vector similarity is not precise enough on its own. It **ignores term frequency importance**, treating rare and common words equally — so a critical but rare keyword in the query may not influence similarity as much as it should. It also **misses out on the richness of a document**: by compressing an entire chunk into a single vector, subtle details and nuanced meaning often get lost. Finally, vector similarity struggles with **long-tail data** — words or concepts that rarely appear in the training data of the embedding model may not be represented accurately, leading to poor retrieval for specialized or uncommon topics.

These limitations are exactly why a **reranker** is introduced. The initial retriever casts a wide net quickly using vector similarity, and then a reranker re-examines the top candidates with a more careful, fine-grained model to fix the accuracy gap.

## How a Cross Encoder Reranker Works

A cross encoder reranker follows a simple flow:

```
[query] + [doc] → Model → Score
```

It takes the query and one document together as a combined input and feeds that combined input into a transformer model. The model outputs a single relevance score for that (query, document) pair. This process is repeated for every document in the candidate list returned by the retriever.

## Why It Is More Accurate

In vanilla retrieval, the query and the documents are embedded separately and compared only at the vector level. The model never sees them together, so it misses fine-grained relationships between the words in the query and the words in the document.

A cross encoder looks at the query and the document at the same time, inside the same model pass. This allows it to capture deep word-level interactions — for example, noticing that *"refund"* in the query matches *"money back"* in the document, or understanding how the query's intent lines up with the document's content. This joint view is what makes it significantly more accurate than plain vector similarity.

## Why It Is Slow

Because the cross encoder must process the query and document together, the embeddings cannot be pre-computed. Each time a new query comes in, the model must run a fresh forward pass for every candidate document.

If the retriever returns 100 candidate chunks, the cross encoder runs 100 separate model calls. This cost grows linearly with the number of candidates, which is why reranking is only applied to a small shortlist — not the entire knowledge base.

## Where It Fits in the RAG Pipeline

The reranker sits between the retriever and the LLM, refining the top results before generation:

```
Query
  ↓
Retriever (fast, approximate)   → Top 100 candidates
  ↓
Reranker (cross encoder, slow)  → Top 5 best
  ↓
LLM (Generation)
  ↓
Answer
```

The retriever casts a wide net quickly, and the reranker refines the top candidates with much higher precision. This two-stage pattern gives you both the speed of vector search and the accuracy of a cross encoder.

## Two Stage Retrieval (Bi-Encoder + Cross-Encoder)

In practice, the combination of a fast retriever and a slow but accurate reranker is formalized as a **Two Stage Retrieval** architecture. This is the standard pattern used in production RAG systems because neither stage can do the job well on its own.

### The Flow

```
Query → Bi-Encoder retrieval → Cross-Encoder ranking → Filter → Final ranked list
        (Millions of docs      (Hundreds of docs)               (Top relevant docs)
         → Hundreds)
```

### Stage 1 — Bi-Encoder Based Retrieval

In the first stage, the query is passed through a bi-encoder, which embeds the query and compares it against the pre-computed vectors of **millions of documents** using fast similarity measures like dot product or cosine similarity. Because the document embeddings are already computed and stored in a vector database, this stage is extremely fast. The output is a shortlist of **hundreds of documents** that are broadly relevant to the query, though not precisely ranked. The role of this stage is to **cast a wide net very quickly** and filter the knowledge base down to a manageable candidate set.

### Stage 2 — Cross-Encoder Based Ranking

In the second stage, each of the hundreds of candidate documents from Stage 1 is passed into a cross-encoder together with the query. The cross-encoder produces a precise relevance score for every (query, document) pair by looking at them jointly. The candidates are then re-ordered according to these scores, so that the documents that are truly most relevant rise to the top. The role of this stage is to **refine the shortlist with fine-grained accuracy** that pure vector similarity cannot achieve.

### Filter Stage

After reranking, a final **filter** step cleans up the list before it is handed to the LLM. This step can apply score thresholds (dropping candidates below a certain relevance score), remove duplicates, enforce access control or permissions, or cap the list to a top-N size that fits comfortably inside the model's context window. The output is a **ranked list of the most relevant documents**, ready for the generation stage.

### Why Two Stages Instead of One

A bi-encoder alone is fast but lacks the precision to rank documents reliably. A cross-encoder alone is extremely accurate but far too slow to run against millions of documents. The two-stage approach combines their strengths: the bi-encoder does the heavy lifting at scale by narrowing millions of documents down to hundreds, and the cross-encoder then does the fine-grained work on that much smaller shortlist. The result is a retrieval pipeline that is **both scalable and accurate**, which is why this architecture has become the default in modern RAG systems.

## Summary in One Line

A Cross Encoder reranker trades speed for accuracy by feeding the query and each candidate document into the model together, producing a much more reliable relevance score than plain vector search.
