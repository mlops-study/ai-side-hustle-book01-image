#!/usr/bin/env python3
"""
배경 투명화 스크립트 (Python 3.11+)

─────────────────────────────────────────────────────────────
 동작 방식 3가지
─────────────────────────────────────────────────────────────
  1) 전체 스캔 방식 (기본)
     - 배경색과 일치하는 픽셀을 이미지 전체에서 찾아 투명화
     - 캐릭터 내부 흰 영역(몸통 안쪽 등)까지 모두 제거됨
     - 컬러 배경 위에 선화(아웃라인)만 올릴 때 적합
     - 처음 실행 시 Pillow 자동 설치

  2) 외곽 플러드필 방식 (--outer-only)
     - 네 모서리에서 시작해 연결된 배경만 BFS로 제거
     - 캐릭터 내부 흰 영역은 그대로 유지됨
     - 흰 속이 남아야 하는 스티커·로고 등에 적합
     - 처음 실행 시 Pillow 자동 설치

  3) AI 방식 (--ai)
     - rembg 딥러닝 모델로 피사체와 배경을 자동 분리
     - 복잡한 배경, 사진, 인물·동물 등에 적합
     - 처음 실행 시 rembg + Pillow 자동 설치 (수백 MB)

─────────────────────────────────────────────────────────────
 옵션
─────────────────────────────────────────────────────────────
  --outer-only          외곽 배경만 제거, 내부 흰 영역 유지
                        (기본값: 내부 흰 영역까지 모두 투명화)
  --ai                  AI 방식으로 배경 제거 (기본값: 전체 스캔 방식)
                        --outer-only 와 함께 사용 불가
  --color R,G,B         배경색 직접 지정 (기본값: 네 모서리 픽셀 평균 자동 감지)
                        --ai 사용 시 무시됨
  --tolerance N         색상 허용 오차 0~255 (기본값: 20, 클수록 넓게 제거)
                        그러데이션 경계가 있으면 30~50 으로 높여볼 것
                        --ai 사용 시 무시됨
  --output 경로         출력 파일 경로 (기본값: 원본파일명_nobg.png)

─────────────────────────────────────────────────────────────
 실행 예시
─────────────────────────────────────────────────────────────
  [전체 스캔, 기본] 흰 배경 일러스트 — 내부 흰 영역 포함 모두 제거
  $ pyenv exec python3 remove_background.py logo.png
  → logo_nobg.png 생성 (캐릭터 몸통 안쪽도 투명)

  [외곽만] 흰 배경 제거 — 캐릭터 내부 흰 영역은 유지
  $ pyenv exec python3 remove_background.py logo.png --outer-only
  → logo_nobg.png 생성 (캐릭터 안쪽 흰 색 보존)

  [AI 방식] 복잡한 배경 사진 처리
  $ pyenv exec python3 remove_background.py photo.jpg --ai
  → photo_nobg.png 생성

  [배경색 수동 지정] 흰 배경, 허용 오차 넓게
  $ pyenv exec python3 remove_background.py banner.png --color "255,255,255" --tolerance 40
  → banner_nobg.png 생성

  [외곽만 + 배경색 지정] 연한 회색 배경 외곽만 제거
  $ pyenv exec python3 remove_background.py icon.png --outer-only --color "240,240,240" --tolerance 15
  → icon_nobg.png 생성

  [출력 파일명 지정]
  $ pyenv exec python3 remove_background.py input.png --output ./output/result.png
  → ./output/result.png 생성

─────────────────────────────────────────────────────────────
 출력
─────────────────────────────────────────────────────────────
  투명 배경 PNG 파일로 저장 (RGBA 포맷)
  기본 저장 경로: 원본과 같은 디렉토리, 파일명_nobg.png
  예) photo.jpg  →  photo_nobg.png
      Chapter_01/images/cover.png  →  Chapter_01/images/cover_nobg.png
"""

import sys
import subprocess
import argparse
from collections import deque
from pathlib import Path
from typing import TypeAlias

RGB: TypeAlias = tuple[int, int, int]
RGBA: TypeAlias = tuple[int, int, int, int]


def ensure_packages(packages: list[str]) -> None:
    for pkg in packages:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            print(f"[설치 중] {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])


def remove_bg_ai(input_path: Path, output_path: Path) -> None:
    """rembg AI 모델로 배경 제거 (복잡한 배경에 적합)"""
    ensure_packages(["rembg", "Pillow"])
    from rembg import remove

    print(f"[AI 방식] 배경 제거 중: {input_path.name}")
    result = remove(input_path.read_bytes())
    output_path.write_bytes(result)
    print(f"[완료] 저장됨: {output_path}")


def _detect_bg_color(pixels, w: int, h: int) -> RGB:
    corners: list[RGB] = [
        pixels[0, 0][:3],
        pixels[w - 1, 0][:3],
        pixels[0, h - 1][:3],
        pixels[w - 1, h - 1][:3],
    ]
    avg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    print(f"  배경색 자동 감지: RGB{avg}")
    return avg  # type: ignore[return-value]


def _color_diff(c1: RGBA, c2: RGB) -> int:
    return sum(abs(int(a) - int(b)) for a, b in zip(c1[:3], c2))


def remove_all_matching(
    input_path: Path,
    output_path: Path,
    bg_color: RGB | None,
    tolerance: int,
) -> None:
    """배경색과 일치하는 픽셀 전체를 투명화 (내부 흰 영역 포함)."""
    ensure_packages(["Pillow"])
    from PIL import Image

    print(f"[전체 스캔 방식] 배경 제거 중: {input_path.name}")
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    color = bg_color if bg_color is not None else _detect_bg_color(pixels, w, h)

    count = 0
    for y in range(h):
        for x in range(w):
            if _color_diff(pixels[x, y], color) <= tolerance:
                pixels[x, y] = (0, 0, 0, 0)
                count += 1

    img.save(output_path)
    print(f"  투명화된 픽셀 수: {count:,}")
    print(f"[완료] 저장됨: {output_path}")


def remove_outer_only(
    input_path: Path,
    output_path: Path,
    bg_color: RGB | None,
    tolerance: int,
) -> None:
    """외곽에서 BFS로 번지는 배경만 투명화 (캐릭터 내부 흰 영역 유지)."""
    ensure_packages(["Pillow"])
    from PIL import Image

    print(f"[외곽 플러드필 방식] 배경 제거 중: {input_path.name}")
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    color = bg_color if bg_color is not None else _detect_bg_color(pixels, w, h)

    visited: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque()

    for sx, sy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if (sx, sy) not in visited and _color_diff(pixels[sx, sy], color) <= tolerance:
            queue.append((sx, sy))
            visited.add((sx, sy))

    count = 0
    while queue:
        x, y = queue.popleft()
        pixels[x, y] = (0, 0, 0, 0)
        count += 1
        for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                if _color_diff(pixels[nx, ny], color) <= tolerance:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    img.save(output_path)
    print(f"  투명화된 픽셀 수: {count:,}")
    print(f"[완료] 저장됨: {output_path}")


def parse_color(value: str) -> RGB:
    parts = [int(v.strip()) for v in value.split(",")]
    if len(parts) < 3:  # noqa: PLR2004
        raise argparse.ArgumentTypeError("색상은 'R,G,B' 형식으로 입력하세요 (예: 255,255,255)")
    return (parts[0], parts[1], parts[2])


def main() -> None:
    parser = argparse.ArgumentParser(description="이미지 배경 투명화")
    parser.add_argument("input", help="입력 이미지 파일 경로")
    parser.add_argument("--outer-only", action="store_true",
                        help="외곽 배경만 제거, 캐릭터 내부 흰 영역 유지")
    parser.add_argument("--ai", action="store_true",
                        help="AI(rembg) 방식으로 배경 제거")
    parser.add_argument("--color", type=parse_color, default=None,
                        help="배경색 지정 (예: '255,255,255'). 미지정 시 자동 감지")
    parser.add_argument("--tolerance", type=int, default=20,
                        help="색상 허용 오차 (기본: 20, 범위: 0~255)")
    parser.add_argument("--output", default=None,
                        help="출력 파일 경로 (기본: 원본파일명_nobg.png)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = (
        Path(args.output) if args.output
        else input_path.with_name(input_path.stem + "_nobg.png")
    )

    match (args.ai, args.outer_only):
        case (True, _):
            remove_bg_ai(input_path, output_path)
        case (False, True):
            remove_outer_only(input_path, output_path, args.color, args.tolerance)
        case _:
            remove_all_matching(input_path, output_path, args.color, args.tolerance)


if __name__ == "__main__":
    main()
