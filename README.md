# AI로 나만의 수입 만들기: Icon Pack Edition

<img src="images/front_cover.png" width="400"/>

이 저장소는 **『AI로 나만의 수입 만들기: Icon Pack Edition』** 도서의 실습 파일과 보조 자료를 제공합니다.

책을 읽으면서 각 장의 명령어를 복사해 바로 실행할 수 있도록 구성되어 있습니다.

---

## 저장소 구조

```
.
├── practice-files/          # 챕터별 실습 파일
│   ├── Chapter_01/          # Ollama 환경 구축과 첫 이미지 생성
│   ├── Chapter_02/          # 이미지 파라미터 완전 정복
│   ├── Chapter_03/          # 프롬프트 작성과 한글→이미지 파이프라인
│   ├── Chapter_04/          # Claude 채팅으로 프롬프트 만들기
│   ├── Chapter_05/          # Claude Code로 이미지 생성 자동화
│   ├── Chapter_06/          # 팔리는 이미지 만들기 — 상업용 품질 기준
│   └── Chapter_07/          # AI 이미지로 수익 만들기 — 판매 플랫폼 완전 정복
├── appendix/                # 부록 PDF (환경 설정 가이드)
│   ├── 부록 A. 터미널 시작하기.pdf
│   ├── 부록 B. 텍스트 에디터로 파일 만들기.pdf
│   ├── 부록 C. Claude.ai 채팅 사용하기.pdf
│   ├── 부록 D. Claude Code 설치하기.pdf
│   ├── 부록 E. Claude Code 기본 사용법.pdf
│   ├── 부록 F. Windows 사용자를 위한 ComfyUI 대체 환경.pdf
│   └── 부록 G. Python 설치하기 (pyenv).pdf
└── remove_background.py     # 배경 투명화 스크립트
```

---

## 챕터별 내용

| 챕터 | 제목 | 주요 내용 |
|------|------|-----------|
| 1장 | Ollama 환경 구축과 첫 이미지 생성 | Ollama 설치, flux2-klein 및 qwen3.5 모델 다운로드, 첫 이미지 생성 |
| 2장 | 이미지 파라미터 완전 정복 | `--width`, `--height`, `--steps`, `--seed`, `--negative` 플래그 사용법 |
| 3장 | 프롬프트 작성과 한글→이미지 파이프라인 | 한글 번역 자동화, 프롬프트 라이브러리 구축, 배치 생성 스크립트 |
| 4장 | Claude 채팅으로 프롬프트 만들기 | Claude.ai로 프롬프트 생성·다듬기, 스타일 시리즈 기획 |
| 5장 | Claude Code로 이미지 생성 자동화 | MCP 설정, `/generate-image` 스킬 제작, 대량 자동 생성 |
| 6장 | 팔리는 이미지 만들기 | 상업용 라이선스 확인, FLUX 버전별 허용 범위 |
| 7장 | AI 이미지로 수익 만들기 | Etsy 아이콘팩 등록, ZIP 패키징, 월간 생산 루틴 자동화 |

---

## 실습 파일 사용법

각 챕터 폴더의 `practice.md`를 열고, 책의 같은 절 번호를 찾아 명령어를 복사해 터미널에 붙여넣습니다.

```bash
# 실습 폴더 생성 (1회)
mkdir -p ~/book-practice/Chapter0{1,2,3,4,5,6,7}
```

---

## 배경 투명화 스크립트 (`remove_background.py`)

생성된 이미지의 배경을 제거해 투명 PNG로 변환합니다. 3가지 방식을 지원합니다.

| 방식 | 명령어 옵션 | 적합한 용도 |
|------|------------|------------|
| 전체 스캔 (기본) | _(옵션 없음)_ | 선화·아웃라인 아이콘, 캐릭터 내부 포함 전체 제거 |
| 외곽 플러드필 | `--outer-only` | 스티커·로고, 캐릭터 내부 흰 영역 유지 |
| AI (rembg) | `--ai` | 복잡한 배경, 사진, 인물·동물 |

**실행 예시**

```bash
# 기본 (흰 배경 전체 제거)
python remove_background.py icon.png

# 외곽만 제거 (캐릭터 내부 흰 색 보존)
python remove_background.py icon.png --outer-only

# AI 방식 (복잡한 배경)
python remove_background.py photo.jpg --ai

# 배경색과 허용 오차 직접 지정
python remove_background.py banner.png --color "255,255,255" --tolerance 40

# 출력 파일명 지정
python remove_background.py input.png --output ./output/result.png
```

> Python 3.11 이상 필요. 첫 실행 시 필요한 패키지(Pillow, rembg)를 자동 설치합니다.

---

## 부록 (appendix/)

환경 설정이 처음이라면 아래 부록 PDF를 순서대로 읽으세요.

| 파일 | 내용 |
|------|------|
| 부록 A | 터미널 시작하기 |
| 부록 B | 텍스트 에디터로 파일 만들기 |
| 부록 C | Claude.ai 채팅 사용하기 |
| 부록 D | Claude Code 설치하기 |
| 부록 E | Claude Code 기본 사용법 |
| 부록 F | Windows 사용자를 위한 ComfyUI 대체 환경 |
| 부록 G | Python 설치하기 (pyenv) |

---

## 사용 모델

| 모델 | 용도 | 라이선스 |
|------|------|---------|
| `x/flux2-klein:4b` | 이미지 생성 (상업용) | Apache 2.0 |
| `x/flux2-klein:9b` | 이미지 생성 (고품질, 연습용) | 비상업용 |
| `qwen3.5:4b` | 한글 → 영어 프롬프트 번역 | - |

---

## 저자

- **김남기** — 카카오뱅크 AI 엔지니어, 『MLOps 구축 가이드북』 저자. 
- 📧 mlops.study@gmail.com
