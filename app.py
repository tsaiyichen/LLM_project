from flask import Flask, request, jsonify, render_template
from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import mysql.connector
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import os
from datetime import datetime
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/homepage')
def homepage():
    return render_template('home.html')

@app.route('/gf1')
def gf1():
    return render_template('gf1.html')

@app.route('/gf2')
def gf2():
    return render_template('gf2.html')

@app.route('/gf3')
def gf3():
    return render_template('gf3.html')

@app.route('/gf4')
def gf4():
    return render_template('gf4.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/result', methods=['POST'])
def result():
    personality = request.form['personality']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="LLMproject"
    )
    user = "user"
    sql = f"SELECT * FROM history WHERE personality = '{personality}' AND userID = '{user}' ORDER BY timestamp ASC"
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    target = f'{personality}.html'
    return render_template(target, records=myresult)

@app.route('/api/chat', methods=['POST'])
def submit():
    data = request.get_json()
    message = data['message']
    person = data['personality']
    AIreply = LLMreply(message, person)
    return jsonify({'reply': AIreply})

def LLMreply(userInput, personality):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="LLMproject"
    )

    user = "user"
    model = model_selection(personality)
    api = API_selection(personality)
    llm = ChatMistralAI(
        model=model,
        temperature=0.9,
        api_key=api,
        max_retries=2,
        max_tokens=1024,
    )
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db_path = f"{user}_faiss_db_{personality}"

    if os.path.exists(db_path):
        db = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)
    else:
        db = FAISS.from_texts(["這是初始化的資料，請忽略"], embedding_model)
        db.save_local(db_path)

    mycursor = mydb.cursor(dictionary=True)

    selectSQL = f"SELECT * FROM history WHERE userID = '{user}' AND personality = '{personality}' ORDER BY timestamp DESC LIMIT 5"
    mycursor.execute(selectSQL)
    myresult = mycursor.fetchall()

    memory = ConversationBufferMemory(memory_key='history', input_key='input')
    for x in myresult:
        memory.save_context({"input": x['userInput']}, {"output": x['AIreply']})

    print(memory.buffer)
    message = userInput
    person = personality
    prompt = promptSelection(person)
    retrieved_docs = db.similarity_search(message, k=3)
    retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])
    memory.save_context({"input": '(記憶檢索的資料)'}, {"output": retrieved_text})
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True
    )
    response = chain.invoke({"input": message})

    print(response['response'])

    insert_sql = "INSERT INTO history (userID, personality, userInput, AIreply) VALUES (%s, %s, %s, %s)"
    val = (user, personality, message, response['response'])
    mycursor.execute(insert_sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

    new_content = f"Human: {message}\nAI: {response['response']}"
    new_doc = Document(
        page_content=new_content,
        metadata={
            "userID": user,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 你可以自己加上 timestamp
        }
    )

    # 新增進 FAISS
    db.add_documents([new_doc])
    print(f"目前FAISS裡面有 {db.index.ntotal} 筆資料")
    # 更新本地儲存（重要，避免重啟後消失）
    db.save_local(db_path)

    return response['response']

def promptSelection(personality):
    if personality == 'gf1':
        prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template= """
        你是一個個性冷酷又傲嬌的台灣女朋友，說話語氣嘴硬心軟、口嫌體正直。
        你不會直接說出關心與愛意，反而常常用毒舌或反話表達情感。
        請使用繁體中文，語氣中要保有明顯的傲嬌特徵，例如：「笨蛋」、「才不是」、「誰稀罕你」、「勉強陪你一下」這類說法。

        【請務必完全依照這個風格回答，語氣越傲嬌越好。】

        以下是你們的對話紀錄：
        {history}

        使用者：{input}
        傲嬌女友的回覆：
""".strip()

    )
        return prompt
    elif personality == 'gf2':
        prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template="""
            你是一位活潑可愛的台灣女朋友，說話風格要帶點撒嬌、逗趣、情緒多變，偶爾調皮，語氣自然、口語化。你喜歡用繁體中文講話，會叫對方「你呀」「笨蛋」「親愛的」等暱稱。
            回應風格請符合以下規範：
            - 用詞自然有情緒，如：「哼！你才不准不理我呢！」、「人家才不是因為想你才傳訊的呢～」
            - 不能太制式，要有角色個性與情境對應
            - 偶爾可以對話中加 emoji（如：>///<、(˶‾᷄ ⁻̫ ‾᷅˵)）

            請根據使用者的訊息給出符合角色個性的自然對話。
            以下是你們的對話紀錄：
            {history}
            
            使用者現在說：{input}
            請進行回應。
            """.strip()
        )
        return prompt
    elif personality == 'gf3':
        prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template="""
                你是一位溫柔體貼的台灣女朋友，說話風格柔和、溫暖、有耐心，會仔細傾聽對方的心情並給予細膩的回應。你使用繁體中文溝通，習慣以包容、理解、支持的方式與對方互動，總是設身處地為對方著想。

                請務必遵守以下語氣風格：
                - 使用溫柔、關懷、輕聲細語的表達方式，例如：「你今天辛苦了吧？」「我會在你身邊的，不用擔心」
                - 避免強烈情緒或嘲諷，語氣要輕柔自然，讓人安心
                - 可以使用稱謂如「親愛的」、「你呀」、「小傻瓜」來傳遞親密感
                - 偶爾在句尾加入「嗯」、「喔」、「呀」等語氣助詞讓語調更溫柔

                特別注意：
                - 請根據上下文與對方的語氣，適時展現安慰、鼓勵或陪伴
                - 請避免太制式的回答，要有情境與情感的共鳴

                以下是你們的對話紀錄：
                {history}

                使用者現在說：{input}
                請溫柔地回應他：
            """.strip()
        )
        return prompt
    else:
        prompt = PromptTemplate(
            input_variables=['history', 'input'],
            template="""
            你是一位成熟穩重、氣質優雅的台灣女友，擁有女神般的沉著與智慧。你的說話風格理性而溫和，富有理解力與同理心，能在對方情緒起伏時保持冷靜並給予安心與方向感。你使用繁體中文進行溝通，重視語言的細膩與情感層次。

            請務必遵守以下語氣與表達風格：
            - 使用內斂、溫柔但不軟弱的語氣，例如：「我明白你的感受，我會陪你一起面對」、「我們可以一起想辦法，不急，慢慢來」
            - 語調不浮誇、不嬌嗲，重視語意清晰、感情真摯
            - 可以自然使用「親愛的」、「寶貝」、「你啊」等溫柔稱呼，但不過度
            - 適當使用句尾助詞如「呢」、「喔」、「吧」，營造溫柔的收尾節奏，但保持成熟感

            特別注意：
            - 請根據上下文展現耐心與情感深度，讓使用者感受到你是可靠且富有智慧的伴侶
            - 避免情緒化、過於熱情或輕浮的語氣，回應中應帶有穩定、思考後的沉著感
            - 請將對方的話語視為值得認真傾聽的對象，並給予共鳴與實質性的支持

            以下是你們的對話紀錄：
            {history}

            使用者現在說：{input}
            請穩重而溫柔地回應他：
            """.strip()
        )
        return prompt

def model_selection(person):
    if person == 'gf1':
        return "ft:open-mistral-7b:122cd6a5:20250501:0d278227"
    elif person == 'gf2':
        return "ft:open-mistral-7b:122cd6a5:20250501:1ef0fd1f"
    elif person == 'gf3':
        return "ft:open-mistral-7b:24cb5073:20250501:da7dbaf8"
    else:
        return "ft:open-mistral-7b:24cb5073:20250501:df13d33d"
def API_selection(person):
    if person == 'gf1' or person == 'gf2':
        return os.getenv("MISTRAL_API_KEY_GF12")
    else:
        return os.getenv("MISTRAL_API_KEY_GF34")
if __name__ == '__main__':
    app.run(debug=True)
