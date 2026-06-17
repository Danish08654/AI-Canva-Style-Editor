FROM python:3.11-slim

#  System dependencies 
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

#  Work directory 
WORKDIR /app

#  Install dependencies 
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#  Copy project 
COPY . .

#  Streamlit config 
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

#  Expose port 
EXPOSE 8501

#  Run app 
CMD ["streamlit", "run", "app.py"]