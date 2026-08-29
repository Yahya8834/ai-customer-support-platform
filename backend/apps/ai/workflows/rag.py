class RAGWorkflow:

    def __init__(self, retrieval_service, llm_provider):
        self.retrieval_service = retrieval_service
        self.llm_provider = llm_provider

    def run(self, workspace_uuid, question):
        chunks = self.retrieval_service.retrieve(
            workspace_uuid=workspace_uuid,
            question=question,
        )

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        return self.llm_provider.generate(
            question=question,
            context=context,
        )