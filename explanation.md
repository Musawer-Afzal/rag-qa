# RAG System – Design & Evaluation Explanation

This document explains key design decisions, observed limitations, and evaluation metrics used in the Retrieval-Augmented Generation (RAG) system.

---

## 1. Chunk Size Selection

**Chosen Chunk Size:** `300 characters`  
**Overlap:** `50 characters`

### Reasoning
The chunk size was selected to balance three competing factors:

1. **Semantic completeness**
   - Chunks must be large enough to contain meaningful context (definitions, explanations, paragraphs).
   - Very small chunks (e.g., 100–200 chars) often lose semantic coherence.

2. **Embedding quality**
   - Sentence-transformer models perform best when text chunks represent a complete idea.
   - Larger chunks improve semantic similarity during retrieval.

3. **Retrieval efficiency**
   - Larger chunks reduce the total number of vectors, improving retrieval speed.
   - Excessively large chunks (>1000 chars) reduce retrieval precision.

### Overlap Justification
An overlap of 50 characters ensures:
- Important sentences at chunk boundaries are not truncated
- Context continuity between adjacent chunks
- Improved recall for questions spanning chunk boundaries

This configuration provided the best tradeoff between accuracy and performance during testing.

---

## 2. Observed Retrieval Failure Case

### Failure Scenario
**Question:**  
> "Explain classical conditioning in psychology"

**Observed Issue:**  
The retriever occasionally returned chunks discussing *learning theories* broadly instead of *classical conditioning specifically*.

### Root Cause
- Semantic similarity models prioritize general topic relevance
- Overlapping concepts (learning, behavior, conditioning) caused false positives
- No keyword-based filtering (BM25) was used alongside embeddings

### Mitigation Strategies (Future Work)
- Hybrid retrieval (FAISS + BM25)
- Query re-ranking using cosine similarity thresholds
- Metadata-based filtering per section or chapter

---

## 3. Metric Tracked

### Metric: Retrieval Latency

**What was measured**
- Time taken from question submission to top-K chunk retrieval

**Why this metric**
- Directly impacts user experience
- Important for real-time QA systems
- Helps identify scalability bottlenecks

**Observed Performance**
- Average retrieval latency: **~40–80 ms per query**
- Latency increased linearly with number of chunks
- FAISS integration significantly reduced retrieval time compared to brute-force similarity search

---

## 4. Summary

The system demonstrates:
- Efficient document chunking
- Accurate semantic retrieval
- Real-time performance suitable for production use

Future improvements include hybrid retrieval, streaming responses, and per-document indexing.
