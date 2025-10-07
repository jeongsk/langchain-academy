---
dg-publish: true
---
이 문서는 LangGraph 애플리케이션을 배포하는 다양한 방법을 자세히 설명합니다.

## 목차

1. [배포 방법 비교](#배포-방법-비교)
2. [방법 1: LangGraph Cloud 배포 (추천)](#방법-1-langgraph-cloud-배포-추천)
3. [방법 2: Docker로 Self-Hosted 배포](#방법-2-docker로-self-hosted-배포)
4. [방법 3: Python 웹 서버로 배포](#방법-3-python-웹-서버로-배포)
5. [환경 변수 및 시크릿 관리](#환경-변수-및-시크릿-관리)
6. [모니터링 및 디버깅](#모니터링-및-디버깅)
7. [FAQ](#faq)

---

## 배포 방법 비교

| 특징 | LangGraph Cloud | Docker Self-Hosted | Python 웹 서버 |
|------|----------------|-------------------|---------------|
| **난이도** | ⭐ 매우 쉬움 | ⭐⭐ 보통 | ⭐⭐⭐ 어려움 |
| **비용** | 사용량 기반 | 서버 비용만 | 서버 비용만 |
| **스케일링** | 자동 | 수동 설정 필요 | 수동 구현 필요 |
| **모니터링** | 내장 (LangSmith) | 직접 구성 | 직접 구현 |
| **배포 시간** | 5분 | 30분 | 1-2시간 |
| **추천 대상** | 초보자, 빠른 프로토타입 | 중급자, 온프레미스 필요 | 고급자, 커스터마이징 필요 |

---

## 방법 1: LangGraph Cloud 배포 (추천)

### 왜 LangGraph Cloud를 추천하나요?

✅ 인프라 관리 불필요  
✅ 자동 스케일링  
✅ 내장 모니터링 (LangSmith)  
✅ HTTPS, 인증 자동 설정  
✅ 스트리밍, 웹훅 지원  

### 1.1 사전 준비

1. **LangSmith 계정 생성**
   - [https://smith.langchain.com/](https://smith.langchain.com/) 접속
   - GitHub 또는 Google 계정으로 가입

2. **LangGraph CLI 설치**
   ```bash
   pip install langgraph-cli
   ```

3. **LangSmith API 키 발급**
   - LangSmith 대시보드 → Settings → API Keys
   - "Create API Key" 클릭
   - 발급받은 키를 안전한 곳에 보관

### 1.2 프로젝트 설정

1. **langgraph.json 확인**

   프로젝트에 `langgraph.json` 파일이 있는지 확인하세요. 없다면 생성하세요:

   ```json
   {
     "dockerfile_lines": [],
     "graphs": {
       "graph": "./graph.py:graph"
     },
     "python_version": "3.12",
     "dependencies": [
       "."
     ],
     "env": ".env"
   }
   ```

2. **환경 변수 설정**

   배포할 환경 변수를 미리 준비하세요 (.env 파일):
   ```bash
   OPENAI_API_KEY=sk-...
   COHERE_API_KEY=...
   TAVILY_API_KEY=...
   LANGSMITH_API_KEY=...
   ```

### 1.3 배포하기

1. **LangSmith 로그인**
   ```bash
   export LANGSMITH_API_KEY=<your-api-key>
   ```

2. **배포 명령 실행**
   ```bash
   langgraph deploy
   ```

   또는 특정 이름으로 배포:
   ```bash
   langgraph deploy --name my-rag-agent
   ```

3. **배포 확인**
   
   명령이 성공하면 다음과 같은 URL이 표시됩니다:
   ```
   ✓ Deployment created successfully!
   URL: https://my-rag-agent-abc123.langchain.app
   ```

### 1.4 배포된 앱 사용하기

#### REST API로 호출

```python
import requests

url = "https://my-rag-agent-abc123.langchain.app/invoke"
headers = {
    "Content-Type": "application/json",
}
data = {
    "input": {
        "messages": [{"role": "user", "content": "LangGraph란 무엇인가요?"}]
    }
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

#### Python SDK로 호출

```python
from langgraph_sdk import get_client

client = get_client(url="https://my-rag-agent-abc123.langchain.app")

# 스레드 생성
thread = client.threads.create()

# 실행
result = client.runs.create(
    thread_id=thread["thread_id"],
    assistant_id="graph",
    input={"messages": [{"role": "user", "content": "LangGraph란?"}]}
)

print(result)
```

### 1.5 환경 변수 업데이트

배포 후 환경 변수를 변경하려면:

```bash
langgraph env set OPENAI_API_KEY=sk-new-key
```

또는 LangSmith 대시보드에서 직접 설정할 수 있습니다.

### 1.6 새 버전 배포

코드를 수정한 후:

```bash
langgraph deploy
```

자동으로 새 버전이 배포되며, 이전 버전으로 롤백도 가능합니다.

---

## 방법 2: Docker로 Self-Hosted 배포

### 2.1 사전 준비

1. **Docker 설치**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/) 다운로드 및 설치

2. **LangGraph CLI 설치**
   ```bash
   pip install langgraph-cli
   ```

### 2.2 Dockerfile 생성

LangGraph CLI가 자동으로 Dockerfile을 생성해줍니다:

```bash
langgraph dockerfile
```

생성된 `Dockerfile`이 프로젝트 루트에 나타납니다.

### 2.3 Docker 이미지 빌드

```bash
docker build -t langgraph-rag-agent .
```

### 2.4 로컬에서 테스트

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  -e COHERE_API_KEY=... \
  -e TAVILY_API_KEY=... \
  langgraph-rag-agent
```

브라우저에서 `http://localhost:8000` 접속하여 확인하세요.

### 2.5 클라우드 서버에 배포

#### AWS ECS에 배포

1. **ECR에 이미지 푸시**
   ```bash
   # ECR 로그인
   aws ecr get-login-password --region ap-northeast-2 | \
     docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com

   # 이미지 태그
   docker tag langgraph-rag-agent:latest \
     <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com/langgraph-rag-agent:latest

   # 푸시
   docker push <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com/langgraph-rag-agent:latest
   ```

2. **ECS 태스크 정의 생성**
   - AWS Console → ECS → Task Definitions
   - "Create new Task Definition"
   - Fargate 선택
   - 컨테이너 이미지: ECR URI 입력
   - 환경 변수: Secrets Manager 연동 (보안)

3. **ECS 서비스 생성**
   - 클러스터 선택 또는 생성
   - 서비스 생성
   - 로드 밸런서 연결 (선택)

#### GCP Cloud Run에 배포

```bash
# Cloud Run에 배포
gcloud run deploy langgraph-rag-agent \
  --image gcr.io/<project-id>/langgraph-rag-agent \
  --platform managed \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=sk-...
```

#### Azure Container Instances에 배포

```bash
az container create \
  --resource-group myResourceGroup \
  --name langgraph-rag-agent \
  --image <registry>.azurecr.io/langgraph-rag-agent \
  --dns-name-label langgraph-rag \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=sk-...
```

### 2.6 Docker Compose로 관리 (선택)

여러 서비스를 함께 실행하려면 `docker-compose.yml` 생성:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - COHERE_API_KEY=${COHERE_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
    volumes:
      - ./faiss_index:/app/faiss_index
    restart: unless-stopped

  # Redis (선택, 캐싱용)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

실행:
```bash
docker-compose up -d
```

---

## 방법 3: Python 웹 서버로 배포

고급 사용자를 위한 방법입니다. FastAPI 또는 Flask로 감싸서 배포할 수 있습니다.

### 3.1 FastAPI로 감싸기

`server.py` 파일 생성:

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from graph import graph
import uvicorn
import json

app = FastAPI(title="LangGraph RAG Agent API")

class QueryRequest(BaseModel):
    messages: list

class QueryResponse(BaseModel):
    answer: str
    sources: list = []

@app.post("/invoke", response_model=QueryResponse)
async def invoke_graph(request: QueryRequest):
    """그래프를 동기적으로 실행"""
    try:
        result = graph.invoke({"messages": request.messages})
        return QueryResponse(
            answer=result["messages"][-1].content,
            sources=[doc.metadata.get("source") for doc in result.get("documents", [])]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream")
async def stream_graph(request: QueryRequest):
    """스트리밍 방식으로 실행"""
    async def event_generator():
        try:
            for chunk in graph.stream({"messages": request.messages}):
                yield f"data: {json.dumps(chunk)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 3.2 의존성 추가

`requirements.txt`에 추가:
```
fastapi
uvicorn[standard]
```

### 3.3 실행

```bash
python server.py
```

### 3.4 배포

일반적인 Python 웹 앱처럼 배포하면 됩니다:

- **Gunicorn + Nginx**
  ```bash
  gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```

- **systemd 서비스로 등록** (Linux)
  
  `/etc/systemd/system/langgraph-rag.service`:
```ini
[Unit]
Description=LangGraph RAG Agent
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/langgraph-rag-agent
Environment="PATH=/home/ubuntu/.venv/bin"
ExecStart=/home/ubuntu/.venv/bin/gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable langgraph-rag
sudo systemctl start langgraph-rag
```

---

## 환경 변수 및 시크릿 관리

### 보안 모범 사례

❌ **절대 하지 말아야 할 것:**
- 코드에 API 키 하드코딩
- `.env` 파일을 Git에 커밋
- 로그에 시크릿 출력

✅ **권장 사항:**

1. **로컬 개발**: `.env` 파일 사용
   ```bash
   # .gitignore에 추가
   .env
   ```

2. **LangGraph Cloud**: 대시보드에서 환경 변수 설정

3. **AWS**: Secrets Manager 또는 Parameter Store 사용
   ```python
   import boto3
   
   def get_secret(secret_name):
       client = boto3.client('secretsmanager')
       response = client.get_secret_value(SecretId=secret_name)
       return response['SecretString']
   
   OPENAI_API_KEY = get_secret('prod/openai-api-key')
   ```

4. **GCP**: Secret Manager 사용
   ```python
   from google.cloud import secretmanager
   
   def get_secret(project_id, secret_id):
       client = secretmanager.SecretManagerServiceClient()
       name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
       response = client.access_secret_version(request={"name": name})
       return response.payload.data.decode("UTF-8")
   ```

5. **Docker**: 환경 변수 파일 사용
   ```bash
   docker run --env-file .env langgraph-rag-agent
   ```

---

## 모니터링 및 디버깅

### LangSmith 추적 (모든 배포 방법 공통)

코드에서 LangSmith 추적을 활성화하세요:

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "production-rag-agent"
os.environ["LANGSMITH_API_KEY"] = "lsv2_..."
```

LangSmith 대시보드에서:
- 모든 요청/응답 확인
- 실행 시간, 토큰 사용량 추적
- 에러 로그 확인
- A/B 테스트

### 로깅 추가

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 노드에서 로깅
def my_node(state):
    logger.info(f"Processing question: {state['question']}")
    # ...
    return state
```

### 메트릭 수집 (Prometheus 예시)

```python
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('langgraph_requests_total', 'Total requests')
REQUEST_DURATION = Histogram('langgraph_request_duration_seconds', 'Request duration')

@REQUEST_DURATION.time()
def invoke_graph(input_data):
    REQUEST_COUNT.inc()
    return graph.invoke(input_data)

# 메트릭 서버 시작 (포트 9090)
start_http_server(9090)
```

---

## FAQ

### Q1: 비용은 얼마나 드나요?

**LangGraph Cloud:**
- 무료 티어: 월 100만 토큰
- Pro: 사용량 기반 ($0.30/1M 토큰)

**Self-Hosted:**
- 서버 비용만 (AWS t3.medium: 월 ~$30)
- LLM API 비용은 동일

### Q2: 스케일링은 어떻게 하나요?

**LangGraph Cloud:** 자동 스케일링

**Docker:**
- AWS ECS/EKS: Auto Scaling Group 설정
- GCP Cloud Run: 자동 스케일링
- Kubernetes: HPA (Horizontal Pod Autoscaler)

### Q3: HTTPS는 어떻게 설정하나요?

**LangGraph Cloud:** 자동 제공

**Self-Hosted:**
- AWS: ALB (Application Load Balancer)
- GCP: Cloud Load Balancer
- Nginx + Let's Encrypt (Certbot)

### Q4: 벡터 스토어는 어떻게 배포하나요?

현재 프로젝트는 로컬 FAISS 인덱스를 사용합니다. 프로덕션에서는:

1. **Pinecone** (관리형, 추천)
   ```python
   from langchain_pinecone import PineconeVectorStore
   vector_store = PineconeVectorStore(index_name="my-index")
   ```

2. **Weaviate** (오픈소스, Self-Hosted)
   ```python
   from langchain_weaviate import WeaviateVectorStore
   vector_store = WeaviateVectorStore(url="http://weaviate:8080")
   ```

3. **PostgreSQL + pgvector** (기존 DB 활용)
   ```python
   from langchain_postgres import PGVector
   vector_store = PGVector(connection_string="postgresql://...")
   ```

### Q5: 배포 후 디버깅이 어렵습니다.

1. **LangSmith 추적 활성화**가 가장 중요합니다.
2. 구조화된 로깅 사용 (JSON 형식)
3. 헬스 체크 엔드포인트 추가
4. 단계별 배포: 로컬 → 스테이징 → 프로덕션

### Q6: 동시 요청이 많을 때 대처 방법은?

1. **Rate Limiting** 추가:
   ```python
   from fastapi_limiter import FastAPILimiter
   from fastapi_limiter.depends import RateLimiter
   
   @app.post("/invoke", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
   ```

2. **Async 처리**:
   ```python
   async def invoke_graph_async(input_data):
       return await asyncio.to_thread(graph.invoke, input_data)
   ```

3. **큐 시스템** 도입 (Celery, RabbitMQ)

### Q7: 프로덕션 체크리스트

배포 전 확인하세요:

- [ ] 환경 변수가 안전하게 관리되는가?
- [ ] LangSmith 추적이 활성화되어 있는가?
- [ ] 에러 핸들링이 적절한가?
- [ ] 로깅이 설정되어 있는가?
- [ ] 헬스 체크 엔드포인트가 있는가?
- [ ] Rate Limiting이 설정되어 있는가?
- [ ] 모니터링/알림 시스템이 있는가?
- [ ] 백업 및 복구 계획이 있는가?
- [ ] 부하 테스트를 수행했는가?
- [ ] 문서화가 완료되었는가?

---

## 추가 리소스

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangGraph Cloud 가이드](https://langchain-ai.github.io/langgraph/cloud/)
- [LangSmith 문서](https://docs.smith.langchain.com/)
- [Docker 공식 문서](https://docs.docker.com/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
