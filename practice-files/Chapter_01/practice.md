# 1장 실습 파일 — Ollama 환경 구축과 첫 이미지 생성

책을 읽으면서 이 파일의 같은 절 번호를 찾아 명령어를 복사해 사용한다.

---

## 1.2 Ollama 설치 및 환경 설정

### 1.2.2 Ollama 다운로드 및 설치

```bash
brew install ollama
```

### 1.2.3 설치 확인

```bash
ollama --version
```

```bash
ollama list
```

### 1.2.4 첫 모델 다운로드

```bash
ollama pull llama3.2:1b
```

```bash
ollama list
```

```bash
ollama run llama3.2:1b "안녕하세요"
```

### 1.2.5 Ollama 서비스 시작/중지

```bash
# 서버 시작 (이 창에서 직접 실행, Ctrl+C로 종료)
ollama serve

# 백그라운드로 시작 (Homebrew 설치 시)
brew services start ollama

# 중지
brew services stop ollama

# 상태 확인
brew services info ollama
```


---

## 1.3 이미지 생성 모델 소개 (flux2-klein 4b / 9b)

### 1.3.7 두 모델 모두 다운로드하기

```bash
# 상업용 (Apache 2.0)
ollama pull x/flux2-klein:4b

# 고품질 연습용 (비상업용)
ollama pull x/flux2-klein:9b
```

```bash
ollama list
```


---

## 1.4 번역 모델 소개 (qwen3.5)

### 1.4.3 모델 다운로드

```bash
ollama pull qwen3.5:4b
```

```bash
ollama list
```

### 1.4.4 번역 품질 테스트

```bash
ollama run qwen3.5:4b --think=false "다음 문장을 영어로 번역해줘: 황금빛 석양이 지는 해변에서 산책하는 커플"
```

```bash
ollama run qwen3.5:4b "다음 문장을 영어로 번역해줘: 황금빛 석양이 지는 해변에서 산책하는 커플"
```

### 1.4.5 이미지 생성에 최적화된 번역

```bash
ollama run qwen3.5:4b --think=false "You are an AI image prompt translator. Convert Korean descriptions into detailed English prompts optimized for image generation. Include visual details like lighting, style, mood, and composition. Korean input: 조용한 카페 분위기"
```


---

## 1.5 첫 번째 이미지 생성해보기

### 1.5.1 터미널에서 직접 실행해보기

```bash
ollama run x/flux2-klein:4b "프롬프트"
```

```bash
mkdir -p ~/book-practice/Chapter01 ~/book-practice/Chapter02 ~/book-practice/Chapter03 ~/book-practice/Chapter04 ~/book-practice/Chapter05 ~/book-practice/Chapter06 ~/book-practice/Chapter07
cd ~/book-practice/Chapter01
```

```bash
ollama run x/flux2-klein:4b --width 256 --height 256 --seed 42 "A serene beach at sunset, golden light reflecting on calm waves, photorealistic"
```

### 1.5.2 생성된 이미지 확인하기

```bash
ollama run x/flux2-klein:4b "A serene beach at sunset, golden light, photorealistic"
```

```bash
ls -lh
```

### 1.5.3 결과 확인 및 품질 평가

```bash
open <저장된_파일명>   # macOS (Apple Silicon 전용)
```

### 1.5.4 프롬프트 수정으로 결과 개선하기

**1차 시도 — 너무 짧은 프롬프트**

```bash
ollama run x/flux2-klein:4b "a cat on a table"
```

**2차 시도 — 스타일과 분위기 추가**

```bash
ollama run x/flux2-klein:4b "a cute orange cat sitting on a wooden table, soft natural lighting, bokeh background, photorealistic"
```

**3차 시도 — 품질 키워드 추가**

```bash
ollama run x/flux2-klein:4b "a cute orange tabby cat sitting on a rustic wooden table, soft window light from the left, shallow depth of field, bokeh background, photorealistic, highly detailed"
```

### 1.5.5 생성 시간과 시스템 부하 확인

```bash
time ollama run x/flux2-klein:4b "A serene beach at sunset, photorealistic"
```

```bash
# macOS / Windows
top
```
