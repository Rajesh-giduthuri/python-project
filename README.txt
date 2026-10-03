python --version
-----virtual environment----------------
py -3.11 -m venv .venv
.venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

------check installations--------------
python -c "import streamlit; print('Streamlit OK')"
python -c "import faster_whisper; print('Faster-Whisper OK')"
python -c "import openai; print('OpenAI SDK OK')"
python -c "import chromadb; print('ChromaDB OK')"

-------------run applicatiion-----------
streamlit run app.py

--------------audio process---------
python audio\processor.py

--------------transcript--------
python audio\transcriber.py

------------summarize----------
python -m ai.summarizer
-----------structured summary----------
python -m ai.extractor

--------------database SQLite---------
python -m database.db
python -m database.service  #(save data to database)
python -m database.queries  #(queriing or searching the data in database)

----------------create RAG (for questions)-----
python -m rag.embeddings
python -m rag.vector_store  #(chroma DB)

-----------semantic search layer--------
python -m rag.search
python -m rag.qa    #(for Q&A)

---------------YouTube URL support--------
python -m audio.youtube
