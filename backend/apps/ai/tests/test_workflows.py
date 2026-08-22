from unittest.mock import Mock
from django.test import TestCase
from apps.ai.workflows.rag import RAGWorkflow



class RAGWorkflowTests(TestCase):

    def test_retrieves_chunks_for_question(self):
        retrieval_service = Mock()
        llm_provider = Mock()

        chunk = Mock()
        chunk.content = "Password reset instructions"

        retrieval_service.retrieve.return_value = [chunk]

        workflow = RAGWorkflow(
            retrieval_service=retrieval_service,
            llm_provider=llm_provider,
        )

        llm_provider.generate.return_value = "Password reset instructions."

        result = workflow.run(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            question="How do I reset my password?",
        )

        self.assertEqual(
            result,
            "Password reset instructions.",
        )

        retrieval_service.retrieve.assert_called_once_with(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            question="How do I reset my password?",
        )


    
    def test_generates_answer_using_retrieved_chunks(self):
        retrieval_service = Mock()
        llm_provider = Mock()

        chunk = Mock()
        chunk.content = "To reset your password, go to Settings > Password."

        retrieval_service.retrieve.return_value = [chunk]
        llm_provider.generate.return_value = "Go to Settings > Password."

        workflow = RAGWorkflow(
            retrieval_service=retrieval_service,
            llm_provider=llm_provider,
        )

        result = workflow.run(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            question="How do I reset my password?",
        )

        self.assertEqual(
            result,
            "Go to Settings > Password.",
        )

        llm_provider.generate.assert_called_once_with(
            question="How do I reset my password?",
            context="To reset your password, go to Settings > Password.",
        )

    

    def test_generates_answer_with_empty_context_when_no_chunks_are_found(self):
        retrieval_service = Mock()
        llm_provider = Mock()

        retrieval_service.retrieve.return_value = []
        llm_provider.generate.return_value = "I don't have enough information to answer that."

        workflow = RAGWorkflow(
            retrieval_service=retrieval_service,
            llm_provider=llm_provider,
        )

        result = workflow.run(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            question="What is the refund policy?",
        )

        self.assertEqual(
            result,
            "I don't have enough information to answer that.",
        )

        llm_provider.generate.assert_called_once_with(
            question="What is the refund policy?",
            context="",
        )
