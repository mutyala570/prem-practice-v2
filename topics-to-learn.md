<!-- Topics i need to cover  -->
prompt compression,

AI Evals

tool calling

inferance optimazTION

memory managment

can the model have hardware(d ram and s ram)

model quantization llm

intent classifier llm

<!-- basics layers required to create a agent -->
 Proposed sections:                                                                                                                                                                                                      
                                                                                                                                                                                                                          
  1. Goal & success criteria — what the agent must do, inputs/outputs, done-when                                                                                                                                          
  2. Architecture layers (each with purpose → topics to learn → what we build):                                                                                                                                           
    - Intent / routing layer                                                                                                                                                                                              
    - Retrieval / RAG layer (embeddings, chunking, vector DB)                                                                                                                                                             
    - Tooling layer (function calling, tool schemas, Pydantic)                                                                                                                                                            
    - Reasoning / planning layer (ReAct, plan-and-execute, LangGraph)                                                                                                                                                     
    - Memory layer (short-term conversation, long-term store)                                                                                                                                                             
    - LLM core (model choice, prompting, structured output)                                                                                                                                                               
    - Guardrails (input/output validation, prompt injection, cost limits)
    - Observability (tracing with LangSmith/Langfuse, evals)                                                                                                                                                              
  3. Build order — milestones from skeleton → RAG → tools → agent loop → guardrails → deploy
  4. Topics checklist — what you own, what I own                                                                                                                                                                          
  5. Deliverables — files to produce, example task to test end-to-end      
<!-- if i want to create a agent what i need to do -->