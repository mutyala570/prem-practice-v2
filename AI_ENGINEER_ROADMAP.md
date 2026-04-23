# AI Engineer Learning Roadmap

A structured path from fundamentals to production-grade Generative AI engineering.

---

## Phase 1: Python Foundations (2–3 weeks)

> You already know Node.js/TypeScript — this phase is about Python fluency, not programming fundamentals.

### Week 1: Python Core (Basics + OOP + Async)

#### Day 1–2: Python Basics
- Variables, data types (int, float, str, bool, None)
- Lists, tuples, sets, dictionaries
- Control flow: `if/elif/else`, `for`, `while`, list comprehensions
- Functions: args, `*args`, `**kwargs`, default values, lambda
- String formatting (f-strings)
- Exception handling: `try/except/finally`, custom exceptions
- File I/O: reading/writing files, `with` context manager
- Modules & imports, `pip`, virtual environments (`venv`)

#### Day 3–4: OOP in Python
- Classes & objects, `__init__`, `self`
- Instance vs class vs static methods
- Inheritance, `super()`, multiple inheritance, MRO
- Magic/dunder methods: `__str__`, `__repr__`, `__eq__`, `__len__`
- Properties: `@property`, getters/setters
- Abstract classes (`abc` module)
- Dataclasses (`@dataclass`)
- Type hints (`typing` module): `List`, `Dict`, `Optional`, `Union`, `Callable`

#### Day 5–6: Async Python
- Difference: sync vs async (you know this from Node.js)
- `async def`, `await`, coroutines
- `asyncio.run()`, `asyncio.gather()`, `asyncio.create_task()`
- `aiohttp` / `httpx` for async HTTP calls
- Async iterators, `async for`, `async with`
- When to use async vs threads vs processes

#### Day 7: Python for AI Ecosystem
- `pydantic` (data validation — critical for LLMs)
- `python-dotenv` (env vars)
- `requests` / `httpx` (HTTP calls)
- Decorators & generators (used heavily in LangChain)
- Package managers: `pip`, `uv`, `poetry`

### Tools (Pick up as needed)
- Git & GitHub (you already know)
- VS Code / Cursor with Python extension
- Jupyter notebooks
- Virtual environments (`venv` or `uv`)

### Math (Optional — skip for now)
You're building AI *applications*, not training models. Learn math only when you hit it (e.g., cosine similarity when doing embeddings).

---

## Phase 2: Machine Learning Basics (4–6 weeks)

- Supervised vs unsupervised learning
- Train/test split, overfitting, regularization
- Algorithms: Linear/Logistic Regression, Decision Trees, Random Forest, KNN
- **Libraries**: `numpy`, `pandas`, `scikit-learn`, `matplotlib`
- Build 3–5 small projects (e.g., Titanic, House Prices)

---

## Phase 3: Deep Learning (4–6 weeks)

- Neural networks: neurons, layers, activations, backprop
- CNNs (images), RNNs / LSTMs (sequences)
- **Frameworks**: PyTorch (preferred) or TensorFlow
- Training loop, loss functions, optimizers
- Transfer learning
- Build: image classifier, sentiment analyzer

---

## Phase 4: NLP & Transformers (3–4 weeks)

- Tokenization, embeddings (Word2Vec, GloVe)
- Attention mechanism
- Transformer architecture (read "Attention Is All You Need")
- BERT, GPT family, T5
- **HuggingFace Transformers** library
- Fine-tuning a pretrained model

---

## Phase 5: Generative AI & LLMs (Core Focus — 6–8 weeks)

### LLM Fundamentals
- How LLMs work, context windows, tokens
- Prompting techniques: zero-shot, few-shot, CoT, ReAct
- Temperature, top-p, sampling

### LLM APIs
- OpenAI, Anthropic Claude, Groq, Google Gemini
- Streaming, function calling, structured outputs

### Frameworks
- **LangChain** / **LangGraph**
- **LlamaIndex**
- **Pydantic AI**

### RAG (Retrieval Augmented Generation)
- Embeddings & vector databases (Pinecone, Chroma, Weaviate, FAISS)
- Chunking strategies
- Hybrid search, reranking

### AI Agents
- Tool use / function calling
- ReAct, Plan-and-Execute patterns
- Multi-agent systems (CrewAI, AutoGen)
- Memory (short-term, long-term)

### Fine-tuning
- LoRA, QLoRA, PEFT
- Datasets, evaluation
- Local models with Ollama, llama.cpp

---

## Phase 6: Production AI Engineering (4–6 weeks)

- **API Development**: FastAPI, Flask
- **Deployment**: Docker, AWS/GCP/Azure, Modal, Replicate
- **Vector DBs in production**
- **Observability**: LangSmith, Langfuse, Weights & Biases
- **Evaluation**: RAGAS, custom evals, LLM-as-judge
- **Guardrails & safety**: prompt injection, output validation
- **Cost optimization**: caching, model routing
- **CI/CD for ML**

---

## Phase 7: Specialization (Pick One)

- **Multimodal AI**: vision + language (GPT-4V, Claude Vision)
- **Voice AI**: Whisper, TTS, real-time agents
- **Code agents**: SWE-bench style autonomous coding
- **Domain-specific**: healthcare, legal, finance AI

---

## Recommended Projects (Build a Portfolio)

1. **Chatbot with memory** — Streamlit + LLM API
2. **Document Q&A** — RAG over PDFs
3. **AI Agent** — Multi-tool agent (web search, code, calculator)
4. **Fine-tuned model** — Custom LoRA on domain data
5. **Production app** — Deployed full-stack AI app with auth, DB, monitoring

---

## Key Resources

### Courses
- Andrew Ng's ML & Deep Learning Specializations (Coursera)
- Fast.ai — Practical Deep Learning
- DeepLearning.AI Short Courses (free)
- Karpathy's "Neural Networks: Zero to Hero" (YouTube)

### Books
- *Hands-On Machine Learning* — Aurélien Géron
- *Deep Learning* — Ian Goodfellow
- *Building LLMs for Production* — Louis-François Bouchard

### Stay Updated
- Twitter/X: @karpathy, @AndrewYNg, @sama, @AnthropicAI
- Newsletters: The Batch, Latent Space, AI Engineer
- Papers: arxiv-sanity, Papers With Code
- Discord: HuggingFace, LangChain communities

---

## Timeline Summary

| Phase | Duration | Outcome |
|-------|----------|---------|
| Foundations | 1 month | Python + math fluency |
| ML Basics | 1.5 months | Build classical ML models |
| Deep Learning | 1.5 months | Train neural nets |
| NLP/Transformers | 1 month | Use & fine-tune LLMs |
| GenAI & Agents | 2 months | Build LLM apps |
| Production | 1.5 months | Deploy real systems |
| **Total** | **~8–9 months** | **Job-ready AI Engineer** |

---

## Tips for Success

- **Build > Watch**: 70% projects, 30% theory
- **Ship publicly**: GitHub, blog posts, Twitter
- **Read code**: Study open-source LLM apps
- **Join communities**: Contribute to open source
- **Stay curious**: This field changes monthly — keep learning

Good luck!
