import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq


logging.basicConfig(level=logging.INFO)

class YouTubeQA:
    """
    A class to handle Question and Answer (QA) generation from YouTube video transcripts.

    Attributes:
        embeddings (GPT4AllEmbeddings): Embeddings used for vector search.
        llm (ChatGroq): Language model used for generating answers.
        config['Models'] (dict): Configuration parameters for embeddings, LLM, and vector store.
        prompt_template (str): Template for question answering.
        vectorstore (Chroma): The vector store used for similarity searches.
    """
    def __init__(self, config):
        """
        Initializes the YouTubeQA class with the provided configuration.

        Args:
            config (dict): Configuration dictionary for embeddings, LLM, and RAG parameters.
        """
        self.config = config
        logging.info(f"Initializing with config: {self.config}")

        self.embeddings = GPT4AllEmbeddings(
            model_name=self.config["Embeddings"]["model_name"], 
            gpt4all_kwargs={'allow_download': True}
        )

        self.llm = self._initialize_llm(self.config["GROQ"])

        self.prompt_template = """
                    You are an expert in answering questions based on the content of YouTube videos. 
                    Use only the context provided to answer the user's question concisely, avoiding any introductory or filler phrases.

                    Context (from YouTube video):
                    {context}

                    Question: {question}

                    Answer:
                    """
        self.prompt = ChatPromptTemplate.from_template(self.prompt_template)
        self.vectorstore = None  # Vectorstore will be created dynamically

    def _initialize_llm(self, llm_config):
        """
        Initializes the ChatGroq language model with the given configuration.

        Args:
            llm_config (dict): LLM configuration parameters.

        Returns:
            ChatGroq: An instance of ChatGroq with validated parameters.
        """
        model_name = llm_config["model_name"]
        temperature = float(llm_config["temperature"])
        max_tokens = self._convert_to_int(llm_config["max_tokens"], default=None)
        timeout = self._convert_to_int(llm_config["timeout"], default=None)
        max_retries = int(llm_config["max_tries"])

        return ChatGroq(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            max_retries=max_retries
        )

    @staticmethod
    def _convert_to_int(value, default):
        """
        Converts a string value to an integer, providing a default value if the string is 'None' or invalid.

        Args:
            value (str): The value to convert to an integer.
            default (int): The default value to return if the conversion fails.

        Returns:
            int: The converted value or the default if the conversion fails.
        """
        try:
            return int(value) if value != 'None' else default
        except ValueError:
            return default

    def load_transcript(self, transcript):
        """
        Loads and processes the YouTube video transcript into a vector store.

        Args:
            transcript (str): The YouTube video transcript to load.
        """
        document = [Document(page_content=transcript)]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config["Rag"]["chunk_size"], 
            chunk_overlap=self.config["Rag"]["chunk_overlap"]
        )
        all_splits = text_splitter.split_documents(document)

        logging.info("Creating Vector Database")
        self.vectorstore = Chroma.from_documents(documents=all_splits, embedding=self.embeddings)
        logging.info("Database Created")

    def get_answer(self, question):
        """
        Retrieves an answer to the provided question using the stored video transcript.

        Args:
            question (str): The question to answer based on the transcript.

        Returns:
            str: The generated answer to the question.

        Raises:
            ValueError: If no transcript has been loaded into the vector store.
        """
        if self.vectorstore is None:
            raise ValueError("No transcript has been loaded. Please load a transcript first.")

        # Similarity search in the vector store
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": self.config["Rag"]["k"]})
        logging.info("Chain Invoked")

        # Set up the processing chain
        chain = {
            "context": retriever, 
            "question": RunnablePassthrough()
        } | self.prompt | self.llm | StrOutputParser()

        # Get the answer to the question
        answer = chain.invoke(question)
        return answer
