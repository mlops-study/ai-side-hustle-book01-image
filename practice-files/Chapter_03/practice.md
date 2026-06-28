# 3장 실습 파일 — 프롬프트 작성과 한글→이미지 파이프라인

책을 읽으면서 이 파일의 같은 절 번호를 찾아 명령어를 복사해 사용한다.

---

## 3.1 프롬프트 작성 기법

```bash
cd ~/book-practice/Chapter03
```


---

## 3.2 한글 입력 → 영어 번역 → 이미지 생성 흐름

### 3.2.2 번역 단계 실습

```bash
ollama run qwen3.5:4b --think=false "You are an expert AI image prompt translator. Convert the following Korean description into a detailed English image generation prompt. Include visual details such as lighting, style, mood, and composition. Output only the English prompt without explanation. Korean: 황금빛 석양이 지는 해변에서 산책하는 커플"
```

### 3.2.4 이미지 생성 단계 실습

```bash
ollama run x/flux2-klein:4b "A couple walking hand in hand on a sandy beach at golden sunset, warm orange and pink sky reflecting on calm ocean waves, silhouette style, romantic atmosphere, soft golden hour lighting, cinematic composition, photorealistic"
```

```bash
open <저장된_파일명>   # macOS
```

### 3.2.5 결과 비교: 한글 직접 입력 vs 번역 후 입력

**테스트 입력: `복고풍 손으로 그린 글자로 된 '블루 플레이트 스페셜 4.99 달러'가 있는 빈티지 식당 메뉴 보드`**

```bash
# 방법 A: 한글 직접 입력
ollama run x/flux2-klein:4b "복고풍 손으로 그린 글자로 된 '블루 플레이트 스페셜 4.99 달러'가 있는 빈티지 식당 메뉴 보드"

# 방법 B: 번역 후 입력
ollama run x/flux2-klein:4b "Vintage diner menu board with 'Blue Plate Special \$4.99' in retro hand-painted lettering"
```

```bash
open ./--------499-------20260617-151230.png
```

### 3.2.6 자동화 스크립트 작성

```bash
vi translate_and_generate.sh
```

```bash
#!/bin/bash
# translate_and_generate.sh — 한글 입력 → 번역 → 이미지 생성 자동화

# 실습 폴더로 이동 (없으면 자동 생성)
mkdir -p ~/book-practice/Chapter03
cd ~/book-practice/Chapter03

if [ -z "$1" ]; then
    echo "사용법: ./translate_and_generate.sh '한글 프롬프트'"
    exit 1
fi

KOREAN_INPUT="$1"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PROMPT_LOG="prompts.log"

echo "▶ 번역 중..."
ENGLISH_PROMPT=$(ollama run qwen3.5:4b --think=false \
    "You are an expert AI image prompt translator. Convert the following Korean description into a detailed English image generation prompt. Include visual details such as lighting, style, mood, and composition. Output only the English prompt without explanation. Korean: ${KOREAN_INPUT}")

echo "▶ 영어 프롬프트: ${ENGLISH_PROMPT}"

# 번역 결과를 prompts.log에 기록
echo "[${TIMESTAMP}]" >> "${PROMPT_LOG}"
echo "  한글: ${KOREAN_INPUT}" >> "${PROMPT_LOG}"
echo "  영어: ${ENGLISH_PROMPT}" >> "${PROMPT_LOG}"
echo "" >> "${PROMPT_LOG}"

echo "▶ 이미지 생성 중..."
ollama run x/flux2-klein:4b "${ENGLISH_PROMPT}"
# 이미지는 ~/book-practice/Chapter03에 자동 저장됨

echo "✅ 완료 — 이미지와 프롬프트 기록이 ~/book-practice/Chapter03에 저장됨"
```

```bash
chmod +x translate_and_generate.sh
```

```bash
./translate_and_generate.sh "황금빛 석양이 지는 해변의 커플"
```

```bash
cat prompts.log
```

```bash
vi translate_and_generate.py
```

```bash
python translate_and_generate.py "황금빛 석양이 지는 해변의 커플"
```

```bash
# 여러 장 일괄 생성 예시
for desc in "황금빛 석양 해변" "눈 덮인 산속 오두막" "봄날 꽃밭의 강아지"; do
    ./translate_and_generate.sh "$desc"
done
```


---

## 3.3 프롬프트 라이브러리 관리

### 3.3.1 프롬프트 라이브러리 폴더 구조

```bash
cd ~/book-practice/Chapter03
mkdir -p prompts/{landscapes,portraits,products,characters,templates}
```

### 3.3.3 카테고리별 파일 관리

```markdown
# [카테고리 이름] 프롬프트

## [주제 이름]
[완성된 영어 프롬프트]

## [다른 주제]
[완성된 영어 프롬프트]

---
최종 수정: YYYY-MM
평균 생성 성공률: XX%
추천 사용처: [상품 유형]
```

```bash
vi prompts/landscapes/sunset.md
```

```markdown
# 석양 풍경 프롬프트

## 해변 석양
A dramatic beach sunset with golden and pink sky, calm waves reflecting warm light, silhouettes of palm trees, cinematic composition, photorealistic

## 산악 석양
A majestic mountain range at sunset, golden hour lighting, misty valleys, pine trees in the foreground, wide angle, photorealistic, highly detailed

## 도시 석양
A city skyline at sunset, warm orange glow reflecting off glass buildings, silhouette of the city, dramatic clouds, cinematic

## 들판 석양
A golden wheat field at sunset, warm light, gentle breeze visible in the grass, dramatic sky with clouds, wide angle, photorealistic

---
최종 수정: 2026-08
평균 생성 성공률: 95%
추천 사용처: 포스터, 배경 이미지, 달력 상품
```

```bash
vi prompts/characters/anime.md
```

```markdown
# 애니메이션 캐릭터 프롬프트

## 귀여운 소녀 캐릭터
A cute anime girl with pastel pink hair, big sparkly eyes, wearing a white summer dress, soft watercolor illustration style, clean white background, sticker design, simple linework

## 판타지 전사 캐릭터
A fantasy anime warrior with silver armor and a blue glowing sword, dynamic action pose, detailed digital illustration, clean white background, full body character design

## 치비 스타일 캐릭터
A chibi-style character with an oversized head and tiny body, cheerful expression, pastel colors, simple clean linework, white background, cute sticker design

## 동물 캐릭터
A cute cartoon fox with big round eyes, wearing a tiny scarf, soft pastel colors, flat illustration style, clean white background, sticker design

---
최종 수정: 2026-09
평균 생성 성공률: 88%
추천 사용처: 스티커, 이모티콘, 캐릭터 굿즈
```

```bash
vi prompts/products/food.md
```

```markdown
# 음식·음료 프롬프트

## 카페 라떼
A steaming cup of latte art on a rustic wooden table, soft morning light from the side, cozy cafe atmosphere, top-down view, photorealistic, food photography

## 초콜릿 케이크
A slice of rich chocolate cake topped with fresh berries on a white ceramic plate, dramatic side lighting, close-up, food photography style, photorealistic

## 트로피컬 과일
Assorted tropical fruits neatly arranged on a clean white background, vibrant colors, top-down flat lay, commercial food photography, photorealistic

## 마카롱
Pastel-colored macarons stacked on a marble surface, soft natural light, elegant composition, close-up, food photography, photorealistic

---
최종 수정: 2026-09
평균 생성 성공률: 90%
추천 사용처: 블로그 섬네일, 소셜미디어 콘텐츠, 레시피 포스터
```

```bash
touch prompts/portraits/lifestyle.md
touch prompts/templates/base_photo.md
```

### 3.3.4 프롬프트 버전 관리

```bash
vi prompts/products/coffee_mug.md
```

```markdown
# 제품 사진 — 커피 머그 프롬프트

## v3 (현재 사용)
A minimalist white ceramic coffee mug on a rustic wooden table, steam rising gently, soft morning light from the left, shallow depth of field, bokeh background, photorealistic, highly detailed, professional product photography

## v2
A white ceramic coffee mug on a wooden table, morning light, bokeh background, photorealistic
→ 개선 이유: 스팀·조명 방향 추가로 분위기 향상

## v1
A coffee mug on a table, photorealistic
→ 개선 이유: 너무 짧아 결과가 랜덤, 주제와 배경 구체화 필요

---
버전 이력: v1(2026-07) → v2(2026-08) → v3(2026-09)
```

### 3.3.5 프롬프트 템플릿화

```bash
vi prompts/templates/base_photo.md
```

```markdown
# 기본 사진 템플릿 (photorealistic)

## 구조
{SUBJECT}, {CONTEXT}, soft natural lighting, shallow depth of field, bokeh background, photorealistic, highly detailed, professional photography

## 변수
- {SUBJECT}: 주요 피사체 (예: a white ceramic coffee mug)
- {CONTEXT}: 배경·상황 (예: on a rustic wooden table)

## 사용 예시
- a white ceramic coffee mug, on a rustic wooden table
- a red rose in full bloom, on a white marble surface
- a vintage leather wallet, next to car keys on a dark wooden desk

## 고정 키워드 (변경 금지)
soft natural lighting, shallow depth of field, bokeh background, photorealistic, highly detailed, professional photography
```

### 3.3.6 배치 생성에 활용하기

```bash
cd ~/book-practice/Chapter03
```

**2단계: `prompts/batch_list.txt` 만들기**

```bash
vi prompts/batch_list.txt
```

**3단계: 배치 생성 스크립트 만들기**

```bash
vi batch_generate.sh
```

```bash
#!/bin/bash
# batch_generate.sh — 프롬프트 목록 파일에서 이미지 일괄 생성

PROMPT_FILE="${1:-prompts/batch_list.txt}"
OUTPUT_DIR="output_$(date +%Y%m%d)"
COUNT=1

mkdir -p "$OUTPUT_DIR"

echo "▶ 배치 생성 시작: $(wc -l < "$PROMPT_FILE")개 프롬프트"

while IFS= read -r prompt; do
    [ -z "$prompt" ] && continue   # 빈 줄 건너뜀

    echo "▶ [${COUNT}] 생성 중: ${prompt:0:60}..."
    (cd "$OUTPUT_DIR" && ollama run x/flux2-klein:4b "$prompt" < /dev/null)

    COUNT=$((COUNT + 1))
done < "$PROMPT_FILE"

echo "✅ 완료: ${OUTPUT_DIR}/ 에 $((COUNT-1))개 이미지 저장됨"
```

**4단계: 실행 권한 부여 후 실행**

```bash
chmod +x batch_generate.sh
./batch_generate.sh prompts/batch_list.txt
```

**`prompts/subjects_photo.txt` 파일 만들기**

```bash
vi prompts/subjects_photo.txt
```

**`template_batch.sh` 스크립트 만들기**

```bash
vi template_batch.sh
```

```bash
#!/bin/bash
# template_batch.sh — 템플릿 + 주제 목록으로 이미지 일괄 생성

SUBJECTS_FILE="${1:-prompts/subjects_photo.txt}"
OUTPUT_DIR="output_template_$(date +%Y%m%d)"
COUNT=1

# base_photo.md 템플릿의 고정 키워드
FIXED="soft natural lighting, shallow depth of field, bokeh background, photorealistic, highly detailed, professional photography"

mkdir -p "$OUTPUT_DIR"

echo "▶ 템플릿 기반 배치 생성 시작"
echo "  사용 템플릿: base_photo"
echo "  생성할 이미지: $(wc -l < "$SUBJECTS_FILE")장"
echo ""

while IFS= read -r subject; do
    [ -z "$subject" ] && continue

    # 주제 + 템플릿 고정 키워드를 합쳐 완성 프롬프트 생성
    PROMPT="${subject}, ${FIXED}"

    echo "▶ [${COUNT}] 주제: ${subject}"
    (cd "$OUTPUT_DIR" && ollama run x/flux2-klein:4b "$PROMPT" < /dev/null)

    COUNT=$((COUNT + 1))
done < "$SUBJECTS_FILE"

echo "✅ 완료: ${OUTPUT_DIR}/ 에 $((COUNT-1))개 이미지 저장됨"
```

```bash
chmod +x template_batch.sh
./template_batch.sh prompts/subjects_photo.txt
```

**`prompts/seed_prompt.txt` 파일 만들기**

```bash
vi prompts/seed_prompt.txt
```

**`prompts/seeds.txt` 파일 만들기**

```bash
vi prompts/seeds.txt
```

**`seed_batch.sh` 스크립트 만들기**

```bash
vi seed_batch.sh
```

```bash
#!/bin/bash
# seed_batch.sh — 동일 프롬프트에 다양한 seed로 이미지 일괄 생성

PROMPT_FILE="${1:-prompts/seed_prompt.txt}"
SEEDS_FILE="${2:-prompts/seeds.txt}"
OUTPUT_DIR="output_seed_$(date +%Y%m%d)"
COUNT=1

PROMPT=$(cat "$PROMPT_FILE")

mkdir -p "$OUTPUT_DIR"

echo "▶ seed 배치 생성 시작"
echo "  프롬프트: ${PROMPT:0:60}..."
echo "  생성할 이미지: $(wc -l < "$SEEDS_FILE")개"
echo ""

while IFS= read -r seed; do
    [ -z "$seed" ] && continue

    echo "▶ [${COUNT}] seed ${seed} 생성 중..."
    (cd "$OUTPUT_DIR" && ollama run x/flux2-klein:4b --seed "$seed" "$PROMPT" < /dev/null)

    COUNT=$((COUNT + 1))
done < "$SEEDS_FILE"

echo "✅ 완료: ${OUTPUT_DIR}/ 에 $((COUNT-1))개 이미지 저장됨"
```

**실행 권한 부여 후 실행**

```bash
chmod +x seed_batch.sh
./seed_batch.sh prompts/seed_prompt.txt prompts/seeds.txt
```
