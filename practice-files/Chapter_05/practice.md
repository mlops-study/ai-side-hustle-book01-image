# 5장 실습 파일 — Claude Code로 이미지 생성 자동화하기

책을 읽으면서 이 파일의 같은 절 번호를 찾아 명령어를 복사해 사용한다.

---

## 5.1 Claude Code 시작하기

```bash
cd ~/book-practice/Chapter05
```

### 5.1.1 Claude Code 소개와 준비

```bash
claude --version     # 버전 번호가 나오면 준비 완료
claude               # ~/book-practice/Chapter05에서 실행
```


---

## 5.2 Claude Code와 Ollama 연결하기 (MCP 설정)

### 5.2.2 ollama-mcp 설치

```bash
cd ~/book-practice/Chapter05
claude
```

```
> ollama-mcp 패키지를 설치해줘.
```

### 5.2.3 Claude Code에 MCP 서버 등록하기

```
> 설치한 ollama-mcp를 MCP 서버로 등록해줘.
```

```
> /exit
```

```bash
claude
```

### 5.2.4 연결 확인

```
> Ollama에 설치된 모델 목록을 보여줘.
```

### 5.2.5 자주 발생하는 오류와 해결법

```
> Ollama 연결이 안 돼.
```

```
> MCP 서버를 찾을 수 없다는 오류가 떠.
```

```
> 연결은 됐는데 모델 목록이 비어 있어.
```

```
> 응, 받아줘.
```


---

## 5.3 Claude Code로 전체 파이프라인 실행하기

### 5.3.2 한 번의 대화로 번역 + 생성 + 저장 완성

**Claude Code를 실행하고 프로젝트 폴더에서 시작한다.**

```bash
cd ~/book-practice/Chapter05
claude
```

**🧑 내가 입력:**

```
> 파스텔 감성 커피잔 미니멀 아이콘 이미지를 만들어줘.
qwen3.5:4b로 영어 프롬프트로 번역하고,
flux2-klein:4b로 이미지 생성해서
images/coffee_icon_001.png로 저장해줘.
```

### 5.3.3 생성 결과를 Claude Code에서 바로 확인하기

```
> 방금 생성한 이미지가 잘 저장됐는지 확인하고, 파일 크기도 알려줘.
```

### 5.3.4 오류 발생 시 Claude Code가 자동으로 해결하는 흐름

**🧑 내가 입력:**

```
> 파스텔 감성 커피잔 미니멀 아이콘 이미지를 만들어줘.
```

**🧑 내가 입력:**

```
> 해결해줘.
```

**🧑 내가 입력:**

```
> 해결해줘.
```


---

## 5.4 Claude Code로 프롬프트 라이브러리 관리하기

### 5.4.1 아이콘 판매용 카테고리 추가하기

**Claude Code를 실행하고 프로젝트 폴더에서 시작한다.**

```bash
cd ~/book-practice/Chapter05
claude
```

```
> prompts/ 폴더 안에 아이콘 판매용 카테고리를 추가해줘.
  icons, clipart, wallpapers 폴더를 만들고,
  각 폴더 안에 README.md도 만들어줘.
```

### 5.4.2 기존 프롬프트 파일을 Claude Code로 정리·분류

```
> prompts/coffee_cup_styles.txt 안에 있는 프롬프트들을
  주제별로 분류해서 icons/, clipart/, wallpapers/ 폴더에 나눠 저장해줘.
  파일명은 내용에서 주제를 뽑아서 만들어줘.
```

### 5.4.3 새 프롬프트 추가 및 버전 관리

```
> 방금 생성한 커피잔 아이콘 프롬프트를
  prompts/icons/coffee_cup_v1.md로 저장해줘.
  사용한 모델, 생성 날짜, 품질 평가(A/B/C)도 함께 기록해줘.
```

```markdown
---
model: x/flux2-klein:4b
date: 2026-06-07
quality: A
---

# Coffee Cup Icon (Minimal Pastel)

minimalist coffee cup icon, flat vector design, pastel pink and beige palette,
thin clean lines, white background, no shadows, no gradients,
cute modern aesthetic, isolated icon

## 메모
Etsy 아이콘팩용. 파스텔 핑크 계열로 세트 10개 생성 예정.
```

### 5.4.4 라이브러리에서 프롬프트 검색·조회하기

```
> prompts/ 폴더에서 "pastel"과 "icon"이 모두 포함된 프롬프트 파일을
  찾아서 목록으로 보여줘.
```

```
> prompts/icons/coffee_cup_v1.md 프롬프트로
  이미지 3장 생성해서 images/에 저장해줘.
```

### 5.4.5 라이브러리 관리의 한계 — 스킬이 필요한 순간

```
> prompts/icons/coffee_cup_v1.md로 이미지 생성해서 images/에 저장해줘.
```


---

## 5.5 나만의 스킬 만들기

### 5.5.4 스킬 파일 작성 및 등록 방법

**Claude Code를 실행하고 프로젝트 폴더에서 시작한다.**

```bash
cd ~/book-practice/Chapter05
claude
```

**🧑 내가 입력:**

```
> ~/.claude/skills/generate-image/SKILL.md 파일을 만들어줘.
아래 내용으로 작성해줘.

---
name: generate-image
description: 한글 아이디어로 이미지 생성 (번역 → flux2-klein → 저장 + 프롬프트 라이브러리 저장)
---

## 역할
한글 이미지 아이디어를 입력받아 qwen3.5:4b로 영어 번역 후 flux2-klein:4b로 이미지를
생성하고 저장한다. 사용한 영어 프롬프트는 prompts/icons/에 기록한다.

## 실행 흐름

1. 사용자 입력에서 한글 아이디어 텍스트를 추출한다.
2. ollama run qwen3.5:4b --think=false로 영어 프롬프트로 번역한다.
   - 번역 지시: "이미지 생성용 영어 프롬프트로 번역해줘. 한글 설명만 영어 키워드로
     변환. 추가 설명 없이 프롬프트만 출력."
3. images/ 폴더가 없으면 생성한다.
4. 파일명을 timestamp 기반으로 결정한다. (예: image_20260607_143200.png)
5. ollama REST API로 이미지를 생성하고 해당 파일명으로 저장한다.
   - `ollama run` CLI는 이미지 생성 모델에 사용할 수 없다. 결과가 stdout으로
     출력되지 않아 빈 파일이 저장된다.
   - 반드시 REST API를 사용한다. 응답 JSON의 `image` 필드에 base64로 결과가 담긴다.
   - 명령 예시:
     ```bash
     curl -s http://localhost:11434/api/generate \
       -d '{"model":"x/flux2-klein:4b","prompt":"<영어 프롬프트>","stream":false,"options":{"seed":42}}' \
       | python3 -c "
     import sys,json,base64
     d=json.load(sys.stdin)
     open('<출력경로>.png','wb').write(base64.b64decode(d['image']))
     "
```

### 응답 스타일

```
> 📌 **참고: 스킬 내용을 어떻게 준비했나**
>
> 위 요청의 내용을 처음부터 혼자 작성할 필요는 없다. Claude(claude.ai)와 대화로 함께 만들면 된다.
>
> **대화 예시:**
>
```

### 5.5.5 `/generate-image "한글 설명"` 한 줄로 이미지 생성 실습

```
> /generate-image "파스텔 커피잔 아이콘, 미니멀 플랫 디자인"
```

```
> 이미지를 확인해줘.
```

### 5.5.6 저장된 프롬프트 확인 및 재사용

**`prompts/icons/20260613_143200.md` 내용:**

```markdown
---
date: 2026-06-13
model: x/flux2-klein:4b
image: images/image_20260613_143200.png
---

# 파스텔 커피잔 아이콘, 미니멀 플랫 디자인

minimalist coffee cup icon, flat vector design, pastel pink tones, white background, clean lines, no shadows
```

```
> prompts/icons/ 폴더에 저장된 프롬프트 파일 목록을 보여줘.
```

```
> prompts/icons/20260613_143200.md 프롬프트로 이미지 3장 더 생성해줘.
```

### 5.5.7 프로젝트 내 스킬 재사용 및 CLAUDE.md 연동

```
> /generate-image 스킬을 CLAUDE.md에 기억해줘.
```


---

## 5.6 스킬 고도화

### 5.6.1 스타일 선택 옵션 추가 (`--style`, `--mood` 파라미터)

**🧑 내가 입력:**

```
> ~/.claude/skills/generate-image/SKILL.md 파일을 아래 내용으로 업데이트해줘.

---
name: generate-image
description: 한글 아이디어로 이미지 생성 (번역 → flux2-klein → 저장), 스타일/배치 옵션 지원
---

## 역할
한글 이미지 아이디어를 영어로 번역하고 flux2-klein:4b로 이미지를 생성해 저장한다.
스타일, 분위기, 생성 수 옵션을 지원한다. 생성된 프롬프트는 항상 prompts/icons/에 저장된다.

## 파라미터

- --style [minimal|watercolor|3d|anime|photo]: 이미지 스타일 (기본값: minimal)
- --mood [pastel|dark|vibrant|muted]: 색감/분위기 (기본값: pastel)
- --count N: 생성할 이미지 수 (기본값: 1, 최대: 20)

## 스타일별 추가 키워드

- minimal: "flat vector design, thin clean lines, no gradients, white background"
- watercolor: "watercolor illustration, soft brush strokes, transparent washes, hand-painted"
- 3d: "isometric 3D render, soft shadows, flat shading, clean geometry"
- anime: "anime illustration, cel shading, clean linework, vibrant colors"
- photo: "photorealistic, DSLR photo, sharp focus, natural lighting"

## 실행 흐름

1. 사용자 입력에서 주제와 파라미터를 추출한다.
2. 스타일·무드 파라미터에 맞는 추가 키워드를 조합한다.
3. qwen3.5:4b로 주제를 영어로 번역하고 스타일 키워드를 결합한다.
4. images/ 폴더가 없으면 생성한다.
5. --count 수만큼 flux2-klein:4b로 이미지를 순차 생성한다.
6. 각 파일을 타임스탬프_순번.png 형식으로 저장한다.
7. prompts/icons/YYYYMMDD_HHMMSS.md에 프롬프트를 저장한다.
   - 프론트매터: date, model, style, mood, image 경로
   - 본문: 한글 아이디어 제목, 영어 프롬프트
8. 생성 결과 요약과 프롬프트 파일 경로를 출력한다.

## 응답 스타일
각 단계 진행 상황을 짧게 알려준다. 완료 후 생성 파일 목록과 프롬프트 경로를 출력한다.
```

```
> /exit
```

```bash
claude
```

### 5.6.3 자동 저장된 프롬프트로 스타일 일관성 유지하기

```markdown
---
date: 2026-06-13
model: x/flux2-klein:4b
style: minimal
mood: pastel
image: images/image_20260613_1432_01.png
---

# 파스텔 커피잔 아이콘

minimalist coffee cup icon, flat vector design, pastel pink and beige palette,
thin clean lines, white background, no shadows, cute modern aesthetic
```

```
> prompts/icons/20260613_143200.md 설정으로 이미지 3장 더 만들어줘.
```


---

## 5.7 실전1: 상품 이미지 10장 만들기

### 5.7.1 상품 컨셉 기획 — Claude와 아이디어 브레인스토밍

```
> Etsy에 판매할 "카페 감성 Notion 아이콘팩"을 기획해줘.
  10종 이미지 목록, 공통 스타일, 타깃 고객, 추천 판매 가격을 정리해줘.
```

### 5.7.2 스킬로 이미지 10장 일괄 생성

```
> /generate-image "카페 감성 커피잔 미니멀 아이콘" --style minimal --mood pastel
```

```
> 아래 9개 주제로 각각 /generate-image 스킬로 이미지 1장씩 생성해줘.
  --style minimal --mood pastel로 통일해줘.
  라떼 글라스, 모카포트, 핸드드립 포트, 커피원두 봉투,
  에스프레소잔, 아이스 아메리카노, 커피그라인더, 마카롱, 케이크 한 조각
```

### 5.7.3 결과물 선별 및 품질 평가

```
> images/ 폴더에 있는 이미지들을 목록으로 보여줘.
  파일명과 파일 크기를 함께 보여줘.
```

```
> images/image_20260613_1432_03.png가 마음에 안 들어.
  prompts/icons/에서 모카포트 프롬프트 찾아서 --style minimal --mood pastel로 2장 더 만들어줘.
```


---

## 5.8 실전2: 클로드에게 일 시켜 놓고 다른 일 보기

### 5.8.1 자리 비우기 전 준비

**① 절전 모드 해제**

```bash
caffeinate -i &
```

### 5.8.2 Claude Code에 대량 작업 지시하기

```
> 아래 30개 주제로 각각 /generate-image 스킬로 이미지 1장씩 생성해줘.
  --style minimal --mood pastel로 모두 통일해줘.
  작업이 끝나면 총 몇 장 생성됐는지 알려줘.

  커피잔, 라떼잔, 모카포트, 핸드드립 포트, 에스프레소잔,
  아이스 아메리카노, 아이스 라떼, 카페모카, 카푸치노, 플랫화이트,
  커피원두 봉투, 커피그라인더, 커피드리퍼, 커피 필터, 커피 스케일,
  마카롱, 케이크 한 조각, 크루아상, 머핀, 스콘,
  커피책, 독서 노트, 펜, 안경, 북마크,
  화분 (작은 선인장), 캔들, 향수 병, 달 모양 오너먼트, 별 모양 오너먼트
```

### 5.8.3 돌아와서 결과 확인하기

```
> images/ 폴더에 파일이 몇 개 있어? 파일 목록도 보여줘.
```

```
> prompts/icons/ 폴더에 파일이 몇 개 있어?
```

### 5.8.4 중간에 멈췄을 때 이어서 시키기

```
> images/ 폴더에 파일이 몇 개 있어?
```

```
> 아래 20개 주제로 이어서 생성해줘.
  --style minimal --mood pastel로 통일해줘.

  커피원두 봉투, 커피그라인더, 커피드리퍼, 커피 필터, 커피 스케일,
  마카롱, 케이크 한 조각, 크루아상, 머핀, 스콘,
  커피책, 독서 노트, 펜, 안경, 북마크,
  화분 (작은 선인장), 캔들, 향수 병, 달 모양 오너먼트, 별 모양 오너먼트
```
