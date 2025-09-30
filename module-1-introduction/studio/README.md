# Lesson 3: 랭그래프 스튜디오

랭그래프 스튜디오를 실행하기 위해서 먼저 [LangGraph CLI](https://docs.langchain.com/langgraph-platform/cli)를 설치합니다.

```
pip install --upgrade "langgraph-cli[inmem]"
```
> 설치 방법 참고: https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/

`module-1-introduction/studio` 폴더에서 필요한 패키지를 설치하고, `langgraph dev` 명령어를 실행합니다.

```
cd module-1-introduction/studio
pip install -r requirements.txt

langgraph dev
```
## 파일 구조

```tree
.
├── langgraph.json  # 랭그래프 스튜디오를 실행하기 위해 필요한 설정 파일
├── agent.py
├── simple.py
├── router.py
├── .env.example    # API 키 설정 예시 파일 (.env로 복사하여 사용)
├── requirements.txt # 랭그래프를 구동하기 위해 필요한 파이썬 패키지
└── README.md
```