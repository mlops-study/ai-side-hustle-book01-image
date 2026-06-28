# 2장 실습 파일 — 이미지 파라미터 완전 정복 — 크기·품질·재현·제거

책을 읽으면서 이 파일의 같은 절 번호를 찾아 명령어를 복사해 사용한다.

---

## 2.1 이미지 생성 플래그란?

```bash
cd ~/book-practice/Chapter02
```

### 2.1.1 `ollama run --help`로 플래그 목록 직접 확인하기

```bash
ollama run --help
```

### 2.1.2 플래그 5가지 한눈에 보기

```bash
# 기본 형식
ollama run x/flux2-klein:4b --플래그명 값 "프롬프트"

# 예시: 1024x1024 크기로 생성
ollama run x/flux2-klein:4b --width 1024 --height 1024 "a minimalist coffee mug icon"
```


---

## 2.2 해상도 지정 — `--width` / `--height`

### 2.2.3 실습: 같은 프롬프트로 해상도별 결과 비교

**① 512×512 — 빠른 시안 확인용**

```bash
ollama run x/flux2-klein:4b --width 512 --height 512 \
  "a minimalist coffee mug icon, flat design, pastel colors, white background"
```

**② 768×1024 — 세로형 (포스터·인물)**

```bash
ollama run x/flux2-klein:4b --width 768 --height 1024 \
  "a minimalist coffee mug icon, flat design, pastel colors, white background"
```

**③ 1280×720 — 가로형 (배경·썸네일)**

```bash
ollama run x/flux2-klein:4b --width 1280 --height 720 \
  "a minimalist coffee mug icon, flat design, pastel colors, white background"
```


---

## 2.3 생성 품질 조절 — `--steps`

### 2.3.3 실습: Steps 2 / 4 / 8 결과 비교

**① Steps 2 — 빠른 시안 확인**

```bash
ollama run x/flux2-klein:4b --width 512 --height 512 --steps 2 \
  "a product photo of a coffee mug on a wooden table, soft lighting, photorealistic"
```

**② Steps 4 — 기본값 (권장)**

```bash
ollama run x/flux2-klein:4b --width 512 --height 512 --steps 4 \
  "a product photo of a coffee mug on a wooden table, soft lighting, photorealistic"
```

**③ Steps 8 — 더 많은 디테일**

```bash
ollama run x/flux2-klein:4b --width 512 --height 512 --steps 8 \
  "a product photo of a coffee mug on a wooden table, soft lighting, photorealistic"
```


---

## 2.4 결과 재현하기 — `--seed`

### 2.4.1 시드(Seed)란?

```bash
# 재현 실패 예시 — 시드는 같지만 크기가 다르다
ollama run x/flux2-klein:4b --seed 42 --width 256 --height 256 "a cute cat"
ollama run x/flux2-klein:4b --seed 42 --width 512 --height 512 "a cute cat"
# → 두 이미지는 서로 다르다
```

### 2.4.2 시드 미사용 vs 시드 고정 비교 실습

**① 시드 없이 두 번 실행 — 결과가 달라진다**

```bash
# 첫 번째 실행
ollama run x/flux2-klein:4b --width 512 --height 512 \
  "a cute cat wearing a hat, cartoon style"

# 두 번째 실행 (같은 명령어)
ollama run x/flux2-klein:4b --width 512 --height 512 \
  "a cute cat wearing a hat, cartoon style"
```

**② 시드 고정 — 결과가 동일하다**

```bash
# 시드 42로 첫 번째 실행
ollama run x/flux2-klein:4b --width 512 --height 512 --seed 42 \
  "a cute cat wearing a hat, cartoon style"

# 시드 42로 두 번째 실행
ollama run x/flux2-klein:4b --width 512 --height 512 --seed 42 \
  "a cute cat wearing a hat, cartoon style"
```

### 2.4.3 마음에 드는 이미지의 시드 찾아 기록하기

```bash
# 시드를 바꿔가며 탐색
ollama run x/flux2-klein:4b --seed 100 "a pastel icon of a coffee cup, flat design"
ollama run x/flux2-klein:4b --seed 200 "a pastel icon of a coffee cup, flat design"
ollama run x/flux2-klein:4b --seed 300 "a pastel icon of a coffee cup, flat design"
```

### 2.4.4 시드를 바꾸며 같은 프롬프트에서 다른 결과 탐색하기

```bash
# 시드를 바꾸며 변형 탐색
ollama run x/flux2-klein:4b --seed 42 \
  "a minimalist logo of a coffee shop, modern design"

ollama run x/flux2-klein:4b --seed 1234 \
  "a minimalist logo of a coffee shop, modern design"

ollama run x/flux2-klein:4b --seed 5678 \
  "a minimalist logo of a coffee shop, modern design"
```

### 2.4.5 시드 활용 전략 — 프롬프트 개선 시 시드 고정으로 변수 통제

```bash
# 시드 고정 + 프롬프트 A
ollama run x/flux2-klein:4b --seed 42 \
  "a coffee mug, white background"

# 같은 시드 + 프롬프트 B (키워드 추가)
ollama run x/flux2-klein:4b --seed 42 \
  "a coffee mug, white background, soft shadow, product photo style"
```


---

## 2.5 원치 않는 요소 제거 — `--negative`

### 2.5.1 네거티브 프롬프트란?

```bash
# 기본 형식
ollama run x/flux2-klein:4b \
  --negative "제거할 요소1, 제거할 요소2" \
  "원하는 이미지 프롬프트"
```

### 2.5.2 실습: 네거티브 없을 때 vs 있을 때 결과 비교

**① 네거티브 없이 생성**

```bash
ollama run x/flux2-klein:4b --width 512 --height 512 \
  --seed 42 \
  "a product photo of a white sneaker on a clean surface, logo"
```

**② 네거티브 추가 후 생성 (같은 시드 사용)**

```bash
ollama run x/flux2-klein:4b --width 512 --height 512 \
  --seed 42 \
  --negative "blurry, low quality, text, watermark, logo" \
  "a product photo of a white sneaker on a clean surface"
```

### 2.5.4 상업용 이미지에 맞는 네거티브 조합 예시

**아이콘·스티커용 (투명 배경 목적)**

```bash
ollama run x/flux2-klein:4b --width 512 --height 512 \
  --negative "blurry, low quality, text, watermark, dark background, gradient background" \
  "a minimalist coffee cup icon, flat design, white background"
```

**제품 사진용 (깔끔한 배경)**

```bash
ollama run x/flux2-klein:4b --width 1024 --height 1024 \
  --negative "blurry, low quality, text, watermark, cluttered background, shadows" \
  "a product photo of a ceramic mug, white studio background, soft lighting"
```

**풍경·배경 이미지용 (인물·텍스트 제외)**

```bash
ollama run x/flux2-klein:4b --width 1280 --height 720 \
  --negative "people, text, watermark, blurry, dark" \
  "a peaceful forest path in autumn, golden light, cinematic"
```


---

## 2.6 플래그 조합 실전

### 2.6.1 크기 + 스텝 + 시드 조합 예시

```bash
# 1024×1024, steps 4, seed 42 조합
ollama run x/flux2-klein:4b \
  --width 1024 \
  --height 1024 \
  --steps 4 \
  --seed 42 \
  "a minimalist coffee mug icon, flat design, pastel pink, white background"
```

### 2.6.2 전체 플래그 조합 명령어

```bash
# 전체 플래그 조합
ollama run x/flux2-klein:4b \
  --width 1024 \
  --height 1024 \
  --steps 4 \
  --seed 100 \
  --negative "blurry, low quality, text, watermark, dark background" \
  "a product photo of a black smartphone on a white surface, studio lighting"
```

### 2.6.3 대화형 모드에서 `/set` 명령으로 크기 변경하기

```bash
# 대화형 모드 진입
ollama run x/flux2-klein:4b
```

```
>>> /set width 512
>>> /set height 512
>>> a minimalist coffee cup icon, flat design, white background
>>> a minimalist tea pot icon, flat design, white background
>>> a minimalist croissant icon, flat design, white background
```
