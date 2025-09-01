import json
import os
import time
from datetime import datetime

import jsbeautifier
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_openai import ChatOpenAI
from config import candidate_config
from prompts import fn_candidate_analysis, system_prompt_candidate


async def save_cv_candidate(file):
    file_name = datetime.now().strftime("%Y%m%d%H%M%S-") + file.filename

    file_path = candidate_config.CV_UPLOAD_DIR + file_name

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    return file_name


def output2json(output):
    opts = jsbeautifier.default_options()
    return json.loads(jsbeautifier.beautify(output["function_call"]["arguments"], opts))


def load_pdf_docx(file_path):
    if os.path.basename(file_path).lower().endswith((".pdf", ".docx")):
        loader = (
            PyPDFLoader(file_path)
            if file_path.lower().endswith(".pdf")
            else Docx2txtLoader(file_path)
        )

    documents = loader.load_and_split()

    return documents


def read_cv_candidate(file_name):
    file_path = candidate_config.CV_UPLOAD_DIR + file_name

    documents = load_pdf_docx(file_path=file_path)
    content = ""
    for page in documents:
        content += page.page_content
    return content


def analyse_candidate(cv_content):
    start = time.time()
    print("Start analyse candidate")

    llm = ChatOpenAI(model=candidate_config.MODEL_NAME, temperature=0.5)
    completion = llm.predict_messages(
        [
            SystemMessage(content=system_prompt_candidate),
            HumanMessage(content=cv_content),
        ],
        functions=fn_candidate_analysis,
    )

    output_analysis = completion.additional_kwargs
    json_output = output2json(output=output_analysis)

    print(f"Time analyse candidate: {time.time() - start}")

    return json_output