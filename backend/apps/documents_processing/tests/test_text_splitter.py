from django.test import SimpleTestCase

from apps.documents_processing.services.text_splitter import (
    RecursiveTextSplitter,
)


class RecursiveTextSplitterTests(SimpleTestCase):

    def test_small_text_returns_single_chunk(self):
        splitter = RecursiveTextSplitter(
            chunk_size=100,
            chunk_overlap=10,
        )

        text = "This is a small document."

        chunks = splitter.split_text(text)

        self.assertEqual(
            chunks,
            [
                "This is a small document.",
            ],
        )


    def test_large_text_is_split_into_multiple_chunks(self):
        splitter = RecursiveTextSplitter(
            chunk_size=50,
            chunk_overlap=10,
        )

        text = (
            "This is the first paragraph.\n\n"
            "This is the second paragraph.\n\n"
            "This is the third paragraph."
        )

        chunks = splitter.split_text(text)

        self.assertGreater(
            len(chunks),
            1,
        )



    def test_chunks_do_not_exceed_chunk_size(self):
        splitter = RecursiveTextSplitter(
            chunk_size=50,
            chunk_overlap=10,
        )

        text = (
            "This is a very long document that needs "
            "to be split into smaller pieces."
        )

        chunks = splitter.split_text(text)

        for chunk in chunks:
            self.assertLessEqual(
                len(chunk),
                50,
            )


    def test_empty_text_returns_no_chunks(self):
        splitter = RecursiveTextSplitter(
            chunk_size=100,
            chunk_overlap=10,
        )

        chunks = splitter.split_text("")

        self.assertEqual(
            chunks,
            [],
        )


    def test_overlap_must_be_smaller_than_chunk_size(self):
        with self.assertRaises(ValueError):
            RecursiveTextSplitter(
                chunk_size=50,
                chunk_overlap=50,
            )


    def test_text_without_separators_is_split_by_size(self):
        splitter = RecursiveTextSplitter(
            chunk_size=20,
            chunk_overlap=5,
        )

        text = "abcdefghijklmnopqrstuvwxyz"

        chunks = splitter.split_text(text)

        self.assertGreater(
            len(chunks),
            1,
        )

        for chunk in chunks:
            self.assertLessEqual(
                len(chunk),
                20,
            )


    
    def test_whitespace_only_text_returns_no_chunks(self):
        splitter = RecursiveTextSplitter(
            chunk_size=100,
            chunk_overlap=10,
        )

        chunks = splitter.split_text(
            "   \n\n   \t   ",
        )

        self.assertEqual(
            chunks,
            [],
        )



    def test_text_exactly_chunk_size_returns_one_chunk(self):
        splitter = RecursiveTextSplitter(
            chunk_size=20,
            chunk_overlap=5,
        )

        text = "12345678901234567890"

        chunks = splitter.split_text(text)

        self.assertEqual(
            chunks,
            [text],
        )



    def test_chunks_include_configured_overlap(self):
        splitter = RecursiveTextSplitter(
            chunk_size=20,
            chunk_overlap=5,
        )

        text = "abcdefghijklmnopqrstuvwxyz"

        chunks = splitter.split_text(text)

        self.assertGreater(
            len(chunks),
            1,
        )

        self.assertTrue(
            chunks[1].startswith(
                chunks[0][-5:],
            ),
        )