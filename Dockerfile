FROM ollama/ollama

# uv をインストール
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# uv の PATH を通す
ENV PATH="/root/.local/bin:$PATH"