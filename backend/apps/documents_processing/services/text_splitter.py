class RecursiveTextSplitter:

    def __init__(
        self,
        chunk_size=1500,
        chunk_overlap=200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.separators = [
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
        ]

    def split_text(self, text: str) -> list[str]:
        if not text.strip():
            return []
        if len(text) <= self.chunk_size:
            return [text.strip()]
        
        chunks = self._split_recursive(
            text=text,
            separators=self.separators,
        )

        return self._apply_overlap(chunks)

    def _split_recursive(
        self,
        *,
        text: str,
        separators: list[str],
    ) -> list[str]:

        if len(text) <= self.chunk_size:
            return [
                text.strip()
            ]

        if not separators:
            return self._split_by_size(text)

        separator = separators[0]

        parts = text.split(separator)

        chunks = []

        current_chunk = ""

        for part in parts:
            candidate = (
                current_chunk + separator + part
                if current_chunk
                else part
            )

            if len(candidate) <= self.chunk_size:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(
                        current_chunk.strip()
                    )

                current_chunk = part

        if current_chunk:
            chunks.append(
                current_chunk.strip()
            )

        final_chunks = []

        for chunk in chunks:
            if len(chunk) > self.chunk_size:
                final_chunks.extend(
                    self._split_recursive(
                        text=chunk,
                        separators=separators[1:],
                    )
                )
            else:
                final_chunks.append(chunk)

        return final_chunks
    

    def _apply_overlap(
        self,
        chunks: list[str],
    ) -> list[str]:

        if len(chunks) <= 1:
            return chunks

        overlapped_chunks = [
            chunks[0],
        ]

        for chunk in chunks[1:]:

            previous_chunk = overlapped_chunks[-1]

            overlap = previous_chunk[
                -self.chunk_overlap:
            ]

            overlapped_chunks.append(
                overlap + chunk
            )

        return overlapped_chunks


    def _split_by_size(
        self,
        text: str,
    ) -> list[str]:

        chunks = []

        start = 0

        while start < len(text):
            end = start + self.chunk_size

            chunks.append(
                text[start:end].strip()
            )

            start = end - self.chunk_overlap

        return chunks