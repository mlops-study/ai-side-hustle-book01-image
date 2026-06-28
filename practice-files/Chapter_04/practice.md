# 4장 실습 파일 — Claude 채팅으로 프롬프트 만들기

책을 읽으면서 이 파일의 같은 절 번호를 찾아 명령어를 복사해 사용한다.

---

## 4.1 Claude 소개 및 시작하기

```bash
cd ~/book-practice/Chapter04
```


---

## 4.2 채팅으로 프롬프트 생성하기

### 4.2.2 한글 한 마디 → 완성된 영어 프롬프트 받기

```bash
ollama run x/flux2-klein:4b "minimalist coffee cup icon, flat vector design, pastel pink and beige color palette, clean simple lines, white background, no shadows, no gradients, no texture, cute modern aesthetic, suitable for digital planner stickers, isolated icon, professional icon design, sharp edges"
```

### 4.2.3 Claude와 대화로 프롬프트 다듬기

**수정된 프롬프트를 Ollama로 바로 실행한다.**

```bash
ollama run x/flux2-klein:4b "minimalist coffee cup icon, flat vector design, pastel pink and beige color palette, thin delicate linework, fine detail, small compact icon, white background, no shadows, no gradients, cute modern aesthetic, digital planner sticker style, isolated on white, professional icon design, crisp edges" --width 512 --height 512 --seed 42
```

### 4.2.4 여러 스타일 옵션 한 번에 요청하기

**3개 프롬프트를 txt 파일로 만들어 배치 생성으로 돌린다.**

```bash
mkdir -p prompts
vi prompts/coffee_cup_styles.txt
```

```bash
~/book-practice/Chapter03/batch_generate.sh prompts/coffee_cup_styles.txt
```

```bash
# 생성된 이미지 확인 (macOS)
# yyyymmdd 자리에 실행한 날짜, hhmmss 자리에 실행한 시간이 들어간다
open output_yyyymmdd/minimalist-coffee-cup-line-icon-thin-outlines-only-yyyymmdd-hhmmss.png

# 예시
open output_20270101/minimalist-coffee-cup-line-icon-thin-outlines-only-20270101-120000.png
```


---

## 4.4 프롬프트 변형과 시리즈 만들기

### 4.4.3 카테고리별 프롬프트 묶음 한 번에 생성하기

**프롬프트 파일에 저장하기**

```bash
vi prompts/notion_icon_set.txt
```

```bash
wc -l prompts/notion_icon_set.txt
```

**배치 스크립트로 30개 이미지 생성하기**

```bash
vi batch_notion_icons.sh
```

```bash
#!/bin/bash
PROMPT_FILE="prompts/notion_icon_set.txt"
OUTPUT_DIR="output_$(date +%Y%m%d)"
mkdir -p "$OUTPUT_DIR"

while IFS= read -r prompt; do
    echo "생성 중: $prompt"
    (cd "$OUTPUT_DIR" && ollama run x/flux2-klein:4b "$prompt" < /dev/null)
done < "$PROMPT_FILE"
```

```bash
bash batch_notion_icons.sh
```

```bash
# yyyymmdd 자리에 실행한 날짜, hhmmss 자리에 실행한 시간이 들어간다
open output_yyyymmdd/[프롬프트-앞부분-kebab-case]-yyyymmdd-hhmmss.png

# 예시
open output_20260801/minimalist-coffee-cup-icon-flat-vector-design-20260801-143200.png
```

```bash
# 2026년 8월 1일에 실행한 경우
ls output_20260801/ | wc -l
```
