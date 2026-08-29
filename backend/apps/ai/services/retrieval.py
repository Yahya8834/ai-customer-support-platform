from apps.ai.retrieval.vector_search import VectorSearch


class RetrievalService:

    def __init__(self, embedding_provider, vector_search=None):
        self.embedding_provider = embedding_provider
        self.vector_search = vector_search or VectorSearch()

    def retrieve(self, workspace_uuid, question, top_k=5):
        embedding = self.embedding_provider.embed(question)

        return self.vector_search.search(
            workspace_uuid=workspace_uuid,
            embedding=embedding,
            top_k=top_k,
        )