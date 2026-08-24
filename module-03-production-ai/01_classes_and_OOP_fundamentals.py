# Tracks LLM experiments with runs and costs

class LLMExperiment:
    def __init__(self, experiment_name: str, model_used: str, max_tokens: int):
        self.experiment_name = experiment_name
        self.model_used = model_used
        self.max_tokens = max_tokens
        self.runs_completed = 0
        self.total_cost_usd = 0.0

    def log_run(self, cost: float, notes: str):
        self.runs_completed += 1
        self.total_cost_usd += cost
        print(notes)

    def summary(self):
        print("Summary:\n")
        print(f"Experiment Name: {self.experiment_name}")
        print(f"Model Used: {self.model_used}")
        print(f"Max Tokens: {self.max_tokens}")
        print(f"Runs Completed: {self.runs_completed}")
        print(f"Total Cost in USD: {self.total_cost_usd}")

design = LLMExperiment("Shirt Design", "nano-banana", 1024)
design.log_run(10, "Draft 1")
design.log_run(8, "Draft 2")
design.log_run(15, "Draft 3")
design.log_run(25, "Draft 4")
print("-" * 20)
design.summary()


# RAGPipeline with validated attribute

class RAGPipeline:
    DEFAULT_CHUNK_SIZE = 512
    DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

    def __init__(self, pipeline_name: str, chunk_size: int | None = None, embedding_model: str = DEFAULT_EMBEDDING_MODEL):
        self.pipeline_name = pipeline_name
        self.chunk_size = chunk_size
        self.embedding_model = embedding_model
        self.documents = []

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        if value is None:
            self._chunk_size = RAGPipeline.DEFAULT_CHUNK_SIZE
            return
        if not isinstance(value, int):
            raise TypeError("chunk_size must be an Integer")
        if not (64 <= value <= 2048):
            raise ValueError("chunk_size must be between 64 and 2048")
        self._chunk_size = value

    def __str__(self):
        return f"Pipeline Name: {self.pipeline_name}\nChunk Size: {self.chunk_size}\nEmbedding Model: {self.embedding_model}"

    def __repr__(self):
        return f"RAGPipeline(pipeline_name= '{self.pipeline_name}', chunk_size= {self.chunk_size}, embedding_model= '{self.embedding_model}')"

    def __len__(self):
        return len(self.documents)

    def add_document(self, filename: str):
        self.documents.append(filename)
        print("File added successfully")

    def run_pipeline(self):
        print("The following documents are in the pipeline:")
        for i in self.documents:
            print("\t", i)
        print(f"Chunk Size: {self.chunk_size}\nEmbedding Model: {self.embedding_model}")

ragbasic = RAGPipeline("Basic RAG")
print()
print(str(ragbasic))
print()
print(repr(ragbasic))
print()
ragbasic.add_document("Document 1.txt")
ragbasic.add_document("Document 2.txt")
print(f"Total Files added: {len(ragbasic)}")
print()
ragbasic.run_pipeline()

ragmedium = RAGPipeline("Medium RAG", 1000)
print()
print(str(ragmedium))
print()
print(repr(ragmedium))

ragadvanced = RAGPipeline("Advanced RAG", 2000, "text-embedding-51")
print()
print(str(ragadvanced))
print()
print(repr(ragadvanced))
print()
ragadvanced.add_document("Document 3.txt")
ragadvanced.add_document("Document 4.txt")
ragadvanced.add_document("Document 5.txt")
ragadvanced.add_document("Document 6.txt")
print(f"Total Files added: {len(ragadvanced)}")
print()
ragadvanced.run_pipeline()

ragerror = RAGPipeline("Medium RAG", 10000)
ragerror = RAGPipeline("Medium RAG", 100.01)
