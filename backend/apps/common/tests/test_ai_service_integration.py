import time
from django.test import SimpleTestCase
from apps.common.integrations.ai_service.client import AIServiceClient



class AIServiceIntegrationTests(SimpleTestCase):

    def test_django_can_call_qwen_through_ai_service(self):
        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        start = time.perf_counter()

        response = client.chat(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            provider="qwen",
            model="qwen3.5-397b-a17b",
            prompt="Reply with exactly: connection successful",
        )

        elapsed = time.perf_counter() - start

        print(f"\nAI service response: {response}")
        print(f"AI service response time: {elapsed:.2f} seconds")

        self.assertTrue(response)
        self.assertIsInstance(response, str)



    def test_django_can_stream_qwen_response_through_ai_service(self):
        client = AIServiceClient(
            base_url="http://ai_service:8001",
        )

        start = time.perf_counter()

        chunks = client.chat_stream(
            workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
            provider="qwen",
            model="qwen3.5-397b-a17b",
            prompt="Explain what a return policy is in 3 short sentences.",
        )

        received_chunks = []

        for chunk in chunks:
            received_chunks.append(chunk)

            print(
                f"\n[{time.perf_counter() - start:.2f}s] "
                f"Received: {chunk}",
                flush=True,
            )

        elapsed = time.perf_counter() - start
        full_response = "".join(received_chunks)

        print(f"\nFull response: {full_response}", flush=True)
        print(f"Total time: {elapsed:.2f}s", flush=True)

        self.assertTrue(received_chunks)
        self.assertTrue(full_response)