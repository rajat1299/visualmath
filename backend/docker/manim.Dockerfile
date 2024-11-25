FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    tipa \
    libcairo2-dev \
    libpango1.0-dev \
    build-essential \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    manim==0.17.3 \
    numpy \
    scipy \
    pillow \
    pycairo \
    manimpango==0.4.4

# Set working directory
WORKDIR /workspace

# Create a non-root user
RUN useradd -m -u 1000 manim
RUN chown -R manim:manim /workspace
USER manim